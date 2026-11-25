#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import math

F = "/tmp/fonts/dejavu-fonts-ttf-2.37/ttf/"
def ft(size, bold=False):
    return ImageFont.truetype(F + ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"), size)

FONTS = {
    "title": ft(30, True), "sub": ft(17),
    "h": ft(22, True),
    "b": ft(15), "bb": ft(15, True),
    "seq": ft(15), "seqb": ft(15, True),
    "seq2": ft(16), "seq2b": ft(16, True),
    "s": ft(12), "sb": ft(12, True),
    "aa": ft(13, True), "sm": ft(13), "leg": ft(14),
}
def f(n): return FONTS[n]

W, H = 1800, 1350
img = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(img)

def txt(xy, s, font="b", fill="#333333", anchor="mm"):
    d.text(xy, s, font=f(font), fill=fill, anchor=anchor)

def fleche(p1, p2, fill="#333333", w=3):
    d.line([p1, p2], fill=fill, width=w)
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    L = 13
    a = (p2[0]-L*math.cos(ang-0.45), p2[1]-L*math.sin(ang-0.45))
    b = (p2[0]-L*math.cos(ang+0.45), p2[1]-L*math.sin(ang+0.45))
    d.polygon([p2, a, b], fill=fill)

ROUGE = "#c0392b"; ROUGEF = "#e02323"; VERTF = "#1b5e20"; VERTC = "#b9e2bb"; GRIS = "#666666"
BLEU1 = "#1565c0"; BLEU2 = "#0d47a1"

# ---------- TITRE ----------
txt((900, 44), "L'expression du patrimoine génétique : de l'ADN à la protéine", "title", "#111111")
txt((900, 82), "Comment la séquence de nucléotides d'un ARNm est-elle convertie en séquence d'acides aminés d'une protéine ?", "sub", "#555555")

# ---------- COMPARTIMENTS ----------
d.rounded_rectangle([30, 115, 990, 1250], radius=22, fill="#eaf2fb", outline="#5b8db8", width=3)
txt((58, 142), "NOYAU", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([1040, 115, 1790, 1250], radius=22, fill="#fdf6ec", outline="#c9a15b", width=3)
txt((1068, 142), "CYTOPLASME", "h", "#9a6d1b", anchor="la")

# enveloppe nucléaire + pore
d.line([998, 120, 998, 1250], fill="#2c5d8a", width=5)
d.line([1012, 120, 1012, 1250], fill="#2c5d8a", width=5)
d.rounded_rectangle([988, 760, 1022, 794], radius=5, fill="#ffffff", outline="#2c5d8a", width=3)
txt((1005, 812), "pore\nnucléaire", "sb", "#2c5d8a")

# ================= ① TRANSCRIPTION =================
txt((58, 180), "① TRANSCRIPTION (ARN polymérase II)", "h", "#2c5d8a", anchor="la")

Y1, Y2 = 285, 320
d.line([80, Y1, 950, Y1], fill=BLEU1, width=5)
d.line([80, Y2, 950, Y2], fill=BLEU2, width=5)
for x in range(105, 945, 17):
    d.line([x, Y1, x, Y2], fill="#9db6cc", width=2)

# séquences (intron = gras)
txt((80, 246), "3' TACG GGA TATCG TATTG CCTAAA GGT ATT 5'   ← brin transcrit (lu 3'→5')", "seq2", BLEU2, anchor="la")
txt((80, 345), "5' ATGC CCT ATAGC ATAAC GGATTT CCA TAA 3'   ← brin non transcrit", "seq2", BLEU1, anchor="la")
# passer les parties en gras au-dessus : on redessine les segments gras
def draw_bold_overlay(line_strings):
    pass
# brin transcrit gras : "GGA", "TATTG", "GGT"
xs = 80
for seg, bold in [("3' ", False), ("TACG ", False), ("GGA ", True), ("TATCG ", False),
                  ("TATTG ", True), ("CCTAAA ", False), ("GGT ", True), ("ATT 5'", False)]:
    d.text((xs, 246), seg, font=f("seq2b" if bold else "seq2"), fill=BLEU2, anchor="lm")
    xs += d.textlength(seg, font=f("seq2b" if bold else "seq2"))
xs = 80
for seg, bold in [("5' ", False), ("ATGC ", False), ("CCT ", True), ("ATAGC ", False),
                  ("ATAAC ", True), ("GGATTT ", False), ("CCA ", True), ("TAA 3'", False)]:
    d.text((xs, 345), seg, font=f("seq2b" if bold else "seq2"), fill=BLEU1, anchor="lm")
    xs += d.textlength(seg, font=f("seq2b" if bold else "seq2"))
txt((80, 382), "en gras = introns (les 3 parties surlignées dans l'énoncé)", "seq2b", GRIS, anchor="la")

txt((82, 258), "↑ promoteur", "sm", "#444444", anchor="lm")
txt((948, 258), "terminaison ↑", "sm", "#444444", anchor="rm")

# ARN polymérase
d.ellipse([420, 255, 560, 350], fill="#8e44ad")
txt((490, 292), "ARN", "bb", "#ffffff")
txt((490, 312), "polymérase II", "bb", "#ffffff")

# nucléotides libres
for (x, y) in [(250, 430), (280, 438), (310, 430), (340, 438)]:
    d.ellipse([x, y, x+26, y+26], fill="#dddddd", outline="#999999", width=2)
txt((295, 478), "ribonucléotides libres", "sm", "#555555")

# ARNpm (intron en gras) : "5' AUGC CCU ATAGC AUAAC GGATTT CCA UAA 3'"
txt((80, 530), "ARNpm (prémessager) synthétisé 5'→3' :", "bb", ROUGE, anchor="la")
cursor = [80]
def mono(seg, y, bold, fill):
    d.text((cursor[0], y), seg, font=f("seq2b" if bold else "seq2"), fill=fill, anchor="lm")
    cursor[0] += d.textlength(seg, font=f("seq2b" if bold else "seq2"))
mono("5' ", 570, False, ROUGE)
mono("AUGC ", 570, False, ROUGE)
mono("CCU ", 570, True, ROUGEF)
mono("ATAGC ", 570, False, ROUGE)
mono("AUAAC ", 570, True, ROUGEF)
mono("GGATTT ", 570, False, ROUGE)
mono("CCA ", 570, True, ROUGEF)
mono("UAA 3'", 570, False, ROUGE)
mono("   ← en gras = introns", 570, False, GRIS)

for i, p in enumerate([
    "Initiation : l'ARN polymérase se fixe sur le promoteur",
    "Élongation : lecture 3'→5' + ajout des nucléotides libres (A↔U, T↔A, G↔C, C↔G)",
    "Terminaison : signal de fin → l'enzyme et l'ARNpm sont libérés",
]):
    txt((95, 620 + 30*i), "• " + p, "b", "#444444", anchor="la")

# ================= ② MATURATION =================
txt((58, 730), "② MATURATION : épissage alternatif", "h", "#2c5d8a", anchor="la")

# 7 segments : E1 Z1 E2 Z2 E3 Z3 E4
segs = [("ATGC", "e"), ("CCT", "i"), ("ATAGC", "e"), ("AUAAC", "i"), ("GGATTT", "e"), ("CCA", "i"), ("UAA", "e")]
widths = {"e": None, "i": None}
xs0 = 80
boxes = []
for s, kind in segs:
    w = d.textlength(("  " + s + "  "), font=f("seq"))
    boxes.append((xs0, kind, s, w))
    xs0 += w + 18
# recentrer dans 80..950
total = boxes[-1][0] + boxes[-1][3] - boxes[0][0]
shift = max(0, (950 - 80 - total) / 2)
boxes = [(a + shift, k, s, w) for (a, k, s, w) in boxes]
for (a, kind, s, w) in boxes:
    if kind == "e":
        d.rounded_rectangle([a, 780, a + w, 816], radius=8, fill=VERTC, outline="#2e7d32", width=2)
        d.text((a + w/2, 798), s, font=f("seq"), fill=VERTF, anchor="mm")
    else:
        d.rounded_rectangle([a, 780, a + w, 816], radius=8, fill="#ffffff", outline=ROUGEF, width=4)
        d.text((a + w/2, 798), s, font=f("seqb"), fill=ROUGEF, anchor="mm")
# arcs au-dessus des introns
for (a, kind, s, w) in boxes:
    if kind == "i":
        d.arc([a, 690, a + w, 810], start=180, end=360, fill="#888888", width=3)
txt((340, 712), "introns excisés", "sm", GRIS)
txt((500, 838), "en gras = introns  |  cases vertes = exons (conservés)", "sm", GRIS)

fleche((620, 880), (740, 880))
txt((680, 860), "épissage", "sb", "#333333")

# ARNm mature
d.rounded_rectangle([80, 925, 950, 961], radius=8, fill=VERTC, outline="#2e7d32", width=2)
txt((515, 943), "5'  AUGC  AUAGC  GGAUUU  UAA  3'", "seq2", VERTF)
txt((515, 905), "ARNm mature — 1 nouvelle molécule (les introns n'y figurent plus)", "bb", ROUGE, anchor="mm")

# ================= ③ MIGRATION =================
txt((58, 1020), "③ MIGRATION", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([150, 1040, 800, 1072], radius=8, fill="#e67e22", outline="#a04000", width=2)
txt((475, 1056), "ARNm mature", "bb", "#ffffff")
fleche((810, 1056), (1030, 1015))
txt((500, 1095), "l'ARNm mature sort du noyau par le pore nucléaire", "b", "#333333")

# ================= ④ TRADUCTION =================
txt((1068, 180), "④ TRADUCTION", "h", "#9a6d1b", anchor="la")

MY = 260
d.line([1070, MY, 1750, MY], fill=ROUGE, width=5)
txt((1070, 238), "5'", "bb", ROUGE, anchor="lm")
txt((1750, 238), "3'", "bb", ROUGE, anchor="lm")
txt((1070, 205), "ARNm mature (arrivé du noyau)", "bb", ROUGE, anchor="la")
codons = [("AUG", 1110), ("CAU", 1175), ("AGC", 1240), ("GGA", 1305), ("UUU", 1370), ("UAA", 1450)]
for cdn, x in codons:
    txt((x, MY + 24), cdn, "bb", "#7d3c00")
txt((1530, MY + 24), "← codon STOP", "sb", ROUGE, anchor="lm")

# ribosome
RX, RY = 1160, 380
d.polygon([(RX, RY), (RX+60, RY-36), (RX+118, RY)], fill="#16a085")
d.rounded_rectangle([RX, RY+2, RX+118, RY+52], radius=10, fill="#1abc9c", outline="#117a65", width=2)
txt((RX+58, 470), "ribosome (grande + petite sous-unité)", "sb", "#117a65")
txt((RX+58, 494), "avance codon par codon, sens 5'→3'", "sm", "#117a65")

# tRNA
def trna(x, anti, aa, colr, ybase):
    d.line([x, ybase-70, x, ybase], fill="#999999", width=2)
    d.rounded_rectangle([x-55, ybase, x+55, ybase+28], radius=6, fill="#ffffff", outline="#27ae60", width=2)
    txt((x, ybase+14), anti, "bb", "#27ae60")
    txt((x, ybase+46), "anticodon", "sm", GRIS)
    d.ellipse([x-26, ybase-118, x+26, ybase-70], fill=colr)
    txt((x, ybase-94), aa, "aa", "#ffffff")
    fleche((x, ybase-66), (x, ybase-14), "#999999", 2)

trna(1110, "UAC", "Met", "#e67e22", 560)
trna(1290, "GUA", "His", "#8e44ad", 650)
trna(1470, "UCG", "Ser", "#27ae60", 560)
txt((1110, 628), "acide aminé porté", "sm", "#555555")
txt((1290, 718), "acide aminé porté", "sm", "#555555")
txt((1470, 628), "acide aminé porté", "sm", "#555555")

# peptide
txt((1070, 800), "chaîne peptidique (liaisons peptidiques) :", "bb", "#333333", anchor="la")
aas = [("Met", 1090), ("His", 1210), ("Ser", 1330), ("Gly", 1450), ("Phe", 1570)]
for a, x in aas:
    d.ellipse([x, 825, x+66, 870], fill="#f39c12")
    txt((x+33, 847), a, "aa", "#ffffff")
for i, (a, x) in enumerate(aas[:-1]):
    fleche((x+68, 847), (x+108, 847), "#333333", 2)

txt((1070, 905), "codon STOP (UAA) : pas de tRNA → fin de la traduction", "sm", GRIS, anchor="la")
txt((1070, 930), "la séquence d'acides aminés se replie en une protéine :", "sm", GRIS, anchor="la")

# protéine
cx, cy2, r = 1140, 1060, 88
d.ellipse([cx-r, cy2-r, cx+r, cy2+r], fill="#9b59b6")
pts = [(cx+int(60*math.cos(math.radians(a))), cy2+int(60*math.sin(math.radians(a)))) for a in range(0, 360, 10)]
for i in range(len(pts)-1):
    d.line([pts[i], pts[i+1]], fill="#6c3483", width=4)
txt((cx, cy2), "PROTÉINE", "h", "#ffffff")
txt((cx, cy2+32), "(repliement)", "sm", "#ffffff")
fleche((1240, 970), (1200, 985), "#333333", 2)

# ---------- LEGENDE ----------
lx, ly = 1400, 985
d.rounded_rectangle([lx, ly, 1780, 1250], radius=12, fill="#ffffff", outline="#333333", width=2)
txt((lx+18, ly+22), "LÉGENDE", "h", "#111111", anchor="la")
yy = ly + 52
def leg_line(colr, x, y, w=44):
    d.line([x, y, x+w, y], fill=colr, width=5)
def leg_ell(colr, x, y, w=22):
    d.ellipse([x, y-10, x+w, y+12], fill=colr)
def leg_box(colr, x, y, w=44, bw=3):
    d.rounded_rectangle([x, y-8, x+w, y+8], radius=5, fill=VERTC, outline=colr, width=bw)
def leg_gras(x, y):
    d.text((x, y), "AUAAC", font=f("leg"), fill="#000000", anchor="lm")

rows = [
    ("line", BLEU1, "ADN (double brin ; brin transcrit lu 3'→5')"),
    ("line", ROUGE, "ARNpm / ARNm (simple brin, 5'→3')"),
    ("ellipse", "#8e44ad", "ARN polymérase II (transcription, noyau)"),
    ("rib", "#1abc9c", "Ribosome (traduction, cytoplasme)"),
    ("trna", "#27ae60", "ARN de transfert (tRNA) : anticodon + aa"),
    ("ellipse", "#f39c12", "Acide aminé (liaisons peptidiques)"),
    ("box", "#2e7d32", "Exon (conservé dans l'ARNm mature)"),
    ("gras", None, "Parties en gras = introns (excisés)"),
]
for kind, colr, label in rows:
    if kind == "line": leg_line(colr, lx+22, yy)
    elif kind == "ellipse": leg_ell(colr, lx+30, yy)
    elif kind == "rib":
        d.polygon([(lx+22, yy+10), (lx+34, yy-6), (lx+46, yy+10)], fill=colr)
        d.rounded_rectangle([lx+22, yy+11, lx+46, yy+23], radius=3, fill=colr)
    elif kind == "trna":
        d.rounded_rectangle([lx+22, yy-9, lx+66, yy+9], radius=4, fill="#ffffff", outline="#27ae60", width=2)
    elif kind == "box": leg_box(colr, lx+22, yy)
    elif kind == "gras": leg_gras(lx+22, yy)
    txt((lx+80, yy), label, "leg", "#333333", anchor="lm")
    yy += 29

yy += 4
txt((lx+22, yy), "Réponse :", "bb", "#111111", anchor="la"); yy += 17
for line in [
    "Chaque codon de 3 nucléotides de l'ARNm est lu par un",
    "tRNA dont l'anticodon complémentaire dépose l'acide",
    "aminé correspondant (code génétique) ; le ribosome relie",
    "les acides aminés entre eux par des liaisons peptidiques :",
    "la séquence de nucléotides devient une séquence",
    "d'acides aminés → protéine Met–His–Ser–Gly–Phe.",
]:
    txt((lx+22, yy), line, "sm", "#555555", anchor="la"); yy += 16

img.save("/workspace/schema_bilan_expression_genetique.png")
print("saved")
