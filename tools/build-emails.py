# -*- coding: utf-8 -*-
"""Genere les 8 e-mails de notification Shopify de Rawstate (HTML + Liquid, en .txt).

    python tools/build-emails.py

Sortie : emails-shopify/*.txt. Ne pas editer les .txt a la main : modifier ce fichier puis relancer.
Jetons : §F = police de texte, §T = police de titre (remplaces a l'ecriture).
"""
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, 'emails-shopify')

F = "'Inter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"
T = "'Fraunces',Georgia,'Times New Roman',serif"

# Couleurs de la marque (styles.css)
ENCRE, GRIS, LIGNE, FOND, TEAL, TERRA, SAPIN = '#111111', '#666666', '#ececec', '#F7F3EC', '#2E6B67', '#C05B33', '#2E5A44'


# ---------------------------------------------------------------- reglages + variables communes
REGLAGES = """{%- comment -%}
  RAWSTATE — réglages (les seules lignes à modifier à la main)
  logo_url : adresse du logo hébergé dans Shopify (Contenu > Fichiers). Si elle est vidée, l'e-mail
             affiche le logo défini dans Réglages > Notifications, ou à défaut « rawstate » en texte.
{%- endcomment -%}
{%- assign logo_url = 'https://cdn.shopify.com/s/files/1/1091/2448/5458/files/rawstate-logo-soleil.png?v=1791823400' -%}
{%- assign email_contact = 'info@rawstate.fr' -%}
{%- assign url_retours = shop.url | append: '/pages/politique-retour' -%}
{%- assign url_cgv = shop.url | append: '/pages/cgv' -%}

{%- assign prenom = customer.first_name | default: shipping_address.first_name | default: billing_address.first_name -%}
{%- assign mois = 'janvier,février,mars,avril,mai,juin,juillet,août,septembre,octobre,novembre,décembre' | split: ',' -%}
{%- if logo_url == blank and shop.email_logo_url -%}{%- assign logo_url = shop.email_logo_url -%}{%- endif -%}
{%- comment -%} Garantie : 90 jours dès 2 tapis The Fold dans la commande, 30 jours sinon {%- endcomment -%}
{%- assign nb_fold = 0 -%}
{%- for l in line_items -%}{%- if l.title contains 'Fold' -%}{%- assign nb_fold = nb_fold | plus: l.quantity -%}{%- endif -%}{%- endfor -%}
{%- assign garantie = 30 -%}{%- if nb_fold >= 2 -%}{%- assign garantie = 90 -%}{%- endif -%}
{%- assign nb_articles = 0 -%}
{%- for l in line_items -%}{%- assign nb_articles = nb_articles | plus: l.quantity -%}{%- endfor -%}
"""

ENVOI = """{%- comment -%} Colis : toute la commande, une partie, ou le dernier colis {%- endcomment -%}
{%- assign envoi_partiel = false -%}
{%- if fulfillment.item_count and item_count and fulfillment.item_count < item_count -%}{%- assign envoi_partiel = true -%}{%- endif -%}
{%- assign reste_a_venir = false -%}
{%- if envoi_partiel and fulfillment_status == 'partial' -%}{%- assign reste_a_venir = true -%}{%- endif -%}
{%- assign lien_suivi = fulfillment.tracking_url | default: fulfillment.tracking_urls.first | default: order_status_url -%}
"""


def date_fr(expr):
    """Date en francais (« 1er mars 2026 ») : Shopify ne traduit pas les noms de mois."""
    return ("{% assign _j = EXPR | date: '%-d' -%}{%- assign _m = EXPR | date: '%-m' | minus: 1 -%}"
            "{% if _j == '1' %}1er{% else %}{{ _j }}{% endif %} {{ mois[_m] }} {{ EXPR | date: '%Y' }}").replace('EXPR', expr)


# ---------------------------------------------------------------- briques
def tete(titre, preheader):
    return """<!DOCTYPE html>
<html lang="fr" xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="color-scheme" content="light only">
  <meta name="supported-color-schemes" content="light only">
  <title>""" + titre + """ — Rawstate</title>
  <!--[if mso]><style>* { font-family: Georgia, Arial, sans-serif !important; }</style><![endif]-->
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap');
    body, table, td { margin:0; padding:0; }
    img { border:0; line-height:100%; outline:none; text-decoration:none; -ms-interpolation-mode:bicubic; }
    a { color:#111111; }
    body { width:100% !important; background:#F7F3EC; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; }
    .wrap { width:600px; max-width:600px; }
    @media only screen and (max-width:620px) {
      .wrap { width:100% !important; }
      .px { padding-left:22px !important; padding-right:22px !important; }
      .h1 { font-size:31px !important; }
      .stack { display:block !important; width:100% !important; padding:0 0 18px 0 !important; }
    }
  </style>
</head>
<body style="margin:0; padding:0; background:#F7F3EC;">
""" + REGLAGES + """[[PRELUDE]]
  <div style="display:none; max-height:0; overflow:hidden; opacity:0; color:#F7F3EC; font-size:1px; line-height:1px;">
    """ + preheader + """&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;&nbsp;&zwnj;
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F7F3EC;">
    <tr>
      <td align="center" style="padding:28px 12px 40px;">
        <table role="presentation" class="wrap" width="600" cellpadding="0" cellspacing="0" style="width:600px; max-width:600px; background:#ffffff; border:1px solid #ececec; border-radius:18px; overflow:hidden;">

          <!-- bandeau -->
          <tr>
            <td align="center" style="background:#111111; padding:11px 16px; font-family:§F; font-size:11px; font-weight:500; letter-spacing:1.8px; color:#ffffff; text-transform:uppercase;">
              Livraison offerte&nbsp;&nbsp;·&nbsp;&nbsp;Garantie {{ garantie }} jours&nbsp;&nbsp;·&nbsp;&nbsp;Paiement sécurisé
            </td>
          </tr>

          <!-- logo -->
          <tr>
            <td align="center" style="padding:34px 24px 8px;">
              <a href="{{ shop.url }}" style="text-decoration:none; color:#111111;">
                {% if logo_url != blank %}
                <img src="{{ logo_url }}" alt="rawstate" width="190" height="32" style="display:block; margin:0 auto; width:190px; height:32px; font-family:§T; font-size:28px; font-weight:600; color:#111111;">
                {% else %}
                <span style="font-family:§T; font-size:30px; font-weight:600; letter-spacing:-0.6px; color:#111111;"><span style="color:#C45831;">&#9679;</span>&nbsp;rawstate</span>
                {% endif %}
              </a>
            </td>
          </tr>
"""


