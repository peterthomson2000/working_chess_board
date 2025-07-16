from typing import Dict, List, Optional, Tuple

def create_empty_board() -> Dict[str, Optional[str]]:
    board = {}
    columns = "abcdefgh"
    rows = "12345678"
    for col in columns:
        for row in rows:
            board[col + row] = None
    return board

def setup_board() -> Dict[str, Optional[str]]:
    board = create_empty_board()
    for col in "abcdefgh":
        board[col + "2"] = "wp"
        board[col + "7"] = "bp"

    # White back rank
    board["a1"] = "wr"
    board["b1"] = "wn"
    board["c1"] = "wb"
    board["d1"] = "wq"
    board["e1"] = "wk"
    board["f1"] = "wb"
    board["g1"] = "wn"
    board["h1"] = "wr"

    # Black back rank
    board["a8"] = "br"
    board["b8"] = "bn"
    board["c8"] = "bb"
    board["d8"] = "bq"
    board["e8"] = "bk"
    board["f8"] = "bb"
    board["g8"] = "bn"
    board["h8"] = "br"

    return board

def promote_pawn(board: Dict[str, Optional[str]], square: str, color_char: str):
    while True:
        choice = input("Promote to (q, r, b, n): ").strip().lower()
        if choice in ['q', 'r', 'b', 'n']:
            board[square] = color_char + choice
            print(f"Pawn promoted to {board[square]}!")
            break
        else:
            print("Invalid choice. Choose one of q, r, b, n.")

def in_bounds(col: str, row: int) -> bool:
    return col in "abcdefgh" and 1 <= row <= 8

def opponent(color: str) -> str:
    return 'b' if color == 'w' else 'w'

def generate_legal_moves(board: Dict[str, Optional[str]], square: str) -> List[str]:
    piece = board.get(square)
    if not piece:
        return []
    color = piece[0]
    ptype = piece[1]
    col, row = square[0], int(square[1])
    moves = []

    directions = []
    cols = "abcdefgh"

    if ptype == 'p':  # Pawn moves
        direction = 1 if color == 'w' else -1
        start_row = 2 if color == 'w' else 7
        # Forward 1
        fwd1 = col + str(row + direction)
        if in_bounds(col, row + direction) and board.get(fwd1) is None:
            moves.append(fwd1)
            # Forward 2 if first move
            fwd2 = col + str(row + 2*direction)
            if row == start_row and board.get(fwd2) is None:
                moves.append(fwd2)
        # Captures
        for dc in [-1, 1]:
            c_col = chr(ord(col) + dc)
            capture_sq = c_col + str(row + direction)
            if in_bounds(c_col, row + direction):
                target = board.get(capture_sq)
                if target is not None and target[0] == opponent(color):
                    moves.append(capture_sq)

    elif ptype == 'r':  # Rook
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dc, dr in directions:
            c_col, c_row = ord(col), row
            while True:
                c_col += dc
                c_row += dr
                if not in_bounds(chr(c_col), c_row):
                    break
                pos = chr(c_col) + str(c_row)
                if board.get(pos) is None:
                    moves.append(pos)
                else:
                    if board[pos][0] == opponent(color):
                        moves.append(pos)
                    break

    elif ptype == 'b':  # Bishop
        directions = [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dc, dr in directions:
            c_col, c_row = ord(col), row
            while True:
                c_col += dc
                c_row += dr
                if not in_bounds(chr(c_col), c_row):
                    break
                pos = chr(c_col) + str(c_row)
                if board.get(pos) is None:
                    moves.append(pos)
                else:
                    if board[pos][0] == opponent(color):
                        moves.append(pos)
                    break

    elif ptype == 'q':  # Queen (rook + bishop)
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dc, dr in directions:
            c_col, c_row = ord(col), row
            while True:
                c_col += dc
                c_row += dr
                if not in_bounds(chr(c_col), c_row):
                    break
                pos = chr(c_col) + str(c_row)
                if board.get(pos) is None:
                    moves.append(pos)
                else:
                    if board[pos][0] == opponent(color):
                        moves.append(pos)
                    break

    elif ptype == 'n':  # Knight
        knight_moves = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        for dc, dr in knight_moves:
            c_col = chr(ord(col) + dc)
            c_row = row + dr
            if in_bounds(c_col, c_row):
                pos = c_col + str(c_row)
                target = board.get(pos)
                if target is None or target[0] == opponent(color):
                    moves.append(pos)

    elif ptype == 'k':  # King
        king_moves = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]
        for dc, dr in king_moves:
            c_col = chr(ord(col) + dc)
            c_row = row + dr
            if in_bounds(c_col, c_row):
                pos = c_col + str(c_row)
                target = board.get(pos)
                if target is None or target[0] == opponent(color):
                    moves.append(pos)

    return moves

