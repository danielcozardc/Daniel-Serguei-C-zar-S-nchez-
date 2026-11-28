"""Genera la propuesta comercial (PDF A4) para JCM Jardinería.
Uso: python3 propuesta.py  -> ../propuesta/Propuesta_Instagram_JCM_Jardineria.pdf (requiere node + playwright)
"""
import json, pathlib, subprocess

SRC = pathlib.Path(__file__).parent.resolve()
OUT = SRC.parent / "propuesta"
OUT.mkdir(exist_ok=True)
IMG = (SRC / "img").as_uri()
POSTS = (SRC.parent / "posts").as_uri()

# Rellena aquí tus datos de contacto antes de enviar
YO = "Daniel"
MI_TEL = "[tu teléfono]"

CSS = f"""
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap');
@page{{size:A4;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--gold:#B8913A;--gold2:#E2C67A;--deep:#1F3A2B;--cream:#FAF6EC;--ink:#1E2420;--mut:#5a615c;--line:#E6DCC3}}
body{{font-family:Montserrat,sans-serif;color:var(--ink);-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.page{{width:210mm;height:297mm;position:relative;overflow:hidden;background:var(--cream);page-break-after:always;padding:22mm 18mm}}
.page:last-child{{page-break-after:auto}}
.serif{{font-family:'Playfair Display',serif}}
.gold{{background:linear-gradient(100deg,#9C7526,#E6CB80 45%,#A9822F 70%,#D9B865);-webkit-background-clip:text;background-clip:text;color:transparent}}
.k{{font-weight:700;letter-spacing:.28em;text-transform:uppercase;font-size:9pt;color:var(--gold)}}
h2{{font-family:'Playfair Display',serif;font-size:30pt;line-height:1.05;color:var(--deep);margin:6px 0 16px}}
p{{font-size:10.5pt;line-height:1.55;color:var(--mut)}}
.logo{{border-radius:50%;background:#fff url({IMG}/logo.jpg) center/102% no-repeat;box-shadow:0 4px 18px rgba(0,0,0,.15)}}
.foot{{position:absolute;left:18mm;right:18mm;bottom:12mm;display:flex;justify-content:space-between;font-size:8pt;color:#9a9f9b;letter-spacing:.12em;text-transform:uppercase;border-top:1px solid var(--line);padding-top:8px}}
.card{{background:#fff;border:1px solid var(--line);border-radius:14px;padding:16px 18px}}
table{{width:100%;border-collapse:collapse;font-size:9.5pt}}
td,th{{padding:9px 8px;border-bottom:1px solid var(--line);text-align:center}}
td:first-child,th:first-child{{text-align:left;color:var(--ink);font-weight:500}}
th{{font-size:10pt}}
.pro{{background:rgba(184,145,58,.10)}}
.ok{{color:var(--deep);font-weight:800}}
.no{{color:#c5c9c6}}
"""


def foot(n):
    return f'<div class="foot"><span>Propuesta Instagram · JCM Jardinería</span><span>{n} / 4</span></div>'


thumbs = "".join(
    f'<img src="{POSTS}/{f}.png" style="width:100%;border-radius:8px;box-shadow:0 4px 14px rgba(0,0,0,.15)">'
    for f in ["01_presentacion", "02_antes_despues_fuente", "04_servicios", "07_presupuesto"]
)

Y, N = '<span class="ok">✓</span>', '<span class="no">—</span>'
rows = [
    ("Posts al mes", "8", "12", "12"),
    ("Stories", N, "3 por semana", "3 por semana"),
    ("Reels montados con vuestros vídeos", N, "2 al mes", "4 al mes"),
    ("Textos, hashtags y planificación mensual", Y, Y, Y),
    ("Antes/después con vuestras fotos", Y, Y, Y),
    ("Ficha de Google Maps (Google Business)", N, Y, Y),
    ("Responder comentarios y mensajes", N, Y, Y),
    ("Anuncios locales en la Sierra de Madrid*", N, N, Y),
    ("Informe mensual de resultados", Y, Y, Y),
]
tabla = "".join(
    f'<tr><td>{r[0]}</td><td>{r[1]}</td><td class="pro">{r[2]}</td><td>{r[3]}</td></tr>' for r in rows
)

