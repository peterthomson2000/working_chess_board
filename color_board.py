from typing import Dict, List, Optional

RESET = "\033[0m"

# Base square colors
BG_LIGHT = "\033[48;5;230m"   # tan
BG_DARK = "\033[48;5;22m"     # forest green

# Highlighting
HIGHLIGHT_LIGHT = "\033[48;5;229m"  # yellow
HIGHLIGHT_DARK = "\033[48;5;120m"   # light green
SELECTED_BG = "\033[48;5;220m"      # gold

# Purple for promotion or castling
PROMO_LIGHT = "\033[48;5;183m"
PROMO_DARK = "\033[48;5;91m"

COLS = "abcdefgh"

def setup_board() -> Dict[str, str]:
    board = {}
    for col in COLS:
        board[col + "2"] = "wp"
        board[col + "7"] = "bp"
    board.update({
        'a1': 'wr', 'b1': 'wn', 'c1': 'wb', 'd1': 'wq', 'e1': 'wk', 'f1': 'wb', 'g1': 'wn', 'h1': 'wr',
        'a8': 'br', 'b8': 'bn', 'c8': 'bb', 'd8': 'bq', 'e8': 'bk', 'f8': 'bb', 'g8': 'bn', 'h8': 'br',
    })
    return board

def inside_board(c: str, r: int) -> bool:
    return 'a' <= c <= 'h' and 1 <= r <= 8

def is_path_clear(board: Dict[str, str], squares: List[str]) -> bool:
    return all(sq not in board for sq in squares)

def is_square_attacked(board: Dict[str, str], square: str, attacker_color: str) -> bool:
    for sq, piece in board.items():
        if piece[0] != attacker_color:
            continue
        if square in generate_legal_moves(board, sq, ignore_castling=True):
            return True
    return False

def generate_legal_moves(board: Dict[str, str], square: str, ignore_castling: bool = False) -> List[str]:
    piece = board.get(square)
    if not piece:
        return []

    color, ptype = piece[0], piece[1]
    row = int(square[1])
    col = square[0]
    directions = []
    moves = []
    enemy = 'b' if color == 'w' else 'w'

    if ptype == 'p':
        step = 1 if color == 'w' else -1
        fwd = col + str(row + step)
        if inside_board(col, row + step) and fwd not in board:
            moves.append(fwd)
            if (color == 'w' and row == 2) or (color == 'b' and row == 7):
                fwd2 = col + str(row + 2 * step)
                if fwd2 not in board:
                    moves.append(fwd2)
        for dcol in [-1, 1]:
            nc = chr(ord(col) + dcol)
            target = nc + str(row + step)
            if inside_board(nc, row + step):
                if target in board and board[target][0] == enemy:
                    moves.append(target)

    elif ptype == 'r':
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
    elif ptype == 'b':
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
    elif ptype == 'q':
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
    elif ptype == 'k':
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == dy == 0: continue
                nc = chr(ord(col) + dx)
                nr = row + dy
                target = nc + str(nr)
                if inside_board(nc, nr):
                    if target not in board or board[target][0] != color:
                        moves.append(target)
        if not ignore_castling and board.get(square) == color + 'k':
            if color == 'w' and square == 'e1':
                # Kingside castling
                if 'h1' in board and board['h1'] == 'wr' and is_path_clear(board, ['f1', 'g1']):
                    if not any(is_square_attacked(board, sq, 'b') for sq in ['e1', 'f1', 'g1']):
                        moves.append('g1')
                # Queenside castling
                if 'a1' in board and board['a1'] == 'wr' and is_path_clear(board, ['b1', 'c1', 'd1']):
                    if not any(is_square_attacked(board, sq, 'b') for sq in ['e1', 'd1', 'c1']):
                        moves.append('c1')
            elif color == 'b' and square == 'e8':
                # Kingside castling
                if 'h8' in board and board['h8'] == 'br' and is_path_clear(board, ['f8', 'g8']):
                    if not any(is_square_attacked(board, sq, 'w') for sq in ['e8', 'f8', 'g8']):
                        moves.append('g8')
                # Queenside castling
                if 'a8' in board and board['a8'] == 'br' and is_path_clear(board, ['b8', 'c8', 'd8']):
                    if not any(is_square_attacked(board, sq, 'w') for sq in ['e8', 'd8', 'c8']):
                        moves.append('c8')

    elif ptype == 'n':
        for dx, dy in [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]:
            nc = chr(ord(col) + dx)
            nr = row + dy
            target = nc + str(nr)
            if inside_board(nc, nr):
                if target not in board or board[target][0] != color:
                    moves.append(target)

    for dc, dr in directions:
        step = 1
        while True:
            nc = chr(ord(col) + dc * step)
            nr = row + dr * step
            target = nc + str(nr)
            if not inside_board(nc, nr):
                break
            if target in board:
                if board[target][0] != color:
                    moves.append(target)
                break
            moves.append(target)
            step += 1

    return moves