def move_piece(board: Dict[str, Optional[str]], start: str, end: str) -> bool:
    if start not in board or end not in board:
        print("Invalid square.")
        return False
    piece = board[start]
    if not piece:
        print(f"No piece at {start}.")
        return False
    legal_moves = generate_legal_moves(board, start)
    if end not in legal_moves:
        print("Illegal move.")
        return False

    # Move piece
    board[end] = piece
    board[start] = None

    # Promotion for pawns only on last rank
    color, ptype = piece[0], piece[1]
    if ptype == 'p':
        if (color == 'w' and end[1] == '8') or (color == 'b' and end[1] == '1'):
            promote_pawn(board, end, color)

    return True

def can_promote(piece: Optional[str], square: str) -> bool:
    if not piece:
        return False
    if piece[1] != 'p':
        return False
    color = piece[0]
    return (color == 'w' and square[1] == '8') or (color == 'b' and square[1] == '1')

def print_board(board: Dict[str, Optional[str]], selected_square: Optional[str]=None,
                legal_moves: Optional[List[str]]=None, promotion_squares: Optional[List[str]]=None):
    columns = "abcdefgh"
    RESET = "\033[0m"
    BG_LIGHT = "\033[47m"        # white
    BG_DARK = "\033[48;5;22m"    # forest green (dark green)
    FG_BLACK = "\033[30m"

    HIGHLIGHT_LIGHT = "\033[48;5;229m"  # light yellow for light squares highlight
    HIGHLIGHT_DARK = "\033[48;5;154m"   # light green for dark squares highlight

    PROMO_LIGHT = "\033[48;5;183m"      # purple-tinted for light squares promotion
    PROMO_DARK = "\033[48;5;90m"        # purple-tinted for dark squares promotion

    col_indices = {c: i for i, c in enumerate(columns)}

    print("\n       " + "         ".join(columns))
    print("  ⌜" + "─────────┬" * 7 + "─────────⌝")

    for row in reversed("12345678"):
        for line_type in ['top', 'mid', 'bot']:
            if line_type == 'mid':
                line = f"{row} │"
            else:
                line = "  │"

            for col in columns:
                idx_sum = col_indices[col] + int(row)
                square = col + row

                base_bg = BG_LIGHT if idx_sum % 2 == 0 else BG_DARK

                if selected_square == square:
                    bg = HIGHLIGHT_LIGHT if base_bg == BG_LIGHT else HIGHLIGHT_DARK
                elif legal_moves and square in legal_moves:
                    bg = HIGHLIGHT_LIGHT if base_bg == BG_LIGHT else HIGHLIGHT_DARK
                elif promotion_squares and square in promotion_squares:
                    bg = PROMO_LIGHT if base_bg == BG_LIGHT else PROMO_DARK
                else:
                    bg = base_bg

                if line_type == 'mid':
                    piece = board.get(square)
                    content = f"    {piece if piece else '  '}   "
                else:
                    content = "         "

                line += f"{bg}{FG_BLACK}{content}{RESET}│"
            print(line)

        if row != '1':
            print("  ├" + "─────────┼" * 7 + "─────────┤")
        else:
            print("  ⌞" + "─────────┴" * 7 + "─────────⌟")

