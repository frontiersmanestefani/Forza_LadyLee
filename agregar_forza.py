#!/usr/bin/env python3
# Agrega las tres secciones nuevas de Forza a templates/index.json
# SIN tocar las secciones que ya estan. Se puede correr varias veces.
import json, re, shutil, sys, collections, os

RUTA = sys.argv[1] if len(sys.argv) > 1 else 'templates/index.json'
OD = collections.OrderedDict
IMG = lambda n: "shopify://shop_images/" + n
MOTOS = "shopify://collections/motocicletas-2-ruedas"

crudo = open(RUTA, encoding='utf-8').read()
cabecera = crudo[:crudo.index('*/') + 2] if crudo.lstrip().startswith('/*') else ''
d = json.loads(re.sub(r'/\*.*?\*/', '', crudo, flags=re.S), object_pairs_hook=OD)

print('--- COMO ESTA AHORA ---')
for i, k in enumerate(d['order']):
    s = d['sections'][k]
    print(f"  {i:2d}  {k:34s} {s.get('type','?'):28s} {'(oculta)' if s.get('disabled') else ''}")

NUEVAS = OD()

NUEVAS['forza_nuestras_motos'] = OD([("type", "forza-nuestras-motos"), ("settings", OD([
    ("background_image", IMG("forza-hero-motos.jpg")),
    ("background_position", "center center"),
    ("logo", IMG("forza-logo.png")), ("logo_white", False),
    ("kicker", "La diferencia"), ("title_top", "Nuestras"), ("title_bottom", "Motos"),
    ("subtitle", "Tu trabajo, tu camino, tu libertad."),
    ("button_label", "Conoce más"), ("button_link", MOTOS),
    ("card_1_title", "Motor Forza"),          ("card_1_text", "12,000 km o 12 meses de garantía."),
    ("card_2_title", "Tablero Digital"),      ("card_2_text", "Tecnología avanzada de seguridad."),
    ("card_3_title", "Foco con Luz Led"),     ("card_3_text", "Diseño y variedad de modelos."),
    ("card_4_title", "Puerto USB"),           ("card_4_text", "Conectividad y practicidad."),
    ("card_5_title", "Disco Delantero"),      ("card_5_text", "Frenado confiable."),
    ("card_6_title", "Barras de Protección"), ("card_6_text", "Pensadas para el día a día."),
    ("accent_color", "#AF190F"), ("overlay_opacity", 91), ("card_opacity", 97),
    ("padding_top", 40), ("padding_bottom", 48),
]))])

def modelo(bid, titulo, uso, foto):
    return (bid, OD([("type", "modelo"), ("settings", OD([
        ("image", IMG(foto)), ("title", titulo), ("tagline", uso),
        ("button_label", "Ver detalles"), ("link", MOTOS), ("new_tab", False)]))]))

NUEVAS['forza_modelos'] = OD([("type", "forza-modelos"),
    ("blocks", OD([
        modelo("modelo_fz150",  "FZ150",  "Trabajo Diario",   "forza-modelo-fz150.jpg"),
        modelo("modelo_fz150a", "FZ150A", "Turismo y Ciudad", "forza-modelo-fz150a.jpg"),
        modelo("modelo_fzx200", "FZX200", "Todo Terreno",     "forza-modelo-fzx200.png"),
    ])),
    ("block_order", ["modelo_fz150", "modelo_fz150a", "modelo_fzx200"]),
    ("settings", OD([
        ("logo", IMG("forza-logo.png")),
        ("title_top", "Tu próxima moto"), ("title_bottom", "Está en Lady Lee"),
        ("subtitle", "Encuentra el modelo ideal para ti y recorre nuevos caminos."),
        ("columns", 3), ("background_color", "#ffffff"), ("heading_color", "#111111"),
        ("text_color", "#2b2b2b"), ("accent_color", "#AF190F"),
        ("corner_red", "#BF4941"), ("corner_gray", "#C5C1C7"), ("corner_scale", 100),
        ("padding_top", 56), ("padding_bottom", 64),
    ]))])

def carta(bid, titulo, texto, foto, grande, enlace):
    return (bid, OD([("type", "carta"), ("settings", OD([
        ("image", IMG(foto)), ("title", titulo), ("text", texto), ("large", grande),
        ("button_label", "Conoce más"), ("link", enlace), ("new_tab", False)]))]))

NUEVAS['forza_productos'] = OD([("type", "forza-productos"),
    ("blocks", OD([
        carta("carta_motos", "Motos Forza", "Tu trabajo, tu camino, tu libertad.",
              "forza-bento-motos.jpg", True, MOTOS),
        carta("carta_accesorios", "Accesorios Forza", "Dale personalidad a tu moto.",
              "forza-bento-accesorios.jpg", False, "/collections/all"),
        carta("carta_bicicletas", "Bicicletas Forza", "Tu trabajo, tu camino, tu libertad.",
              "forza-bento-bicicletas.jpg", False, "/collections/all"),
    ])),
    ("block_order", ["carta_motos", "carta_accesorios", "carta_bicicletas"]),
    ("settings", OD([
        ("logo", IMG("forza-logo.png")), ("logo_white", False),
        ("side_image", IMG("forza-moto-lateral.png")), ("side_height", 70), ("side_shift", 47),
        ("kicker", "Conoce nuestros"), ("title_bottom", "Productos"),
        ("subtitle", "Más que una motocicleta, una compañera en tu camino."),
        ("gradient_from", "#f8f8f8"), ("gradient_to", "#0b0b0b"),
        ("accent_color", "#AF190F"), ("card_overlay", 20),
        ("padding_top", 44), ("padding_bottom", 52),
    ]))])

for k, v in NUEVAS.items():
    d['sections'][k] = v

# las dos viejas se ocultan, no se borran
VIEJAS = {'forza-diferenciales', 'tu_proxima_moto', 'tu-proxima-moto'}
ocultadas = []
for k, s in d['sections'].items():
    if s.get('type') in VIEJAS and k not in NUEVAS:
        s['disabled'] = True
        ocultadas.append(k)

# se colocan despues del banner
BANNER = ('slideshow', 'slide-show', 'image-banner', 'banner', 'hero')
orden = [k for k in d['order'] if k not in NUEVAS]
pos = 0
for i, k in enumerate(orden):
    if d['sections'][k].get('type') in BANNER and not d['sections'][k].get('disabled'):
        pos = i + 1
for n in reversed(list(NUEVAS)):
    orden.insert(pos, n)
d['order'] = orden

shutil.copy(RUTA, RUTA + '.bak')
open(RUTA, 'w', encoding='utf-8').write(cabecera + '\n' + json.dumps(d, indent=2, ensure_ascii=False) + '\n')

print('\n--- COMO QUEDA ---')
for i, k in enumerate(d['order']):
    s = d['sections'][k]
    marca = '  <-- NUEVA' if k in NUEVAS else ''
    print(f"  {i:2d}  {k:34s} {s.get('type','?'):28s} {'(oculta)' if s.get('disabled') else ''}{marca}")
print('\nOcultadas:', ', '.join(ocultadas) if ocultadas else 'ninguna')
print('Respaldo guardado en', RUTA + '.bak')