def hero(surtitre, h1, texte):
    return """
          <!-- accroche -->
          <tr>
            <td class="px" align="center" style="padding:18px 48px 0; font-family:§F; font-size:12px; font-weight:600; letter-spacing:3px; color:#C05B33; text-transform:uppercase;">
              """ + surtitre + """
            </td>
          </tr>
          <tr>
            <td class="px" align="center" style="padding:10px 44px 0;">
              <h1 class="h1" style="margin:0; font-family:§T; font-size:38px; line-height:1.1; letter-spacing:-0.8px; font-weight:600; color:#111111;">""" + h1 + """</h1>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" style="padding:16px 52px 4px; font-family:§F; font-size:15px; line-height:1.65; color:#666666;">
              """ + texte + """
            </td>
          </tr>
"""


def bouton(href, libelle):
    return """
          <tr>
            <td align="center" style="padding:24px 24px 6px;">
              <table role="presentation" cellpadding="0" cellspacing="0" align="center"><tr>
                <td align="center" bgcolor="#111111" style="border-radius:100px;">
                  <a href=\"""" + href + """\" style="display:inline-block; padding:15px 40px; font-family:§F; font-size:15px; font-weight:600; letter-spacing:0.2px; color:#ffffff; text-decoration:none; border-radius:100px;">""" + libelle + """</a>
                </td>
              </tr></table>
            </td>
          </tr>
"""


def suivi_etapes(etape):
    """Barre de progression Confirmee > Expediee > En livraison > Livree (etape 1 a 4)."""
    pct = {1: 12, 2: 40, 3: 68, 4: 100}[etape]
    noms = ['Confirmée', 'Expédiée', 'En livraison', 'Livrée']
    align = ['left', 'center', 'center', 'right']
    cases = ''
    for i, nom in enumerate(noms, 1):
        style = 'color:#111111; font-weight:700;' if i == etape else ('color:#111111; font-weight:500;' if i < etape else 'color:#b3b3b3;')
        cases += '\n                  <td align="%s" width="25%%" style="%s">%s</td>' % (align[i - 1], style, nom)
    reste = ('<td style="background:#ececec; height:4px; line-height:4px; font-size:0; border-radius:0 4px 4px 0;" width="%d%%">&nbsp;</td>' % (100 - pct)) if pct < 100 else ''
    rayon = '4px 0 0 4px' if pct < 100 else '4px'
    return """
          <!-- progression : etape """ + str(etape) + """/4 -->
          <tr>
            <td class="px" style="padding:26px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>
                <td style="background:#2E6B67; height:4px; line-height:4px; font-size:0; border-radius:""" + rayon + """;" width=\"""" + str(pct) + """%">&nbsp;</td>
                """ + reste + """
              </tr></table>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin-top:10px; font-family:§F; font-size:11px; letter-spacing:0.3px;">
                <tr>""" + cases + """
                </tr>
              </table>
            </td>
          </tr>
"""


def encart(contenu, fond='#F7F3EC'):
    return """
          <tr>
            <td class="px" style="padding:24px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:""" + fond + """; border-radius:14px;">
                <tr>
                  <td style="padding:18px 22px; font-family:§F; font-size:14px; line-height:1.6; color:#666666;">
""" + contenu + """
                  </td>
                </tr>
              </table>
            </td>
          </tr>
"""


def etiquette(texte):
    return '<div style="font-size:11px; font-weight:600; letter-spacing:1.5px; color:#111111; text-transform:uppercase; margin-bottom:6px;">' + texte + '</div>'


FILET = """
          <tr><td class="px" style="padding:26px 48px 0;"><div style="border-top:1px solid #ececec; font-size:0; line-height:0;">&nbsp;</div></td></tr>
"""


def titre_section(texte):
    return """
          <tr>
            <td class="px" style="padding:24px 48px 4px; font-family:§F; font-size:13px; font-weight:600; letter-spacing:2px; color:#111111; text-transform:uppercase;">""" + texte + """</td>
          </tr>
"""


