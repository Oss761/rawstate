# -*- coding: utf-8 -*-
"""Visuels provisoires des produits, en SVG, dans la charte Rawstate.

A remplacer par les vraies photos : deposer assets/produit-<slug>.webp
puis lancer  python tools/swap-product-art.py  (ou editer les <img>).
"""
import io, os

BG, INK, ACCENT, ACC_D, LINE = '#F2EDE4', '#16150F', '#2E6B67', '#245450', '#DED6C8'
CORK, CORK_D, GLASS = '#C89A6B', '#B0824F', '#BFD4D2'

def svg(body, bg=BG):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" role="img">'
            '<rect width="800" height="800" fill="%s"/>%s</svg>' % (bg, body))

def shadow(cx=400, cy=640, rx=210, ry=26):
    return '<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s" opacity=".16"/>' % (cx, cy, rx, ry, INK)

def dots(x0, y0, w, h, step, r, fill, op='.5'):
    out = []
    y = y0
    row = 0
    while y < y0 + h:
        x = x0 + (step / 2 if row % 2 else 0)
        while x < x0 + w:
            out.append('<circle cx="%.1f" cy="%.1f" r="%s" fill="%s" opacity="%s"/>' % (x, y, r, fill, op))
            x += step
        y += step; row += 1
    return ''.join(out)

ART = {}

# --- Tapis en liege : tapis deroule en perspective, grain de liege
ART['liege'] = shadow(400, 700, 230, 22) + (
  '<g transform="translate(400 400) skewY(-9) translate(-400 -400)">'
  '<rect x="245" y="150" width="310" height="500" rx="26" fill="%s"/>'
  '<rect x="245" y="150" width="310" height="500" rx="26" fill="none" stroke="%s" stroke-width="5"/>'
  % (CORK, CORK_D)) + dots(275, 185, 250, 430, 26, 4.2, CORK_D, '.45') + (
  '<rect x="245" y="150" width="310" height="500" rx="26" fill="none" stroke="%s" stroke-width="2" opacity=".35"/></g>' % INK)

# --- Tapis 2 personnes : un tapis large, deux zones
ART['duo'] = shadow(400, 690, 265, 24) + (
  '<g transform="translate(400 400) skewY(-7) translate(-400 -400)">'
  '<rect x="150" y="215" width="500" height="380" rx="26" fill="%s"/>'
  '<line x1="400" y1="225" x2="400" y2="585" stroke="%s" stroke-width="4" stroke-dasharray="14 12" opacity=".55"/>'
  '<rect x="150" y="215" width="500" height="380" rx="26" fill="none" stroke="%s" stroke-width="5"/>'
  '<circle cx="275" cy="405" r="46" fill="none" stroke="%s" stroke-width="5" opacity=".7"/>'
  '<circle cx="525" cy="405" r="46" fill="none" stroke="%s" stroke-width="5" opacity=".7"/>'
  '</g>' % ('#A9C4C2', ACC_D, ACC_D, ACC_D, ACC_D))

# --- Planche d'acupression : plaque + picots
ART['acupression'] = shadow(400, 660, 215, 22) + (
  '<g transform="translate(400 400) skewY(-8) translate(-400 -400)">'
  '<rect x="215" y="245" width="370" height="330" rx="30" fill="%s"/>'
  '<rect x="215" y="245" width="370" height="330" rx="30" fill="none" stroke="%s" stroke-width="5"/>'
  % (ACCENT, ACC_D)) + dots(250, 285, 300, 255, 30, 8, '#FFFFFF', '.85') + '</g>'

# --- Bloc de yoga : parallelepipede
ART['bloc'] = shadow(400, 640, 190, 22) + (
  '<g>'
  '<path d="M235 330 L400 250 L565 330 L400 410 Z" fill="%s"/>'
  '<path d="M235 330 L235 505 L400 585 L400 410 Z" fill="%s"/>'
  '<path d="M565 330 L565 505 L400 585 L400 410 Z" fill="%s"/>'
  '<path d="M235 330 L400 250 L565 330 L565 505 L400 585 L235 505 Z" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round"/>'
  '<path d="M235 330 L400 410 L565 330 M400 410 L400 585" fill="none" stroke="%s" stroke-width="4" opacity=".55"/>'
  '</g>' % ('#8FB3B0', ACCENT, ACC_D, INK, INK))