extras = [
    ("Dosier para administradores de fincas", "PDF con trabajos, servicios y contacto para conseguir contratos de comunidades.", "120 €"),
    ("Flyer para buzones", "Diseño listo para imprimir y repartir por urbanizaciones de chalets.", "60 €"),
    ("Web de una página", "Web sencilla con vuestros servicios, fotos, WhatsApp y formulario de presupuesto.", "400 €"),
    ("Plantillas de presupuesto y factura", "Con vuestra marca, editables.", "50 €"),
]

HTML = f"""<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>

<!-- 1 PORTADA -->
<div class="page" style="background:radial-gradient(circle at 50% 35%,#2B4D3A 0,#1F3A2B 55%,#152a1f 100%);color:#fff;text-align:center;padding-top:48mm">
  <div style="position:absolute;width:260mm;height:260mm;border:2px solid var(--gold);border-radius:50%;left:-25mm;top:-40mm;opacity:.35"></div>
  <div class="logo" style="width:62mm;height:62mm;margin:0 auto"></div>
  <div class="k" style="color:var(--gold2);margin-top:22mm">Propuesta de redes sociales</div>
  <h1 class="serif" style="font-size:46pt;line-height:1.02;margin-top:8mm">Más presupuestos<br><i class="gold">desde Instagram</i></h1>
  <p style="color:rgba(255,255,255,.85);font-size:13pt;margin-top:8mm">Para JCM Jardinería · Mantenimiento y podas</p>
  <div style="position:absolute;bottom:22mm;left:0;right:0;font-size:9pt;letter-spacing:.22em;text-transform:uppercase;color:var(--gold2)">Preparada por {YO} · Noviembre 2026</div>
</div>

<!-- 2 SITUACIÓN + DEMO -->
<div class="page">
  <div class="k">Dónde estáis y a dónde vamos</div>
  <h2>Hacéis un trabajo top.<br>Falta que se vea.</h2>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:6px 0 16px">
    <div class="card"><div class="serif gold" style="font-size:28pt;font-weight:700">6</div><p>publicaciones en el perfil</p></div>
    <div class="card"><div class="serif gold" style="font-size:28pt;font-weight:700">59</div><p>seguidores: el perfil aún no trabaja para vosotros</p></div>
    <div class="card"><div class="serif gold" style="font-size:28pt;font-weight:700">&lt;1</div><p>post al mes de media: falta constancia</p></div>
  </div>
  <p><b style="color:var(--deep)">El objetivo no son los likes, son las llamadas.</b> Publicar de forma constante vuestros antes/después, enseñar lo que hacéis y llegar a quien decide: vecinos de la sierra con chalet y <b style="color:var(--deep)">administradores de comunidades</b>, que es donde están los contratos fijos.</p>
  <div class="k" style="margin-top:18px">Así podría verse vuestro perfil</div>
  <p style="margin:4px 0 10px">Muestra hecha con vuestras propias fotos y vuestro logo:</p>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:9px">{thumbs}</div>
  <div class="card" style="margin-top:16px;background:var(--deep);border:none">
    <p style="color:#fff;font-size:11.5pt"><b class="gold" style="font-size:13pt">Las cuentas claras:</b> un solo contrato de mantenimiento de una comunidad os paga el año entero de Instagram.</p>
  </div>
  {foot(2)}
</div>

<!-- 3 PAQUETES -->
<div class="page">
  <div class="k">Paquetes mensuales</div>
  <h2>Elegid el ritmo</h2>
  <div style="display:grid;grid-template-columns:1.5fr 1fr 1fr 1fr;align-items:end;margin-bottom:4px;text-align:center">
    <div></div>
    <div style="padding:10px"><div style="font-weight:800;color:var(--deep)">Básico</div><div class="serif" style="font-size:24pt;color:var(--deep)">150€</div><div style="font-size:8pt;color:var(--mut)">al mes</div></div>
    <div style="padding:12px 10px;background:var(--deep);color:#fff;border-radius:12px 12px 0 0"><div style="font-size:7.5pt;letter-spacing:.2em;color:var(--gold2);font-weight:800">RECOMENDADO</div><div style="font-weight:800">Pro</div><div class="serif gold" style="font-size:28pt;font-weight:700">250€</div><div style="font-size:8pt;opacity:.8">al mes</div></div>
    <div style="padding:10px"><div style="font-weight:800;color:var(--deep)">Completo</div><div class="serif" style="font-size:24pt;color:var(--deep)">400€</div><div style="font-size:8pt;color:var(--mut)">al mes</div></div>
  </div>
  <table>{tabla}</table>
  <p style="font-size:8.5pt;margin-top:8px">* El dinero de los anuncios se paga aparte, directamente a Meta (recomendado desde 3–5 € al día). Precios sin IVA.</p>
  <div class="card" style="margin-top:18px;border:2px solid var(--gold);display:flex;gap:16px;align-items:center">
    <div class="serif gold" style="font-size:34pt;font-weight:700;flex:none">-50%</div>
    <div><div style="font-weight:800;color:var(--deep);font-size:12pt">Oferta de arranque: el primer mes a mitad de precio</div><p>Sin permanencia. Si en un mes no notáis movimiento, lo dejamos sin compromiso.</p></div>
  </div>
  <div class="k" style="margin-top:20px">Cómo trabajamos</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:8px">
    <div class="card"><div style="font-weight:800;color:var(--deep)">1 · Me mandáis fotos</div><p>Por WhatsApp, tal cual las hacéis en el curro: antes y después.</p></div>
    <div class="card"><div style="font-weight:800;color:var(--deep)">2 · Yo lo preparo</div><p>Diseño, textos y calendario. Lo aprobáis de un vistazo.</p></div>
    <div class="card"><div style="font-weight:800;color:var(--deep)">3 · Publicamos y medimos</div><p>Cada mes os paso qué ha funcionado y cuántas consultas ha traído.</p></div>
  </div>
  {foot(3)}
</div>

<!-- 4 EXTRAS + CIERRE -->
<div class="page">
  <div class="k">Extras de pago único</div>
  <h2>Para ir a por más</h2>
  <div style="display:grid;gap:10px">
    {''.join(f'<div class="card" style="display:flex;justify-content:space-between;align-items:center;gap:16px"><div><div style="font-weight:800;color:var(--deep);font-size:11.5pt">{t}</div><p>{d}</p></div><div class="serif" style="font-size:20pt;color:var(--gold);font-weight:700;flex:none">{pr}</div></div>' for t,d,pr in extras)}
  </div>
  <div class="card" style="margin-top:16px;background:rgba(184,145,58,.10);border-color:var(--gold)">
    <div style="font-weight:800;color:var(--deep);font-size:11.5pt">Mi recomendación para vosotros</div>
    <p><b>Pack Pro + dosier para administradores de fincas.</b> Instagram para que os vean los vecinos y el dosier para entrar en comunidades, que es el trabajo fijo y el que más deja.</p>
  </div>
  <div style="margin-top:22px;background:var(--deep);border-radius:16px;padding:22px 24px;color:#fff;display:flex;align-items:center;gap:22px">
    <div class="logo" style="width:30mm;height:30mm;flex:none"></div>
    <div>
      <div class="k" style="color:var(--gold2)">Siguiente paso</div>
      <div class="serif" style="font-size:22pt;margin-top:4px">¿Empezamos este mes?</div>
      <p style="color:rgba(255,255,255,.85);margin-top:6px">Respondedme con el paquete elegido y en una semana tenéis el primer calendario listo.</p>
      <div style="margin-top:10px;font-weight:800;font-size:13pt;color:var(--gold2)">{YO} · {MI_TEL}</div>
    </div>
  </div>
  {foot(4)}
</div>
</body></html>"""

src = SRC / "html" / "propuesta.html"
src.parent.mkdir(exist_ok=True)
src.write_text(HTML)
pdf = OUT / "Propuesta_Instagram_JCM_Jardineria.pdf"
JS = """
const { chromium } = require('playwright');
(async () => {
  const [u, o, png] = JSON.parse(process.argv[1]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto(u, { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: o, format: 'A4', printBackground: true, preferCSSPageSize: true });
  await p.screenshot({ path: png, fullPage: true });
  await b.close();
  console.log('ok', o);
})();
"""
subprocess.run(["node", "-e", JS, json.dumps([src.as_uri(), str(pdf), str(SRC / "html" / "preview.png")])], check=True)
