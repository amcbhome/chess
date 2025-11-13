import requests
import streamlit as st
import pandas as pd
import chess

# -----------------------------
# Helper functions
# -----------------------------


def validate_fen(fen: str) -> bool:
    """Return True if FEN is valid, False otherwise."""
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False


def build_lichess_explorer_url(
    fen: str,
    use_masters: bool,
    speeds: list[str] | None = None,
    rating_groups: list[str] | None = None,
) -> tuple[str, dict]:
    """
    Build endpoint and params for the Lichess Opening Explorer API.

    - If use_masters is True: use /masters endpoint (no speeds/ratings)
    - Else: use /lichess endpoint with speeds/ratings filters if provided
    """

    if use_masters:
        base_url = "https://explorer.lichess.ovh/masters"
        params = {
            "fen": fen,
            "variant": "standard",
            "topGames": 0,
            "recentGames": 0,
        }
        return base_url, params

    # Lichess online database
    base_url = "https://explorer.lichess.ovh/lichess"
    params: dict[str, str | int] = {
        "fen": fen,
        "variant": "standard",
        "topGames": 0,
        "recentGames": 0,
    }

    if speeds:
        params["speeds"] = ",".join(speeds)

    if rating_groups:
        params["ratings"] = ",".join(rating_groups)

    return base_url, params


def fetch_explorer_data(url: str, params: dict) -> dict | None:
    """Call the Lichess Opening Explorer API and return JSON, or None on error."""
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException as e:
        st.error(f"Error contacting Lichess Opening Explorer API:\n{e}")
        return None


def build_moves_dataframe(data: dict) -> pd.DataFrame:
    """
    Given the explorer JSON response, return a DataFrame of moves with:
    - SAN, UCI, games, freq%, white%, draw%, black%, avg rating
    """
    total_white = data.get("white", 0)
    total_black = data.get("black", 0)
    total_draws = data.get("draws", 0)
    total_games = total_white + total_black + total_draws

    moves = data.get("moves", [])
    rows = []

    for mv in moves:
        mv_white = mv.get("white", 0)
        mv_black = mv.get("black", 0)
        mv_draws = mv.get("draws", 0)
        mv_games = mv_white + mv_black + mv_draws

        if mv_games == 0:
            continue

        freq_pct = (mv_games / total_games * 100) if total_games > 0 else 0.0
        white_pct = (mv_white / mv_games * 100) if mv_games > 0 else 0.0
        draw_pct = (mv_draws / mv_games * 100) if mv_games > 0 else 0.0
        black_pct = (mv_black / mv_games * 100) if mv_games > 0 else 0.0

        rows.append(
            {
                "Move (SAN)": mv.get("san", "?"),
                "Move (UCI)": mv.get("uci", "?"),
                "Games": mv_games,
                "Frequency %": round(freq_pct, 2),
                "White win %": round(white_pct, 2),
                "Draw %": round(draw_pct, 2),
                "Black win %": round(black_pct, 2),
                "Avg Opp. Rating": mv.get("averageRating", None),
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values(by="Games", ascending=False).reset_index(drop=True)
    return df


# -----------------------------
# Streamlit UI
# -----------------------------


def main():
    st.set_page_config(
        page_title="Lichess Opening Stats from FEN",
        page_icon="♟️",
        layout="wide",
    )

    st.title("♟️ Lichess Opening Statistics from FEN")
    st.write(
        "Enter any chess position in **FEN** format and query the "
        "**Lichess Opening Explorer** (online games or Masters DB) "
        "to see the most common next moves and their statistics."
    )

    # Default FEN: starting position
    default_fen = chess.STARTING_FEN

    fen = st.text_input(
        "FEN position",
        value=default_fen,
        help="Paste a valid FEN. Default is the standard starting position.",
    )

    # Sidebar controls
    st.sidebar.header("Database & Filters")

    db_choice = st.sidebar.radio(
        "Database",
        ["Lichess (online games)", "Masters (OTB)"],
        help=(
            "Lichess database = all rated online games.\n"
            "Masters = curated over-the-board master games."
        ),
    )

    use_masters = db_choice == "Masters (OTB)"

    # Filters only apply to Lichess online DB
    speeds = []
    rating_groups = []

    if not use_masters:
        st.sidebar.subheader("Game speeds (online)")

        speed_options = ["bullet", "blitz", "rapid", "classical"]
        speeds = st.sidebar.multiselect(
            "Speeds",
            options=speed_options,
            default=["blitz", "rapid", "classical"],
            help="Select which time controls to include.",
        )

        st.sidebar.subheader("Rating filters (online)")

        rating_label_to_value = {
            "All ratings": None,
            "1600–1799": "1600",
            "1800–1999": "1800",
            "2000–2199": "2000",
            "2200–2499": "2200",
            "2500+": "2500",
        }

        rating_labels = list(rating_label_to_value.keys())

        selected_rating_labels = st.sidebar.multiselect(
            "Rating buckets",
            options=rating_labels,
            default=["All ratings"],
            help=(
                "These are Lichess Opening Explorer rating groups. "
                "If 'All ratings' is selected, other buckets are ignored."
            ),
        )

        if "All ratings" in selected_rating_labels:
            rating_groups = []
        else:
            rating_groups = [
                rating_label_to_value[label]
                for label in selected_rating_labels
                if rating_label_to_value[label] is not None
            ]

    st.sidebar.markdown("---")
    run_button = st.sidebar.button("Query Lichess")

    if run_button:
        if not validate_fen(fen):
            st.error("❌ Invalid FEN. Please check the string and try again.")
            return

        with st.spinner("Contacting Lichess Opening Explorer…"):
            url, params = build_lichess_explorer_url(
                fen=fen,
                use_masters=use_masters,
                speeds=speeds if speeds else None,
                rating_groups=rating_groups if rating_groups else None,
            )
            data = fetch_explorer_data(url, params)

        if data is None:
            return

        total_white = data.get("white", 0)
        total_black = data.get("black", 0)
        total_draws = data.get("draws", 0)
        total_games = total_white + total_black + total_draws

        st.subheader("Position overview")
        col1, col2 = st.columns(2)

        with col1:
            st.code(fen, language="text")
            st.write(
                f"**Total games in this position**: {total_games:,} "
                f"({total_white:,} white wins, {total_draws:,} draws, {total_black:,} black wins)"
            )

        with col2:
            try:
                board = chess.Board(fen)
                st.image(board._repr_svg_(), use_column_width=True)
            except Exception:
                st.info("Unable to render board (but FEN was accepted).")

        df_moves = build_moves_dataframe(data)

        if df_moves.empty:
            st.warning("No moves found for this position in the selected database/filters.")
            return

        st.subheader("Next move statistics")
        st.dataframe(
            df_moves,
            use_container_width=True,
            hide_index=True,
        )

        # Simple bar chart of frequency
        st.subheader("Move frequency chart")
        freq_chart_df = df_moves[["Move (SAN)", "Games"]]
        st.bar_chart(
            freq_chart_df.set_index("Move (SAN)"),
            use_container_width=True,
        )

        st.caption(
            "Data source: Lichess Opening Explorer API "
            "(https://explorer.lichess.ovh). Please respect Lichess rate limits."
        )


if __name__ == "__main__":
    main()