def articles(source, prix=True):
    """Liste d'articles. source = 'commande' | 'envoi' | 'remboursement'."""
    boucle = {
        'commande': "{% for line in subtotal_line_items %}{% assign qte = line.quantity %}",
        'envoi': "{% for fline in fulfillment.fulfillment_line_items %}{% assign line = fline.line_item %}{% assign qte = fline.quantity %}",
        'remboursement': "{% for rline in refund_line_items %}{% assign line = rline.line_item %}{% assign qte = rline.quantity %}",
    }[source]
    col_prix = """
                  <td valign="top" align="right" style="padding:14px 0; border-bottom:1px solid #ececec; font-family:§F; font-size:14px; font-weight:600; color:#111111; white-space:nowrap;">
                    {% if line.final_line_price == 0 %}
                      <span style="color:#C05B33;">Offert</span>
                    {% else %}
                      {% if line.original_line_price > line.final_line_price %}<span style="font-weight:400; color:#999999; text-decoration:line-through;">{{ line.original_line_price | money }}</span><br>{% endif %}
                      {{ line.final_line_price | money }}
                    {% endif %}
                  </td>""" if prix else ''
    remises = """
                    {% for da in line.line_level_discount_allocations %}
                    <br><span style="color:#C05B33; font-size:12px; font-weight:600;">{{ da.discount_application.title }} (−{{ da.amount | money }})</span>
                    {% endfor %}""" if prix else ''
    return """
          <tr>
            <td class="px" style="padding:2px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                """ + boucle + """
                <tr>
                  <td width="68" valign="top" style="padding:14px 0; border-bottom:1px solid #ececec;">
                    {% if line.image %}<img src="{{ line | img_url: 'compact_cropped' }}" alt="" width="60" height="60" style="display:block; width:60px; height:60px; border-radius:10px; background:#F7F3EC; border:1px solid #ececec;">{% endif %}
                  </td>
                  <td valign="top" style="padding:14px 12px; border-bottom:1px solid #ececec; font-family:§F; font-size:14px; color:#111111; line-height:1.45;">
                    <span style="font-weight:600;">{{ line.product.title | default: line.title }}</span>
                    {% if line.variant.title != blank and line.variant.title != 'Default Title' %}<br><span style="color:#666666; font-size:13px;">{{ line.variant.title }}</span>{% endif %}
                    {% if line.selling_plan_allocation %}<br><span style="color:#666666; font-size:13px;">{{ line.selling_plan_allocation.selling_plan.name }}</span>{% endif %}
                    {% for p in line.properties %}{% assign p1 = p.first | slice: 0 %}{% unless p.last == blank or p1 == '_' %}
                    <br><span style="color:#666666; font-size:13px;">{{ p.first }}&nbsp;: {{ p.last }}</span>
                    {% endunless %}{% endfor %}
                    <br><span style="color:#666666; font-size:13px;">Quantité&nbsp;: {{ qte }}</span>""" + remises + """
                  </td>""" + col_prix + """
                </tr>
                {% endfor %}
              </table>
            </td>
          </tr>
"""


TOTAUX = """
          <!-- totaux -->
          <tr>
            <td class="px" style="padding:18px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-family:§F; font-size:14px; color:#666666;">
                <tr>
                  <td style="padding:5px 0;">Sous-total</td>
                  <td align="right" style="padding:5px 0; color:#111111;">{{ line_items_subtotal_price | default: subtotal_price | money }}</td>
                </tr>
                {% for da in discount_applications %}{% if da.target_type == 'line_item' and da.target_selection == 'all' %}
                <tr>
                  <td style="padding:5px 0;">Réduction <span style="color:#C05B33; font-weight:600;">{{ da.title }}</span></td>
                  <td align="right" style="padding:5px 0; color:#C05B33;">−{{ da.total_allocated_amount | money }}</td>
                </tr>
                {% endif %}{% endfor %}
                {% if requires_shipping %}
                <tr>
                  <td style="padding:5px 0;">Livraison{% if shipping_method.title %} <span style="color:#999999;">· {{ shipping_method.title }}</span>{% endif %}</td>
                  <td align="right" style="padding:5px 0; color:#111111;">{% if shipping_price == 0 %}<span style="color:#2E5A44; font-weight:600;">Offerte</span>{% else %}{{ shipping_price | money }}{% endif %}</td>
                </tr>
                {% endif %}
                {% if total_duties and total_duties > 0 %}
                <tr>
                  <td style="padding:5px 0;">Droits de douane</td>
                  <td align="right" style="padding:5px 0; color:#111111;">{{ total_duties | money }}</td>
                </tr>
                {% endif %}
                {% if tax_price and tax_price > 0 %}
                <tr>
                  <td style="padding:5px 0;">{% if taxes_included %}Dont TVA{% else %}TVA{% endif %}</td>
                  <td align="right" style="padding:5px 0; color:#111111;">{{ tax_price | money }}</td>
                </tr>
                {% endif %}
                <tr><td colspan="2" style="padding-top:10px;"><div style="border-top:1px solid #ececec; font-size:0; line-height:0;">&nbsp;</div></td></tr>
                <tr>
                  <td style="padding:12px 0 0; font-family:§T; font-size:19px; font-weight:600; color:#111111;">Total</td>
                  <td align="right" style="padding:12px 0 0; font-family:§T; font-size:19px; font-weight:600; color:#111111;">{{ total_price | money }}</td>
                </tr>
                {% if total_discounts and total_discounts > 0 %}
                <tr>
                  <td colspan="2" align="right" style="padding:4px 0 0; font-size:13px; color:#C05B33; font-weight:600;">Vous économisez {{ total_discounts | money }}</td>
                </tr>
                {% endif %}
              </table>
            </td>
          </tr>
"""


