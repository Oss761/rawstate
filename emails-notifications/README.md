# Emails de notification client — Rawstate

8 gabarits aux couleurs de la marque (monochrome `#fff · #f5f5f5 · #d9d9d9 · #666 · #111`,
typo Inter / Archivo, boutons pilule sombres, **vrai logo Rawstate** en header et footer),
prêts à coller dans Shopify.

> Fichiers au format **`.txt`** : le code (HTML + Liquid) s'ouvre tel quel pour un copier-coller
> propre, sans que le navigateur ne le « rende ».

## Où les coller dans Shopify

**Admin → Réglages → Notifications → Notifications client** → ouvrir la notification →
tout sélectionner dans le champ de code → **remplacer par le contenu du fichier** → *Enregistrer*.

> ⚠️ Colle **tout** le fichier (du `<!DOCTYPE html>` à `</html>`). Le champ Shopify attend le document complet.

| Fichier | Notification Shopify à remplacer |
|---|---|
| `01-confirmation-commande.txt` | **Confirmation de commande** (Order confirmation) |
| `02-confirmation-expedition.txt` | **Confirmation d'expédition** (Shipping confirmation) |
| `03-commande-en-cours-livraison.txt` | **En cours de livraison** (Out for delivery) |
| `04-commande-livree.txt` | **Livrée** (Delivered) |
| `05-confirmation-remboursement.txt` | **Remboursement de commande** (Order refund) |
| `06-commande-annulee.txt` | **Commande annulée** (Order cancelled) |
| `07-mise-a-jour-suivi.txt` | **Mise à jour de l'expédition** (Shipping update) |
| `08-facture-commande-en-attente.txt` | **Facture de commande** (Order invoice) — envoi manuel pour une commande en attente de paiement |

## Aperçu

- **Ouvrir le fichier dans un navigateur** (le renommer en `.html` d'abord) = tu vois la mise en
  page **et le vrai logo**, mais les balises `{{ ... }}` / `{% ... %}` restent en texte brut
  (c'est normal, c'est du Liquid interprété côté Shopify uniquement).
- **Vrai aperçu + données réelles** : dans l'éditeur de notification Shopify, bouton
  **« Aperçu »**, puis **« Envoyer un e-mail de test »** pour recevoir le rendu final.

## Logo

Le logo est **hébergé sur le CDN Shopify** (Fichiers) et câblé en dur dans chaque mail :

```
https://cdn.shopify.com/s/files/1/1091/2448/5458/files/rawstate-logo.png
```

Rien à configurer côté branding des notifications — il s'affiche partout (header 168×28, footer
120×20). Généré depuis `assets/logo-dark.svg` (converti en PNG, fond transparent).

## Variables Liquid utilisées (fournies par Shopify selon la notification)

- Commande : `name`, `customer.first_name`, `email`, `order_status_url`, `subtotal_line_items`,
  `subtotal_price`, `shipping_price`, `total_discounts`, `total_tax`, `total_price`, `shipping_address`.
- Expédition : `fulfillment.tracking_company`, `fulfillment.tracking_numbers`,
  `fulfillment.tracking_urls`, `fulfillment.fulfillment_line_items`.
- Remboursement : `amount`, `refund_line_items`.
- Facture : `invoice_url`, `custom_message`, `total_price`.

## Détails de marque intégrés

- Bandeau noir « Livraison mondiale · Expédition sous 24h · Retour 30 jours ».
- Vrai wordmark Rawstate (logo image) en header et footer.
- **Tracker de livraison monochrome** (Confirmée → Expédiée → En livraison → Livrée) sur les
  e-mails d'expédition.
- Livraison affichée **« Offerte »** quand le montant est 0 (seuil 90 € de la boutique).
- Ligne TVA masquée automatiquement (`total_tax > 0`) → cohérent avec la franchise en base
  (art. 293 B du CGI, EI Ossmane BAALI).
- Contact `info@rawstate.fr`, signature de marque en pied.

## À vérifier / ajuster

- Les liens `04` et `06` pointent vers `{{ shop.url }}/products/rawstate-the-fold` (fiche produit).
  Adapte le handle si besoin.
- Le bouton « Laisser un avis » (`04`) renvoie vers la fiche produit — branche-le sur ton app
  d'avis (Judge.me / Loox…) quand elle sera installée.
- Compatibilité testée pour Gmail, Apple Mail, Outlook (tables + CSS inline). Le logo, hébergé sur
  le CDN Shopify (image PNG), s'affiche dans tous les clients.
