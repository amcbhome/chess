import streamlit as st
import requests
import chess
import chess.svg
import base64

st.set_page_config(
    page_title="Lichess FEN Explorer",
    page_icon="♟",
    layout="wide"
)

st.title("♟ Lichess Opening Explorer from FEN")
st.write(
    "Enter any **FEN position** to query the Lichess Opening Explorer API.\n"
    "This tool returns: **most common next moves**, **play frequency**, **win rates**, "
    "**ECO codes**, and displays an **SVG board viewer**."
)

# -----------------------------
# Sidebar
# -----------------------------
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

# -----------------------------
# SVG Board Viewer (works everywhere)
# -----------------------------
def show_svg_board(fen):
    board = chess.Board(fen)
    svg_code = chess.svg.board(board, size=450)

    # Encode SVG as base64
    b64 = base64.b64encode(svg_code.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" />'

    st.markdown("### Position Viewer")
    st.markdown(html, unsafe_allow_html=True)


# -----------------------------
# Lichess API
# -----------------------------
def query_lichess(fen):
    url = "https://explorer.lichess.ovh/master" if db_choice == "Masters OTB" else "https://explorer.lichess.ovh/lichess"

    params = {
        "fen": fen,
        "moves": 1,
        "topGames": 0,
        "speeds": ",".join(speeds),
        "ratings": ratings
    }

    r = requests.get(url, params=params)
    return r.json()


# -----------------------------
# Move Table
# -----------------------------
def show_move_table(data):
    moves = data.get("moves", [])
    if not moves:
        st.warning("No move statistics available.")
        return

    table_data = []
    for m in moves:
        total = m["white"] + m["black"] + m["draws"]
        win_rate = round(100 * m["white"] / total, 1) if total > 0 else 0

        table_data.append({
            "Move (SAN)": m.get("san", "?"),
            "Move (UCI)": m["uci"],
            "White Win %": win_rate,
            "Games": total
        })

    st.dataframe(table_data)


# -----------------------------
# Input FEN
# -----------------------------
fen_input = st.text_input(
    "FEN Position",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

if st.button("Query Lichess"):
    try:
        data = query_lichess(fen_input)

        # Show board
        show_svg_board(fen_input)
        st.write("---")

        # ECO code
        if data.get("eco"):
            st.success(f"**ECO:** {data['eco']} — {data.get('name','')}")
        else:
            st.info("No ECO classification for this position.")

        st.write("---")

        # Move stats
        show_move_table(data)

    except Exception as e:
        st.error(f"Error querying Lichess API: {e}")


st.write("---")
st.caption("© 2025 — Lichess FEN Explorer (SVG version, Streamlit Cloud compatible)")
