from color_board import (
    setup_board,
    print_board,
    generate_legal_moves,
    move_piece,
    can_promote,
    promote_pawn,
)

def main():
    board = setup_board()

    while True:
        print_board(board)

        selected_square = input("Select piece (e.g., e2) or 'quit': ").strip().lower()
        if selected_square == "quit":
            break

        if selected_square not in board:
            print("Invalid square or no piece there.")
            continue

        legal_moves = generate_legal_moves(board, selected_square)

        promotion_squares = [
            move for move in legal_moves if can_promote(board[selected_square], move)
        ]

        # Detect castling squares (king moves two spaces)
        castling_squares = [
            move for move in legal_moves
            if board[selected_square][1] == 'k' and abs(ord(move[0]) - ord(selected_square[0])) == 2
        ]

        print_board(
            board,
            legal_moves=legal_moves,
            promotion_squares=promotion_squares,
            castling_squares=castling_squares,
            selected_square=selected_square,
        )

        user_input = input(f"Enter your move for {selected_square} or 'cancel': ").strip().lower()
        if user_input == "cancel":
            continue

        if user_input not in legal_moves:
            print("Illegal move.")
            continue

        moved = move_piece(board, selected_square, user_input)

        if moved and can_promote(board[user_input], user_input):
            promote_pawn(board, user_input, 'q')  # Auto promote to queen

if __name__ == "__main__":
    main()