# --- Roue en liege : anneau + rayons
ART['roue'] = shadow(400, 660, 175, 20) + (
  '<g>'
  '<circle cx="400" cy="400" r="215" fill="%s"/>'
  '<circle cx="400" cy="400" r="215" fill="none" stroke="%s" stroke-width="6"/>'
  '<circle cx="400" cy="400" r="140" fill="%s"/>'
  '<circle cx="400" cy="400" r="140" fill="none" stroke="%s" stroke-width="6"/>'
  % (CORK, CORK_D, BG, CORK_D)) + dots(230, 230, 340, 340, 30, 4.5, CORK_D, '.4') + (
  '<circle cx="400" cy="400" r="140" fill="%s"/>'
  '<circle cx="400" cy="400" r="140" fill="none" stroke="%s" stroke-width="6"/>'
  '<g stroke="%s" stroke-width="5" opacity=".5">'
  '<line x1="400" y1="260" x2="400" y2="540"/><line x1="260" y1="400" x2="540" y2="400"/></g>'
  '</g>' % (BG, CORK_D, CORK_D))

# --- Chaussettes antiderapantes : paire + picots sous la semelle
def sock(dx):
    return ('<g transform="translate(%d 0)">'
      '<path d="M355 215 h95 v195 c0 46 14 62 46 88 l38 31 c30 24 24 74 -14 88 '
      'c-34 12 -70 -4 -92 -30 l-58 -68 c-20 -24 -30 -50 -30 -84 Z" fill="%s"/>'
      '<path d="M355 215 h95 v195 c0 46 14 62 46 88 l38 31 c30 24 24 74 -14 88 '
      'c-34 12 -70 -4 -92 -30 l-58 -68 c-20 -24 -30 -50 -30 -84 Z" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round"/>'
      '<rect x="355" y="215" width="95" height="42" fill="%s" opacity=".45"/>'
      '<g fill="%s" opacity=".9">'
      '<circle cx="404" cy="556" r="7"/><circle cx="436" cy="578" r="7"/><circle cx="468" cy="600" r="7"/>'
      '<circle cx="392" cy="592" r="7"/><circle cx="424" cy="614" r="7"/>'
      '</g></g>') % (dx, '#A9C4C2', ACC_D, ACC_D, BG)
ART['chaussettes'] = shadow(400, 700, 215, 20) + sock(-135) + sock(35)

# --- Gants antiderapants : gant + picots
ART['gants'] = shadow(400, 690, 195, 20) + (
  '<g>'
  '<path d="M300 300 c0 -26 40 -26 40 0 v-40 c0 -26 42 -26 42 0 v-20 c0 -26 42 -26 42 0 v30 '
  'c0 -24 40 -24 40 2 v170 c0 90 -56 148 -132 148 c-74 0 -122 -52 -122 -128 v-140 '
  'c0 -26 40 -26 40 0 Z" fill="%s"/>'
  '<path d="M300 300 c0 -26 40 -26 40 0 v-40 c0 -26 42 -26 42 0 v-20 c0 -26 42 -26 42 0 v30 '
  'c0 -24 40 -24 40 2 v170 c0 90 -56 148 -132 148 c-74 0 -122 -52 -122 -128 v-140 '
  'c0 -26 40 -26 40 0 Z" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round"/>'
  % (ACCENT, ACC_D)) + dots(300, 420, 165, 165, 32, 7.5, BG, '.9') + '</g>'

# --- Gourde transparente
ART['gourde'] = shadow(400, 672, 128, 18) + (
  '<g>'
  '<rect x="355" y="150" width="90" height="52" rx="14" fill="%s"/>'
  '<rect x="355" y="150" width="90" height="52" rx="14" fill="none" stroke="%s" stroke-width="5"/>'
  '<path d="M330 202 h140 c16 0 26 12 26 28 v390 c0 30 -22 52 -52 52 h-88 c-30 0 -52 -22 -52 -52 '
  'v-390 c0 -16 10 -28 26 -28 Z" fill="%s" opacity=".55"/>'
  '<path d="M330 202 h140 c16 0 26 12 26 28 v390 c0 30 -22 52 -52 52 h-88 c-30 0 -52 -22 -52 -52 '
  'v-390 c0 -16 10 -28 26 -28 Z" fill="none" stroke="%s" stroke-width="5"/>'
  '<path d="M356 260 v300" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round" opacity=".75"/>'
  '<path d="M330 470 h192" stroke="%s" stroke-width="4" opacity=".5"/>'
  '<path d="M330 470 v150 c0 30 22 52 52 52 h88 c30 0 52 -22 52 -52 v-150 Z" fill="%s" opacity=".35"/>'
  '</g>' % (ACC_D, INK, GLASS, INK, ACC_D, ACCENT))

if __name__ == '__main__':
    out = 'assets'
    for slug, body in ART.items():
        p = os.path.join(out, 'produit-%s.svg' % slug)
        io.open(p, 'w', encoding='utf-8').write(svg(body))
        print('%-14s %5d octets' % (slug, os.path.getsize(p)))
