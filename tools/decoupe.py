# -*- coding: utf-8 -*-
"""Detourage des packshots produit (PIL pur, pas de numpy sur cette machine).

Une methode par type d'objet, choisie a l'appel :
  'dmax'    objet opaque, colore ou non  -> ecart au fond (gris, liege, mousse)
  'sat'     objet colore, ombre grise    -> saturation (l'ombre portee ne ressort pas)
  'texture' textile clair                -> |laplacien| de luminance (le revers blanc
            des chaussettes a la couleur du fond, mais la maille est texturee)
  'translu' objet transparent (gourde)   -> silhouette du fond + alpha progressif,
            pour que l'arriere-plan transparaisse au lieu d'un aplat

Communs a toutes : plus grandes composantes connexes, bouchage des PETITS trous
seulement (le centre ouvert de la roue doit rester transparent), leger retrait
du bord puis adoucissement.
"""
from collections import deque
from PIL import Image, ImageChops, ImageFilter


def _otsu(hist):
    total = sum(hist)
    somme = sum(i * h for i, h in enumerate(hist))
    wb = sb = 0
    best, seuil = -1, 0
    for t in range(256):
        wb += hist[t]
        if wb == 0:
            continue
        wf = total - wb
        if wf == 0:
            break
        sb += t * hist[t]
        var = wb * wf * (sb / wb - (somme - sb) / wf) ** 2
        if var > best:
            best, seuil = var, t
    return seuil


def _composantes(m, w, h):
    lab = [0] * (w * h)
    tailles = {}
    n = 0
    for s in range(w * h):
        if m[s] and not lab[s]:
            n += 1
            q = deque([s]); lab[s] = n; c = 0
            while q:
                p = q.popleft(); c += 1
                x, y = p % w, p // w
                for v in ((p - 1) if x else -1, (p + 1) if x < w - 1 else -1,
                          (p - w) if y else -1, (p + w) if y < h - 1 else -1):
                    if v >= 0 and m[v] and not lab[v]:
                        lab[v] = n; q.append(v)
            tailles[n] = c
    return lab, tailles


def _fond(im):
    px = im.load()
    w, h = im.size
    cadre = ([px[x, y] for x in range(0, w, 2) for y in (1, h - 2)]
             + [px[x, y] for y in range(0, h, 2) for x in (1, w - 2)])
    return tuple(sorted(c[i] for c in cadre)[len(cadre) // 2] for i in range(3))


def _mesure(im, methode):
    """Carte de 'distance au fond' sur laquelle Otsu decide."""
    r, g, b = im.split()
    if methode == 'sat':
        hi = ImageChops.lighter(ImageChops.lighter(r, g), b)
        lo = ImageChops.darker(ImageChops.darker(r, g), b)
        return ImageChops.subtract(hi, lo).filter(ImageFilter.MedianFilter(3))
    if methode == 'texture':
        L = im.convert("L")
        lap = L.filter(ImageFilter.Kernel((3, 3), [0, 1, 0, 1, -4, 1, 0, 1, 0], scale=1, offset=128))
        t = ImageChops.difference(lap, Image.new("L", im.size, 128)).filter(ImageFilter.BoxBlur(4))
        cadre = Image.new("L", im.size, 0)
        cadre.paste(255, (12, 12, im.width - 12, im.height - 12))
        return ImageChops.multiply(t, cadre)
    dr, dg, db = ImageChops.difference(im, Image.new("RGB", im.size, _fond(im))).split()
    return ImageChops.lighter(ImageChops.lighter(dr, dg), db).filter(ImageFilter.MedianFilter(3))


def silhouette(im, methode='dmax', seuil=None, part_mini=0.2, trou_maxi=0.02):
    """Masque binaire de l'objet (liste de bool), a la resolution de l'image."""
    w, h = im.size
    d = _mesure(im, methode)
    t = seuil if seuil is not None else _otsu(d.histogram())
    lab, tailles = _composantes([v > t for v in d.getdata()], w, h)
    if not tailles:
        raise SystemExit('rien de detecte')
    gmax = max(tailles.values())
    gardees = {k for k, s in tailles.items() if s > part_mini * gmax}
    plein = [lab[i] in gardees for i in range(w * h)]

    # trous : on bouche les petits (picots, reflets), jamais les grands
    # (le centre ajoure de la roue doit rester transparent)
    lab2, tailles2 = _composantes([not v for v in plein], w, h)
    bords = set()
    for i in range(w):
        bords |= {lab2[i], lab2[(h - 1) * w + i]}
    for j in range(h):
        bords |= {lab2[j * w], lab2[j * w + w - 1]}
    surface = sum(plein)
    petits = {k for k, s in tailles2.items() if k not in bords and s < trou_maxi * surface}
    return [v or (lab2[i] in petits) for i, v in enumerate(plein)]


def detourer(src, methode='dmax', retrait=5, gain=3.2, seuil=None, trou_maxi=0.02, part_mini=0.2):
    """Renvoie le packshot en RGBA, fond retire, recadre sur l'objet.
    trou_maxi : part de la surface au-dela de laquelle un trou reste transparent
    (0.02 garde le centre ajoure de la roue ; 1.0 bouche tout, utile pour la maille)."""
    im = Image.open(src).convert("RGB")
    w, h = im.size
    plein = silhouette(im, methode, seuil=seuil, trou_maxi=trou_maxi, part_mini=part_mini)
    masque = Image.new("L", (w, h))
    masque.putdata([255 if v else 0 for v in plein])
    if retrait > 1:
        masque = masque.filter(ImageFilter.MinFilter(retrait))
    masque = masque.filter(ImageFilter.GaussianBlur(0.9))

    if methode == 'translu':
        # l'objet laisse passer le fond : l'opacite suit l'ecart au fond
        d = _mesure(im, 'dmax')
        progressif = d.point(lambda v: min(255, int(v * gain)))
        masque = ImageChops.multiply(masque, progressif)

    rgba = im.convert("RGBA")
    rgba.putalpha(masque)
    boite = masque.point(lambda v: 255 if v > 16 else 0).getbbox()
    return rgba.crop(boite)
