from tkinter import *
from tkinter import messagebox

def next_turn(row, col):
    global player

    if buttons[row][col]['text'] == "" and not check_winner():
        buttons[row][col]['text'] = player
        buttons[row][col]['fg'] = "#ff1493" if player == 'X' else "#4B0082"

        if check_winner():
            label.config(text=(player + ' wins!'))
        elif not check_empty_space():
            label.config(text="No Winner!")
        else:
            player = 'O'
            label.config(text=(player + " turn"))
            ai_move()
    elif buttons[row][col]['text'] != "":
        messagebox.showinfo("Invalid move", "This square is already taken!")

def ai_move():
    best_score = -float('inf')
    best_move = None

    for row in range(3):
        for col in range(3):
            if buttons[row][col]['text'] == "":
                buttons[row][col]['text'] = 'O'
                score = minimax(buttons, 0, False, -float('inf'), float('inf'))
                buttons[row][col]['text'] = ""
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    if best_move:
        buttons[best_move[0]][best_move[1]]['text'] = 'O'
        buttons[best_move[0]][best_move[1]]['fg'] = "#4B0082"

    if check_winner():
        label.config(text='O wins!')
    elif not check_empty_space():
        label.config(text="No Winner!")
    else:
        global player
        player = 'X'
        label.config(text=(player + " turn"))

def minimax(board, depth, is_maximizing, alpha, beta):
    winner = get_winner()
    if winner == 'O':
        return 1
    elif winner == 'X':
        return -1
    elif not check_empty_space():
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col]['text'] == "":
                    board[row][col]['text'] = 'O'
                    score = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col]['text'] = ""
                    best_score = max(score, best_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col]['text'] == "":
                    board[row][col]['text'] = 'X'
                    score = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col]['text'] = ""
                    best_score = min(score, best_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score

def get_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != "":
            return buttons[row][0]['text']
    for col in range(3):
        if buttons[0][col]['text'] == buttons[1][col]['text'] == buttons[2][col]['text'] != "":
            return buttons[0][col]['text']
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != "":
        return buttons[0][0]['text']
    if buttons[0][2]['text'] == buttons[1][1]['text'] == buttons[2][0]['text'] != "":
        return buttons[0][2]['text']
    return None

def check_winner():
    return get_winner() is not None

def check_empty_space():
    for row in range(3):
        for col in range(3):
            if buttons[row][col]['text'] == "":
                return True
    return False

def start_new_game():
    global player
    player = 'X'
    label.config(text=(player + " turn"))
    for row in range(3):
        for col in range(3):
            buttons[row][col].config(text="", bg="white", fg="black")

window = Tk()
window.title("Tic Tac Toe vs AI")

player = 'X'
buttons = [[0, 0, 0] for _ in range(3)]

label = Label(text=(player + " turn"), font=('consolas', 40))
label.pack(side="top")

restart_btn = Button(text="Restart", font=('consolas', 20), command=start_new_game)
restart_btn.pack(side="top")

btns_frame = Frame(window)
btns_frame.pack()

for row in range(3):
    for col in range(3):
        buttons[row][col] = Button(btns_frame, text="", font=('consolas', 40), width=5, height=2,
                                   bg="white",
                                   command=lambda row=row, col=col: next_turn(row, col))
        buttons[row][col].grid(row=row, column=col)

window.mainloop()