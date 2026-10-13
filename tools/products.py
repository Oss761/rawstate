# -*- coding: utf-8 -*-
"""Catalogue Rawstate. Source de verite unique pour toutes les pages generees."""

ARTICLES = [
    dict(url="https://rawstate.fr/blogs/news/tapis-yoga-voyage-criteres",
         img="https://cdn.shopify.com/s/files/1/1091/2448/5458/articles/hf_20260831_100531_d25ffc6b-b056-4582-8b0b-a4a8d261b849.png?v=1788172507&amp;width=800",
         alt="Tapis de yoga pliable pret pour le voyage, pose a cote d'un sac cabine",
         date_iso="2026-08-31", date="31 août 2026",
         titre="Tapis de yoga de voyage : les 5 critères qui comptent (et les 3 pièges à éviter)",
         resume="Volume plié, poids, épaisseur, adhérence : les 5 critères et les 3 pièges à éviter avant d'acheter."),
    dict(url="https://rawstate.fr/blogs/news/quelle-epaisseur-tapis-de-yoga",
         img="https://cdn.shopify.com/s/files/1/1091/2448/5458/articles/hf_20260824_175129_d742f099-b840-4018-8242-6b0a3f14b416.png?v=1787595309&amp;width=800",
         alt="Tapis de yoga pliable The Fold de Rawstate, 4 mm d'epaisseur",
         date_iso="2026-08-24", date="24 août 2026",
         titre="Quelle épaisseur pour un tapis de yoga ? Le guide clair, de 1,5 mm à 8 mm",
         resume="Confort, stabilité, transport : ce que change chaque épaisseur, et laquelle choisir selon votre pratique."),
    dict(url="https://rawstate.fr/blogs/news/tapis-yoga-pliable-ou-roule-appartement",
         img="https://cdn.shopify.com/s/files/1/1091/2448/5458/articles/hf_20260820_151912_e2149674-861a-4171-864e-e5472797a482.png?v=1787241559&amp;width=800",
         alt="Tapis de yoga plie et tapis de yoga roule cote a cote",
         date_iso="2026-08-20", date="20 août 2026",
         titre="Tapis de yoga pliable ou roulé : lequel choisir quand on vit en appartement ?",
         resume="Comparatif honnête, avantages, inconvénients et conseils pour bien choisir."),
    dict(url="https://rawstate.fr/blogs/news/plier-tapis-de-yoga",
         img="https://cdn.shopify.com/s/files/1/1091/2448/5458/articles/hf_20260817_183600_00de264c-16d4-4b2c-9e46-d1c0014e9b01.png?v=1787241712&amp;width=800",
         alt="Tapis de yoga pliable rose plie en pile compacte sur un parquet clair",
         date_iso="2026-08-17", date="17 août 2026",
         titre="Peut-on plier un tapis de yoga sans l'abîmer ?",
         resume="Tout dépend de la matière. Le test simple pour savoir si le vôtre supporte le pliage, et la bonne méthode en quatre étapes."),
]