def adresse(var):
    return ("{{ V.name }}<br>{% if V.company != blank %}{{ V.company }}<br>{% endif %}{{ V.address1 }}<br>"
            "{% if V.address2 != blank %}{{ V.address2 }}<br>{% endif %}{{ V.zip }} {{ V.city }}<br>{{ V.country }}").replace('V', var)


ADRESSE_LIVRAISON = """
          {% if requires_shipping and shipping_address %}
          <tr>
            <td class="px" style="padding:24px 48px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              """ + etiquette('Adresse de livraison') + """
              """ + adresse('shipping_address') + """
            </td>
          </tr>
          {% endif %}
"""

ADRESSES = """
          <!-- adresses -->
          <tr>
            <td class="px" style="padding:28px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  {% if requires_shipping and shipping_address %}
                  <td class="stack" valign="top" width="50%" style="padding:0 10px 0 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
                    """ + etiquette('Livraison') + """
                    """ + adresse('shipping_address') + """
                  </td>
                  {% endif %}
                  {% if billing_address %}
                  <td class="stack" valign="top" width="50%" style="padding:0 0 0 10px; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
                    """ + etiquette('Facturation') + """
                    """ + adresse('billing_address') + """
                  </td>
                  {% endif %}
                </tr>
              </table>
            </td>
          </tr>
"""


def paiements(genre):
    """genre = 'paiement' (sale/capture) | 'remboursement' (refund)."""
    cond = ("transaction.kind == 'refund'" if genre == 'remboursement'
            else "transaction.kind == 'sale' or transaction.kind == 'capture'")
    return """
                {% for transaction in transactions %}{% if transaction.status == 'success' %}{% if """ + cond + """ %}
                <tr>
                  <td style="padding:4px 0; color:#666666;">
                    {% if transaction.payment_details.credit_card_company %}{{ transaction.payment_details.credit_card_company }}{% else %}{{ transaction.gateway_display_name }}{% endif %}{% if transaction.payment_details.credit_card_last_four_digits %} se terminant par {{ transaction.payment_details.credit_card_last_four_digits }}{% endif %}
                  </td>
                  <td align="right" style="padding:4px 0; color:#111111; font-weight:600; white-space:nowrap;">{{ transaction.amount | money }}</td>
                </tr>
                {% endif %}{% endif %}{% endfor %}"""


def bloc_suivi():
    return encart("""                    {% if fulfillment.tracking_numbers.size > 0 %}
                    """ + etiquette("{% if fulfillment.tracking_numbers.size > 1 %}Numéros de suivi{% else %}Numéro de suivi{% endif %}") + """
                    {% if fulfillment.tracking_company %}<span style="color:#111111;">{{ fulfillment.tracking_company }}</span><br>{% endif %}
                    {% for numero in fulfillment.tracking_numbers %}
                      {% assign lien_numero = fulfillment.tracking_urls[forloop.index0] %}
                      {% if lien_numero %}<a href="{{ lien_numero }}" style="color:#111111; font-weight:600;">{{ numero }}</a>{% else %}<span style="color:#111111; font-weight:600;">{{ numero }}</span>{% endif %}<br>
                    {% endfor %}
                    {% else %}
                    """ + etiquette('Suivi') + """
                    Le numéro de suivi n'est pas encore disponible. Vous pouvez suivre l'avancement depuis la page de votre commande.
                    {% endif %}
                    {% if fulfillment.estimated_delivery_at %}
                    <div style="margin-top:10px; padding-top:10px; border-top:1px solid #e6dfd3;">Livraison estimée&nbsp;: <strong style="color:#111111;">""" + date_fr('fulfillment.estimated_delivery_at') + """</strong></div>
                    {% endif %}""")


NOTE_COLIS = """
          {% if envoi_partiel %}
          <tr>
            <td class="px" align="center" style="padding:16px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              {% if reste_a_venir %}
              Ce colis contient <strong style="color:#111111;">une partie</strong> de votre commande. Les autres articles voyagent séparément&nbsp;: vous recevrez un e-mail de suivi pour chacun.
              {% else %}
              Ce colis contient les <strong style="color:#111111;">derniers articles</strong> de votre commande {{ name }}.
              {% endif %}
            </td>
          </tr>
          {% endif %}
"""


