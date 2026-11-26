#!/usr/bin/env python3
"""Draw the front page for Thursday 26 November 2026.

A newspaper-style page: navy masthead, one wide hero story (Trump's new
tariffs), three panels, two wide panels and a footer. Everything is drawn
with Pillow; the finished page is written to entry.png next to this file:

    python3 generate_image.py
"""

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
PAPER = (248, 243, 231)
INK = (26, 26, 30)
SOFT = (78, 76, 82)
NAVY = (18, 34, 68)
GOLD = (228, 188, 88)
CRIMSON = (172, 30, 30)
TEAL = (34, 104, 98)
NIGHT = (16, 24, 42)
CARD_EDGE = (184, 176, 154)
WHITE = (255, 255, 255)
CREAM = (250, 246, 238)

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, face, max_width):
    """Greedy word wrap into lines no wider than max_width pixels."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=face) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, face, colour, leading):
    for line in lines:
        draw.text((x, y), line, font=face, fill=colour)
        y += leading
    return y


def shade(draw, box, top, bottom):
    """Paint a smooth vertical blend from top colour to bottom colour."""
    x0, y0, x1, y1 = box
    height = max(1, y1 - y0)
    for row in range(y0, y1):
        frac = (row - y0) / height
        colour = tuple(
            int(top[i] + (bottom[i] - top[i]) * frac) for i in range(3)
        )
        draw.line([(x0, row), (x1, row)], fill=colour)


def burst(draw, cx, base_y, half_w, height, core=(255, 216, 96),
          edge=(255, 118, 0)):
    """A flame licking upward from base_y, centred on cx."""
    draw.polygon(
        [
            (cx - half_w, base_y),
            (cx + half_w, base_y),
            (cx + half_w * 0.55, base_y - height * 0.6),
            (cx, base_y - height),
            (cx - half_w * 0.55, base_y - height * 0.6),
        ],
        fill=edge,
    )
    draw.polygon(
        [
            (cx - half_w * 0.55, base_y),
            (cx + half_w * 0.55, base_y),
            (cx + half_w * 0.3, base_y - height * 0.42),
            (cx, base_y - height * 0.68),
            (cx - half_w * 0.3, base_y - height * 0.42),
        ],
        fill=core,
    )


def puff(draw, cx, cy, rx, ry, colour=(58, 58, 64)):
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=colour)


def frame(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE,
                   outline=CARD_EDGE, width=2)


def panel_text(draw, x, y, w, h, picture_h, kicker, headline, subline,
               accent, head_px=23):
    """Kicker, headline and subline below a panel's picture strip."""
    tx = x + 14
    tw = w - 28
    ty = y + picture_h + 10
    draw.text((tx, ty), kicker, font=font(SANS_BOLD, 15), fill=accent)
    ty += 24
    head_face = font(SERIF_BOLD, head_px)
    ty = draw_lines(draw, tx, ty,
                    wrap(draw, headline, head_face, tw),
                    head_face, INK, head_px + 4)
    ty += 4
    sub_face = font(SANS, 16)
    draw_lines(draw, tx, ty,
               wrap(draw, subline, sub_face, tw),
               sub_face, SOFT, 21)


def scene_tariffs(draw, x, y, w, h):
    """Hero picture: a tariff chart climbing steeply, Capitol dome behind."""
    shade(draw, (x, y, x + w, y + h), (24, 42, 84), (58, 84, 122))
    # Capitol dome silhouette, far left.
    dome_cx = x + 66
    draw.rectangle([dome_cx - 34, y + h - 46, dome_cx + 34, y + h],
                   fill=(14, 24, 50))
    draw.pieslice([dome_cx - 26, y + h - 96, dome_cx + 26, y + h - 44],
                  180, 360, fill=(14, 24, 50))
    draw.rectangle([dome_cx - 3, y + h - 108, dome_cx + 3, y + h - 92],
                   fill=(14, 24, 50))
    # Rising tariff bars.
    bars = [(150, 52, (228, 188, 88), "10%"),
            (205, 78, (228, 188, 88), "20%"),
            (260, 108, (240, 120, 60), "30%"),
            (315, 142, (200, 44, 44), "45%")]
    for bx, bh, colour, label in bars:
        draw.rectangle([x + bx, y + h - 18 - bh, x + bx + 42, y + h - 18],
                       fill=colour)
        draw.text((x + bx + 2, y + h - 34 - bh),
                  label, font=font(SANS_BOLD, 17), fill=WHITE)
    # Baseline and arrow sweeping up.
    draw.line([(x + 140, y + h - 18), (x + 380, y + h - 18)],
              fill=(200, 204, 216), width=2)
    draw.line([(x + 372, y + h - 170), (x + 418, y + h - 188),
               (x + 428, y + h - 172)], fill=GOLD, width=4)
    draw.text((x + 386, y + 22), "SECTION 301",
              font=font(SANS_BOLD, 20), fill=GOLD)
    draw.text((x + 386, y + 48), "14 PARTNERS",
              font=font(SANS_BOLD, 16), fill=(214, 218, 230))


