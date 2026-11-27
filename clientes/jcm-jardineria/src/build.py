"""Genera los posts de Instagram (1080x1350) de JCM Jardinería.
Uso: python3 build.py  -> escribe los PNG en ../posts/ (requiere node + playwright)
"""
import pathlib
import json, subprocess

SRC = pathlib.Path(__file__).parent.resolve()
OUT = SRC.parent / "posts"
OUT.mkdir(exist_ok=True)
IMG = (SRC / "img").as_uri()

TEL = "656 951 557"
MAIL = "jcmjardineria@outlook.com"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Playfair+Display:ital,wght@0,600;0,700;1,500&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
:root{--gold:#B8913A;--gold2:#E2C67A;--deep:#1F3A2B;--cream:#FAF6EC;--ink:#1E2420}
body{width:1080px;height:1350px;overflow:hidden;font-family:Montserrat,Inter,sans-serif;color:var(--ink);background:var(--cream)}
.post{position:relative;width:1080px;height:1350px;overflow:hidden}
.goldtxt{background:linear-gradient(100deg,#9C7526,#E6CB80 45%,#A9822F 70%,#D9B865);-webkit-background-clip:text;background-clip:text;color:transparent}
.serif{font-family:'Playfair Display',serif}
.kicker{font-weight:700;letter-spacing:.32em;text-transform:uppercase;font-size:24px;color:var(--gold)}
.foot{position:absolute;left:0;right:0;bottom:0;height:120px;display:flex;align-items:center;justify-content:space-between;padding:0 64px;background:var(--deep);color:#fff}
.foot .tel{font-weight:800;font-size:40px;letter-spacing:.02em}
.foot .tel span{color:var(--gold2)}
.foot .zona{font-size:20px;letter-spacing:.18em;text-transform:uppercase;opacity:.85;text-align:right;line-height:1.5}
.logo{width:150px;height:150px;border-radius:50%;background:#fff url(IMG/logo.jpg) center/102% no-repeat;box-shadow:0 6px 24px rgba(0,0,0,.18)}
.ring{position:absolute;border-radius:50%;border:3px solid var(--gold);opacity:.35}
.tag{display:inline-block;padding:10px 22px;border-radius:40px;font-weight:800;font-size:24px;letter-spacing:.2em;text-transform:uppercase}
""".replace("IMG", IMG)


def foot(zona="Madrid · Sierra de Madrid"):
    return f'<div class="foot"><div class="tel"><span>✆</span> {TEL}</div><div class="zona">{zona}<br>Presupuesto sin compromiso</div></div>'


def antes_despues(n, kicker, titulo, sub, a, b, la="ANTES", lb="DESPUÉS"):
    return n, f"""
<div class="post" style="background:var(--cream)">
  <div style="padding:70px 64px 0;display:flex;justify-content:space-between;align-items:flex-start">
    <div><div class="kicker">{kicker}</div>
      <h1 class="serif" style="font-size:78px;line-height:1.02;margin-top:18px;color:var(--deep)">{titulo}</h1>
      <p style="font-size:28px;margin-top:18px;color:#4a514c;max-width:720px;line-height:1.4">{sub}</p></div>
    <div class="logo" style="flex:none"></div>
  </div>
  <div style="position:absolute;left:64px;right:64px;top:445px;height:745px;display:grid;grid-template-rows:1fr 1fr;gap:14px">
    <div style="position:relative;border-radius:24px;overflow:hidden;background:url({IMG}/{a}) center/cover"><span class="tag" style="position:absolute;left:22px;top:22px;background:rgba(20,20,20,.75);color:#fff">{la}</span></div>
    <div style="position:relative;border-radius:24px;overflow:hidden;background:url({IMG}/{b}) center/cover;outline:5px solid var(--gold);outline-offset:-5px"><span class="tag" style="position:absolute;left:22px;top:22px;background:var(--gold);color:#fff">{lb}</span></div>
  </div>
  {foot()}
</div>"""


POSTS = [
    ("01_presentacion", f"""
<div class="post" style="background:radial-gradient(circle at 50% 38%,#fff 0,#FAF6EC 55%,#EFE6D0 100%)">
  <div class="ring" style="width:1300px;height:1300px;left:-110px;top:-260px"></div>
  <div class="ring" style="width:1500px;height:1500px;left:-210px;top:-360px;opacity:.15"></div>
  <div style="position:absolute;top:150px;left:0;right:0;text-align:center">
    <div class="logo" style="width:330px;height:330px;margin:0 auto"></div>
    <div class="kicker" style="margin-top:60px">Jardinería profesional</div>
    <h1 class="serif" style="font-size:96px;line-height:1.02;margin-top:22px;color:var(--deep)">Tu jardín,<br><i class="goldtxt">en buenas manos</i></h1>
    <p style="font-size:32px;margin:34px auto 0;max-width:800px;line-height:1.45;color:#4a514c">Mantenimiento, podas y recuperación de zonas verdes para particulares y comunidades.</p>
    <div style="display:flex;justify-content:center;gap:16px;margin-top:46px">
      <span class="tag" style="border:2px solid var(--gold);color:var(--gold)">Podas</span>
      <span class="tag" style="border:2px solid var(--gold);color:var(--gold)">Césped</span>
      <span class="tag" style="border:2px solid var(--gold);color:var(--gold)">Setos</span>
      <span class="tag" style="border:2px solid var(--gold);color:var(--gold)">Desbroce</span>
    </div>
  </div>
  {foot()}
</div>"""),
    antes_despues("02_antes_despues_fuente", "Resiembra · Cerceda", "Del barro<br>al verde", "Recuperamos el césped alrededor de la fuente: preparación de tierra, siembra y cuidado.", "fuente_antes.jpg", "fuente_despues.jpg"),
    antes_despues("03_antes_despues_hiedra", "Poda de mantenimiento", "Orden<br>que se nota", "Enredadera recortada y perfilada: más sana, más densa y sin invadir la acera.", "hiedra_antes.jpg", "hiedra_despues.jpg"),
    ("04_servicios", f"""
<div class="post" style="background:var(--deep);color:#fff">
  <div class="ring" style="width:900px;height:900px;right:-420px;top:-380px;opacity:.5"></div>
  <div style="padding:80px 70px 0">
    <div class="kicker" style="color:var(--gold2)">Lo que hacemos</div>
    <h1 class="serif" style="font-size:88px;line-height:1.02;margin-top:18px">Un jardín <i class="goldtxt">cuidado</i><br>todo el año</h1>
  </div>
  <div style="position:absolute;top:420px;left:70px;right:70px;display:grid;grid-template-columns:1fr 1fr;gap:22px">
    {''.join(f'<div style="border:2px solid rgba(226,198,122,.45);border-radius:22px;padding:30px 30px;background:rgba(255,255,255,.04)"><div style="font-size:46px">{i}</div><div style="font-weight:800;font-size:31px;margin-top:12px">{t}</div><div style="font-size:22px;opacity:.8;margin-top:8px;line-height:1.4">{d}</div></div>' for i,t,d in [
      ("✂️","Podas","Árboles, arbustos y frutales en su época."),
      ("🌲","Setos y arizónicas","Recorte, perfilado y saneado."),
      ("🌱","Césped","Siega, resiembra y escarificado."),
      ("🍂","Desbroce","Limpieza de parcelas y zonas verdes."),
      ("🏡","Mantenimiento","Visitas periódicas para casas y comunidades."),
      ("🚛","Retirada de restos","Te lo dejamos todo limpio."),
    ])}
  </div>
  <div class="foot" style="background:var(--gold)"><div class="tel"><span style="color:#fff">✆</span> {TEL}</div><div class="zona">Madrid · Sierra de Madrid<br>Presupuesto sin compromiso</div></div>
</div>"""),
    ("05_consejos_invierno", f"""
<div class="post" style="background:var(--cream)">
  <div style="height:470px;background:linear-gradient(180deg,rgba(31,58,43,.15),rgba(31,58,43,.85)),url({IMG}/arizonica_2.jpg) center 35%/cover;padding:70px 64px;color:#fff;display:flex;flex-direction:column;justify-content:flex-end">
    <div class="kicker" style="color:var(--gold2)">Guarda este post</div>
    <h1 class="serif" style="font-size:80px;line-height:1.02;margin-top:14px">Tu jardín<br>en invierno</h1>
  </div>
  <div style="padding:44px 64px 0">
    {''.join(f'<div style="display:flex;gap:26px;align-items:flex-start;padding:34px 0;border-bottom:2px solid #E6DCC3"><div class="serif goldtxt" style="font-size:72px;font-weight:700;line-height:1;width:74px;flex:none">{n}</div><div><div style="font-weight:800;font-size:34px;color:var(--deep)">{t}</div><div style="font-size:26px;color:#4a514c;margin-top:6px;line-height:1.4">{d}</div></div></div>' for n,t,d in [
      ("1","Poda de árboles de hoja caduca","Con el árbol en reposo, el corte cicatriza mejor."),
      ("2","Riego mínimo","En la sierra, regar con helada daña raíces y césped."),
      ("3","No pises el césped helado","Las hojas se rompen y salen calvas en primavera."),
      ("4","Recoge la hoja","Evita hongos y deja respirar el césped."),
    ])}
  </div>
  {foot()}
</div>"""),
    ("06_comunidades", f"""
<div class="post" style="background:url({IMG}/fuente_despues.jpg) center/cover">
  <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,30,22,.25) 0%,rgba(15,30,22,.92) 60%)"></div>
  <div style="position:absolute;left:64px;right:64px;bottom:190px;color:#fff">
    <div class="kicker" style="color:var(--gold2)">Comunidades de vecinos</div>
    <h1 class="serif" style="font-size:86px;line-height:1.02;margin-top:18px">¿Administras<br>una comunidad?</h1>
    <p style="font-size:30px;margin-top:26px;line-height:1.45;max-width:880px;opacity:.92">Contrato de mantenimiento con visitas fijas, un único interlocutor y zonas comunes siempre presentables.</p>
    <div style="display:flex;gap:16px;margin-top:34px">
      {''.join(f'<span class="tag" style="background:rgba(255,255,255,.12);border:2px solid var(--gold2);color:#fff;font-size:20px;letter-spacing:.12em;white-space:nowrap">{t}</span>' for t in ["Visitas periódicas","Precio cerrado","Sin sorpresas"])}
    </div>
  </div>
  <div class="logo" style="position:absolute;top:60px;right:64px"></div>
  {foot()}
</div>"""),
    ("07_presupuesto", f"""
<div class="post" style="background:radial-gradient(circle at 50% 30%,#2B4D3A 0,#1F3A2B 50%,#152a1f 100%);color:#fff;text-align:center">
  <div class="ring" style="width:1100px;height:1100px;left:-10px;top:-120px;opacity:.45"></div>
  <div style="position:absolute;top:120px;left:0;right:0">
    <div class="logo" style="width:240px;height:240px;margin:0 auto"></div>
    <div class="kicker" style="color:var(--gold2);margin-top:60px">Temporada de podas</div>
    <h1 class="serif" style="font-size:104px;line-height:1;margin-top:20px">Pide tu<br><i class="goldtxt">presupuesto</i></h1>
    <p style="font-size:32px;margin-top:28px;opacity:.9">Gratis y sin compromiso. Vamos, lo vemos y te decimos.</p>
    <div style="margin:60px auto 0;display:inline-block;padding:30px 60px;border-radius:999px;background:linear-gradient(100deg,#9C7526,#E6CB80 50%,#A9822F)">
      <div style="font-weight:800;font-size:76px;color:#1F3A2B;letter-spacing:.02em">✆ {TEL}</div>
    </div>
    <div style="font-size:30px;margin-top:34px;opacity:.9">✉ {MAIL}</div>
    <div style="font-size:22px;margin-top:22px;letter-spacing:.24em;text-transform:uppercase;color:var(--gold2)">WhatsApp · Llamada · Instagram</div>
  </div>
  <div style="position:absolute;bottom:60px;left:0;right:0;font-size:22px;letter-spacing:.24em;text-transform:uppercase;opacity:.7">📍 Madrid · Sierra de Madrid y alrededores</div>
</div>"""),
]

HTML = SRC / "html"
HTML.mkdir(exist_ok=True)
jobs = []
for name, body in POSTS:
    f = HTML / f"{name}.html"
    f.write_text(f"<!doctype html><html><head><meta charset=utf-8><style>{CSS}</style></head><body>{body}</body></html>")
    jobs.append([f.as_uri(), str(OUT / f"{name}.png")])
JS = """
const { chromium } = require('playwright');
(async () => {
  const jobs = JSON.parse(process.argv[1]);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const [u, o] of jobs) {
    await p.goto(u, { waitUntil: 'networkidle' });
    await p.evaluate(() => document.fonts.ready);
    await p.screenshot({ path: o });
    console.log('ok', o.split('/').pop());
  }
  await b.close();
})();
"""
subprocess.run(["node", "-e", JS, json.dumps(jobs)], check=True)
