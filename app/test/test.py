
marked_tiles = [[2, 2], [3, 2], [2, 0], [1, 1], 
                 [3, 4], [3, 4], [3, 4], [3, 4], 
                 [2, 3], [2, 3], [2, 3], [2, 3], 
                 [0, 2], [1, 0], [0, 4], [0, 1], 
                 [4, 4], [4, 0], [2, 4], [1, 4],
                 [0, 0], [1, 1], [2, 2], [3, 3], [4, 4]]

def check_bingo(marked_tiles):
    marked = { (r, c) for r, c in marked_tiles }
    lines = []
    # Rows
    for r in range(5):
        lines.append([(r, c) for c in range(5)])
    print(f"Row: {lines}")
    # Columns
    for c in range(5):
        lines.append([(r, c) for r in range(5)])
    print(f"Column: {lines}")
    # Diagonals
    lines.append([(i, i) for i in range(5)])
    print(f"Diagonal 1: {lines}")
    lines.append([(i, 4 - i) for i in range(5)])
    print(f"Diagonal 2: {lines}")
    return any(all(coord in marked for coord in line) for line in lines)
print(check_bingo(marked_tiles))