def pied(rassurance=True):
    bande = encart("""                    <div style="text-align:center; font-size:12px; font-weight:600; letter-spacing:0.4px; color:#111111;">Livraison offerte&nbsp;&nbsp;·&nbsp;&nbsp;Garantie {{ garantie }} jours&nbsp;&nbsp;·&nbsp;&nbsp;Paiement sécurisé</div>""") if rassurance else ''
    return bande + """
          <!-- pied -->
          <tr>
            <td align="center" style="padding:34px 48px 8px; font-family:§T; font-size:20px; font-weight:600; letter-spacing:-0.3px; color:#111111;">
              {% if logo_url != blank %}
              <img src="{{ logo_url }}" alt="rawstate" width="125" height="21" style="display:block; margin:0 auto; width:125px; height:21px;">
              {% else %}
              <span style="color:#C45831;">&#9679;</span>&nbsp;rawstate
              {% endif %}
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:2px 48px 4px; font-family:§F; font-size:12px; line-height:1.7; color:#999999;">
              Une question&nbsp;? Répondez à cet e-mail ou écrivez-nous&nbsp;: <a href="mailto:{{ email_contact }}" style="color:#111111; text-decoration:none;">{{ email_contact }}</a>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:4px 48px 4px; font-family:§F; font-size:12px; line-height:1.7; color:#999999;">
              <a href="{{ url_retours }}" style="color:#666666;">Politique de retour</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="{{ url_cgv }}" style="color:#666666;">CGV</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="{{ shop.url }}" style="color:#666666;">Boutique</a>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:6px 48px 32px; font-family:§F; font-size:11px; line-height:1.7; color:#b3b3b3;">
              Rawstate — Des rituels de yoga pensés pour la maison.<br>
              © {{ 'now' | date: '%Y' }} Rawstate. Tous droits réservés.
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


BONJOUR = "{% if prenom != blank %}{{ prenom }}, votre{% else %}Votre{% endif %}"
CMD = '<strong style="color:#111111;">{{ name }}</strong>'


# ================================================================ 01 — confirmation de commande
def confirmation_commande():
    attente = "{%- assign paiement_attente = false -%}{%- if has_pending_payment or financial_status == 'pending' -%}{%- assign paiement_attente = true -%}{%- endif -%}\n"
    return (
        tete('Confirmation de commande', "{% if paiement_attente %}Commande {{ name }} enregistrée — en attente de votre paiement.{% else %}Votre commande {{ name }} est confirmée. Merci de votre confiance.{% endif %}").replace('[[PRELUDE]]', attente)
        + hero("{% if paiement_attente %}Commande enregistrée{% else %}Commande confirmée{% endif %}",
               "Merci{% if prenom != blank %}, {{ prenom }}{% endif %}.",
               """{% if paiement_attente %}
              Nous avons bien enregistré votre commande """ + CMD + """. Elle partira en préparation dès que votre paiement sera validé — vous n'avez rien d'autre à faire si vous l'avez déjà lancé.
              {% elsif requires_shipping %}
              Nous avons bien reçu votre commande """ + CMD + """. Nous la préparons avec soin&nbsp;: vous recevrez un e-mail avec le suivi dès son expédition.
              {% else %}
              Nous avons bien reçu votre commande """ + CMD + """. Vous trouverez son récapitulatif ci-dessous.
              {% endif %}""")
        + "{% if requires_shipping %}" + suivi_etapes(1) + "{% endif %}"
        + bouton('{{ order_status_url }}', 'Voir ma commande')
        + "{% if requires_shipping %}"
        + encart("""                    """ + etiquette('Et maintenant&nbsp;?') + """
                    Votre commande est livrée{% if shipping_price == 0 %} gratuitement{% endif %}, généralement sous <strong style="color:#111111;">5 à 14 jours</strong>.
                    {% if garantie == 90 %}Avec vos {{ nb_fold }} tapis The Fold, vous profitez d'une garantie étendue de <strong style="color:#111111;">90 jours</strong>.{% else %}Vous disposez de <strong style="color:#111111;">{{ garantie }} jours</strong> après réception pour changer d'avis.{% endif %}""")
        + "{% if nb_articles > 1 %}"
        + encart("""                    """ + etiquette('Livraison en plusieurs colis possible') + """
                    Vous avez commandé plusieurs articles&nbsp;: il se peut qu'ils ne soient pas livrés en une seule fois. Nos fournisseurs ne se trouvent pas tous au même endroit selon les articles, chacun expédie donc de son côté. Vous pourriez ainsi recevoir <strong style="color:#111111;">plusieurs colis, à des dates différentes</strong>&nbsp;: c'est tout à fait normal.""", fond='#f5f5f5')
        + "{% endif %}"
        + "{% endif %}"
        + FILET
        + titre_section("Votre commande · {{ nb_articles }} article{% if nb_articles > 1 %}s{% endif %}")
        + articles('commande')
        + TOTAUX
        + """
          <!-- paiement -->
          <tr>
            <td class="px" style="padding:14px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-family:§F; font-size:13px;">""" + paiements('paiement') + """
                {% if paiement_attente %}
                <tr><td colspan="2" style="padding:4px 0; color:#C05B33; font-weight:600;">Paiement en attente de validation</td></tr>
                {% endif %}
              </table>
            </td>
          </tr>
"""
        + ADRESSES
        + """
          {% if note != blank %}
          <tr>
            <td class="px" style="padding:22px 48px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              """ + etiquette('Votre message') + """
              {{ note }}
            </td>
          </tr>
          {% endif %}
"""
        + pied())


