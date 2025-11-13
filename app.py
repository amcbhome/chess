import streamlit as st
import requests
import chess
import chess.svg
import base64

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Lichess FEN Explorer",
    page_icon="♟",
    layout="wide"
)

st.title("**FEN**")
st.write(
    "Enter any **FEN position** to query the Lichess Opening Explorer API. "
    "This tool returns: **most common next moves**, **play frequency**, "
    "**win rates**, **ECO codes**, and displays an **SVG board viewer**."
)

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("Database & Filters")

db_choice = st.sidebar.radio(
    "Database",
    ["Lichess Online", "Masters OTB"],
    index=0
)

speeds = st.sidebar.multiselect(
    "Game Speeds",
    ["bullet", "blitz", "rapid", "classical"],
    default=["blitz", "rapid"]
)

ratings = st.sidebar.selectbox(
    "Rating Range",
    ["all", "0-1400", "1400-1800", "1800-2200", "2200-9999"],
    index=0
)

# ---------------------------------------------------------
# SVG BOARD RENDERER
# ---------------------------------------------------------
def show_svg_board(fen):
    board = chess.Board(fen)
    svg_data = chess.svg.board(board, size=450)

    # encode SVG to base64
    b64 = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'

    st.markdown("### Board Viewer")
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# LICHESS API REQUEST FUNCTION
# ---------------------------------------------------------
def query_lichess(fen):
    # Select database
    url = "https://explorer.lichess.ovh/master" if db_choice == "Masters OTB" else "https://explorer.lichess.ovh/lichess"

    params = {
        "fen": fen.strip(),   # requests auto-encodes the spaces correctly
        "moves": 1,
        "topGames": 0,
    }

    # Lichess online DB only
    if db_choice == "Lichess Online":
        params["speeds"] = ",".join(speeds)
        params["ratings"] = ratings

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Lichess API returned status {response.status_code}")

    # Parse JSON safely
    try:
        return response.json()
    except:
        raise Exception("Invalid JSON returned by Lichess (likely no data available for this position).")


# ---------------------------------------------------------
# MOVE TABLE
# ---------------------------------------------------------
def show_move_table(data):
    moves = data.get("moves", [])

    if not moves:
        st.warning("No move statistics available for this position.")
        return

    table_data = []
    for m in moves:
        total = m["white"] + m["black"] + m["draws"]
        win_rate = round(100 * m["white"] / total, 1) if total > 0 else 0

        table_data.append({
            "Move (SAN)": m.get("san", "?"),
            "Move (UCI)": m["uci"],
            "White Win %": win_rate,
            "Games Played": total
        })

    st.subheader("Most Common Next Moves")
    st.dataframe(table_data, use_container_width=True)


# ---------------------------------------------------------
# MAIN INTERFACE
# ---------------------------------------------------------
fen_input = st.text_input(
    "FEN Position",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

if st.button("Query Lichess"):
    # Validate FEN first
    try:
        chess.Board(fen_input)
    except:
        st.error("Invalid FEN string. Please check for typos.")
        st.stop()

    try:
        data = query_lichess(fen_input)

        # Show chessboard
        show_svg_board(fen_input)
        st.write("---")

        # Show ECO Code
        if data.get("eco"):
            st.success(f"**ECO:** {data['eco']} — {data.get('name', '')}")
        else:
            st.info("No ECO classification for this position.")
        st.write("---")

        # Show move statistics
        show_move_table(data)

    except Exception as e:
        st.error(f"Error querying Lichess API: {e}")

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.write("---")
st.caption("© 2025 — Lichess FEN Explorer (SVG version, Streamlit Cloud compatible)")

