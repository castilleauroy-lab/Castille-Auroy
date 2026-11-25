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
    "seq": ft(16), "seqb": ft(16, True),
    "seq2": ft(17), "seq2b": ft(17, True),
    "s": ft(12), "sb": ft(12, True),
    "aa": ft(13, True), "sm": ft(13), "leg": ft(14),
}
def f(n): return FONTS[n]

W, H = 1800, 1330
img = Image.new("RGB", (W, H), "#ffffff")
d = ImageDraw.Draw(img)

def txt(xy, s, font="b", fill="#333", anchor="mm"):
    d.text(xy, s, font=f(font), fill=fill, anchor=anchor)

def fleche(p1, p2, fill="#333", w=3):
    d.line([p1, p2], fill=fill, width=w)
    ang = math.atan2(p2[1]-p1[1], p2[0]-p1[0])
    L = 13
    a = (p2[0]-L*math.cos(ang-0.45), p2[1]-L*math.sin(ang-0.45))
    b = (p2[0]-L*math.cos(ang+0.45), p2[1]-L*math.sin(ang+0.45))
    d.polygon([p2, a, b], fill=fill)

# ---------- TITRE ----------
txt((900, 44), "L'expression du patrimoine génétique : de l'ADN à la protéine", "title", "#111")
txt((900, 82), "Comment la séquence de nucléotides d'un ARNm est-elle convertie en séquence d'acides aminés d'une protéine ?", "sub", "#555")

