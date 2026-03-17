import streamlit as st
from copy import deepcopy

st.set_page_config(layout="wide")

# -----------------------------
# FULL BACKGROUND + BUTTON STYLE
# -----------------------------
st.markdown("""
<style>

/* FULL PAGE BACKGROUND */
html, body, [data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #0f1020, #1a1d38, #05060f);
    color: white;
}

/* REMOVE WHITE HEADER */
header {visibility: hidden;}

/* BUTTON BASE STYLE */
.stButton > button {
    width: 100%;
    border-radius: 30px;
    padding: 18px;
    font-size: 18px;
    font-weight: bold;
    border: none;
    color: white;
}

/* INDIVIDUAL BUTTON COLORS */
div[data-testid="column"] > div:nth-child(1) .stButton:nth-child(1) button {
    background: linear-gradient(135deg,#ff7a18,#ff3d77);
}

div[data-testid="column"] > div:nth-child(1) .stButton:nth-child(2) button {
    background: linear-gradient(135deg,#ff7a18,#ff3d77);
}

div[data-testid="column"] > div:nth-child(1) .stButton:nth-child(3) button {
    background: linear-gradient(135deg,#ff7a18,#ff3d77);
}

div[data-testid="column"] > div:nth-child(1) .stButton:nth-child(4) button {
    background: linear-gradient(135deg,#ff7a18,#ff3d77);
}

div[data-testid="column"] > div:nth-child(1) .stButton:nth-child(5) button {
    background: linear-gradient(135deg,#ff4d6d,#ff758c);
}

/* BOARD */
.board {
    display:grid;
    grid-template-columns: repeat(8, 1fr);
    max-width:520px;
    margin:auto;
    border-radius:20px;
    overflow:hidden;
}

/* CELLS */
.cell {
    height:65px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:28px;
}

/* STATUS CARD */
.status {
    padding:20px;
    border-radius:15px;
    background: rgba(255,255,255,0.1);
    margin-bottom:10px;
}

.pill {
    background:#6C63FF;
    padding:6px 14px;
    border-radius:20px;
    display:inline-block;
    margin-bottom:8px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOGIC
# -----------------------------
def is_safe(board, row, col, n):
    for i in range(row):
        if board[i][col] == 1:
            return False

    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1; j -= 1

    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1; j += 1

    return True

def solve_with_steps(n=8):
    board = [[0]*n for _ in range(n)]
    steps = []

    def add(action,msg=""):
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

            if is_safe(board,row,col,n):
                board[row][col]=1
                add("PLACE", f"Placed at ({row+1},{col+1})")

                if backtrack(row+1):
                    return True

                board[row][col]=0
                add("REMOVE", f"Backtrack from ({row+1},{col+1})")
            else:
                add("UNSAFE", f"Conflict at ({row+1},{col+1})")

        return False

    backtrack(0)
    return steps

def board_to_html(board):
    html = "<div class='board'>"
    for r in range(8):
        for c in range(8):
            color = "#f5f3ff" if (r+c)%2==0 else "#c4b5fd"
            queen = "♛" if board[r][c]==1 else ""
            html += f"<div class='cell' style='background:{color}'>{queen}</div>"
    html += "</div>"
    return html

# -----------------------------
# STATE
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
        return [[0]*8 for _ in range(8)], "", "No Data", "0/0"

    idx = max(0, min(idx, len(steps)-1))
    step = steps[idx]

    history = "\n".join(
        [f"{i+1}. {s['message']}" for i,s in enumerate(steps[:idx+1])]
    )

    return step["board"], history, step["message"], f"{idx+1}/{len(steps)}"

# -----------------------------
# UI
# -----------------------------
st.markdown("## 👑 8-Queens Visual Solver")

col1, col2, col3 = st.columns([1,2,2])

with col1:
    if st.button("Generate Steps"):
        st.session_state.steps = solve_with_steps()
        st.session_state.idx = 0

    if st.button("⬅ Previous Step"):
        st.session_state.idx -= 1

    if st.button("Next Step ➡"):
        st.session_state.idx += 1

    if st.button("Show Final Solution"):
        if st.session_state.steps:
            st.session_state.idx = len(st.session_state.steps)-1

    if st.button("Reset"):
        st.session_state.steps = []
        st.session_state.idx = 0

board, history, status_msg, counter = get_view()

with col2:
    st.markdown(board_to_html(board), unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="status">
        <div class="pill">STATUS</div>
        <div>{status_msg}</div>
    </div>
    """, unsafe_allow_html=True)

    st.text_area("Algorithm History", history, height=420)

st.markdown(f"### {counter}")
