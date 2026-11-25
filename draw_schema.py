#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

F = "/tmp/fonts/dejavu-fonts-ttf-2.37/ttf/"
FONTS = {
    "t": ImageFont.truetype(F + "DejaVuSans.ttf", 28),      # titre
    "st": ImageFont.truetype(F + "DejaVuSans.ttf", 17),     # sous-titre
    "h": ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 21), # entetes section
    "b": ImageFont.truetype(F + "DejaVuSans.ttf", 15),      # texte
    "s": ImageFont.truetype(F + "DejaVuSans.ttf", 12.5),
    "sb": ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 15),
    "ssb": ImageFont.truetype(F + "DejaVuSans-Bold.ttf", 13),
}
def f(n): return FONTS[n]

W, H = 1800, 1240
img = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(img)

def txt(xy, s, font="b", fill="#333", anchor="mm"):
    d.text(xy, s, font=f(font), fill=fill, anchor=anchor)

def fleche(p1, p2, fill="#333", w=3):
    d.line([p1, p2], fill=fill, width=w)
    import math
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    L = 14
    a = (p2[0]-L*math.cos(ang-0.45), p2[1]-L*math.sin(ang-0.45))
    b = (p2[0]-L*math.cos(ang+0.45), p2[1]-L*math.sin(ang+0.45))
    d.polygon([p2, a, b], fill=fill)

# ---------- TITRE ----------
txt((W/2, 38), "L'expression du patrimoine génétique : de l'ADN à la protéine", "t", "#111")
txt((850, 72), "Comment la séquence de nucléotides d'un ARNm est-elle convertie en séquence d'acides aminés d'une protéine ?", "st", "#555")

