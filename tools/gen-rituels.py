# -*- coding: utf-8 -*-
"""Visuels des packs "Rituels" : produits detoures, poses sur un fond de marque.

OBSOLETE depuis le 2026-09-25 : les cartes utilisent desormais les PHOTOS fournies
par Oss (assets/rituel-<slug>-photo.webp). Ce script ecrit toujours
assets/rituel-<slug>.webp, qui ne sont plus references nulle part.

  python tools/gen-rituels.py

Produit assets/rituel-<slug>.webp (1200 x 900). Rejouable : tout repart des
packshots, rien n'est retouche a la main. Le detourage vit dans tools/decoupe.py.
"""
import io, os, sys
from PIL import Image, ImageChops, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from decoupe import detourer

L, H = 1200, 900
SOL = 0.88          # ligne de pose, en part de la hauteur

# (fichier, options de detourage)
DECOUPES = {
    'fold':     ('mat-grey.webp',      dict(methode='dmax')),
    'grip':     ('liege-2.webp',       dict(methode='dmax')),
    'roue':     ('roue-1.webp',        dict(methode='dmax')),
    'board':    ('acupression-1.webp', dict(methode='sat', trou_maxi=1.0)),
    'bloc':     ('bloc-1.webp',        dict(methode='sat')),
    'bloc_bleu':('bloc-4.webp',        dict(methode='sat')),
    'socks':    ('chaussettes-1.webp', dict(methode='texture', seuil=3, trou_maxi=1.0, retrait=9)),
    'bottle':   ('gourde-1.webp',      dict(methode='translu')),
}

# (cle, hauteur en part du cadre, centre x en part, decalage vertical du sol, rotation)
# L'ordre compte : du fond vers l'avant. Les pieces les plus basses passent devant.
RITUELS = {
    'essentiel': ('#4F6158', [
        ('socks', 0.50, 0.71, -0.05, -12),
        ('fold',  0.56, 0.38, -0.02, 0),
        ('bloc',  0.19, 0.60, 0.03, 0),
    ]),
    'studio': ('#1F4E47', [
        ('grip',      0.38, 0.19, -0.04, 0),
        ('bottle',    0.49, 0.76, -0.03, 0),
        ('roue',      0.58, 0.45, 0.00, 0),
        ('bloc_bleu', 0.19, 0.62, 0.04, 0),
    ]),
    'recup': ('#8A7361', [
        ('bottle', 0.47, 0.19, -0.04, 0),
        ('socks',  0.47, 0.78, -0.03, 10),
        ('board',  0.50, 0.46, 0.01, 0),
    ]),
}


def fond(couleur):
    """Aplat de marque, eclairci vers le haut : les objets ne flottent pas dans du plat."""
    base = Image.new('RGB', (L, H), couleur)
    halo = Image.new('L', (L, H), 0)
    d = ImageDraw.Draw(halo)
    for i in range(28):
        k = i / 27.0
        d.ellipse((L * 0.5 - L * (0.75 - 0.5 * k), -H * 0.45 - H * 0.2 * k,
                   L * 0.5 + L * (0.75 - 0.5 * k), H * (0.95 - 0.35 * k)), fill=int(9 * (1 - k)))
    halo = halo.filter(ImageFilter.GaussianBlur(60))
    return Image.composite(Image.new('RGB', (L, H), '#ffffff'), base, halo)


def poser(scene, obj, haut, cx, dy, rot=0):
    """Pose l'objet a l'echelle voulue, avec ombre de contact + ombre portee."""
    if rot:
        obj = obj.rotate(rot, resample=Image.BICUBIC, expand=True)
    ech = (haut * H) / obj.height
    o = obj.resize((max(1, int(obj.width * ech)), max(1, int(obj.height * ech))), Image.LANCZOS)
    x = int(cx * L - o.width / 2)
    y = int((SOL + dy) * H - o.height)

    # ombre de contact : l'objet touche le sol, sinon il flotte
    contact = Image.new('RGBA', (L, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(contact)
    larg = o.width * 0.52
    d.ellipse((x + o.width / 2 - larg, y + o.height - 18, x + o.width / 2 + larg, y + o.height + 26),
              fill=(10, 16, 13, 120))
    scene.alpha_composite(contact.filter(ImageFilter.GaussianBlur(22)))

    ombre = Image.new('RGBA', (L, H), (0, 0, 0, 0))
    sil = o.split()[3].point(lambda v: int(v * 0.40))
    ombre.paste(Image.new('RGBA', o.size, (12, 18, 15, 255)), (x + 10, y + 16), sil)
    ombre = ombre.filter(ImageFilter.GaussianBlur(16))
    scene.alpha_composite(ombre)
    scene.alpha_composite(o.convert('RGBA'), (x, y))


def main():
    cache = {}
    for slug, (couleur, items) in RITUELS.items():
        scene = fond(couleur).convert('RGBA')
        for cle, haut, cx, dy, rot in items:
            if cle not in cache:
                src, kw = DECOUPES[cle]
                cache[cle] = detourer(os.path.join(ROOT, 'assets', src), **kw)
                print('  decoupe %-10s %s' % (cle, cache[cle].size))
            poser(scene, cache[cle], haut, cx, dy, rot)
        dst = os.path.join(ROOT, 'assets', 'rituel-%s.webp' % slug)
        scene.convert('RGB').save(dst, 'WEBP', quality=86, method=6)
        print('%-28s %6d octets' % ('assets/rituel-%s.webp' % slug, os.path.getsize(dst)))


if __name__ == '__main__':
    main()
