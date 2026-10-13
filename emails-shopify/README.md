# E-mails de notification Shopify — Rawstate

8 gabarits HTML + Liquid, au format `.txt`, à coller dans Shopify.
Ils remplacent l'ancienne série `emails-notifications/` (époque monoproduit, ancien logo).

## Où les coller

**Admin Shopify → Paramètres → Notifications → Notifications client** → ouvrir la notification →
**Modifier le code** → tout sélectionner → coller le contenu **entier** du fichier → Enregistrer.

| Fichier | Notification Shopify |
|---|---|
| `01-confirmation-commande.txt` | Confirmation de commande |
| `02-confirmation-expedition.txt` | Confirmation d'expédition |
| `03-commande-en-cours-livraison.txt` | En cours de livraison |
| `04-commande-livree.txt` | Livrée |
| `05-confirmation-remboursement.txt` | Remboursement de commande |
| `06-commande-annulee.txt` | Commande annulée |
| `07-mise-a-jour-suivi.txt` | Mise à jour de l'expédition |
| `08-facture-commande-en-attente.txt` | Facture de commande (fonctionne aussi pour « Facture de commande provisoire ») |

Après collage : bouton **Aperçu**, puis **Envoyer un e-mail de test**.

## Le logo

Le logo Rawstate (soleil + « rawstate ») est hébergé dans les Fichiers Shopify
(`rawstate-logo-soleil.png`, copie de `assets/logo-dark.png`) et déjà câblé en tête de chaque fichier :

```liquid
{%- assign logo_url = 'https://cdn.shopify.com/s/files/1/1091/2448/5458/files/rawstate-logo-soleil.png?v=1791823400' -%}
```

Il s'affiche en en-tête et en pied. Si cette adresse est vidée, l'e-mail retombe sur le logo de
*Paramètres → Notifications → Personnaliser*, puis sur le nom « rawstate » en texte.
Ne pas supprimer ce fichier dans *Contenu → Fichiers* : les e-mails déjà envoyés perdraient leur logo.

Juste en dessous se règlent aussi l'adresse de contact et les liens « Politique de retour » / « CGV ».

## Ce qui s'adapte à chaque commande

- **Prénom** : celui du client, sinon de l'adresse de livraison ou de facturation, sinon formule neutre.
- **Articles** : photo, variante, options, quantité, prix barré et nom de la remise, mention « Offert » pour un article à 0 €.
- **Totaux** : codes de réduction nommés, livraison « Offerte » ou payante, TVA et droits de douane affichés seulement s'ils existent, économie totale.
- **Paiement** : carte et 4 derniers chiffres ou autre moyen ; message spécifique si le paiement est en attente.
- **Garantie** : 90 jours dès 2 tapis The Fold dans la commande, 30 jours sinon (bandeau, textes, pied).
- **Colis** : commande entière, envoi partiel (« le reste suit ») ou dernier colis ; un ou plusieurs numéros de suivi, ou aucun ; date de livraison estimée en français quand le transporteur la fournit.
- **Remboursement** : intégral ou partiel, avec ou sans articles retournés, moyen de paiement recrédité.
- **Annulation** : texte selon le motif (client, rupture, paiement refusé, sécurité, autre) et selon l'état du paiement (non débité, remboursé, remboursement en cours).
- **Facture** : montant total ou reste dû, date limite si elle existe, message personnel saisi dans Shopify à la place du texte par défaut.

## À vérifier

- La règle des 90 jours repose sur le mot « Fold » dans le nom du produit : à adapter si le produit change de nom ou si l'offre évolue.
- Délai annoncé dans la confirmation : « 5 à 14 jours » (celui des CGV).
- Délai bancaire annoncé pour les remboursements : « 5 à 10 jours ouvrés ».

## Modifier les e-mails

Les 8 fichiers sont générés : modifier `tools/build-emails.py`, puis lancer
`python tools/build-emails.py`. Une retouche faite directement dans un `.txt` serait écrasée
au prochain lancement.