# page : fichier de destination. img : visuel (SVG provisoire, a remplacer par une photo).
PRODUITS = [
    dict(slug="the-fold", page="the-fold.html", cat="tapis", vedette=True,
         nom="Tapis pliable The Fold", accroche="Le tapis pliable qui se range partout",
         prix=69.90, img="assets/mat-grey.webp",
         alt="Tapis de yoga pliable Tapis pliable The Fold",
         # coloris repris a l'identique de VARIANTS dans script.js (fiche The Fold).
         # Sert au choix des coloris dans les rituels ; la fiche The Fold garde son propre JS.
         coloris=[("Fog",    "#383b3e", "assets/swatch-grey.webp", 0),
                  ("Lagoon", "#a9cfe3", "assets/swatch-blue.webp", 0),
                  ("Dusk",   "#ebc7d2", "assets/swatch-pink.webp", 0)],
         resume="Se plie comme une serviette, se range dans un placard ou un sac. 183 × 61 cm, 4 mm, 700 g.",
         bullets=["Pliable en 10 secondes", "Format cabine, 700 g", "TPE écoresponsable"]),

    dict(slug="liege", page="tapis-liege.html", cat="tapis",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Tapis de yoga The Grip", accroche="Le grip qui s'améliore quand vous transpirez",
         prix=89.90, img="assets/liege-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/liege-1.webp", "Tapis de yoga en liege deroule, vue trois quarts"),
               ("assets/liege-2.webp", "Tapis de yoga en liege a moitie roule, base TPE visible"),
               ("assets/liege-3.webp", "Pratiquante en chien tete en bas sur le tapis en liege"),
               ("assets/liege-4.webp", "Pratiquant allonge sur le tapis en liege apres l'effort"),
               ("assets/liege-5.webp", "Dimensions du tapis en liege : 183 x 61 cm"),
               ("assets/liege-6.webp", "Coin du tapis retourne : une face en liege pour l'adherence, une face en TPE pour l'appui au sol"),
               ("assets/liege-7.webp", "Pratiquante portant le tapis The Grip roule sous le bras : leger et simple a porter")],
         alt="Tapis de yoga en liege deroule",
         # pastille unique pour "Composez votre rituel" (produit sans coloris)
         pastille=("Liège", "#e3c9a4", "assets/liege-sw.webp"),
         resume="Surface en liège naturel sur base TPE. Plus la main est humide, meilleure est l'adhérence.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Une face en liège naturel, une base en TPE stable. Plus vous transpirez, plus "
                    "l'adhérence se renforce, l'inverse de la plupart des tapis classiques. Sans "
                    "traitement chimique, juste la texture brute du liège sous vos mains et vos pieds.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(8, 14),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         bullets=["Liège naturel, sans traitement", "Adhérence renforcée à l'humidité", "Base TPE antidérapante"],
         # cadeau offert au-dessus du bouton d'ajout : (titre, mention, vignette)
         # meme carte claire a bordure terracotta que sur les rituels
         cadeau_offert=("Programme 21 jours pour reprendre le yoga", "Offert", "assets/perk-guide.webp"),
         specs=[("Dimensions", "183 × 61 cm"), ("Épaisseur", "6 mm"), ("Poids", "850 g"),
                ("Matière", "Liège naturel + TPE"), ("Entretien", "Chiffon humide, séchage à l'air libre")],
         desc="Le liège a une propriété rare : il devient plus adhérent au contact de l'humidité. "
              "Là où un tapis classique se dérobe en fin de séance, celui-ci se stabilise. La surface est "
              "naturellement antibactérienne et ne retient pas les odeurs. Sous le liège, une base en "
              "TPE ancre le tapis au sol, même sur parquet.",
         usage="Pensé pour le yoga dynamique, le vinyasa et les pratiques où l'on transpire.",
         # renvoi vers le pack qui contient ce tapis, entre la bande de photos et
         # les accordeons : (slug du rituel, composition, enumeration des autres)
         # Les prix affiches sont calcules, jamais saisis ici.
         rituel_lie=("studio", "The Grip + roue + bloc + gourde", "la roue, le bloc et la gourde",
                     "Ce tapis existe en rituel"),
         # photos en situation, bande 9:16 sous les moyens de paiement
         ugc=[("assets/grip-ugc-1.webp", "Tapis The Grip deroule sur un parquet, pieds nus au bord"),
              ("assets/grip-ugc-2.webp", "Main qui deroule le tapis The Grip, base noire visible"),
              ("assets/grip-ugc-3.webp", "Pratiquante souriante tenant le tapis The Grip roule sous le bras"),
              ("assets/grip-ugc-4.webp", "Pratiquante de dos marchant avec le tapis The Grip en bandouliere")],
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Fold
         accordeons=[
             ("Description",
              "<p>Le liège n'est pas un choix esthétique, c'est une question d'adhérence. "
              "Plus vous transpirez, plus il accroche : l'inverse de la plupart des tapis, "
              "qui glissent justement quand vous en avez le plus besoin.</p>"
              "<p>The Grip est un tapis de yoga en liège naturel, monté sur une base en TPE, "
              "pensé pour les séances où l'appui compte : postures debout, transitions, mains et "
              "pieds qui glissent en fin de séance. 183 × 61 cm, 6 mm d'épaisseur : assez de surface "
              "pour ne pas se sentir à l'étroit, assez d'amorti pour protéger les genoux et les "
              "poignets sans perdre la stabilité au sol.</p>"
              "<p>Le liège est une matière vivante : chaque tapis a son grain, ses nuances, sa "
              "texture. Le vôtre ne ressemblera à aucun autre.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Dimensions :</strong> 183 × 61 cm</li>"
              "<li><strong>Épaisseur :</strong> 6 mm</li>"
              "<li><strong>Surface :</strong> liège naturel</li>"
              "<li><strong>Base :</strong> TPE (thermoplastique élastomère)</li>"
              "<li><strong>Propriétés :</strong> antidérapant, y compris humide ; absorbe la transpiration</li>"
              "<li><strong>Composition :</strong> sans produits chimiques préoccupants, inodore</li>"
              "<li><strong>Usage :</strong> intérieur et extérieur, tous niveaux, particulièrement adapté "
              "aux débutants recherchant un soutien doux et stable</li>"
              "<li><strong>Entretien :</strong> facile, adapté à une utilisation régulière à la maison ou en studio</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 8 à 14 jours.</p>"),
         ]),

    dict(slug="acupression", page="planche-acupression.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         # renvoi vers le pack qui contient cette planche, sous les badges de paiement :
         # (slug du rituel, composition, enumeration des autres, eyebrow). Prix calcules.
         rituel_lie=("recup", "The Board + chaussettes + gourde", "les chaussettes et la gourde",
                     "Cette planche existe en rituel"),
         nom="Planche d'acupression The Board", accroche="Cinq minutes pieds nus, debout",
         prix=49.90, img="assets/acupression-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/acupression-1.webp", "Planche d'acupression ronde bleue a picots et billes metalliques"),
               ("assets/acupression-2.webp", "Pieds en chaussettes poses sur la planche d'acupression"),
               ("assets/acupression-3.webp", "Pratiquante debout pieds nus sur la planche apres le yoga"),
               ("assets/acupression-4.webp", "Planche d'acupression en TPE posee sur un tapis"),
               ("assets/acupression-5.webp", "Gros plans sur une bille metallique et une zone a pointes"),
               ("assets/acupression-6.webp", "Mode d'emploi en trois etapes : poser la planche au sol, poser les pieds dessus, profiter du massage"),
               ("assets/acupression-7.webp", "Homme assis, pieds poses sur la planche d'acupression : une therapie en douceur")],
         alt="Planche d'acupression ronde pour les pieds",
         pastille=("Bleu", "#cfeaf9", "assets/acupression-sw.webp"),
         resume="Une planche ronde à picots et billes métalliques pour détendre la voûte plantaire après une journée debout.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Une planche ronde à picots et billes métalliques pour stimuler la voûte plantaire. "
                    "Posez-y vos pieds quelques minutes après une séance de yoga, et laissez le relief "
                    "faire le travail. Simple, sans rituel, pour une détente ciblée au quotidien.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(5, 10),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         bullets=["Picots et billes métalliques", "TPE durable et sans odeur", "S'utilise debout ou assis"],
         specs=[("Format", "Rond"), ("Hauteur des picots", "8 mm"), ("Poids", "620 g"),
                ("Matière", "TPE"), ("Entretien", "Eau savonneuse")],
         desc="La plante du pied concentre une densité inhabituelle de terminaisons nerveuses. "
              "Y appliquer une pression répartie procure une sensation de détente très nette, en quelques minutes. "
              "La planche se pose au sol : on monte dessus progressivement, on respire, on redescend.",
         usage="À utiliser en fin de journée, avant ou après la séance. Commencez par une minute, chaussettes aux pieds.",
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         accordeons=[
             ("Description",
              "<p>Après une séance de yoga intense, la plante des pieds encaisse tout. The Board est "
              "une planche d'acupression ronde, conçue pour stimuler les points de pression du pied et "
              "relâcher les tensions accumulées, quelques minutes suffisent pour sentir la différence.</p>"
              "<p>Posez-la au sol, installez vos pieds dessus, laissez le poids du corps faire le travail. "
              "Pas de rituel, pas de matériel en plus : un objet simple à glisser sous le bureau, au pied "
              "du lit, ou à la fin d'une séance de yoga.</p>"
              "<p>Son bleu franc et son relief travaillé en font aussi un objet qu'on n'a pas envie de "
              "ranger : posé dans un salon ou une chambre, il a sa place à la vue de tous.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Diamètre :</strong> 34 cm</li>"
              "<li><strong>Forme :</strong> ronde, à reliefs (picots de réflexologie)</li>"
              "<li><strong>Couleur :</strong> bleu</li>"
              "<li><strong>Composition :</strong> sans produits chimiques préoccupants, adaptée aux peaux sensibles</li>"
              "<li><strong>Usage :</strong> intérieur, sol plat</li>"
              "<li><strong>Utilisation conseillée :</strong> quelques minutes par jour, pieds nus, en position "
              "assise ou debout selon la tolérance</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 5 à 10 jours.</p>"),
         ]),

    dict(slug="bloc", page="bloc-yoga.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Bloc de yoga The Block", accroche="Le sol, remonté jusqu'à vous",
         prix=24.90, img="assets/bloc-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/bloc-1.webp", "Bloc de yoga rose"),
               ("assets/bloc-2.webp", "Bloc de yoga vert"),
               ("assets/bloc-3.webp", "Bloc de yoga noir"),
               ("assets/bloc-4.webp", "Bloc de yoga bleu"),
               ("assets/bloc-5.webp", "Quatre blocs de yoga empiles, bleu, noir, vert et rose, garantie 30 jours"),
               ("assets/bloc-6.webp", "Pratiquante en fente basse, main posee sur un bloc de yoga rose : ideal pour le yoga ou le renforcement musculaire"),
               ("assets/bloc-7.webp", "Blocs de yoga vert et bleu en EVA sans odeur"),
               ("assets/bloc-8.webp", "Dimensions du bloc de yoga : 230 x 150 x 76 mm")],
         # selecteur de coloris : (nom, couleur de la pastille, vignette detouree, vue de la galerie)
         coloris=[("Rose", "#f3bfd0", "assets/bloc-sw-rose.webp", 0),
                  ("Vert", "#cfe39a", "assets/bloc-sw-vert.webp", 1),
                  ("Noir", "#6f6a66", "assets/bloc-sw-noir.webp", 2),
                  ("Bleu", "#b7dcf5", "assets/bloc-sw-bleu.webp", 3)],
         alt="Bloc de yoga en mousse EVA",
         resume="Un bloc en mousse EVA pour aller chercher une posture sans forcer. Trois hauteurs selon la face posée.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Un bloc en mousse EVA pour aller chercher une posture sans forcer. Trois hauteurs "
                    "selon la face posée, pour ajuster la distance au sol à votre niveau du jour. Stable "
                    "sous l'appui, léger à transporter, il s'intègre à toute pratique, du débutant au confirmé.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(6, 10),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         # offres par lot : remplacent le selecteur de quantite. Le 4e element est
         # un prix impose (sinon le 2e sert de remise en %). Un coloris par bloc.
         offres=[(1, 0, "Pour ajuster une posture"),
                 (2, 0, "Un sous chaque main", 44.90)],
         unite_lot="bloc",
         coloris_par_lot=True,   # un coloris a choisir par bloc du lot
         bullets=["Trois hauteurs en un bloc", "EVA sans odeur", "Rose, vert, noir ou bleu"],
         specs=[("Dimensions", "230 × 150 × 76 mm"), ("Poids", "180 g"), ("Charge", "Jusqu'à 120 kg"),
                ("Matière", "Mousse EVA"), ("Coloris", "Rose, vert, noir, bleu"), ("Entretien", "Chiffon humide")],
         desc="Un bloc ne compense pas un manque de souplesse : il rapproche le sol de la main pour que "
              "la posture reste juste. Posé sur l'une de ses trois faces, il offre 7,6, 15 ou 23 cm de hauteur. "
              "La mousse EVA est assez ferme pour supporter le poids du corps, assez souple pour rester confortable, "
              "et ne dégage aucune odeur.",
         usage="Précieux en yin yoga, en restauratif, dans toutes les flexions avant, et en renforcement musculaire.",
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         accordeons=[
             ("Description",
              "<p>Une posture qui ne descend pas encore jusqu'au sol n'est pas un échec, c'est une "
              "question de distance. The Block raccourcit cet écart : en mousse dense, il vous permet "
              "d'aller chercher une posture sans forcer, de gagner en stabilité dans les appuis, ou "
              "d'ajouter du lest dans un mouvement de renforcement.</p>"
              "<p>Trois hauteurs selon la face posée, une prise en main franche, un poids qui ne bouge "
              "pas sous l'appui. Aussi utile en début de pratique, pour construire l'alignement, qu'en "
              "pratique avancée, pour approfondir un étirement.</p>"
              "<p>Vendu à l'unité, il se glisse partout : sous un lit, dans un sac, à côté du tapis.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Matériau :</strong> mousse EVA</li>"
              "<li><strong>Coloris disponibles :</strong> rose, vert, noir, bleu</li>"
              "<li><strong>Usage :</strong> yoga, étirements, renforcement musculaire, intérieur et extérieur</li>"
              "<li><strong>Composition :</strong> sans produits chimiques préoccupants</li>"
              "<li><strong>Conditionnement :</strong> vendu à l'unité</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 6 à 10 jours.</p>"),
         ]),

    dict(slug="roue", page="roue-liege.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Roue de yoga The Wheel", accroche="Ouvrir la poitrine, dérouler le dos",
         prix=59.90, img="assets/roue-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/roue-1.webp", "Roue de yoga grise a l'exterieur et rose a l'interieur"),
               ("assets/roue-2.webp", "Pratiquante assise, jambe tendue posee sur la roue de yoga"),
               ("assets/roue-3.webp", "Pratiquante souriante tenant la roue de yoga : soulage les douleurs dorsales, aide a ameliorer la flexibilite"),
               ("assets/roue-4.webp", "Roue de yoga : 30 cm de diametre, 12 cm de largeur, 770 g"),
               ("assets/roue-5.webp", "Gros plan sur l'interieur de la roue : coussin robuste, pour un soutien confortable lors des etirements"),
               ("assets/roue-6.webp", "Pratiquante en extension arriere sur la roue : ideal pour les seances d'etirement et de relaxation")],
         alt="Roue de yoga grise et rose",
         pastille=("Gris et rose", "#d8ccce", "assets/roue-sw.webp"),
         resume="Un appui circulaire pour les extensions arrière, les étirements et le relâchement du dos. 30 cm, 770 g.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Un appui circulaire pour les extensions arrière, les étirements et le relâchement "
                    "du dos. 30 cm, 770 g : assez stable pour guider le mouvement, assez léger pour se "
                    "transporter partout. Le revêtement en PP assure une bonne accroche, même en pleine "
                    "transpiration.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(7, 14),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         bullets=["30 cm de diamètre", "Surface extérieure texturée", "770 g seulement"],
         specs=[("Diamètre", "30 cm"), ("Largeur", "12 cm"), ("Poids", "770 g"),
                ("Coloris", "Gris et rose"), ("Entretien", "Chiffon humide")],
         desc="Le dos passe la journée fermé, penché vers l'avant. La roue propose l'inverse : "
              "on s'allonge dessus, le thorax s'ouvre, la colonne se déroule vertèbre après vertèbre. "
              "Sa surface extérieure texturée offre une prise franche, et ses 770 g la rendent facile "
              "à poser sous le dos, une jambe ou un pied.",
         usage="Pour les ouvertures de poitrine, les étirements dorsaux, la souplesse des jambes et le travail d'équilibre.",
         # section "A completer avec", sous les badges de reassurance : (slug, coloris)
         # -> ajout immediat au panier, 1 exemplaire du coloris indique
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         # (texte fourni par Oss ; cf. reserves signalees : mention "liege" et coloris gris seul)
         accordeons=[
             ("Description",
              "<p>Le dos qui reste raide après une journée assise a besoin d'une extension douce, pas "
              "d'un étirement forcé. The Wheel est une roue de yoga pensée pour ça : posez le dos dessus, "
              "laissez le poids du corps guider le mouvement, et gagnez en amplitude au fil des séances "
              "sans jamais forcer une position.</p>"
              "<p>Son diamètre de 30 cm offre un appui stable, que ce soit pour une extension arrière "
              "progressive, un relâchement des épaules, ou un travail de flexibilité plus poussé une fois "
              "la confiance installée. Le revêtement en TPE + PP assure une accroche franche, même en pleine "
              "transpiration.</p>"
              "<p>Légère et compacte, elle se range aussi facilement qu'un tapis plié, et trouve sa place "
              "aussi bien dans une pratique sportive que dans une routine plus calme, en fin de journée.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Diamètre :</strong> 30 cm</li>"
              "<li><strong>Poids :</strong> 0,770 kg</li>"
              "<li><strong>Revêtement :</strong> TPE + PP</li>"
              "<li><strong>Coloris disponible :</strong> gris</li>"
              "<li><strong>Usage :</strong> étirement, relâchement du dos, amélioration de la flexibilité, intérieur</li>"
              "<li><strong>Composition :</strong> sans produits chimiques préoccupants, adaptée aux peaux sensibles</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 7 à 14 jours.</p>"),
         ]),

    dict(slug="chaussettes", page="chaussettes-antiderapantes.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Chaussettes The Socks", accroche="La stabilité, sans les pieds nus",
         prix=19.90, img="assets/chaussettes-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/chaussettes-1.webp", "Paire de chaussettes antiderapantes noir et blanc, semelle a picots silicone"),
               ("assets/chaussettes-2.webp", "Paire de chaussettes antiderapantes bleues, semelle a picots silicone"),
               ("assets/chaussettes-3.webp", "Paire de chaussettes antiderapantes rose et rouge, semelle a picots silicone"),
               ("assets/chaussettes-4.webp", "Chaussettes bleues portees : coton, nylon et polyester, resistantes a l'usure"),
               ("assets/chaussettes-5.webp", "Chaussettes rose portees sur un tapis, stabilite et liberte de mouvement"),
               ("assets/chaussettes-6.webp", "Gros plan sur les picots de silicone de la semelle")],
         # selecteur de coloris : (nom, couleur de la pastille, vignette detouree, vue de la galerie)
         coloris=[("Noir", "#6f6a66", "assets/chaussettes-sw-noir.webp", 0),
                  ("Bleu", "#b5d3f3", "assets/chaussettes-sw-bleu.webp", 1),
                  ("Rose", "#f7cfcf", "assets/chaussettes-sw-rose.webp", 2)],
         alt="Chaussettes de yoga antiderapantes",
         resume="Picots de silicone sous la semelle. L'adhérence du pied nu, en gardant les pieds couverts.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Picots de silicone sous la semelle. L'adhérence du pied nu, en gardant les pieds "
                    "couverts. Une coupe mi-mollet ajustée, sans glissement, pour bouger librement dans "
                    "chaque posture.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(6, 10),
         # mention affichee a cote de "Livraison offerte", sur la ligne du prix
         mention_prix="Taille : 37-43",
         # mention ajoutee apres le coloris dans "Composez votre rituel" des packs
         composer_mention="(Taille : 37-43)",
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         # offres par lot : (nombre, remise en %, sous-titre, prix impose).
         # Remplacent le selecteur de quantite. Ici les prix sont imposes et la
         # remise est a 0 : pas de pastille de pourcentage, seule l'economie en
         # euros est annoncee (elle, elle est exacte).
         offres=[(1, 0, "Pour essayer"),
                 (2, 0, "Une paire d'avance", 34.90),
                 (3, 0, "Toute la semaine", 44.90)],
         unite_lot="paire",
         coloris_par_lot=True,   # un coloris a choisir par paire du lot
         bullets=["Semelle à picots silicone", "Coton, nylon et polyester", "Noir, bleu ou rose"],
         specs=[("Tailles", "37-43"), ("Matière", "Coton, nylon, polyester"),
                ("Semelle", "Picots de silicone"), ("Coloris", "Noir, bleu, rose"),
                ("Lavage", "Machine 30°, à l'envers"), ("Vendu par", "Paire")],
         desc="Pratiquer pieds nus n'est pas toujours possible : sol froid, cours collectif, chambre d'hôtel. "
              "Les picots de silicone reproduisent l'accroche de la peau sur le tapis, sans la sensation "
              "de glisser dans le tissu. La maille en coton, nylon et polyester reste fine pour garder le "
              "retour d'information au sol, et résiste au lavage répété.",
         usage="Yoga, pilates, barre au sol — et tous les parquets froids de l'hiver.",
         # section "A completer avec", sous les badges de reassurance : (slug, coloris)
         # -> ajout immediat au panier, 1 exemplaire du coloris indique
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         accordeons=[
             ("Description",
              "<p>Pieds nus sur un tapis, l'adhérence est excellente jusqu'à ce que le sol soit froid ou "
              "que la semelle capte la poussière. The Socks règlent ce compromis : une semelle en silicone "
              "antidérapant qui garde l'accroche d'un pied nu, sans les inconvénients.</p>"
              "<p>La coupe mi-mollet couvre sans comprimer, pour une liberté de mouvement complète dans "
              "les flexions et les appuis au sol. Le tricot en coton, nylon et polyester respire et garde "
              "son élasticité séance après séance.</p>"
              "<p>Disponibles en noir, bleu et rose-pourpre, elles s'utilisent aussi bien en yoga qu'au "
              "quotidien, pour les pieds qui ont toujours un peu froid.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Hauteur :</strong> mi-mollet</li>"
              "<li><strong>Matériau :</strong> coton, nylon, polyester</li>"
              "<li><strong>Semelle :</strong> silicone antidérapant</li>"
              "<li><strong>Coloris disponibles :</strong> noir, bleu, rose-pourpre</li>"
              "<li><strong>Tailles disponibles :</strong> 37 à 43</li>"
              "<li><strong>Coupe :</strong> ajustée, sans glissement pendant l'activité</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 6 à 10 jours.</p>"),
         ]),

    dict(slug="gants", page="gants-antiderapants.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Gants de yoga The Gloves", accroche="Les mains qui ne glissent plus",
         prix=19.90, img="assets/gants-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/gants-1.webp", "Paire de gants de yoga noirs, paume a picots silicone"),
               ("assets/gants-2.webp", "Paire de gants de yoga lilas, paume a picots silicone"),
               ("assets/gants-3.webp", "Paire de gants de yoga bleu marine, paume a picots silicone"),
               ("assets/gants-4.webp", "Paire de gants de yoga jaune pale, paume a picots silicone"),
               ("assets/gants-5.webp", "Pratiquante en planche, gants lilas en appui sur le tapis : coton et polyester, excellente adherence"),
               ("assets/gants-6.webp", "Gros plan sur des mains gantees posees sur un tapis en liege"),
               ("assets/gants-7.webp", "Les quatre coloris de gants disposes en cercle : noir, lilas, bleu marine et jaune, paume a picots et dos de main")],
         # selecteur de coloris : (nom, couleur de la pastille, vignette detouree, vue de la galerie)
         coloris=[("Noir",        "#6f6a66", "assets/gants-sw-noir.webp",   0),
                  ("Lilas",       "#ddd3ef", "assets/gants-sw-lilas.webp",  1),
                  ("Bleu marine", "#8e9bbd", "assets/gants-sw-marine.webp", 2),
                  ("Jaune",       "#f6ebc0", "assets/gants-sw-jaune.webp",  3)],
         alt="Gants de yoga antiderapants",
         # offres : remplacent le selecteur de quantite. La 2e est un lot de
         # produits DIFFERENTS -> dict avec `produits` (une ligne de coloris par
         # produit). Prix plein et economie calcules depuis le catalogue.
         offres=[(1, 0, "Pour les appuis sur les mains"),
                 dict(titre="Duo gants + chaussettes", sous="Les mains et les pieds",
                      prix=34.90, produits=["gants", "chaussettes"])],
         unite_lot="paire",
         coloris_par_lot=True,   # le coloris se choisit dans chaque offre
         resume="Le pendant des chaussettes, pour les appuis sur les mains. Doigts libres, paume à picots.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="Le pendant des chaussettes, pour les appuis sur les mains. Doigts libres, paume à "
                    "picots, pour une adhérence franche sans perdre en sensation. Respirants et lavables, "
                    "ils accompagnent aussi bien le yoga que d'autres activités demandant une bonne prise.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(5, 9),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         bullets=["Paume à picots silicone", "Doigts ouverts", "Noir, lilas, bleu marine ou jaune"],
         specs=[("Taille", "S/M"), ("Matière", "Coton et polyester"),
                ("Paume", "Picots de silicone"), ("Coloris", "Noir, lilas, bleu marine, jaune"),
                ("Lavage", "Machine 30°, à l'envers"), ("Vendu par", "Paire")],
         desc="En chien tête en bas, ce sont les mains qui lâchent en premier. Les picots de silicone "
              "sur la paume tiennent la position, y compris sur un tapis humide. Les doigts restent "
              "découverts pour ne rien perdre du contact avec le sol, et la maille en coton et polyester "
              "reste confortable même sur les séances longues.",
         usage="Pour les planches, les appuis inversés et les enchaînements longs.",
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         accordeons=[
             ("Description",
              "<p>En pleine séance, ce sont souvent les mains qui glissent en premier : appuis inversés, "
              "planches prolongées, transpiration qui s'accumule. The Gloves offrent une adhérence "
              "supplémentaire là où le tapis seul ne suffit plus.</p>"
              "<p>Le design à demi-doigts laisse les articulations libres tout en couvrant la paume, là "
              "où l'appui se joue vraiment. Le tissu tricoté en coton et polyester respire, même sur les "
              "séances les plus intenses, et garde sa forme lavage après lavage.</p>"
              "<p>Disponibles en plusieurs teintes, ils se glissent facilement dans un sac de sport, "
              "prêts pour le yoga comme pour d'autres activités demandant une bonne prise.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Design :</strong> demi-doigts</li>"
              "<li><strong>Matériau :</strong> coton, polyester, tissu tricoté</li>"
              "<li><strong>Propriétés :</strong> antidérapant, respirant</li>"
              "<li><strong>Entretien :</strong> lavable, résistant à l'usure</li>"
              "<li><strong>Coloris disponibles :</strong> noir, bleu marine, lilas, jaune</li>"
              "<li><strong>Usage :</strong> yoga et autres activités sportives</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 5 à 9 jours.</p>"),
         ]),

    dict(slug="gourde", page="gourde-transparente.html", cat="accessoires",
         sans_cross=True,   # pas de section « Ça va bien ensemble »
         nom="Gourde The Bottle", accroche="Voir ce qu'il reste, d'un coup d'œil",
         prix=29.90, img="assets/gourde-1.webp",
         # galerie de la fiche produit, dans l'ordre fourni
         imgs=[("assets/gourde-1.webp", "Gourde transparente noire avec bouchon noir et dragonne"),
               ("assets/gourde-2.webp", "Gourde transparente bleue avec bouchon bleu et dragonne"),
               ("assets/gourde-3.webp", "Gourde transparente rouge avec bouchon rouge et dragonne"),
               ("assets/gourde-4.webp", "Gourde transparente rose avec bouchon rose et dragonne"),
               ("assets/gourde-5.webp", "Gourde rouge tenue en main : 650 mL, design moderne, usage polyvalent, resistante aux chocs et aux chutes"),
               ("assets/gourde-6.webp", "Les quatre coloris de la gourde : noir, bleu, rouge et rose")],
         # selecteur de coloris : (nom, couleur de la pastille, vignette detouree, vue de la galerie)
         coloris=[("Noir",  "#6f6a66", "assets/gourde-sw-noir.webp",  0),
                  ("Bleu",  "#7fb6dd", "assets/gourde-sw-bleu.webp",  1),
                  ("Rouge", "#f0544a", "assets/gourde-sw-rouge.webp", 2),
                  ("Rose",  "#f0bfc8", "assets/gourde-sw-rose.webp",  3)],
         alt="Gourde d'eau transparente 650 ml",
         resume="650 mL, bouchon à clapet et dragonne. Transparente : on voit ce qu'on a bu, et ce qu'il reste.",
         # texte affiche sous le prix SUR LA FICHE (resume reste la version courte
         # des cartes de la page de garde et de la meta description)
         pdp_resume="650 mL, bouchon à clapet et dragonne. Transparente : on voit ce qu'on a bu, et ce "
                    "qu'il reste. Résistante aux chocs du quotidien, elle suit du tapis au sac de sport "
                    "sans encombrer.",
         # delai de livraison estime affiche sous le titre : (jours mini, jours maxi), calcule au chargement
         livraison=(6, 10),
         # prix total (x quantite) affiche sur le bouton d'ajout
         prix_sur_bouton=True,
         bullets=["650 mL, sans BPA", "Bouchon à clapet et dragonne", "Noir, bleu, rouge ou rose"],
         specs=[("Contenance", "650 mL"), ("Bouchon", "À clapet, avec dragonne"),
                ("Matière", "Plastique sans BPA"), ("Coloris", "Noir, bleu, rouge, rose"),
                ("Entretien", "Eau savonneuse")],
         desc="Une gourde opaque oblige à deviner. Celle-ci est transparente : on voit ce qu'on a bu, "
              "et ce qu'il reste. Le bouchon à clapet se referme d'un geste et tient fermé dans un sac, "
              "tapis roulé par-dessus, et la dragonne permet de la porter au doigt entre deux séances.",
         usage="Assez fine pour tenir dans la poche latérale d'un sac de sport.",
         # section "A completer avec", sous les badges de reassurance : (slug, coloris)
         # -> ajout immediat au panier, 1 exemplaire du coloris indique
         # accordeons affiches sous les moyens de paiement, comme sur la fiche The Grip
         accordeons=[
             ("Description",
              "<p>Après une séance, l'hydratation compte autant que l'étirement final. The Bottle est une "
              "gourde de 650 ml pensée pour suivre partout : du tapis au sac de sport, du bureau au studio.</p>"
              "<p>Le matériau transparent permet de voir en un coup d'œil ce qu'il reste à boire : simple, "
              "mais redoutablement pratique pour tenir un objectif d'hydratation dans la journée. Sa forme "
              "ergonomique tient bien en main, même en mouvement, et résiste aux chocs du quotidien.</p>"
              "<p>Disponible en plusieurs coloris sobres, elle s'adapte à tous les styles, sans distinction "
              "d'âge ni de genre.</p>"),
             ("Caractéristiques",
              "<ul>"
              "<li><strong>Capacité :</strong> 650 ml</li>"
              "<li><strong>Matériau :</strong> transparent</li>"
              "<li><strong>Coloris disponibles :</strong> noir, bleu, rouge, rose</li>"
              "<li><strong>Résistance :</strong> aux chocs et aux chutes</li>"
              "<li><strong>Usage :</strong> yoga, quotidien, déplacements</li>"
              "</ul>"),
             ("Livraison",
              "<p>Votre commande est préparée sous 1 à 2 jours ouvrés. Expédition sous 6 à 10 jours.</p>"),
         ]),
]


