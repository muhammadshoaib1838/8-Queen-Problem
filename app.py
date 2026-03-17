import streamlit as st
from copy import deepcopy

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
        i -= 1; j -= 1

    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i][j] == 1:
            return False
        i -= 1; j += 1

    return True


# -----------------------------
# SOLVER
# -----------------------------
def solve_with_steps(n=8):
    board = [[0]*n for _ in range(n)]
    steps = []

    def add(action,row=None,col=None,msg=""):
        steps.append({
            "board": deepcopy(board),
            "action": action,
            "row": row,
            "col": col,
            "message": msg
        })

    def backtrack(row):
        if row==n:
            add("solved",msg="All queens placed successfully!")
            return True

        for col in range(n):
            add("try",row,col,f"Trying ({row+1},{col+1})")

            if is_safe(board,row,col,n):
                board[row][col]=1
                add("place",row,col,f"Placed at ({row+1},{col+1})")

                if backtrack(row+1):
                    return True

                board[row][col]=0
                add("remove",row,col,f"Backtrack from ({row+1},{col+1})")
            else:
                add("unsafe",row,col,f"Conflict at ({row+1},{col+1})")

        return False

    backtrack(0)
    return steps


# -----------------------------
# BOARD DISPLAY
# -----------------------------
def board_to_html(board):
    html = "<div style='display:grid;grid-template-columns:repeat(8,1fr);max-width:500px;'>"
    for r in range(8):
        for c in range(8):
            color = "#f5f3ff" if (r+c)%2==0 else "#c4b5fd"
            queen = "♛" if board[r][c]==1 else ""
            html += f"<div style='height:60px;display:flex;align-items:center;justify-content:center;background:{color};font-size:24px'>{queen}</div>"
    html += "</div>"
    return html


# -----------------------------
# STREAMLIT STATE INIT
# -----------------------------
if "steps" not in st.session_state:
    st.session_state.steps = []

if "idx" not in st.session_state:
    st.session_state.idx = 0


# -----------------------------
# VIEW FUNCTION
# -----------------------------
def get_view():
    steps = st.session_state.steps
    idx = st.session_state.idx

    if not steps:
        empty = [[0]*8 for _ in range(8)]
        return board_to_html(empty), "", "No Data", "0 / 0"

    idx = max(0, min(idx, len(steps)-1))
    step = steps[idx]

    board = board_to_html(step["board"])

    history = "\n".join(
        [f"{i+1}. {s['message']}" for i,s in enumerate(steps[:idx+1])]
    )

    status = f"{step['action'].upper()} → {step['message']}"
    counter = f"{idx+1} / {len(steps)}"

    return board, history, status, counter


# -----------------------------
# UI
# -----------------------------
st.title("👑 8-Queens Visual Solver")

col1, col2, col3 = st.columns([1,2,2])

with col1:
    if st.button("Generate Steps"):
        st.session_state.steps = solve_with_steps(8)
        st.session_state.idx = 0

    if st.button("⬅ Previous"):
        st.session_state.idx -= 1

    if st.button("Next ➡"):
        st.session_state.idx += 1

    if st.button("Final"):
        if st.session_state.steps:
            st.session_state.idx = len(st.session_state.steps) - 1

    if st.button("Reset"):
        st.session_state.steps = []
        st.session_state.idx = 0


board, history, status, counter = get_view()

with col2:
    st.markdown(board, unsafe_allow_html=True)

with col3:
    st.markdown(f"**Status:** {status}")
    st.text_area("Algorithm History", history, height=400)

st.markdown(f"### Step: {counter}")