# ================================================================ 02 — confirmation d'expedition
def confirmation_expedition():
    return (
        tete("Confirmation d'expédition", "{% if envoi_partiel %}Une partie de votre commande {{ name }} vient d'être expédiée.{% else %}Votre commande {{ name }} vient d'être expédiée.{% endif %}").replace('[[PRELUDE]]', ENVOI)
        + hero('Colis expédié', "C'est en route.",
               """{% if envoi_partiel and reste_a_venir %}
              {% if prenom != blank %}{{ prenom }}, une{% else %}Une{% endif %} première partie de votre commande """ + CMD + """ vient de partir.
              {% elsif envoi_partiel %}
              {% if prenom != blank %}{{ prenom }}, le{% else %}Le{% endif %} dernier colis de votre commande """ + CMD + """ vient de partir.
              {% else %}
              """ + BONJOUR + """ commande """ + CMD + """ vient de partir. {% endif %}
              {% if fulfillment.tracking_numbers.size > 0 %}Suivez son acheminement à tout moment.{% else %}Le suivi sera disponible sous peu.{% endif %}""")
        + suivi_etapes(2)
        + bloc_suivi()
        + bouton('{{ lien_suivi }}', 'Suivre mon colis')
        + NOTE_COLIS
        + """
          <tr>
            <td class="px" align="center" style="padding:14px 52px 0; font-family:§F; font-size:12px; line-height:1.6; color:#999999;">
              Le suivi peut mettre 24 à 48&nbsp;h à s'actualiser après la prise en charge par le transporteur.
            </td>
          </tr>
"""
        + FILET
        + titre_section("Dans ce colis")
        + articles('envoi', prix=False)
        + ADRESSE_LIVRAISON
        + pied())


# ================================================================ 03 — en cours de livraison
def en_cours_livraison():
    return (
        tete('Commande en cours de livraison', "Votre colis Rawstate est en cours de livraison{% if shipping_address.city != blank %} à {{ shipping_address.city }}{% endif %}.").replace('[[PRELUDE]]', ENVOI)
        + hero('En cours de livraison', "Il arrive{% if prenom != blank %}, {{ prenom }}{% endif %}.",
               """{% if envoi_partiel %}Un colis{% else %}Le colis{% endif %} de votre commande """ + CMD + """ est entre les mains du livreur{% if shipping_address.city != blank %} et se dirige vers <strong style="color:#111111;">{{ shipping_address.city }}</strong>{% endif %}.""")
        + suivi_etapes(3)
        + bloc_suivi()
        + bouton('{{ lien_suivi }}', 'Suivre la livraison')
        + NOTE_COLIS
        + encart("""                    """ + etiquette('Bon à savoir') + """
                    En cas d'absence, le transporteur laisse un avis de passage ou dépose le colis en point de retrait&nbsp;: les instructions figurent sur la page de suivi.""", fond='#f5f5f5')
        + FILET
        + titre_section("Dans ce colis")
        + articles('envoi', prix=False)
        + ADRESSE_LIVRAISON
        + pied())


# ================================================================ 04 — commande livree
def commande_livree():
    return (
        tete('Commande livrée', "Votre colis Rawstate a été livré. Bonne pratique.").replace('[[PRELUDE]]', ENVOI)
        + hero('Colis livré', "C'est arrivé.",
               """{% if reste_a_venir %}
              {% if prenom != blank %}{{ prenom }}, un{% else %}Un{% endif %} premier colis de votre commande """ + CMD + """ a été livré. Le reste est en chemin.
              {% else %}
              """ + BONJOUR + """ commande """ + CMD + """ a été livrée{% if shipping_address.city != blank %} à {{ shipping_address.city }}{% endif %}. Il ne reste plus qu'à dérouler, respirer, pratiquer.
              {% endif %}""")
        + "{% unless reste_a_venir %}" + suivi_etapes(4) + "{% endunless %}"
        + bouton('{{ order_status_url }}', 'Voir ma commande')
        + encart("""                    """ + etiquette('Votre garantie') + """
                    Vous avez <strong style="color:#111111;">{{ garantie }} jours</strong> à compter de la réception{% if reste_a_venir or envoi_partiel %} du dernier colis{% endif %} pour essayer vos articles. S'ils ne vous conviennent pas, le retour est simple&nbsp;: <a href="{{ url_retours }}" style="color:#2E6B67; font-weight:600;">voir la politique de retour</a>.""")
        + encart("""                    """ + etiquette('Colis introuvable ou abîmé&nbsp;?') + """
                    Regardez d'abord dans votre boîte aux lettres, auprès d'un voisin ou du gardien. Si vous ne le trouvez pas, ou si un article est arrivé endommagé, répondez à cet e-mail (avec une photo si possible)&nbsp;: nous nous en occupons.""", fond='#f5f5f5')
        + FILET
        + titre_section("Articles livrés")
        + articles('envoi', prix=False)
        + pied())


