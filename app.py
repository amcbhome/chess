import streamlit as st
import requests
import chess
import chess.pgn
import chess.svg
from streamlit_chessboard import st_chessboard

# -----------------------------
# Streamlit Page Config
# -----------------------------
st.set_page_config(
    page_title="Lichess FEN Explorer",
    page_icon="♟",
    layout="wide"
)

st.title("♟ Lichess Opening Explorer from FEN")
st.write(
    "Enter any **FEN position** to query the Lichess Opening Explorer API.\n"
    "This tool returns: **most common next moves**, **play frequency**, **win rates**, "
    "**ECO codes**, and an **interactive board viewer**."
)

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("Database & Filters")

db_choice = st.sidebar.radio(
    "Database",
    ["Lichess Online", "Masters OTB"],
    index=0
)

speeds_map = {
    "bullet": "bullet",
    "blitz": "blitz",
    "rapid": "rapid",
    "classical": "classical"
}

speeds = st.sidebar.multiselect(
    "Game Speeds (Online only)",
    list(speeds_map.keys()),
    default=["blitz", "rapid"]
)

ratings = st.sidebar.selectbox(
    "Rating Range",
    ["all", "0-1400", "1400-1800", "1800-2200", "2200-9999"],
    index=0
)

# -----------------------------
# FEN Input
# -----------------------------
fen_input = st.text_input(
    "FEN Position",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

# -----------------------------
# Function: Query Lichess API
# -----------------------------
def query_lichess(fen):
    if db_choice == "Masters OTB":
        url = "https://explorer.lichess.ovh/master"
    else:
        url = "https://explorer.lichess.ovh/lichess"

    params = {
        "fen": fen,
        "moves": 1,
        "topGames": 0,
        "speeds": ",".join(speeds),
        "ratings": ratings
    }

    response = requests.get(url, params=params)
    return response.json()


# -----------------------------
# Board Viewer
# -----------------------------
def show_board(fen):
    st.subheader("Interactive Board Viewer")
    st_chessboard(
        fen=fen,
        key="board"
    )


# -----------------------------
# Show ECO classification
# -----------------------------
def show_eco(data):
    eco = data.get("eco")
    name = data.get("name")
    if eco:
        st.success(f"**Opening ECO:** {eco} — {name}")
    else:
        st.info("ECO code not available for this position.")


# -----------------------------
# Show Move Statistics
# -----------------------------
def show_move_table(data):
    moves = data.get("moves", [])

    if not moves:
        st.warning("No move statistics available for this position.")
        return

    st.subheader("Most Common Next Moves")
    table_data = []
    for m in moves:
        uci = m["uci"]
        san = m.get("san", "?")
        white = m["white"]
        black = m["black"]
        draws = m["draws"]
        total = white + black + draws

        win_rate = round(100 * white / total, 1) if total > 0 else 0

        table_data.append({
            "Move (SAN)": san,
            "Move (UCI)": uci,
            "White Wins %": win_rate,
            "Games": total
        })

    st.dataframe(table_data)


# -----------------------------
# MAIN LOGIC
# -----------------------------
if st.button("Query Lichess"):
    try:
        data = query_lichess(fen_input)

        show_board(fen_input)
        st.write("---")

        show_eco(data)
        st.write("---")

        show_move_table(data)

    except Exception as e:
        st.error(f"Error querying Lichess API: {e}")

# FOOTER
st.write("---")
st.caption("© 2025 — Lichess FEN Explorer | Built using Lichess API, python-chess, and streamlit-chessboard.")

