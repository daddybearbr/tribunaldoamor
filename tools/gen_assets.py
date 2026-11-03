import sys
from PIL import Image, ImageChops, ImageFilter
src, out = sys.argv[1], sys.argv[2]
base = Image.open(src + '/Base_Quiz.jpg.jpeg').convert('RGB')
viz = Image.open(src + '/Base_Quiz_Visualizacao.jpg.jpeg').convert('RGB')
capa = Image.open(src + '/Capa.jpg.jpeg').convert('RGB')
capav = Image.open(src + '/Capa_Visualizacao.jpg.jpeg').convert('RGB')

# martelo recortado (diferença entre a arte com conteúdo e o fundo limpo)
box = (40, 100, 300, 270)
a = viz.crop(box); b = base.crop(box); th = 18
m = ImageChops.difference(a, b).convert('L').point(lambda v: 0 if v < th else min(255, (v - th) * 6))
m = m.filter(ImageFilter.MaxFilter(3)).filter(ImageFilter.GaussianBlur(1))
a.putalpha(m); a.save(out + '/gavel.png')

# capa do telão: fundo limpo + corações + texto "Aponte a câmera..."
lobby = capa.copy()
for bx in [(90, 100, 340, 360), (200, 770, 1000, 915)]:
    lobby.paste(capav.crop(bx), bx[:2])
lobby.save(out + '/capa.jpg', quality=84, optimize=True, progressive=True)
base.save(out + '/fundo.jpg', quality=84, optimize=True, progressive=True)

c = capa.crop((300, 60, 1500, 700)); c.thumbnail((900, 900))
c.save(out + '/capa-celular.jpg', quality=80, optimize=True, progressive=True)
t = base.crop((0, 0, 1200, 1200)); t.thumbnail((700, 700))
t.save(out + '/fundo-celular.jpg', quality=78, optimize=True, progressive=True)
print('imagens geradas')
