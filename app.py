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
    "This tool returns **common next moves**, **ECO codes**, "
    "**winrates**, and displays a **board viewer**."
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
    "Game Speeds (online db)",
    ["bullet", "blitz", "rapid", "classical"],
    default=["blitz", "rapid"]
)

ratings = st.sidebar.selectbox(
    "Rating Range (online db)",
    ["all", "0-1400", "1400-1800", "1800-2200", "2200-9999"],
    index=0
)

# ---------------------------------------------------------
# BOARD RENDERER (SVG)
# ---------------------------------------------------------
def show_svg_board(fen):
    board = chess.Board(fen)
    svg = chess.svg.board(board, size=450)

    b64 = base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    html = f'<img src="data:image/svg+xml;base64,{b64}" />'

    st.markdown("### Board Viewer")
    st.markdown(html, unsafe_allow_html=True)


# ---------------------------------------------------------
# FIXED LICHESS API QUERY (SPEEDS[] + RATINGS[] correct)
# ---------------------------------------------------------
def query_lichess(fen):
    url = (
        "https://explorer.lichess.ovh/master"
        if db_choice == "Masters OTB"
        else "https://explorer.lichess.ovh/lichess"
    )

    params = {
        "fen": fen.strip(),
        "moves": 1,
        "topGames": 0,
    }

    # Online DB only
    if db_choice == "Lichess Online":

        # Add speeds[] correctly
        for sp in speeds:
            params.setdefault("speeds[]", []).append(sp)

        # Add rating range correctly
        if ratings != "all":
            lo, hi = ratings.split("-")
            params["ratings[]"] = [lo, hi]

    # Send request
    r = requests.get(url, params=params)

    if r.status_code != 200:
        raise Exception(f"Lichess returned error {r.status_code}")

    try:
        return r.json()
    except:
        raise Exception("Invalid or empty JSON from Lichess (likely no games match filters).")


# ---------------------------------------------------------
# MOVE TABLE
# ---------------------------------------------------------
def show_move_table(data):
    moves = data.get("moves", [])

    if not moves:
        st.warning("No moves found for this position.")
        return

    rows = []
    for m in moves:
        total = m["white"] + m["black"] + m["draws"]
        winrate = round(m["white"] * 100 / total, 1) if total > 0 else 0

        rows.append({
            "Move (SAN)": m.get("san", "?"),
            "Move (UCI)": m["uci"],
            "White Win %": winrate,
            "Games Played": total
        })

    st.subheader("Most Common Next Moves")
    st.dataframe(rows, use_container_width=True)


# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
fen_input = st.text_input(
    "FEN Position",
    "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

if st.button("Query Lichess"):

    # Validate FEN
    try:
        chess.Board(fen_input)
    except:
        st.error("Invalid FEN. Check for mistakes.")
        st.stop()

    try:
        data = query_lichess(fen_input)

        # Board
        show_svg_board(fen_input)
        st.write("---")

        # ECO
        if data.get("eco"):
            st.success(f"**ECO:** {data['eco']} — {data.get('name','')}")
        else:
            st.info("No ECO code available.")

        st.write("---")

        # Moves
        show_move_table(data)

    except Exception as e:
        st.error(str(e))

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------
st.write("---")
st.caption("© 2025 — Lichess FEN Explorer (Streamlit Cloud compatible)")