# ---------- COMPARTIMENTS ----------
d.rounded_rectangle([30, 115, 990, 1240], radius=22, fill="#eaf2fb", outline="#5b8db8", width=3)
txt((58, 142), "NOYAU", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([1040, 115, 1790, 1240], radius=22, fill="#fdf6ec", outline="#c9a15b", width=3)
txt((1068, 142), "CYTOPLASME", "h", "#9a6d1b", anchor="la")

# enveloppe nucléaire + pore
d.line([998, 120, 998, 1240], fill="#2c5d8a", width=5)
d.line([1012, 120, 1012, 1240], fill="#2c5d8a", width=5)
d.rounded_rectangle([988, 745, 1022, 779], radius=5, fill="#ffffff", outline="#2c5d8a", width=3)
txt((1005, 798), "pore\nnucléaire", "sb", "#2c5d8a")

# ================= ① TRANSCRIPTION =================
txt((58, 180), "① TRANSCRIPTION (ARN polymérase II)", "h", "#2c5d8a", anchor="la")

# ADN double brin
Y1, Y2 = 285, 320
d.line([80, Y1, 950, Y1], fill="#1565c0", width=5)
d.line([80, Y2, 950, Y2], fill="#0d47a1", width=5)
for x in range(105, 945, 17):
    d.line([x, Y1, x, Y2], fill="#9db6cc", width=2)

# séquences sous les lignes (pas de chevauchement)
txt((80, 246), "3' TACGGGA TATCGTATTGCCTAAAGGTATT 5'   ← brin transcrit (lu 3'→5')", "seq2", "#0d47a0", anchor="la")
txt((80, 345), "5' ATGCCCT ATAGCATA ACGGATTTCCATAA 3'   ← brin non transcrit", "seq2", "#1565c0", anchor="la")
txt((80, 380), "en gras = introns : TATCGTAT (= ATAGCATA sur le brin non transcrit)", "seq2b", GRIS_ := "#666666", anchor="la")

# promoteur / terminaison
txt((82, 258), "↑ promoteur", "sm", "#444", anchor="lm")
txt((948, 258), "terminaison ↑", "sm", "#444", anchor="rm")

# ARN polymérase sur l'ADN
d.ellipse([420, 255, 560, 350], fill="#8e44ad")
txt((490, 292), "ARN", "bb", "white")
txt((490, 312), "polymérase II", "bb", "white")

# nucléotides libres
for i, (x, y) in enumerate([(250, 430), (280, 438), (310, 430), (340, 438)]):
    d.ellipse([x, y, x+26, y+26], fill="#dddddd", outline="#999", width=2)
txt((290, 478), "ribonucléotides libres", "sm", "#555")

# ARNpm néosynthétisé (5'→3'), intron EN GRAS
txt((80, 530), "ARNpm (prémessager) synthétisé 5'→3' :", "bb", "#c0392b", anchor="la")
cursor = [80]
def mono(s, y, font, fill):
    d.text((cursor[0], y), s, font=f(font), fill=fill, anchor="lm")
    cursor[0] += d.textlength(s, font=f(font))
txt((cursor[0], 570), "5'", "sb", "#c0392b", anchor="lm"); cursor[0] += 22
mono("AUG CCC  ", 570, "seq2", "#c0392b")
mono("AUAGCAUA", 570, "seq2b", "#e02323")       # intron EN GRAS
mono("  ACG GAU UUC CAU AA  3'", 570, "seq2", "#c0392b")
mono("   ← parties en gras = intron", 570, "sm", "#666666")

# 3 phases
for i, p in enumerate([
    "Initiation : l'ARN polymérase se fixe sur le promoteur",
    "Élongation : lecture 3'→5' + ajout des nucléotides libres (A↔U, T↔A, G↔C, C↔G)",
    "Terminaison : signal de fin → l'enzyme et l'ARNpm sont libérés",
]):
    txt((95, 620 + 30*i), "• " + p, "b", "#444", anchor="la")

# ================= ② MATURATION =================
txt((58, 730), "② MATURATION : épissage alternatif", "h", "#2c5d8a", anchor="la")

E1 = [80, 780, 300, 816]; E2 = [305, 780, 520, 816]; E3 = [525, 780, 950, 816]
d.rounded_rectangle(E1, radius=8, fill="#b9e2bb", outline="#2e7d32", width=2)
d.rounded_rectangle(E2, radius=8, fill="#ffffff", outline="#e02323", width=4)
d.rounded_rectangle(E3, radius=8, fill="#b9e2bb", outline="#2e7d32", width=2)
txt((190, 798), "AUG CCC", "seq", "#1b5e20")
txt((412, 798), "AUAGCAUA", "seqb", "#e02323")
txt((737, 798), "ACG GAU UUC CAU AA", "seq", "#1b5e20")
d.arc([305, 685, 520, 805], start=180, end=360, fill="#888", width=3)
txt((412, 700), "intron excisé", "sm", "#666666")
txt((190, 838), "exon", "sm", "#2e7d32")
txt((412, 838), "intron", "sb", "#e02323")
txt((737, 838), "exon", "sm", "#2e7d32")

fleche((620, 880), (740, 880))
txt((680, 862), "épissage", "sb", "#333")

# ARNm mature
d.rounded_rectangle([80, 925, 300, 959], radius=8, fill="#b9e2bb", outline="#2e7d32", width=2)
d.rounded_rectangle([300, 925, 950, 959], radius=8, fill="#b9e2bb", outline="#2e7d32", width=2)
txt((190, 942), "AUG CCC", "seq", "#1b5e20")
txt((625, 942), "ACG GAU UUC CAU AA", "seq", "#1b5e20")
txt((515, 905), "ARNm mature — 1 nouvelle molécule (l'intron n'y figure plus)", "bb", "#c0392b", anchor="mm")

# ================= ③ MIGRATION =================
txt((58, 1010), "③ MIGRATION", "h", "#2c5d8a", anchor="la")
d.rounded_rectangle([150, 1030, 800, 1062], radius=8, fill="#e67e22", outline="#a04000", width=2)
txt((475, 1046), "ARNm mature", "bb", "#ffffff")
fleche((810, 1046), (1030, 1000))
txt((500, 1085), "l'ARNm mature sort du noyau par le pore nucléaire", "b", "#333")

# ================= ④ TRADUCTION =================
txt((1068, 180), "④ TRADUCTION", "h", "#9a6d1b", anchor="la")

MY = 260
d.line([1070, MY, 1750, MY], fill="#c0392b", width=5)
txt((1070, 238), "5'", "bb", "#c0392b", anchor="lm")
txt((1750, 238), "3'", "bb", "#c0392b", anchor="lm")
txt((1070, 205), "ARNm mature (arrivé du noyau)", "bb", "#c0392b", anchor="la")
codons = [("AUG", 1115), ("CCC", 1180), ("UAC", 1245), ("GGA", 1310), ("UUU", 1375), ("CCA", 1440), ("UAA", 1520)]
for c, x in codons:
    txt((x, MY + 24), c, "bb", "#7d3c00")
txt((1615, MY + 24), "← codon STOP", "sb", "#c0392b", anchor="lm")

# ribosome sur les 2e-3e codons
RX, RY = 1165, 380
d.polygon([(RX, RY), (RX+60, RY-36), (RX+118, RY)], fill="#16a085")
d.rounded_rectangle([RX, RY+2, RX+118, RY+52], radius=10, fill="#1abc9c", outline="#117a65", width=2)
txt((RX+58, 470), "ribosome (grande + petite sous-unité)", "sb", "#117a65")
txt((RX+58, 494), "avance codon par codon, sens 5'→3'", "sm", "#117a65")

# tRNA (anticodon + aa)
def trna(x, anti, aa, colr, ybase):
    d.line([x, ybase-70, x, ybase], fill="#999", width=2)
    d.rounded_rectangle([x-55, ybase, x+55, ybase+28], radius=6, fill="#fff", outline="#27ae60", width=2)
    txt((x, ybase+14), anti, "bb", "#27ae60")
    txt((x, ybase+46), "anticodon", "sm", "#666666")
    d.ellipse([x-26, ybase-118, x+26, ybase-70], fill=colr)
    txt((x, ybase-94), aa, "aa", "#ffffff")
    fleche((x, ybase-66), (x, ybase-14), "#999999", 2)

trna(1120, "UAC", "Met", "#e67e22", 560)
trna(1300, "GGG", "Pro", "#8e44ad", 650)
trna(1480, "AUG", "Tyr", "#27ae60", 560)
txt((1120, 628), "acide aminé porté", "sm", "#555555")
txt((1300, 718), "acide aminé porté", "sm", "#555555")
txt((1480, 628), "acide aminé porté", "sm", "#555555")

# peptide
txt((1070, 800), "chaîne peptidique (liaisons peptidiques) :", "bb", "#333333", anchor="la")
aas = [("Met", 1090), ("Pro", 1210), ("Tyr", 1330), ("Gly", 1450), ("Phe", 1570), ("Pro", 1690)]
for aa, x in aas:
    d.ellipse([x, 825, x+66, 870], fill="#f39c12")
    txt((x+33, 847), aa, "aa", "#ffffff")
for i, (aa, x) in enumerate(aas[:-1]):
    fleche((x+68, 847), (x+108, 847), "#333333", 2)

txt((1070, 905), "codon STOP (UAA) : pas de tRNA → fin de la traduction", "sm", "#666666", anchor="la")
txt((1070, 930), "la séquence d'acides aminés se replie en une protéine :", "sm", "#666666", anchor="la")

# protéine repliée
cx, cy2, r = 1140, 1040, 90
d.ellipse([cx-r, cy2-r, cx+r, cy2+r], fill="#9b59b6")
pts = [(cx+int(62*math.cos(math.radians(a))), cy2+int(62*math.sin(math.radians(a)))) for a in range(0, 360, 10)]
for i in range(len(pts)-1):
    d.line([pts[i], pts[i+1]], fill="#6c3483", width=4)
txt((cx, cy2), "PROTÉINE", "h", "#ffffff")
txt((cx, cy2+32), "(repliement)", "sm", "#ffffff")
fleche((1240, 955), (1200, 975), "#333333", 2)

# ---------- LEGENDE ----------
lx, ly = 1400, 980
d.rounded_rectangle([lx, ly, 1780, 1240], radius=12, fill="#ffffff", outline="#333333", width=2)
txt((lx+18, ly+22), "LÉGENDE", "h", "#111111", anchor="la")
yy = ly + 52
def leg_line(colr, x, y, w=44):
    d.line([x, y, x+w, y], fill=colr, width=5)
def leg_ell(colr, x, y, w=22):
    d.ellipse([x, y-10, x+w, y+12], fill=colr)
def leg_box(colr, x, y, w=44, h=16, bw=3, fillr="#b9e2bb"):
    d.rounded_rectangle([x, y-8, x+w, y+8], radius=5, fill=fillr, outline=colr, width=bw)
def leg_trna(x, y):
    d.rounded_rectangle([x, y-9, x+44, y+9], radius=4, fill="#fff", outline="#27ae60", width=2)
def leg_dejavu_gras(x, y):
    txt((x, y), "AUAGCAUA", "leg", "#000000", anchor="lm")
    txt((x+118, y), "", "leg", "#000", anchor="lm")

rows = [
    ("line",  "#1565c0", "ADN (double brin ; brin transcrit lu 3'→5')"),
    ("line",  "#c0392b", "ARNpm / ARNm (simple brin, 5'→3')"),
    ("ellipse","#8e44ad", "ARN polymérase II (transcription, noyau)"),
    ("rib",   "#1abc9c", "Ribosome (traduction, cytoplasme)"),
    ("trna",  "#27ae60", "ARN de transfert (tRNA) : anticodon + aa"),
    ("ellipse","#f39c12", "Acide aminé (liaisons peptidiques)"),
    ("box",   "#2e7d32", "Exon (conservé dans l'ARNm mature)"),
    ("gras",  None,      "Parties en gras = introns (excisés)"),
]
for kind, colr, label in rows:
    if kind == "line": leg_line(colr, lx+22, yy)
    elif kind == "ellipse": leg_ell(colr, lx+30, yy)
    elif kind == "rib":
        d.polygon([(lx+22, yy+10), (lx+34, yy-6), (lx+46, yy+10)], fill=colr)
        d.rounded_rectangle([lx+22, yy+11, lx+46, yy+23], radius=3, fill=colr)
    elif kind == "trna": leg_trna(lx+22, yy)
    elif kind == "box": leg_box(colr, lx+22, yy)
    elif kind == "gras": leg_dejavu_gras(lx+22, yy)
    txt((lx+60, yy), label, "leg", "#333333", anchor="lm")
    yy += 29

yy += 4
txt((lx+22, yy), "Réponse :", "bb", "#111111", anchor="la"); yy += 17
for line in [
    "Chaque codon de 3 nucléotides de l'ARNm est lu par un",
    "tRNA dont l'anticodon complémentaire dépose l'acide",
    "aminé correspondant (code génétique) ; le ribosome relie",
    "les acides aminés entre eux par des liaisons peptidiques :",
    "la séquence de nucléotides devient une séquence",
    "d'acides aminés, c'est-à-dire une protéine.",
]:
    txt((lx+22, yy), line, "sm", "#555555", anchor="la"); yy += 16

img.save("/workspace/schema_bilan_expression_genetique.png")
print("saved")
