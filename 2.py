from typing import List

def tic_tac_toe_checker(board: List[List[str]]) -> str:
    # строки и столбцы
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "-":
            return f"{board[i][0]} wins!"  # win row
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "-":
            return f"{board[0][i]} wins!"  # win column

    # диагонали
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "-":
        return f"{board[0][0]} wins!"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "-":
        return f"{board[0][2]} wins!"

    # пустые клетки
    if any("-" in row for row in board):
        return "unfinished!"

    return "draw!"  # draw

# Примеры вызова функции
if __name__ == "__main__":
    board1 = [["-", "-", "o"],
              ["-", "x", "o"],
              ["x", "o", "x"]]
    print(tic_tac_toe_checker(board1))  # null

    board2 = [["-", "-", "o"],
              ["-", "o", "o"],
              ["x", "x", "x"]]
    print(tic_tac_toe_checker(board2))  # win

    board3 = [["o", "x", "o"],
              ["x", "o", "x"],
              ["x", "o", "x"]]
    print(tic_tac_toe_checker(board3))  # draw