def scene_cairo(draw, x, y, w, h):
    """Night on the Ring Road: an overturned tanker burning, cars behind."""
    shade(draw, (x, y, x + w, y + h), (26, 22, 34), (84, 52, 44))
    # Road sweeping across the bottom.
    draw.polygon([(x, y + h), (x + w, y + h), (x + w, y + h - 26),
                  (x, y + h - 12)], fill=(30, 30, 36))
    draw.line([(x + 10, y + h - 8), (x + w - 10, y + h - 18)],
              fill=(214, 186, 90), width=2)
    # Overturned tanker: cylinder on its side, cab crushed beside it.
    draw.rounded_rectangle([x + 88, y + h - 62, x + 208, y + h - 26],
                           radius=16, fill=(168, 162, 150))
    draw.rectangle([x + 196, y + h - 58, x + 226, y + h - 28],
                   fill=(120, 34, 34))
    draw.ellipse([x + 118, y + h - 26, x + 138, y + h - 6], fill=(24, 24, 28))
    draw.ellipse([x + 168, y + h - 26, x + 188, y + h - 6], fill=(24, 24, 28))
    # Flames along the spill and a column of smoke. Kept short so the
    # tongues stay inside the 96 px picture strip.
    burst(draw, x + 148, y + h - 60, 30, 30)
    burst(draw, x + 196, y + h - 58, 20, 22)
    burst(draw, x + 240, y + h - 40, 14, 16)
    puff(draw, x + 62, y + 14, 30, 11)
    puff(draw, x + 238, y + 10, 22, 9)
    # Two cars caught in the fire further down the road.
    for car_x in (246, 276):
        draw.rectangle([car_x, y + h - 30, car_x + 24, y + h - 16],
                       fill=(52, 52, 60))
    draw.text((x + 14, y + 10), "RING ROAD",
              font=font(SANS_BOLD, 16), fill=(238, 226, 200))


def scene_nasdaq(draw, x, y, w, h):
    """A market chart: a long red slide, then a small bounce."""
    draw.rectangle([x, y, x + w, y + h], fill=CREAM)
    for gy in range(y + 16, y + h - 6, 16):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(228, 222, 208))
    # The plunge, kept shallow enough that the labels below stay clear.
    fall = [(x + 14, y + 16), (x + 84, y + 26), (x + 148, y + 22),
            (x + 206, y + 46), (x + 258, y + 62)]
    draw.line(fall, fill=CRIMSON, width=5)
    draw.polygon([(x + 258, y + 62), (x + 240, y + 56), (x + 254, y + 46)],
                 fill=CRIMSON)
    # The small recovery at the close.
    rise = [(x + 258, y + 62), (x + 276, y + 50), (x + 294, y + 40)]
    draw.line(rise, fill=(28, 128, 58), width=5)
    draw.polygon([(x + 294, y + 40), (x + 278, y + 36), (x + 288, y + 24)],
                 fill=(28, 128, 58))
    draw.text((x + 16, y + h - 26), "INTRADAY -4%",
              font=font(SANS_BOLD, 17), fill=CRIMSON)
    draw.text((x + 178, y + h - 26), "CLOSE -0.6%",
              font=font(SANS_BOLD, 17), fill=(28, 128, 58))


