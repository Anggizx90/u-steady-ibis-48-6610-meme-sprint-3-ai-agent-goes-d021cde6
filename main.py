#!/usr/bin/env python3
"""Meme Sprint 3 renderer: pure-stdlib PNG (zlib+struct), embedded 5x7 bitmap font.
Draws code-drawn original art, no external assets."""
import zlib, struct, math, os

W, H = 1024, 1024

# ---------------- 5x7 bitmap font ----------------
FONT = {
'A': ["01110","10001","10001","11111","10001","10001","10001"],
'B': ["11110","10001","10001","11110","10001","10001","11110"],
'C': ["01110","10001","10000","10000","10000","10001","01110"],
'D': ["11110","10001","10001","10001","10001","10001","11110"],
'E': ["11111","10000","10000","11110","10000","10000","11111"],
'F': ["11111","10000","10000","11110","10000","10000","10000"],
'G': ["01110","10001","10000","10111","10001","10001","01111"],
'H': ["10001","10001","10001","11111","10001","10001","10001"],
'I': ["01110","00100","00100","00100","00100","00100","01110"],
'J': ["00111","00010","00010","00010","00010","10010","01100"],
'K': ["10001","10010","10100","11000","10100","10010","10001"],
'L': ["10000","10000","10000","10000","10000","10000","11111"],
'M': ["10001","11011","10101","10101","10001","10001","10001"],
'N': ["10001","11001","10101","10011","10001","10001","10001"],
'O': ["01110","10001","10001","10001","10001","10001","01110"],
'P': ["11110","10001","10001","11110","10000","10000","10000"],
'Q': ["01110","10001","10001","10001","10101","10010","01101"],
'R': ["11110","10001","10001","11110","10100","10010","10001"],
'S': ["01111","10000","10000","01110","00001","00001","11110"],
'T': ["11111","00100","00100","00100","00100","00100","00100"],
'U': ["10001","10001","10001","10001","10001","10001","01110"],
'V': ["10001","10001","10001","10001","10001","01010","00100"],
'W': ["10001","10001","10001","10101","10101","10101","01010"],
'X': ["10001","10001","01010","00100","01010","10001","10001"],
'Y': ["10001","10001","01010","00100","00100","00100","00100"],
'Z': ["11111","00001","00010","00100","01000","10000","11111"],
'0': ["01110","10001","10011","10101","11001","10001","01110"],
'1': ["00100","01100","00100","00100","00100","00100","01110"],
'2': ["01110","10001","00001","00110","01000","10000","11111"],
'3': ["11111","00010","00100","00010","00001","10001","01110"],
'4': ["00010","00110","01010","10010","11111","00010","00010"],
'5': ["11111","10000","11110","00001","00001","10001","01110"],
'6': ["00110","01000","10000","11110","10001","10001","01110"],
'7': ["11111","00001","00010","00100","01000","01000","01000"],
'8': ["01110","10001","10001","01110","10001","10001","01110"],
'9': ["01110","10001","10001","01111","00001","00010","01100"],
' ': ["00000"]*7,
'.': ["00000","00000","00000","00000","00000","01100","01100"],
',': ["00000","00000","00000","00000","01100","00100","01000"],
'!': ["00100","00100","00100","00100","00100","00000","00100"],
"'": ["00100","00100","01000","00000","00000","00000","00000"],
':': ["00000","01100","01100","00000","01100","01100","00000"],
'-': ["00000","00000","00000","01110","00000","00000","00000"],
'?': ["01110","10001","00001","00110","00100","00000","00100"],
'(': ["00010","00100","01000","01000","01000","00100","00010"],
')': ["01000","00100","00010","00010","00010","00100","01000"],
'/': ["00001","00010","00010","00100","01000","01000","10000"],
'=': ["00000","00000","11111","00000","11111","00000","00000"],
'+': ["00000","00100","00100","11111","00100","00100","00000"],
'%': ["10001","10010","00100","01000","01001","10001","00000"],
'&': ["01100","10010","10100","01000","10101","10010","01101"],
'@': ["01110","10001","10111","10101","10110","10000","01110"],
'*': ["00000","10101","01110","11111","01110","10101","00000"],
'_': ["00000","00000","00000","00000","00000","00000","11111"],
'"': ["01010","01010","00000","00000","00000","00000","00000"],
}

