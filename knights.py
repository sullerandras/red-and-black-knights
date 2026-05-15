#!/usr/bin/env python3
"""
Red/black knights on an infinite spiral board.

Rules: alternating black (first) / red knights.  Each is placed on the
smallest spiral-numbered square that is (a) unoccupied and (b) not attacked
by any knight of the opposite colour.

Spiral numbering (right = +x, up = +y):
    4 3 2
    5 0 1
    6 7 8  …

Usage:  python knights.py [N=500] [output.png]
Needs:  pip install Pillow
"""

import sys

KNIGHT_MOVES = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]
_DIRS        = [(1,0),(0,1),(-1,0),(0,-1)]   # R, U, L, D


def make_spiral(size):
    """Return list of (x,y) for positions 0 … size-1."""
    coords = [(0, 0)]
    x = y = 0
    seg, rem = 0, 1          # segment index, steps remaining in segment
    while len(coords) < size:
        dx, dy = _DIRS[seg % 4]
        x += dx; y += dy
        coords.append((x, y))
        rem -= 1
        if rem == 0:
            seg += 1
            rem = seg // 2 + 1   # segment lengths: 1,1,2,2,3,3,…
    return coords


def play(n, spiral):
    """Place n alternating knights (black first).  Returns {pos: 'B'|'R'}."""
    xy_to_n  = {xy: i for i, xy in enumerate(spiral)}
    occupied = {}
    black_pos, red_pos = set(), set()
    is_black = True

    for _ in range(n):
        opposite = red_pos if is_black else black_pos

        attacked = set()
        for p in opposite:
            ox, oy = spiral[p]
            for dx, dy in KNIGHT_MOVES:
                q = xy_to_n.get((ox + dx, oy + dy))
                if q is not None:
                    attacked.add(q)

        pos = 0
        while pos in occupied or pos in attacked:
            pos += 1

        color = 'B' if is_black else 'R'
        occupied[pos] = color
        (black_pos if is_black else red_pos).add(pos)
        is_black = not is_black

    return occupied


def render(occupied, spiral, pad=4):
    from PIL import Image

    hi = max(occupied)
    xs = [spiral[i][0] for i in range(hi + 1)]
    ys = [spiral[i][1] for i in range(hi + 1)]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)

    w = x1 - x0 + 1 + 2 * pad
    h = y1 - y0 + 1 + 2 * pad
    img = Image.new('RGB', (w, h), (255, 255, 255))
    pix = img.load()

    for pos, color in occupied.items():
        x, y = spiral[pos]
        ix = x - x0 + pad
        iy = y1 - y + pad          # flip y: image row 0 = top
        pix[ix, iy] = (0, 0, 0) if color == 'B' else (210, 30, 30)

    return img


def main():
    n   = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    out = sys.argv[2]       if len(sys.argv) > 2 else 'knights.png'

    # Precompute enough of the spiral.  At step k there are at most k/2
    # opposite knights, each attacking ≤8 squares, so max position ≤5k.
    spiral_size = n * 8 + 500
    spiral = make_spiral(spiral_size)

    print(f"Playing {n} knights …")
    occ = play(n, spiral)

    print("Rendering …")
    img = render(occ, spiral)
    img.save(out)
    print(f"Saved {out}  ({img.width}×{img.height} px, highest position {max(occ)})")


if __name__ == '__main__':
    main()