# Packs "Rituels" : produits vendus ensemble, a prix rond. Le prix plein et
# l'economie sont calcules depuis PRODUITS -> jamais de prix qui se contredisent.
# Visuels generes par tools/gen-rituels.py (produits detoures sur fond de marque).
RITUELS = [
    dict(slug="essentiel", nom="L'Essentiel", badge="Rituel 01",
         sous="Pour commencer chez soi, sans rien connaître au yoga.",
         pdp_resume="Ce rituel réunit l'essentiel pour dérouler votre premier tapis, même dans un "
                    "studio ou un coin de salon : Tapis pliable The Fold se plie et se range en un geste, "
                    "le bloc vous soutient dans les postures que votre corps ne tient pas encore, et "
                    "les chaussettes antidérapantes vous évitent de glisser sur le parquet. Pensé pour "
                    "débuter sans y laisser tout son salon, ni tout son budget.",
         # cadeaux du pack, affiches sous "Composez votre rituel" : une ligne par cadeau
         cadeau=[("1 sac de rangement", "Offert", "assets/perk-bag.webp"),
                 ("Programme 21 jours pour reprendre le yoga", "Offert", "assets/perk-guide.webp")],
         produits=["the-fold", "bloc", "chaussettes"], prix=99.0,
         # date de livraison estimee sous le titre : (mini, maxi) jours ajoutes a aujourd'hui
         livraison=(6, 12),
         # galerie de la fiche du rituel, dans l'ordre fourni
         imgs=[("assets/rituel-essentiel-1.webp", "Le rituel L'Essentiel : tapis pliable The Fold, bloc de yoga bleu et chaussettes antiderapantes"),
               ("assets/rituel-essentiel-2.webp", "Le rituel L'Essentiel a 99 € au lieu de 114,70 €, soit 15,70 € d'economie"),
               ("assets/rituel-essentiel-3.webp", "Pratiquante assise sur le tapis pliable deroule, bloc de yoga pose a cote"),
               ("assets/rituel-essentiel-4.webp", "Tapis pliable range plie sur une etagere, entre des serviettes et un panier"),
               ("assets/rituel-essentiel-5.webp", "Gros plan sur la semelle a picots des chaussettes antiderapantes"),
               ("assets/rituel-essentiel-6.webp", "Main en appui sur le bloc de yoga pendant une fente basse"),
               ("assets/rituel-essentiel-7.webp", "Livraison offerte, garantie 30 jours, retour 30 jours")],
         img="assets/rituel-essentiel-photo.webp",
         alt="Le rituel L'Essentiel sur fond vert : tapis pliable The Fold, bloc de yoga bleu et chaussettes antiderapantes noires",
         # section "En detail" : titre, texte et "Bon a savoir" ecrits a la main
         # (sinon produit_rituel() les calcule depuis `sous` et l'economie)
         titre_detail="Tout ce qu'il faut. Rien de plus.",
         desc="Quand on débute, le vrai risque n'est pas de mal choisir son tapis : c'est "
              "d'arrêter au bout de deux semaines, parce que tout est compliqué à sortir, à "
              "installer, à ranger. Ce rituel retire ces obstacles un à un. Un tapis qui se range "
              "en un geste, un bloc pour ne jamais forcer, des chaussettes pour ne pas glisser. "
              "Il ne reste plus qu'à dérouler.",
         usage_ico="shield",   # bouclier a coche, trait fin, vert accent
         usage="Garantie 30 jours : si le yoga n'est finalement pas pour vous, renvoyez le "
               "rituel : on vous rembourse.",
         # section "Comment proceder a ce rituel ?" : (titre, sous-titre, image, alt)
         # rendue entre la buy box et la section "En detail"
         etapes=[
             ("Déroulez",
              "Le tapis se déplie en deux gestes, même entre le canapé et la table basse.",
              "assets/rituel-essentiel-etape-1.webp",
              "Main qui deplie le tapis rose sur le parquet, entre le canape et la table basse"),
             ("Ancrez-vous",
              "Les chaussettes tiennent au sol, le bloc soutient les postures que vous ne tenez pas encore.",
              "assets/rituel-essentiel-etape-2.webp",
              "Main en appui sur le bloc de yoga noir, pied en chaussette antiderapante sur le tapis rose"),
             ("Rangez",
              "Il se replie comme une serviette et disparaît dans un placard.",
              "assets/rituel-essentiel-etape-3.webp",
              "Tapis rose plie range sur une etagere, a cote de serviettes pliees et d'un panier en osier"),
         ],
         # remplace les 2 accordeons generes par defaut dans produit_rituel()
         accordeons=[
             ("Ce que contient le rituel",
              "<p>Le rituel L'Essentiel réunit trois objets, livrés en une seule commande :</p>"
              "<ul>"
              "<li><strong>Tapis pliable The Fold :</strong> tapis de yoga pliable, 183 × 61 cm déplié, "
              "4 mm d'épaisseur, environ 700 g. Se range comme une serviette.</li>"
              "<li><strong>The Block :</strong> bloc de yoga en mousse dense, pour soutenir les "
              "postures le temps que la souplesse s'installe.</li>"
              "<li><strong>The Socks :</strong> chaussettes en coton et polyester, semelle à picots "
              "de silicone antidérapants.</li>"
              "</ul>"
              "<p>Trois objets pensés pour un usage quotidien à la maison, sans rien d'autre à prévoir.</p>"),
             ("Livraison",
              "<p>Les trois produits de ce rituel viennent de fournisseurs spécialisés différents : "
              "le tapis, le bloc et les chaussettes ne sont pas fabriqués au même endroit. Ils peuvent "
              "donc arriver en plusieurs colis distincts plutôt qu'un seul. Comptez entre 6 et 12 jours "
              "ouvrés pour recevoir l'ensemble du rituel. La livraison reste offerte, comme sur chaque "
              "rituel Rawstate.</p>"),
         ]),
    dict(slug="studio", nom="Le Studio", badge="Le plus complet", vedette=True,
         sous="Le niveau studio, sans sortir de chez vous.",
         pdp_resume="Ce rituel réunit ce qu'il faut pour une vraie séance à domicile : le liège de "
                    "The Grip pour l'adhérence, la roue pour l'ouverture, le bloc pour la profondeur, "
                    "la gourde pour tenir la distance. Le studio, chez vous.",
         # cadeau du pack, affiche sous "Composez votre rituel"
         cadeau=("Programme 21 jours pour reprendre le yoga", "Offert", "assets/perk-guide.webp"),
         produits=["liege", "roue", "bloc", "gourde"], prix=159.0,
         # date de livraison estimee sous le titre : (mini, maxi) jours ajoutes a aujourd'hui
         livraison=(6, 14),
         # galerie de la fiche du rituel, dans l'ordre fourni
         imgs=[("assets/rituel-studio-1.webp", "Le rituel Le Studio : tapis en liege The Grip, roue de yoga, bloc rose et gourde"),
               ("assets/rituel-studio-2.webp", "Le rituel Le Studio a 159 € au lieu de 204,60 €, soit 45,60 € d'economie"),
               ("assets/rituel-studio-3.webp", "Le tapis en liege deroule dans un salon, roue, bloc et gourde poses dessus"),
               ("assets/rituel-studio-4.webp", "Main posee sur la surface en liege du tapis, gros plan sur le grain"),
               ("assets/rituel-studio-5.webp", "Pratiquante en extension arriere sur la roue, posee sur le tapis en liege"),
               ("assets/rituel-studio-6.webp", "159 € une fois pour l'equipement complet, contre 60 € par mois en studio"),
               ("assets/rituel-studio-7.webp", "Dimensions : tapis 183 x 61 cm, roue 33 cm"),
               ("assets/rituel-studio-8.webp", "Livraison offerte, garantie 30 jours, retour 30 jours")],
         img="assets/rituel-studio-photo.webp",
         alt="Le rituel Le Studio sur fond vert : tapis en liege The Grip deroule, roue de yoga rose, bloc rose et gourde",
         # section "En detail" : titre, texte et "Bon a savoir" ecrits a la main
         # (sinon produit_rituel() les calcule depuis `sous` et l'economie)
         titre_detail="S'équiper une fois, pour longtemps.",
         desc="Le liège, la roue et le bloc forment le setup qu'on retrouve dans les studios "
              "bien équipés. Ce sont des objets qu'on achète pour une pratique régulière, pas "
              "pour essayer. Réunis dans un seul rituel, ils coûtent ce qu'ils coûteraient "
              "séparément, moins le superflu.",
         usage_ico="calendar",   # calendrier, trait fin, vert accent
         usage="Faites le calcul : à raison de trois séances par semaine, le rituel revient à "
               "environ 1 € la séance la première année.",
         # section "Comment proceder a ce rituel ?" : (titre, sous-titre, image, alt)
         # rendue entre la buy box et la section "En detail"
         etapes=[
             ("Installez",
              "Le liège se déroule à plat et accroche dès la première posture, même quand les mains transpirent.",
              "assets/rituel-studio-etape-1.webp",
              "Main a plat sur la surface en liege du tapis The Grip, gros plan sur le grain"),
             ("Ouvrez",
              "La roue libère le dos et la cage thoracique après une journée assise.",
              "assets/rituel-studio-etape-2.webp",
              "Pratiquante en extension arriere sur la roue de yoga rose, posee sur le tapis en liege"),
             ("Tenez",
              "Le bloc pour la profondeur, la gourde pour ne pas couper la séance.",
              "assets/rituel-studio-etape-3.webp",
              "Bloc de yoga bleu, roue et gourde poses sur le tapis en liege deroule dans un salon"),
         ],
         # remplace les 2 accordeons generes par defaut dans produit_rituel()
         accordeons=[
             ("Ce que contient le rituel",
              "<p>Le rituel Le Studio réunit quatre objets, livrés en une seule commande :</p>"
              "<ul>"
              "<li><strong>The Grip :</strong> tapis de yoga en liège naturel sur base TPE. "
              "L'adhérence s'améliore avec l'humidité de la main ou du pied, à l'inverse d'un tapis "
              "classique qui glisse en transpirant.</li>"
              "<li><strong>The Wheel :</strong> roue de yoga, extérieur texturé, intérieur lisse, "
              "pour accompagner les ouvertures de dos et de cage thoracique.</li>"
              "<li><strong>The Block :</strong> bloc de yoga en mousse dense, pour approfondir les "
              "postures que votre pratique appelle désormais.</li>"
              "<li><strong>The Bottle :</strong> gourde étanche avec bouchon à clapet et dragonne, "
              "pour garder de l'eau à portée sans interrompre la séance.</li>"
              "</ul>"
              "<p>Quatre objets pensés pour une pratique régulière, avec le niveau d'équipement "
              "d'un studio, chez vous.</p>"),
             ("Livraison",
              "<p>Les quatre produits de ce rituel viennent de fournisseurs spécialisés différents : "
              "le tapis, la roue, le bloc et la gourde ne sont pas fabriqués au même endroit. Ils "
              "peuvent donc arriver en plusieurs colis distincts plutôt qu'un seul. Comptez entre 6 "
              "et 14 jours ouvrés pour recevoir l'ensemble du rituel. La livraison reste offerte, "
              "comme sur chaque rituel Rawstate.</p>"),
         ]),
    dict(slug="recup", nom="La Récup'", badge="Rituel 03",
         sous="La détente plantaire, après la journée debout.",
         pdp_resume="Planche d'acupression, chaussettes et gourde : un rituel du soir pour les pieds "
                    "fatigués, qu'on pratique le yoga ou qu'on soit simplement resté debout toute la journée.",
         produits=["acupression", "chaussettes", "gourde"], prix=85.0,
         # date de livraison estimee sous le titre : (mini, maxi) jours ajoutes a aujourd'hui
         livraison=(5, 10),
         # galerie de la fiche du rituel, dans l'ordre fourni
         imgs=[("assets/rituel-recup-1.webp", "Le rituel La Recup : chaussettes antiderapantes, planche d'acupression et gourde"),
               ("assets/rituel-recup-2.webp", "Le rituel La Recup a 85 € au lieu de 99,70 €, soit 14,70 € d'economie"),
               ("assets/rituel-recup-3.webp", "Pieds nus poses sur la planche d'acupression, assis dans un canape"),
               ("assets/rituel-recup-4.webp", "D'abord avec les chaussettes, ensuite pieds nus : deux facons de s'habituer a la planche"),
               ("assets/rituel-recup-5.webp", "Gros plan sur les picots et les billes metalliques de la planche, sous un doigt"),
               ("assets/rituel-recup-6.webp", "La planche, la gourde et les chaussettes posees dans un salon en fin de journee"),
               ("assets/rituel-recup-7.webp", "Mode d'emploi : 01 chaussettes, 02 debout 3 minutes, 03 respirer"),
               ("assets/rituel-recup-8.webp", "Livraison offerte, garantie 30 jours, retour 30 jours")],
         img="assets/rituel-recup-photo.webp",
         alt="Le rituel La Recup sur fond taupe : planche d'acupression bleue, chaussettes antiderapantes bleues et gourde",
         # section "En detail" : titre, texte et "Bon a savoir" ecrits a la main
         # (sinon produit_rituel() les calcule depuis `sous` et l'economie)
         titre_detail="Pas besoin de faire du yoga.",
         desc="La planche ne demande ni tapis, ni souplesse, ni tenue de sport. Elle est faite "
              "pour toutes celles et ceux qui finissent la journée sur leurs pieds : en boutique, "
              "en cuisine, en salle de soins, ou après un footing. Trois minutes debout le soir, "
              "le temps d'un appel ou d'un thé, et c'est tout.",
         usage_ico="info",   # « i » dans un cercle, trait fin, vert accent
         usage="Pour bien débuter : commencez une à deux minutes avec les chaussettes, puis "
               "allongez progressivement. En cas de problème de santé aux pieds ou de circulation, "
               "demandez l'avis d'un professionnel de santé avant utilisation.",
         # section "Comment proceder a ce rituel ?" : (titre, sous-titre, image, alt)
         # rendue entre la buy box et la section "En detail"
         etapes=[
             ("Chaussez",
              "Les premières fois, gardez les chaussettes : les picots passent en douceur.",
              "assets/rituel-recup-etape-1.webp",
              "Pieds en chaussettes antiderapantes poses sur la planche d'acupression bleue"),
             ("Tenez trois minutes",
              "Debout sur la planche, le temps d'un café ou d'un appel.",
              "assets/rituel-recup-etape-2.webp",
              "Pieds nus debout sur la planche d'acupression, dans un salon"),
             ("Respirez",
              "Un verre d'eau, et la journée debout se termine vraiment.",
              "assets/rituel-recup-etape-3.webp",
              "Fin de journee : planche d'acupression et gourde au sol, chaussettes posees sur le canape"),
         ],
         # remplace les 2 accordeons generes par defaut dans produit_rituel()
         accordeons=[
             ("Ce que contient le rituel",
              "<p>Le rituel La Récup' réunit trois objets, livrés en une seule commande :</p>"
              "<ul>"
              "<li><strong>The Board :</strong> planche d'acupression ronde, picots en silicone et "
              "billes métalliques, pour détendre la voûte plantaire après une journée debout ou en "
              "mouvement.</li>"
              "<li><strong>The Socks :</strong> chaussettes en coton et polyester, semelle à picots "
              "de silicone antidérapants, pour commencer en douceur avant de passer pieds nus sur "
              "la planche.</li>"
              "<li><strong>The Bottle :</strong> gourde étanche avec bouchon à clapet et dragonne, "
              "à garder près du canapé pour la pause qui suit.</li>"
              "</ul>"
              "<p>Trois objets pensés pour un rituel du soir, qu'on pratique le yoga ou qu'on soit "
              "simplement resté debout toute la journée.</p>"),
             ("Livraison",
              "<p>Les trois produits de ce rituel viennent de fournisseurs spécialisés différents : "
              "la planche, les chaussettes et la gourde ne sont pas fabriqués au même endroit. Ils "
              "peuvent donc arriver en plusieurs colis distincts plutôt qu'un seul. Comptez entre 5 "
              "et 10 jours ouvrés pour recevoir l'ensemble du rituel. La livraison reste offerte, "
              "comme sur chaque rituel Rawstate.</p>"),
         ]),
]


def par_slug(s):
    return next(p for p in PRODUITS if p["slug"] == s)


def prix_plein(r):
    """Somme des prix a l'unite des produits du rituel."""
    return round(sum(par_slug(s)["prix"] for s in r["produits"]), 2)


def nom_court(p):
    """Nom commercial court : "Bloc de yoga The Block" -> "The Block",
    "Rituel L'Essentiel" -> "L'Essentiel".
    L'assertion previent un renommage silencieux des produits."""
    mots = p["nom"].split()
    if mots[-2] == "The":
        return " ".join(mots[-2:])
    assert p.get("cat") == "rituels", 'nom sans "The X" : %s' % p["nom"]
    return " ".join(mots[1:]) if mots[0] == "Rituel" else p["nom"]