# ---------- COMPARTIMENTS ----------
d.rounded_rectangle([30, 95, 900, 1180], radius=22, fill="#eaf2fb", outline="#5b8db8", width=3)
txt((55, 120), "NOYAU", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([950, 95, 1790, 1180], radius=22, fill="#fdf6ec", outline="#c9a15b", width=3)
txt((975, 120), "CYTOPLASME", "h", "#9a6d1b", anchor="la")

# enveloppe nucleaire + pore
d.line([908, 100, 908, 480], fill="#2c5d8a", width=5)
d.line([922, 100, 922, 480], fill="#2c5d8a", width=5)
d.rounded_rectangle([898, 400, 932, 430], radius=5, fill="#ffffff", outline="#2c5d8a", width=3)
txt((916, 448), "pore\nnucléaire", "s", "#2c5d8a")

# ================= 1. TRANSCRIPTION =================
txt((55, 150), "① TRANSCRIPTION (ARN polymérase II)", "h", "#2c5d8a", anchor="la")

# ADN double brin
Y1, Y2 = 200, 232
d.line([70, Y1, 760, Y1], fill="#1565c0", width=5)
d.line([70, Y2, 760, Y2], fill="#0d47a1", width=5)
for x in range(95, 755, 25):
    d.line([x, Y1, x, Y2], fill="#90a4b8", width=2)
txt((70, 172), "ADN (gène : suite de nucléotides A, T, G, C)", "b", "#333", anchor="la")
txt((770, Y1-8), "← brin non transcrit (5'→3')", "s", "#1565c0", anchor="lm")
txt((770, Y2+8), "← brin transcrit (3'→5')", "s", "#0d47a0", anchor="lm")

# ARN polymérase (ellipse) sur l ADN
d.ellipse([350, 182, 480, 252], fill="#8e44ad")
txt((415, 217), "ARN\npolymérase II", "ssb", "white")
fleche((400, 285), (400, 320))
txt((412, 300), "lecture 3'→5', synthèse d'ARN 5'→3'", "b", "#333", anchor="lm")

# ARNm premessager (trait rouge 5'→3')
d.line([100, 340, 500, 340], fill="#c0392b", width=5)
txt((100, 322), "5'", "sb", "#c0392b", anchor="lm")
txt((75, 365), "ARNm prémessager (5'→3') :", "sb", "#c0392b", anchor="la")
txt((75, 388), "AUG CCC  UAU AGC AUA  CGG AUU UCC CAU  AA", "b", "#c0392b", anchor="la")

# 3 phases
phases = [
    "• Initiation : l'ARN polymérase II se fixe sur le promoteur (début du gène)",
    "• Élongation : lecture du brin transcrit 3'→5', ajout des ribonucléotides",
    "   complémentaires (A↔U, T↔A, G↔C, C↔G)",
    "• Terminaison : signal de fin de gène → arrêt, l'enzyme et l'ARN",
    "   prémessager sont libérés",
]
yy = 420
for p in phases:
    txt((75, yy), p, "b", "#444", anchor="la"); yy += 22

# ================= 2. MATURATION =================
txt((55, 545), "② MATURATION : épissage alternatif", "h", "#2c5d8a", anchor="la")

# ARNm premessager : exon - intron - exon
E1, E2, E3 = [80, 575, 320, 600], [330, 575, 465, 600], [475, 575, 750, 600]
for r, fill, outline in [(E1, "#82c785", "#2e7d32"), (E2, "#dddddd", "#888"), (E3, "#82c785", "#2e7d32")]:
    d.rounded_rectangle(r, radius=7, fill=fill, outline=outline, width=2)
txt((200, 587), "exon 1 : AUG CCC", "s", "#1b5e20")
txt((397, 587), "intron : UAU AGC AUA", "s", "#555")
txt((612, 587), "exon 2 : CGG AUU UCC CAU", "s", "#1b5e20")
# boucle d'intron
d.arc([330, 500, 465, 610], start=180, end=360, fill="#888", width=3)
txt((397, 512), "intron (excisé)", "s", "#777")
# ciseaux
d.line([410, 622, 422, 637], fill="#555", width=3); d.line([422, 620, 408, 642], fill="#555", width=3)
fleche((770, 587), (820, 587))
txt((795, 565), "épissage", "s", "#555")

# ARNm matures (2 variantes)
d.rounded_rectangle([60, 660, 260, 684], radius=7, fill="#82c785", outline="#2e7d32", width=2)
d.rounded_rectangle([262, 660, 430, 684], radius=7, fill="#82c785", outline="#2e7d32", width=2)
txt((160, 672), "AUG CCC", "ssb", "#1b5e20")
txt((346, 672), "CGG AUU UCC CAU", "ssb", "#1b5e20")
txt((245, 644), "ARNm mature n°1 (tous les exons, intron excisé)", "ssb", "#c0392b", anchor="ms")

d.rounded_rectangle([60, 715, 190, 739], radius=7, fill="#82c785", outline="#2e7d32", width=2)
d.rounded_rectangle([192, 715, 310, 739], radius=7, fill="#82c785", outline="#2e7d32", width=2)
txt((125, 727), "AUG CCC", "ssb", "#1b5e20")
txt((251, 727), "CGG AUU", "ssb", "#1b5e20")
txt((245, 699), "ARNm mature n°2 (autre combinaison d'exons)", "ssb", "#c0392b", anchor="ms")
txt((330, 727), "→ protéines différentes =", "s", "#555", anchor="lm")
txt((330, 748), "épissage alternatif", "sb", "#555", anchor="lm")

# ================= 3. MIGRATION =================
txt((55, 790), "③ MIGRATION vers le cytoplasme", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([560, 810, 700, 836], radius=8, fill="#e67e22", outline="#a04000", width=2)
txt((630, 823), "ARNm mature", "ssb", "#7d3c00")
fleche((705, 823), (860, 823))
txt((780, 800), "sortie par le pore nucléaire", "s", "#333")

# ================= 4. TRADUCTION =================
txt((975, 155), "④ TRADUCTION", "h", "#9a6d1b", anchor="la")

# ARNm mature horizontal
MY = 210
d.line([975, MY, 1710, MY], fill="#c0392b", width=5)
txt((975, 188), "5'", "sb", "#c0392b", anchor="lm")
txt((1710, 188), "3'", "sb", "#c0392b", anchor="lm")
codons = [("AUG", 1010), ("CCC", 1070), ("CGG", 1130), ("AUU", 1190), ("UCC", 1250), ("CAU", 1310), ("UAA", 1390)]
for c, x in codons:
    txt((x, MY+24), c, "ssb", "#7d3c00")
txt((1445, MY+24), "codon STOP → fin de la traduction", "s", "#555", anchor="lm")

# ribosome (2 sous-unites sur 2e codon)
RX, RY = 1155, 165
d.polygon([(RX, RY+30), (RX+55, RY), (RX+110, RY+30)], fill="#16a085")
d.rounded_rectangle([RX, RY+32, RX+110, RY+75], radius=10, fill="#1abc9c", outline="#117a65", width=2)
txt((RX+55, 268), "ribosome", "sb", "#117a65")
txt((RX+55, 290), "(grande + petite sous-unité)", "s", "#117a65")
txt((RX+55, 112), "avance sur l'ARNm codon", "s", "#117a65")
txt((RX+55, 130), "par codon, sens 5'→3'", "s", "#117a65")

# ARNt : anticodon + acide amine
def draw_trna(x, cod, anti, aa, colr, ybase):
    d.line([x, ybase-40, x, ybase], fill="#999", width=2)
    d.rounded_rectangle([x-42, ybase, x+42, ybase+26], radius=6, fill="#fff", outline="#27ae60", width=2)
    txt((x, ybase+13), anti, "ssb", "#27ae60")
    txt((x, ybase+42), "anticodon ← apparié", "s", "#666")
    txt((x, ybase+58), f"au codon {cod}", "s", "#666")
    d.ellipse([x-24, ybase-80, x+24, ybase-38], fill=colr)
    txt((x, ybase-59), aa, "ssb", "white")
    txt((x, ybase-100), "acide aminé porté", "s", "#555")

draw_trna(1010, "AUG", "UAC", "Met", "#e67e22", 470)
draw_trna(1210, "CCC", "GGG", "Pro", "#8e44ad", 560)
draw_trna(1420, "CGG", "GCC", "Arg", "#27ae60", 650)

# chaine peptidique + liaisons peptidiques
txt((975, 730), "chaîne peptidique (acides aminés reliés par liaisons peptidiques) :", "sb", "#333", anchor="la")
aas = ["Met", "Pro", "Arg", "Ile", "Ser", "His", "(STOP)"]
x = 1000
for i, aa in enumerate(aas):
    if aa == "(STOP)":
        d.rounded_rectangle([x, 760, x+110, 790], radius=8, fill="#eeeeee", outline="#888", width=2)
        txt((x+55, 775), "codon STOP", "ssb", "#888")
        break
    d.ellipse([x, 758, x+80, 800], fill="#f39c12")
    txt((x+40, 779), aa, "ssb", "white")
    if i < len(aas)-2:
        fleche((x+82, 779), (x+115, 779), w=3)
    x += 125
txt((1600, 779), "→ cette séquence", "s", "#555", anchor="lm")

# proteine repliee
import math, random
random.seed(3)
cx, cy, r = 1010, 900, 90
d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#9b59b6")
pts = [(cx+int(70*math.cos(math.radians(a))), cy+int(70*math.sin(math.radians(a)))) for a in range(0, 360, 9)]
for i in range(len(pts)-1):
    d.line([pts[i], pts[i+1]], fill="#6c3483", width=4)
txt((cx, cy), "PROTÉINE", "t", "white")
txt((cx, cy+40), "(repliement de la chaîne, forme 3D fonctionnelle)", "s", "white")

fleche((1500, 800), (1130, 828))

# ---------- LEGENDE ----------
lx, ly = 1200, 830
d.rounded_rectangle([lx, ly, 1780, 1160], radius=12, fill="#ffffff", outline="#333", width=2)
txt((lx+20, ly+28), "LÉGENDE", "h", "#111", anchor="la")
items = [
    ("#1565c0", "rect", "ADN (double brin ; brin transcrit lu 3'→5')"),
    ("#c0392b", "rect", "ARN messager (simple brin, 5'→3')"),
    ("#8e44ad", "ellipse", "ARN polymérase II (transcription)"),
    ("#1abc9c", "rect", "Ribosome (traduction codon par codon)"),
    ("#27ae60", "trna", "ARN de transfert (tRNA) : anticodon + acide aminé"),
    ("#f39c12", "circle", "Acide aminé (reliés par liaisons peptidiques)"),
    ("#82c785", "rect", "Exon (conservé dans l'ARNm mature)"),
    ("#dddddd", "rect", "Intron (excisé lors de l'épissage alternatif)"),
]
yy = ly + 62
for colr, shape, label in items:
    if shape == "rect":
        d.rectangle([lx+22, yy-8, lx+82, yy+8], fill=colr)
    elif shape == "ellipse":
        d.ellipse([lx+22, yy-10, lx+82, yy+12], fill=colr)
    elif shape == "circle":
        d.ellipse([lx+42, yy-11, lx+64, yy+11], fill=colr)
    elif shape == "trna":
        d.rounded_rectangle([lx+32, yy-8, lx+74, yy+8], radius=5, fill="#fff", outline=colr, width=2)
    txt((lx+98, yy), label, "b", "#333", anchor="lm")
    yy += 36

yy += 8
txt((lx+22, yy), "Réponse :", "sb", "#111", anchor="la"); yy += 22
for line in [
    "Chaque codon de 3 nucléotides de l'ARNm est reconnu",
    "par l'anticodon d'un tRNA qui dépose l'acide aminé",
    "correspondant (code génétique). Le ribosome relie",
    "ces acides aminés entre eux par des liaisons",
    "peptidiques : la séquence de nucléotides devient",
    "une séquence d'acides aminés → une protéine.",
]:
    txt((lx+22, yy), line, "b", "#555", anchor="la"); yy += 20

img.save("/workspace/schema_bilan_expression_genetique.png")
print("saved", img.size)
