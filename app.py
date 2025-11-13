import streamlit as st

st.set_page_config(
    page_title="Lichess Opening Statistics from FEN",
    page_icon="♟",
    layout="wide",
)

# ---------------------------------------------
# SIDEBAR — DATABASE & FILTERS
# ---------------------------------------------

st.sidebar.header("Database & Filters")

db_choice = st.sidebar.radio(
    "Database",
    options=["Lichess (online games)", "Masters (OTB)"],
    index=0
)

speeds = st.sidebar.multiselect(
    "Game speeds (online)",
    ["bullet", "blitz", "rapid", "classical"],
    default=["blitz", "rapid", "classical"]
)

ratings = st.sidebar.selectbox(
    "Rating buckets (online)",
    ["All ratings", "0–1400", "1400–1800", "1800–2200", "2200+"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.caption("Filters ready.")


# ---------------------------------------------
# MAIN TITLE
# ---------------------------------------------

st.title("♟ Lichess Opening Statistics from FEN")
st.write(
    "Enter any chess position in **FEN format** and query the Lichess Opening Explorer "
    "(online games or Masters DB) to see the most common next moves and their statistics."
)


# ---------------------------------------------
# FEN INPUT
# ---------------------------------------------

fen_input = st.text_input(
    "FEN position",
    value="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
)

if st.button("Query Lichess"):
    st.info("🔍 Lichess API query would run here (your API logic).")
    st.write("FEN queried:", fen_input)

    # placeholder output
    st.success("Example output: Move statistics would be displayed here.")


# ---------------------------------------------
# END OF APP
# ---------------------------------------------

st.write("---")
st.caption("© 2025 — Lichess FEN Opening Stats Tool (Streamlit)")