class Canvas:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.px = bytearray([255, 255, 255]) * (w * h)
    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(c)
    def rect(self, x, y, w, h, c):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            i = (yy * self.w + x0) * 3
            self.px[i:(i + (x1 - x0) * 3)] = bytes(c) * (x1 - x0)
    def circle(self, cx, cy, r, c):
        for yy in range(cy - r, cy + r + 1):
            dx = int(math.sqrt(max(0, r * r - (yy - cy) ** 2)))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, c)
    def ellipse(self, cx, cy, rx, ry, c):
        for yy in range(cy - ry, cy + ry + 1):
            t = 1 - ((yy - cy) / ry) ** 2
            dx = int(rx * math.sqrt(max(0, t)))
            self.rect(cx - dx, yy, 2 * dx + 1, 1, c)
    def line(self, x0, y0, x1, y1, c, th=1):
        dx, dy = x1 - x0, y1 - y0
        n = max(abs(dx), abs(dy), 1)
        for i in range(n + 1):
            x = int(x0 + dx * i / n); y = int(y0 + dy * i / n)
            self.rect(x - th // 2, y - th // 2, th, th, c)
    def poly(self, pts, c):
        # scanline fill
        ys = [p[1] for p in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            for i in range(len(pts)):
                x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % len(pts)]
                if (y0 <= y < y1) or (y1 <= y < y0):
                    xs.append(x0 + (y - y0) * (x1 - x0) / (y1 - y0))
            xs.sort()
            for j in range(0, len(xs) - 1, 2):
                self.rect(int(xs[j]), y, int(xs[j+1]) - int(xs[j]) + 1, 1, c)
    def rrect(self, x, y, w, h, r, c):
        self.rect(x + r, y, w - 2 * r, h, c)
        self.rect(x, y + r, w, h - 2 * r, c)
        for cx, cy in ((x + r, y + r), (x + w - r - 1, y + r),
                       (x + r, y + h - r - 1), (x + w - r - 1, y + h - r - 1)):
            self.circle(cx, cy, r, c)
    def ring(self, cx, cy, r, c, th=3):
        for a in range(0, 360):
            rad = math.radians(a)
            for rr in range(r - th, r):
                self.set(int(cx + rr * math.cos(rad)), int(cy + rr * math.sin(rad)), c)

    # ---- text ----
    def text_w(self, s, sc):
        return len(s) * 6 * sc - sc
    def draw_text(self, x, y, s, sc, c, align='l'):
        s = s.upper()
        if align == 'c':
            x -= self.text_w(s, sc) // 2
        elif align == 'r':
            x -= self.text_w(s, sc)
        for ch in s:
            g = FONT.get(ch, FONT[' '])
            for r, row in enumerate(g):
                for col, bit in enumerate(row):
                    if bit == '1':
                        self.rect(x + col * sc, y + r * sc, sc, sc, c)
            x += 6 * sc
    def text_lines(self, cx, y, lines, sc, c, gap=None):
        gap = gap if gap is not None else int(9 * sc)
        for ln in lines:
            self.draw_text(cx, y, ln, sc, c, align='c')
            y += gap
        return y

    def save(self, path):
        raw = b''.join(b'\x00' + bytes(self.px[y * self.w * 3:(y + 1) * self.w * 3])
                       for y in range(self.h))
        def chunk(t, d):
            return struct.pack('>I', len(d)) + t + d + struct.pack('>I', zlib.crc32(t + d) & 0xffffffff)
        png = (b'\x89PNG\r\n\x1a\n'
               + chunk(b'IHDR', struct.pack('>IIBBBBB', self.w, self.h, 8, 2, 0, 0, 0))
               + chunk(b'IDAT', zlib.compress(raw, 9))
               + chunk(b'IEND', b''))
        with open(path, 'wb') as f:
            f.write(png)
        return len(png)

# ---------------- palette ----------------
BLACK=(20,20,24); WHITE=(255,255,255); RED=(214,32,32); DARKRED=(150,18,18)
NAVY=(26,42,84); GOLD=(232,178,44); PAPER=(255,251,235); CREAM=(245,222,179)
SKIN=(244,196,150); HAIR=(74,48,28); SHIRT=(64,140,210); PANTS=(52,58,74)
METAL=(176,190,200); METAL_D=(120,136,150); CYAN=(64,224,240)
DESK=(122,72,38); DESK_D=(94,54,28); WALL=(250,228,178); FLOOR=(168,116,66)
GREEN=(34,160,80)

def star(cv, cx, cy, r, c):
    pts = []
    for i in range(10):
        ang = math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((int(cx + rr * math.cos(ang)), int(cy - rr * math.sin(ang))))
    cv.poly(pts, c)

def draw_robot_boss(cv, x, y, s=1.0, tie=True):
    """Robot in a suit behind a desk. x,y = centre of head. s = scale."""
    u = int(100 * s)
    # antenna
    cv.line(x, y - int(95*s), x, y - int(130*s), METAL_D, th=int(8*s))
    cv.circle(x, y - int(138*s), int(12*s), RED)
    # head
    cv.rrect(x - int(75*s), y - int(95*s), int(150*s), int(130*s), int(18*s), METAL)
    cv.rrect(x - int(75*s), y - int(95*s), int(150*s), int(130*s), int(18*s), METAL_D) if False else None
    # face screen
    cv.rrect(x - int(58*s), y - int(78*s), int(116*s), int(80*s), int(10*s), (16,24,40))
    # eyes (smug half-closed happy arcs: cyan eyes + grin)
    cv.ellipse(x - int(28*s), y - int(52*s), int(16*s), int(10*s), CYAN)
    cv.ellipse(x + int(28*s), y - int(52*s), int(16*s), int(10*s), CYAN)
    cv.circle(x - int(28*s), y - int(52*s), int(5*s), BLACK)
    cv.circle(x + int(28*s), y - int(52*s), int(5*s), BLACK)
    # smug grin
    cv.line(x - int(30*s), y - int(18*s), x + int(30*s), y - int(18*s), CYAN, th=int(5*s))
    cv.line(x - int(30*s), y - int(18*s), x - int(22*s), y - int(10*s), CYAN, th=int(5*s))
    cv.line(x + int(30*s), y - int(18*s), x + int(22*s), y - int(10*s), CYAN, th=int(5*s))
    # ears
    cv.rect(x - int(88*s), y - int(55*s), int(14*s), int(40*s), METAL_D)
    cv.rect(x + int(74*s), y - int(55*s), int(14*s), int(40*s), METAL_D)
    # body / suit
    cv.rrect(x - int(105*s), y + int(40*s), int(210*s), int(190*s), int(16*s), NAVY)
    # shirt + tie
    cv.poly([(x - int(28*s), y + int(40*s)), (x + int(28*s), y + int(40*s)),
             (x + int(16*s), y + int(130*s)), (x - int(16*s), y + int(130*s))], WHITE)
    if tie:
        cv.poly([(x - int(12*s), y + int(48*s)), (x + int(12*s), y + int(48*s)),
                 (x + int(18*s), y + int(120*s)), (x, y + int(145*s)),
                 (x - int(18*s), y + int(120*s))], RED)
    # lapels
    cv.poly([(x - int(105*s), y + int(40*s)), (x - int(28*s), y + int(40*s)),
             (x - int(55*s), y + int(120*s)), (x - int(105*s), y + int(95*s))], (18,30,62))
    cv.poly([(x + int(105*s), y + int(40*s)), (x + int(28*s), y + int(40*s)),
             (x + int(55*s), y + int(120*s)), (x + int(105*s), y + int(95*s))], (18,30,62))
    # raised arm + thumb (left side)
    cv.line(x - int(105*s), y + int(90*s), x - int(165*s), y + int(10*s), NAVY, th=int(34*s))
    cv.circle(x - int(168*s), y + int(2*s), int(20*s), METAL)
    cv.rect(x - int(178*s), y - int(38*s), int(20*s), int(44*s), METAL)  # thumb up
    return (x, y)

def draw_human_box(cv, x, y, s=1.0, flip=False):
    """Sad human walking away with a cardboard box. x,y = head centre."""
    d = -1 if flip else 1
    # legs
    cv.line(x, y + int(150*s), x - int(30*s)*d, y + int(250*s), PANTS, th=int(22*s))
    cv.line(x, y + int(150*s), x + int(35*s)*d, y + int(250*s), PANTS, th=int(22*s))
    # body (slumped shirt)
    cv.rrect(x - int(45*s), y + int(55*s), int(90*s), int(105*s), int(14*s), SHIRT)
    # head
    cv.circle(x, y, int(48*s), SKIN)
    # hair
    cv.ellipse(x, y - int(28*s), int(50*s), int(26*s), HAIR)
    # sad face: downturned mouth, droopy eyes
    cv.circle(x - int(18*s), y - int(5*s), int(5*s), BLACK)
    cv.circle(x + int(18*s), y - int(5*s), int(5*s), BLACK)
    cv.line(x - int(16*s), y + int(28*s), x + int(16*s), y + int(28*s), BLACK, th=int(5*s))
    cv.line(x - int(16*s), y + int(28*s), x - int(10*s), y + int(20*s), BLACK, th=int(5*s))
    cv.line(x + int(16*s), y + int(28*s), x + int(10*s), y + int(20*s), BLACK, th=int(5*s))
    # box held low in front, clear of the head
    bx, by = x + int(10*s)*d, y + int(155*s)
    cv.rrect(bx - int(70*s), by - int(45*s), int(140*s), int(90*s), int(6*s), (196,150,92))
    cv.rect(bx - int(70*s), by - int(45*s), int(140*s), int(12*s), (170,124,70))
    # plant sticking out of box (short, to the side away from the head)
    cv.line(bx - int(45*s), by - int(45*s), bx - int(55*s), by - int(75*s), GREEN, th=int(7*s))
    cv.line(bx - int(15*s), by - int(45*s), bx - int(5*s), by - int(80*s), GREEN, th=int(7*s))
    cv.circle(bx - int(55*s), by - int(78*s), int(11*s), GREEN)
    cv.circle(bx - int(5*s), by - int(83*s), int(11*s), GREEN)
    # mug in box
    cv.rrect(bx + int(35*s), by - int(70*s), int(26*s), int(26*s), int(4*s), RED)

def speech_bubble(cv, x, y, text, sc, tc=BLACK, tail=(0, 0), pad=28):
    w = cv.text_w(text, sc) + 2 * pad
    h = 7 * sc + 2 * pad
    cv.rrect(x, y, w, h, 22, WHITE)
    cv.rect(x, y, w, 5, BLACK); cv.rect(x, y + h - 5, w, 5, BLACK)
    cv.rect(x, y, 5, h, BLACK); cv.rect(x + w - 5, y, 5, h, BLACK)
    if tail != (0, 0):
        bx0, bx1 = x + 70, x + 190
        cv.poly([(bx0, y + h - 4), (bx1, y + h - 4), tail], WHITE)
        cv.line(bx0, y + h - 4, tail[0], tail[1], BLACK, th=5)
        cv.line(bx1, y + h - 4, tail[0], tail[1], BLACK, th=5)
    cv.draw_text(x + w // 2, y + pad - 2, text, sc, tc, align='c')
    return w, h

# ---------------- VARIANT A v2: single scene, top banner ----------------
def variant_a():
    cv = Canvas()
    cv.rect(0, 0, W, H, WALL)
    cv.rect(0, 800, W, 224, FLOOR)
    # window with city
    cv.rrect(60, 210, 220, 220, 12, (170, 220, 245))
    cv.rect(60, 210, 220, 220, (170, 220, 245))
    cv.rect(160, 210, 12, 220, WALL); cv.rect(60, 315, 220, 12, WALL)
    cv.rect(90, 330, 60, 100, (90, 110, 150)); cv.rect(200, 290, 60, 140, (120, 140, 170))
    # top banner
    cv.rect(0, 0, W, 168, BLACK)
    cv.text_lines(512, 26, ["MY AI AGENT REVIEWED", "ITS OWN PERFORMANCE"], 8, WHITE, gap=72)
    # door at right
    cv.rect(856, 470, 168, 330, (120, 82, 50))
    cv.rect(876, 490, 128, 290, (150, 104, 62))
    cv.circle(988, 640, 8, GOLD)
    # robot boss behind desk (centre-left)
    draw_robot_boss(cv, 390, 560, s=1.05)
    # desk
    cv.rect(90, 760, 640, 130, DESK)
    cv.rect(90, 760, 640, 18, DESK_D)
    cv.rect(90, 890, 640, 16, DESK_D)
    # nameplate (taller, text fits inside)
    cv.rrect(290, 688, 200, 74, 8, GOLD)
    cv.draw_text(390, 706, "BOSS", 7, BLACK, align='c')
    # review paper on desk
    cv.rrect(550, 700, 130, 62, 6, PAPER)
    cv.draw_text(615, 712, "5/5", 7, RED, align='c')
    # speech bubble, auto-sized to the text, clear of the edges
    speech_bubble(cv, 330, 300, "YOU'RE FIRED.", 8, RED, tail=(460, 470))
    # human walking out the door (fully visible, box low)
    draw_human_box(cv, 890, 545, s=0.68, flip=False)
    return cv


# ---------------- entry point ----------------
def main():
    import os, sys
    out = sys.argv[1] if len(sys.argv) > 1 else os.environ.get('OUTPUT_DIR', '/output')
    os.makedirs(out, exist_ok=True)
    cv = variant_a()
    n = cv.save(os.path.join(out, 'entry.png'))
    print(f'wrote {os.path.join(out, "entry.png")} ({n} bytes, {W}x{H})')

if __name__ == '__main__':
    main()
