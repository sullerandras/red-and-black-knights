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

import sys, math

KNIGHT_MOVES = [(1,2),(1,-2),(-1,2),(-1,-2),(2,1),(2,-1),(-2,1),(-2,-1)]


def spiral_xy(n):
    """(x, y) for 0-indexed spiral position n — O(1), no precomputation."""
    if n == 0:
        return (0, 0)
    n1 = n + 1
    k  = (math.isqrt(n1 - 1) + 1) // 2
    m  = (2 * k + 1) ** 2
    t  = 2 * k
    if n1 >= m - t:
        return (k - (m - n1), -k)
    m -= t
    if n1 >= m - t:
        return (-k, -k + (m - n1))
    m -= t
    if n1 >= m - t:
        return (-k + (m - n1), k)
    return (k, k - (m - n1 - t))


def xy_to_spiral(x, y):
    """0-indexed spiral position for coordinates (x, y) — O(1)."""
    if x == 0 and y == 0:
        return 0
    k = max(abs(x), abs(y))
    m = (2 * k + 1) ** 2
    if   y == -k: return m - k + x - 1
    elif x == -k: return m - 3 * k - y - 1
    elif y ==  k: return m - 5 * k - x - 1
    else:         return m - 7 * k + y - 1  # x == k


def play(n):
    """Place n alternating knights (black first).  Returns {pos: 'B'|'R'}."""
    occupied           = {}
    attacked_by_black: set = set()
    attacked_by_red:   set = set()
    next_b = next_r = 0
    is_black = True

    for _ in range(n):
        blocked = attacked_by_red if is_black else attacked_by_black
        pos = next_b if is_black else next_r
        while pos in occupied or pos in blocked:
            pos += 1

        color = 'B' if is_black else 'R'
        occupied[pos] = color
        if is_black:
            next_b = pos + 1
        else:
            next_r = pos + 1

        x, y = spiral_xy(pos)
        target = attacked_by_black if is_black else attacked_by_red
        for dx, dy in KNIGHT_MOVES:
            target.add(xy_to_spiral(x + dx, y + dy))

        is_black = not is_black

    return occupied


def render(occupied, pad=4):
    from PIL import Image

    coords = {pos: spiral_xy(pos) for pos in occupied}
    all_x  = [c[0] for c in coords.values()]
    all_y  = [c[1] for c in coords.values()]
    x0, x1 = min(all_x), max(all_x)
    y0, y1 = min(all_y), max(all_y)

    w = x1 - x0 + 1 + 2 * pad
    h = y1 - y0 + 1 + 2 * pad
    img = Image.new('RGB', (w, h), (255, 255, 255))
    pix = img.load()

    for pos, color in occupied.items():
        x, y = coords[pos]
        ix = x - x0 + pad
        iy = y1 - y + pad          # flip y: image row 0 = top
        pix[ix, iy] = (0, 0, 0) if color == 'B' else (210, 30, 30)

    return img


def main():
    n   = int(sys.argv[1]) if len(sys.argv) > 1 else 500
    out = sys.argv[2]       if len(sys.argv) > 2 else f'knights-{n}.png'

    print(f"Playing {n} knights …")
    occ = play(n)

    print("Rendering …")
    img = render(occ)
    img.save(out)
    print(f"Saved {out}  ({img.width}×{img.height} px, highest position {max(occ)})")


if __name__ == '__main__':
    main()