def scene_court(draw, x, y, w, h):
    """A courthouse front: pediment, columns and a judge's gavel."""
    draw.rectangle([x, y, x + w, y + h], fill=NAVY)
    # Pediment.
    draw.polygon([(x + 30, y + 14), (x + w - 30, y + 14),
                  (x + w // 2, y + 42)], fill=(234, 228, 212))
    # Four columns.
    for col_x in (56, 108, 160, 212):
        draw.rectangle([x + col_x, y + 44, x + col_x + 14, y + h - 14],
                       fill=(234, 228, 212))
    draw.rectangle([x + 40, y + h - 16, x + w - 40, y + h - 8],
                   fill=(234, 228, 212))
    # Gavel laid across the steps: head, handle and sound block.
    draw.rectangle([x + 232, y + 58, x + 282, y + 74], fill=GOLD)
    draw.line([(x + 256, y + 66), (x + 292, y + 84)], fill=GOLD, width=5)
    draw.ellipse([x + 284, y + 80, x + 300, y + 90], fill=GOLD)


def scene_envoy(draw, x, y, w, h):
    """A diplomatic exit: an embassy, a flag at half-mast, a plane leaving."""
    shade(draw, (x, y, x + w, y + h), (30, 52, 92), (96, 118, 158))
    # Embassy block with lit windows.
    draw.rectangle([x + 24, y + 34, x + 190, y + h - 12], fill=(226, 222, 210))
    draw.rectangle([x + 24, y + 34, x + 190, y + 44], fill=(178, 44, 44))
    for wy in (56, 76):
        for wx in (40, 72, 104, 136, 168):
            draw.rectangle([x + wx, y + wy, x + wx + 12, y + wy + 12],
                           fill=(240, 210, 110))
    draw.rectangle([x + 96, y + h - 34, x + 118, y + h - 12],
                   fill=(52, 48, 44))
    # Flagpole with the flag lowered halfway.
    draw.line([(x + 214, y + 12), (x + 214, y + h - 12)], fill=(220, 220, 224),
              width=3)
    draw.rectangle([x + 214, y + 34, x + 246, y + 54], fill=(200, 40, 40))
    draw.text((x + 214, y + 60), "48 HRS",
              font=font(SANS_BOLD, 17), fill=WHITE)
    # A small plane climbing away, top right.
    px, py = x + 330, y + 22
    draw.polygon([(px, py), (px + 46, py + 8), (px, py + 14)],
                 fill=WHITE)
    draw.polygon([(px + 12, py + 4), (px + 22, py - 8), (px + 28, py + 6)],
                 fill=WHITE)


def scene_hormuz(draw, x, y, w, h):
    """Night sea: one tanker burning, an oil barrel and the Brent price.

    The strip is only 98 px tall, so the hull, tower and flames are all
    kept compact — nothing may rise above the top of the strip.
    """
    shade(draw, (x, y, x + w, y + h), (14, 26, 58), (54, 76, 100))
    for sx, sy in [(120, 16), (180, 30), (260, 14), (330, 28), (60, 44),
                   (300, 44)]:
        draw.ellipse([x + sx - 2, y + sy - 2, x + sx + 2, y + sy + 2],
                     fill=(222, 226, 236))
    # Moon, top left, clear of the price tag.
    draw.ellipse([x + 14, y + 10, x + 50, y + 46], fill=(238, 234, 214))
    # Sea band.
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(16, 42, 66))
    for wx in range(0, w, 44):
        draw.line([(x + wx, y + h - 20), (x + wx + 22, y + h - 20)],
                  fill=(92, 122, 152), width=2)
    # Tanker with a fire on deck.
    draw.rectangle([x + 30, y + h - 66, x + 240, y + h - 34],
                   fill=(40, 40, 46))
    draw.rectangle([x + 30, y + h - 66, x + 240, y + h - 60],
                   fill=(212, 206, 196))
    draw.rectangle([x + 196, y + h - 84, x + 224, y + h - 66],
                   fill=(240, 238, 232))
    burst(draw, x + 120, y + h - 64, 26, 26)
    burst(draw, x + 164, y + h - 64, 18, 20)
    puff(draw, x + 78, y + 12, 24, 9)
    puff(draw, x + 250, y + 8, 20, 8)
    # Oil barrel in the foreground and the price tag.
    draw.rectangle([x + 300, y + h - 48, x + 344, y + h - 8],
                   fill=(52, 52, 58))
    draw.rectangle([x + 300, y + h - 38, x + 344, y + h - 32],
                   fill=(90, 90, 98))
    draw.rectangle([x + 356, y + 14, x + 452, y + 48], fill=(16, 24, 42))
    draw.text((x + 366, y + 20), "BRENT $91.40",
              font=font(SANS_BOLD, 18), fill=GOLD)


def build():
    img = Image.new("RGB", (SIZE, SIZE), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, SIZE, 118], fill=NAVY)
    d.rectangle([0, 118, SIZE, 122], fill=GOLD)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=font(SERIF_BOLD, 46))
    d.text(((SIZE - tw) / 2, 14), title, font=font(SERIF_BOLD, 46),
           fill=WHITE)
    date = "THURSDAY 26 NOVEMBER 2026"
    dw = d.textlength(date, font=font(SANS_BOLD, 27))
    d.text(((SIZE - dw) / 2, 72), date, font=font(SANS_BOLD, 27), fill=GOLD)

    # ---- Hero: Trump's new tariffs ----
    hx, hy, hw, hh = 24, 134, 976, 276
    frame(d, hx, hy, hw, hh)
    scene_tariffs(d, hx + 2, hy + 2, 520, hh - 4)
    tx = hx + 544
    tw2 = hw - 568
    d.text((tx, hy + 22), "TRADE  •  UNITED STATES",
           font=font(SANS_BOLD, 18), fill=CRIMSON)
    head_face = font(SERIF_BOLD, 40)
    ty = draw_lines(d, tx, hy + 52,
                    wrap(d, "TRUMP'S NEW TARIFFS", head_face, tw2),
                    head_face, INK, 46)
    sub_face = font(SANS, 20)
    ty = draw_lines(d, tx, ty + 10,
                    wrap(d, "Washington proposes 20% more on Chinese "
                            "goods — up to 45% in all — plus levies on "
                            "the EU, Japan and 11 others.",
                         sub_face, tw2),
                    sub_face, SOFT, 26)
    d.text((tx, ty + 12),
           "Section 301 • 14 partners • hearings 25 January.",
           font=font(SERIF, 18), fill=(92, 92, 98))

    # ---- Row 1: three panels ----
    row1_y, row1_h, pw = 424, 262, 312
    for x, scene, kicker, headline, subline, accent in [
        (24, scene_cairo, "EGYPT  •  DISASTER",
         "CAIRO TANKER FIRE KILLS 31",
         "A fuel tanker overturns on Cairo's Ring Road; the fire "
         "engulfs 27 vehicles, killing 31 and injuring 21.",
         (150, 60, 20)),
        (356, scene_nasdaq, "MARKETS  •  WALL STREET",
         "NASDAQ PLUNGES ON AI FEARS",
         "The Nasdaq dives about 4% intraday before closing 0.6% "
         "down; Nvidia falls 4% as AI doubts deepen.",
         CRIMSON),
        (688, scene_court, "ISRAEL  •  COURTS",
         "NETANYAHU WINS COURT BOOST",
         "Jerusalem judges urge prosecutors to drop the bribery "
         "charge in Case 4000 and reconsider Case 2000.",
         NAVY),
    ]:
        frame(d, x, row1_y, pw, row1_h)
        scene(d, x + 2, row1_y + 2, pw - 4, 96)
        panel_text(d, x, row1_y, pw, row1_h, 96, kicker, headline,
                   subline, accent, head_px=23)

    # ---- Row 2: two wide panels ----
    row2_y, row2_h, w2 = 700, 244, 478
    for x, scene, kicker, headline, subline, accent in [
        (24, scene_envoy, "KOREA  •  DIPLOMACY",
         "PYONGYANG EXPELS SWISS ENVOY",
         "North Korea gives envoy Sylvain Astier 48 hours to leave "
         "over Swiss sanctions on a children's camp.",
         TEAL),
        (522, scene_hormuz, "ENERGY  •  HORMUZ",
         "BRENT REBOUNDS ON HORMUZ ATTACKS",
         "Brent climbs 2.3% to $91.40 as fresh tanker attacks are "
         "reported; Gulf transits are down about 40%.",
         (150, 60, 20)),
    ]:
        frame(d, x, row2_y, w2, row2_h)
        scene(d, x + 2, row2_y + 2, w2 - 4, 98)
        panel_text(d, x, row2_y, w2, row2_h, 98, kicker, headline,
                   subline, accent, head_px=27)

    # ---- Footer ----
    foot = ("Six stories from Thursday 26 November 2026  •  "
            "Trade, disaster, markets, courts, diplomacy and energy  •  "
            "The World in One Page")
    fw = d.textlength(foot, font=font(SANS, 17))
    d.text(((SIZE - fw) / 2, 962), foot, font=font(SANS, 17),
           fill=(92, 86, 72))

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