def can_promote(piece: str, square: str) -> bool:
    if piece not in ('wp', 'bp'):
        return False
    rank = int(square[1])
    return (piece == 'wp' and rank == 8) or (piece == 'bp' and rank == 1)

def promote_pawn(board: Dict[str, str], square: str, new_piece_type: str) -> None:
    color = board[square][0]
    board[square] = color + new_piece_type

def move_piece(board: Dict[str, str], start: str, end: str) -> bool:
    piece = board.get(start)
    if not piece:
        return False
    legal = generate_legal_moves(board, start)
    if end not in legal:
        return False

    if piece[1] == 'k' and abs(ord(end[0]) - ord(start[0])) == 2:
        # Castling move
        if end[0] == 'g':
            rook_start, rook_end = 'h' + start[1], 'f' + start[1]
        else:
            rook_start, rook_end = 'a' + start[1], 'd' + start[1]
        board[rook_end] = board[rook_start]
        del board[rook_start]

    board[end] = piece
    del board[start]
    return True

def print_board(board: Dict[str, str], legal_moves: Optional[List[str]] = None,
                promotion_squares: Optional[List[str]] = None,
                castling_squares: Optional[List[str]] = None,
                selected_square: Optional[str] = None) -> None:

    col_indices = {c: i for i, c in enumerate(COLS)}

    print()
    print("       " + "         ".join(COLS))
    print("  ⌜" + "─────────┬" * 7 + "─────────⌝")

    # Combine promotion and castling squares for purple highlight
    purple_squares = set()
    if promotion_squares:
        purple_squares.update(promotion_squares)
    if castling_squares:
        purple_squares.update(castling_squares)

    for r in reversed("12345678"):
        for line in ["top", "mid", "bot"]:
            if line == "top":
                print(f"{r} │", end="")
            else:
                print("  │", end="")

            for c in COLS:
                sq = c + r
                idx_sum = col_indices[c] + int(r)
                base_bg = BG_LIGHT if idx_sum % 2 == 0 else BG_DARK
                highlight_bg = HIGHLIGHT_LIGHT if idx_sum % 2 == 0 else HIGHLIGHT_DARK
                promo_bg = PROMO_LIGHT if idx_sum % 2 == 0 else PROMO_DARK

                bg = base_bg
                if sq in purple_squares:
                    bg = promo_bg
                elif legal_moves and sq in legal_moves:
                    bg = highlight_bg
                if selected_square == sq:
                    bg = SELECTED_BG

                piece = board.get(sq, "")
                content = piece.center(5) if piece else "     "

                if line == "top" or line == "bot":
                    print(bg + "         " + RESET, end="│")
                elif line == "mid":
                    print(bg + f"  {content}  " + RESET, end="│")

            if line == "mid":
                print(f" {r}")
            else:
                print()

        if r != "1":
            print("  ├" + "─────────┼" * 7 + "─────────┤")
    print("  ⌞" + "─────────┴" * 7 + "─────────⌟")
