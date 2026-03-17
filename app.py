import streamlit as st
from copy import deepcopy

st.set_page_config(
    page_title="8-Queens Visual Solver",
    layout="wide"
)

# -----------------------------
# PROFESSIONAL CSS
# -----------------------------
st.markdown("""
<style>
/* Full app background */
.stApp {
    background: linear-gradient(135deg, #070b2d 0%, #12163f 45%, #1a1d45 100%);
    color: white;
}

/* Hide Streamlit header spacing issues a bit */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Main content spacing */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1rem;
}

/* Buttons - this selector is reliable */
.stButton > button {
    width: 100%;
    min-height: 68px;
    border: none !important;
    border-radius: 28px !important;
    font-size: 18px !important;
    font-weight: 700 !important;
    color: white !important;
    background: linear-gradient(135deg, #ff7a18, #ff4b6e) !important;
    box-shadow: 0 8px 20px rgba(0,0,0,0.22);
    transition: 0.2s ease-in-out;
}

/* Force inner text color too */
.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: white !important;
    font-weight: 700 !important;
    font-size: 18px !important;
}

/* Hover */
.stButton > button:hover {
    transform: translateY(-1px);
    filter: brightness(1.05);
}

/* Board */
.board {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    width: 100%;
    max-width: 640px;
    margin: 0 auto;
    border-radius: 26px;
    overflow: hidden;
    box-shadow: 0 12px 28px rgba(0,0,0,0.30);
}

.cell {
    aspect-ratio: 1 / 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    line-height: 1;
}

/* Status card */
.status-card {
    background: rgba(255,255,255,0.12);
    border-radius: 24px;
    padding: 22px 24px;
    margin-bottom: 18px;
}

.status-pill {
    display: inline-block;
    background: linear-gradient(135deg, #6b5cff, #6d6bff);
    color: white;
    font-weight: 700;
    font-size: 18px;
    padding: 10px 22px;
    border-radius: 999px;
    margin-bottom: 16px;
}

.status-text {
    color: white;
    font-size: 20px;
    font-weight: 600;
}

/* Text area styling */
textarea {
    background: #f1f2f6 !important;
    color: #222 !important;
    border-radius: 16px !important;
}

/* Label styling */
label, .stTextArea label, .stMarkdown, h1, h2, h3 {
    color: white !important;
}

/* Counter */
.counter-text {
    color: white;
    font-size: 28px;
    font-weight: 800;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SAFE CHECK
# -----------------------------
def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1:
            return False

    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1
        j += 1

    return True


# -----------------------------
# SOLVER
# -----------------------------
def solve_with_steps(n=8):
    board = [[0] * n for _ in range(n)]
    steps = []

    def add(action, msg=""):
        steps.append({
            "board": deepcopy(board),
            "action": action,
            "message": msg
        })

    def backtrack(row):
        if row == n:
            add("SOLVED", "All queens placed successfully!")
            return True

        for col in range(n):
            add("TRY", f"Trying ({row+1},{col+1})")

            if is_safe(board, row, col, n):
                board[row][col] = 1
                add("PLACE", f"Placed at ({row+1},{col+1})")

                if backtrack(row + 1):
                    return True

                board[row][col] = 0
                add("REMOVE", f"Backtrack from ({row+1},{col+1})")
            else:
                add("UNSAFE", f"Conflict at ({row+1},{col+1})")

        return False

    backtrack(0)
    return steps


# -----------------------------
# BOARD HTML
# -----------------------------
def board_to_html(board):
    html = "<div class='board'>"
    for r in range(8):
        for c in range(8):
            bg = "#efedf7" if (r + c) % 2 == 0 else "#a58be8"
            queen = "<span style='color:#1b174b; font-weight:900;'>♛</span>" if board[r][c] == 1 else ""
            html += f"<div class='cell' style='background:{bg};'>{queen}</div>"
    html += "</div>"
    return html


# -----------------------------
# SESSION STATE
# -----------------------------
if "steps" not in st.session_state:
    st.session_state.steps = []

if "idx" not in st.session_state:
    st.session_state.idx = 0


# -----------------------------
# VIEW
# -----------------------------
def get_view():
    steps = st.session_state.steps
    idx = st.session_state.idx

    if not steps:
        empty_board = [[0] * 8 for _ in range(8)]
        return empty_board, "", "No Data", "0 / 0"

    idx = max(0, min(idx, len(steps) - 1))
    st.session_state.idx = idx
    step = steps[idx]

    history = "\n".join(
        [f"{i+1}. {s['message']}" for i, s in enumerate(steps[:idx+1])]
    )

    return step["board"], history, step["message"], f"{idx+1} / {len(steps)}"


# -----------------------------
# TITLE
# -----------------------------
st.markdown("<h1 style='margin-bottom:18px;'>👑 8-Queens Visual Solver</h1>", unsafe_allow_html=True)

left, middle, right = st.columns([1.05, 2.1, 2.0], gap="large")

# -----------------------------
# BUTTONS
# -----------------------------
with left:
    if st.button("Generate Steps", use_container_width=True):
        st.session_state.steps = solve_with_steps(8)
        st.session_state.idx = 0

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    if st.button("⬅ Previous Step", use_container_width=True):
        if st.session_state.steps:
            st.session_state.idx = max(0, st.session_state.idx - 1)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    if st.button("Next Step ➡", use_container_width=True):
        if st.session_state.steps:
            st.session_state.idx = min(len(st.session_state.steps) - 1, st.session_state.idx + 1)

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    if st.button("Show Final Solution", use_container_width=True):
        if st.session_state.steps:
            st.session_state.idx = len(st.session_state.steps) - 1

    st.markdown("<div style='height:18px;'></div>", unsafe_allow_html=True)

    if st.button("Reset", use_container_width=True):
        st.session_state.steps = []
        st.session_state.idx = 0

# -----------------------------
# DISPLAY
# -----------------------------
board, history, status_msg, counter = get_view()

with middle:
    st.markdown(board_to_html(board), unsafe_allow_html=True)

with right:
    st.markdown(
        f"""
        <div class="status-card">
            <div class="status-pill">STATUS</div>
            <div class="status-text">{status_msg}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.text_area("Algorithm History", history, height=560)

st.markdown(f"<div class='counter-text'>{counter}</div>", unsafe_allow_html=True)
