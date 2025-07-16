from color_board import (
    setup_board, print_board, generate_legal_moves,
    move_piece, is_in_check, is_checkmate,
    can_promote, promote_pawn
)

def main():
    board = setup_board()
    current_turn = 'w'
    last_move = (None, None)  # (start_sq, end_sq)

    while True:
        # Find legal moves for selected piece
        print_board(board)

        if is_in_check(board, current_turn):
            if is_checkmate(board, current_turn):
                print(f"\nCheckmate! {'Black' if current_turn == 'w' else 'White'} wins!")
                break
            print(f"\n{'White' if current_turn == 'w' else 'Black'} is in check!")

        print(f"\n{'White' if current_turn == 'w' else 'Black'} to move.")

        selected_square = input("Select piece (e.g., e2) or 'quit': ").strip().lower()
        if selected_square == "quit":
            break

        if selected_square not in board or board[selected_square][0] != current_turn:
            print("Invalid selection or no piece of your color there.")
            continue

        legal_moves = generate_legal_moves(board, selected_square, last_move=last_move)
        if not legal_moves:
            print("No legal moves for that piece. Select another.")
            continue

        promotion_squares = [sq for sq in legal_moves if can_promote(board[selected_square], sq)]

        # Detect castling squares for king moves
        castling_squares = []
        piece = board[selected_square]
        if piece[1] == 'k':
            castling_squares = [sq for sq in legal_moves if abs(ord(sq[0]) - ord(selected_square[0])) == 2]

        # Detect en passant squares
        en_passant_squares = []
        for sq in legal_moves:
            # En passant squares are empty squares diagonally in front of pawn
            if sq not in board and piece[1] == 'p' and abs(ord(sq[0]) - ord(selected_square[0])) == 1:
                en_passant_squares.append(sq)

        print_board(
            board,
            legal_moves=legal_moves,
            promotion_squares=promotion_squares,
            castling_squares=castling_squares,
            en_passant_squares=en_passant_squares,
            selected_square=selected_square,
        )

        dest_square = input(f"Enter move target for {selected_square} or 'cancel': ").strip().lower()
        if dest_square == "cancel":
            continue

        if dest_square not in legal_moves:
            print("Illegal move.")
            continue

        moved = move_piece(board, selected_square, dest_square, last_move=last_move)
        if not moved:
            print("Move failed.")
            continue

        # Update last move after successful move
        last_move = (selected_square, dest_square)

        # Handle pawn promotion
        if can_promote(board.get(dest_square, ""), dest_square):
            while True:
                choice = input("Promote to (q, r, b, n): ").strip().lower()
                if choice in ('q', 'r', 'b', 'n'):
                    promote_pawn(board, dest_square, choice)
                    break
                print("Invalid choice. Choose one of q, r, b, or n.")

        current_turn = 'b' if current_turn == 'w' else 'w'

if __name__ == "__main__":
    main()