# ================================================================ 05 — confirmation de remboursement
def confirmation_remboursement():
    prelude = ("{%- assign rembt_total = false -%}{%- if financial_status == 'refunded' -%}{%- assign rembt_total = true -%}{%- endif -%}\n"
               "{%- assign nb_rendus = 0 -%}{%- for r in refund_line_items -%}{%- assign nb_rendus = nb_rendus | plus: r.quantity -%}{%- endfor -%}\n")
    return (
        tete('Confirmation de remboursement', "{% if amount > 0 %}Un remboursement de {{ amount | money }} a été émis pour votre commande {{ name }}.{% else %}Votre commande {{ name }} a été mise à jour.{% endif %}").replace('[[PRELUDE]]', prelude)
        + hero("{% if rembt_total %}Remboursement intégral{% else %}Remboursement partiel{% endif %}", "C'est remboursé.",
               """{% if prenom != blank %}{{ prenom }}, nous{% else %}Nous{% endif %} avons émis
              {% if rembt_total %}le remboursement intégral de votre commande """ + CMD + """.
              {% elsif nb_rendus > 0 %}un remboursement pour {% if nb_rendus > 1 %}{{ nb_rendus }} articles{% else %}un article{% endif %} de votre commande """ + CMD + """.
              {% else %}un remboursement partiel sur votre commande """ + CMD + """.
              {% endif %}""")
        + """
          {% if amount > 0 %}
          <tr>
            <td class="px" style="padding:24px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F7F3EC; border-radius:14px;">
                <tr>
                  <td align="center" style="padding:24px 22px 8px; font-family:§F; font-size:11px; font-weight:600; letter-spacing:1.5px; color:#666666; text-transform:uppercase;">Montant remboursé</td>
                </tr>
                <tr>
                  <td align="center" style="padding:0 22px 14px; font-family:§T; font-size:40px; font-weight:600; letter-spacing:-1px; color:#2E5A44;">{{ amount | money }}</td>
                </tr>
                <tr>
                  <td style="padding:0 22px 18px;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="font-family:§F; font-size:13px; border-top:1px solid #e6dfd3;">
                      <tr><td colspan="2" style="height:10px; line-height:10px; font-size:0;">&nbsp;</td></tr>""" + paiements('remboursement') + """
                    </table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td class="px" align="center" style="padding:16px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              Le montant est recrédité sur votre moyen de paiement d'origine. Selon votre banque, il apparaît sur votre compte sous <strong style="color:#111111;">5 à 10 jours ouvrés</strong>.
            </td>
          </tr>
          {% else %}
          <tr>
            <td class="px" align="center" style="padding:16px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              Aucun montant n'était à recréditer pour cette opération.
            </td>
          </tr>
          {% endif %}
"""
        + bouton('{{ order_status_url }}', 'Voir ma commande')
        + """
          {% if refund_line_items.size > 0 %}"""
        + FILET
        + titre_section("{% if nb_rendus > 1 %}Articles remboursés{% else %}Article remboursé{% endif %}")
        + articles('remboursement', prix=False)
        + """
          {% endif %}
          {% unless rembt_total %}
          <tr>
            <td class="px" align="center" style="padding:20px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#999999;">
              Le reste de votre commande n'est pas modifié.
            </td>
          </tr>
          {% endunless %}
"""
        + pied(rassurance=False))


# ================================================================ 06 — commande annulee
def commande_annulee():
    return (
        tete('Commande annulée', "Votre commande {{ name }} a été annulée.").replace('[[PRELUDE]]', '')
        + hero('Commande annulée', "Votre commande est annulée.",
               """{% case cancel_reason %}
              {% when 'customer' %}
              {% if prenom != blank %}{{ prenom }}, comme{% else %}Comme{% endif %} vous l'avez demandé, votre commande """ + CMD + """ a bien été annulée.
              {% when 'inventory' %}
              {% if prenom != blank %}{{ prenom }}, nous{% else %}Nous{% endif %} sommes désolés&nbsp;: un ou plusieurs articles de votre commande """ + CMD + """ ne sont plus disponibles, et nous avons dû l'annuler.
              {% when 'declined' %}
              {% if prenom != blank %}{{ prenom }}, le{% else %}Le{% endif %} paiement de votre commande """ + CMD + """ n'a pas pu être validé&nbsp;: elle a donc été annulée.
              {% when 'fraud' %}
              Votre commande """ + CMD + """ n'a pas pu être validée lors de nos vérifications de sécurité&nbsp;: elle a été annulée.
              {% else %}
              """ + BONJOUR + """ commande """ + CMD + """ a été annulée.
              {% endcase %}""")
        + encart("""                    """ + etiquette('Côté paiement') + """
                    {% if financial_status == 'voided' %}
                    L'autorisation de paiement a été levée&nbsp;: <strong style="color:#111111;">aucun montant n'a été débité</strong>. Une trace temporaire peut rester visible quelques jours sur votre relevé.
                    {% elsif financial_status == 'refunded' %}
                    Votre paiement de <strong style="color:#111111;">{{ total_price | money }}</strong> a été intégralement remboursé sur votre moyen de paiement d'origine. Il apparaît sous 5 à 10 jours ouvrés selon votre banque.
                    {% elsif financial_status == 'partially_refunded' %}
                    Un remboursement a été émis sur votre moyen de paiement d'origine. Il apparaît sous 5 à 10 jours ouvrés selon votre banque.
                    {% elsif financial_status == 'paid' or financial_status == 'partially_paid' %}
                    Votre remboursement est en cours de traitement&nbsp;: vous recevrez un e-mail de confirmation dès qu'il sera émis.
                    {% else %}
                    Aucun montant n'a été débité pour cette commande.
                    {% endif %}""")
        + """
          {% if cancel_reason == 'declined' %}
          <tr>
            <td class="px" align="center" style="padding:16px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              Vous pouvez repasser commande avec un autre moyen de paiement&nbsp;: vos articles vous attendent.
            </td>
          </tr>
          {% elsif cancel_reason == 'fraud' %}
          <tr>
            <td class="px" align="center" style="padding:16px 52px 0; font-family:§F; font-size:13px; line-height:1.6; color:#666666;">
              S'il s'agit d'une erreur, répondez simplement à cet e-mail&nbsp;: nous regarderons cela avec vous.
            </td>
          </tr>
          {% endif %}
"""
        + bouton('{{ shop.url }}', "{% if cancel_reason == 'declined' %}Repasser commande{% else %}Retourner à la boutique{% endif %}")
        + FILET
        + titre_section("Articles annulés")
        + articles('commande')
        + pied(rassurance=False))


# ================================================================ 07 — mise a jour du suivi
def mise_a_jour_suivi():
    return (
        tete('Mise à jour du suivi', "Les informations de suivi de votre commande {{ name }} ont été mises à jour.").replace('[[PRELUDE]]', ENVOI)
        + hero('Suivi mis à jour', "Du nouveau sur votre colis.",
               BONJOUR + """ commande """ + CMD + """ est toujours en chemin&nbsp;: {% if fulfillment.tracking_numbers.size > 0 %}ses informations de suivi viennent d'être mises à jour. Utilisez désormais {% if fulfillment.tracking_numbers.size > 1 %}les numéros{% else %}le numéro{% endif %} ci-dessous.{% else %}son expédition vient d'être mise à jour.{% endif %}""")
        + bloc_suivi()
        + bouton('{{ lien_suivi }}', 'Suivre mon colis')
        + NOTE_COLIS
        + """
          <tr>
            <td class="px" align="center" style="padding:14px 52px 0; font-family:§F; font-size:12px; line-height:1.6; color:#999999;">
              Un nouveau numéro peut mettre 24 à 48&nbsp;h à s'activer chez le transporteur. Vous n'avez rien à faire de votre côté.
            </td>
          </tr>
"""
        + FILET
        + titre_section("Dans ce colis")
        + articles('envoi', prix=False)
        + ADRESSE_LIVRAISON
        + pied())


# ================================================================ 08 — facture / commande en attente
def facture_en_attente():
    prelude = ("{%- assign lien_paiement = checkout_payment_collection_url | default: invoice_url | default: order_status_url -%}\n"
               "{%- assign reste_du = total_outstanding | default: total_price -%}\n"
               "{%- assign echeance = payment_terms.next_payment.due_at | default: payment_terms.payment_schedules.first.due_at -%}\n")
    return (
        tete('Votre commande vous attend', "Finalisez le paiement de votre commande {{ name }} : {{ reste_du | money }}.").replace('[[PRELUDE]]', prelude)
        + hero('Commande en attente de paiement', "Il ne manque plus que vous.",
               """{% if custom_message != blank %}
              {{ custom_message }}
              {% else %}
              """ + BONJOUR + """ commande """ + CMD + """ est prête. Il ne reste qu'à régler son montant pour que nous lancions sa préparation.
              {% endif %}""")
        + """
          <tr>
            <td class="px" style="padding:24px 48px 0;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#F7F3EC; border-radius:14px;">
                <tr>
                  <td align="center" style="padding:24px 22px 8px; font-family:§F; font-size:11px; font-weight:600; letter-spacing:1.5px; color:#666666; text-transform:uppercase;">{% if reste_du < total_price %}Reste à régler{% else %}Montant à régler{% endif %}</td>
                </tr>
                <tr>
                  <td align="center" style="padding:0 22px {% if echeance %}6px{% else %}22px{% endif %}; font-family:§T; font-size:40px; font-weight:600; letter-spacing:-1px; color:#111111;">{{ reste_du | money }}</td>
                </tr>
                {% if echeance %}
                <tr>
                  <td align="center" style="padding:0 22px 22px; font-family:§F; font-size:13px; color:#C05B33; font-weight:600;">À régler avant le """ + date_fr('echeance') + """</td>
                </tr>
                {% endif %}
              </table>
            </td>
          </tr>
"""
        + bouton('{{ lien_paiement }}', 'Régler ma commande')
        + """
          <tr>
            <td class="px" align="center" style="padding:14px 52px 0; font-family:§F; font-size:12px; line-height:1.6; color:#999999;">
              Paiement sécurisé. Vos articles ne sont pas réservés tant que le paiement n'est pas finalisé.<br>
              Vous avez déjà réglé&nbsp;? Ne tenez pas compte de ce message.
            </td>
          </tr>
"""
        + FILET
        + titre_section("Votre commande · {{ nb_articles }} article{% if nb_articles > 1 %}s{% endif %}")
        + articles('commande')
        + TOTAUX
        + ADRESSES
        + pied())


EMAILS = [
    ('01-confirmation-commande.txt', confirmation_commande),
    ('02-confirmation-expedition.txt', confirmation_expedition),
    ('03-commande-en-cours-livraison.txt', en_cours_livraison),
    ('04-commande-livree.txt', commande_livree),
    ('05-confirmation-remboursement.txt', confirmation_remboursement),
    ('06-commande-annulee.txt', commande_annulee),
    ('07-mise-a-jour-suivi.txt', mise_a_jour_suivi),
    ('08-facture-commande-en-attente.txt', facture_en_attente),
]

if __name__ == '__main__':
    os.makedirs(SORTIE, exist_ok=True)
    for nom, fabrique in EMAILS:
        html = fabrique().replace('§F', F).replace('§T', T)
        assert '[[' not in html and '§' not in html, nom
        with open(os.path.join(SORTIE, nom), 'w', encoding='utf-8', newline='\n') as f:
            f.write(html)
        print('%-40s %6d octets' % (nom, len(html.encode('utf-8'))))
