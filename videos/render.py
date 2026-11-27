"""Render DAVAI comic videos (Reel 9:16, Feed 4:5, Teaser 9:16) from src/comic.png.

Usage: python3 render.py [reel|feed|teaser|all]
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "comic.png"
OUT = ROOT
FPS = 30
XF = 0.35  # crossfade seconds

FONT_BLACK = "/usr/share/fonts/opentype/inter/InterDisplay-Black.otf"
FONT_BOLD = "/usr/share/fonts/opentype/inter/InterDisplay-ExtraBold.otf"
RED = (214, 30, 36)
WHITE = (245, 245, 245)

COMIC = Image.open(SRC).convert("RGB")
BOXES = {
    "logo": (8, 12, 264, 165),
    "header": (0, 0, 268, 323),
    "p1": (272, 0, 706, 323),
    "p2": (708, 0, 1254, 323),
    "p3": (0, 327, 671, 613),
    "p4": (673, 327, 1254, 613),
    "p5": (138, 615, 671, 906),
    "p6": (674, 615, 1254, 906),
    "p7": (0, 908, 1254, 1125),
    "foot": (0, 1125, 1254, 1254),
}
UP = 3  # pre-upscale factor for smoother sub-pixel crops
CROPS = {}


def crop(name):
    if name not in CROPS:
        im = COMIC.crop(BOXES[name])
        CROPS[name] = im.resize((im.width * UP, im.height * UP), Image.LANCZOS)
    return CROPS[name]


def font(path, size):
    return ImageFont.truetype(path, size)


def ease(x):
    x = max(0.0, min(1.0, x))
    return x * x * (3 - 2 * x)


# ---------- segment definitions ----------
# kind "panel": src, caption, dur, zoom (start, end) and focus (fx0,fy0)->(fx1,fy1) in 0..1
STORY = [
    dict(kind="intro", dur=2.6),
    dict(kind="panel", src="p1", dur=4.2, cap=["MÁS QUE PELEAR,", "UNA FORMA DE VIDA"], z=(1.0, 1.10), f=((0.5, 0.5), (0.55, 0.4))),
    dict(kind="panel", src="p2", dur=4.2, cap=["PEQUEÑOS PASOS,", "GRANDES GUERREROS"], z=(1.0, 1.10), f=((0.5, 0.5), (0.45, 0.45))),
    dict(kind="panel", src="p3", dur=4.2, cap=["ENTRENA. APRENDE.", "SUPÉRATE."], z=(1.0, 1.10), f=((0.5, 0.5), (0.6, 0.45))),
    dict(kind="panel", src="p4", dur=4.2, cap=["MENTE · CUERPO", "ESTRATEGIA"], z=(1.0, 1.10), f=((0.5, 0.5), (0.45, 0.5))),
    dict(kind="panel", src="p5", dur=4.2, cap=["SALUD · EQUILIBRIO", "CONSTANCIA"], z=(1.0, 1.10), f=((0.5, 0.5), (0.55, 0.45))),
    dict(kind="panel", src="p6", dur=4.2, cap=["DISCIPLINA HOY,", "UN MEJOR MAÑANA"], z=(1.0, 1.10), f=((0.5, 0.5), (0.5, 0.45))),
    dict(kind="panel", src="p7", dur=5.6, cap=["PEQUEÑOS GUERREROS,", "GRANDES HISTORIAS"], z=(1.0, 1.0), f=((0.33, 0.5), (0.61, 0.5))),
    dict(kind="outro", dur=3.4),
]
TEASER = [
    dict(kind="intro", dur=2.2),
    dict(kind="panel", src="p2", dur=3.6, cap=["PEQUEÑOS PASOS,", "GRANDES GUERREROS"], z=(1.0, 1.12), f=((0.5, 0.5), (0.45, 0.45))),
    dict(kind="panel", src="p4", dur=3.6, cap=["MENTE · CUERPO", "ESTRATEGIA"], z=(1.0, 1.12), f=((0.5, 0.5), (0.45, 0.5))),
    dict(kind="panel", src="p7", dur=5.0, cap=["PEQUEÑOS GUERREROS,", "GRANDES HISTORIAS"], z=(1.0, 1.0), f=((0.33, 0.5), (0.61, 0.5))),
    dict(kind="outro", dur=3.0),
]


class Layout:
    def __init__(self, W, H):
        self.W, self.H = W, H
        tall = H / W > 1.5
        self.margin = 40
        self.logo_w = 460 if tall else 340
        self.logo_y = 120 if tall else 50
        self.panel_top = 420 if tall else 260
        self.max_panel_h = 900 if tall else 720
        self.cap_size = 74 if tall else 60
        self.footer_y = H - (150 if tall else 80)


def text_center(draw, cx, y, text, fnt, fill, spacing=0):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return w


def footer_layer(L):
    layer = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = font(FONT_BOLD, 34)
    parts = [("HONOR", WHITE), ("  ·  ", WHITE), ("VALOR", RED), ("  ·  ", WHITE), ("RESPETO", WHITE)]
    total = sum(d.textlength(p, font=f) for p, _ in parts)
    x = (L.W - total) / 2
    for p, c in parts:
        d.text((x, L.footer_y), p, font=f, fill=c)
        x += d.textlength(p, font=f)
    return layer


def logo_img(width):
    lg = crop("logo")
    h = int(lg.height * width / lg.width)
    return lg.resize((width, h), Image.LANCZOS)


def make_bg(L, src):
    im = COMIC.crop(BOXES[src])
    s = max(L.W / im.width, L.H / im.height)
    im = im.resize((int(im.width * s) + 2, int(im.height * s) + 2), Image.BILINEAR)
    x = (im.width - L.W) // 2
    y = (im.height - L.H) // 2
    im = im.crop((x, y, x + L.W, y + L.H)).filter(ImageFilter.GaussianBlur(40))
    dark = Image.new("RGB", (L.W, L.H), (0, 0, 0))
    im = Image.blend(im, dark, 0.62)
    # vignette
    vig = Image.new("L", (L.W, L.H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse((-L.W * 0.4, -L.H * 0.2, L.W * 1.4, L.H * 1.2), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    return Image.composite(im, dark, vig)


class Renderer:
    def __init__(self, L, segs):
        self.L = L
        self.segs = segs
        self.footer = footer_layer(L)
        self.logo = logo_img(L.logo_w)
        self.bgs = {}
        self.capfont = font(FONT_BLACK, L.cap_size)

    def bg(self, src):
        if src not in self.bgs:
            self.bgs[src] = make_bg(self.L, src)
        return self.bgs[src]

    # ---- segment frames ----
    def frame_intro(self, t, dur):
        L = self.L
        im = Image.new("RGB", (L.W, L.H), (8, 8, 8))
        # red slash
        d = ImageDraw.Draw(im)
        p = ease(t / 0.6)
        cx, cy = L.W / 2, L.H / 2
        lw = int(L.W * 0.7 * p)
        d.rectangle((cx - lw / 2, cy + 165, cx + lw / 2, cy + 175), fill=RED)
        # logo zoom-in
        s = 0.8 + 0.2 * ease(t / 0.8) + 0.03 * (t / dur)
        lw2 = int(min(L.W - 120, 720) * s)
        lg = logo_img(lw2)
        a = ease(t / 0.5)
        lg_rgba = lg.convert("RGBA")
        lg_rgba.putalpha(int(255 * a))
        im.paste(lg_rgba, (int(cx - lg.width / 2), int(cy - lg.height / 2 - 110)), lg_rgba)
        # tagline
        a2 = ease((t - 0.7) / 0.5)
        if a2 > 0:
            layer = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
            dl = ImageDraw.Draw(layer)
            f = font(FONT_BLACK, 58)
            off = int(30 * (1 - a2))
            text_center(dl, cx, cy + 215 + off, "MÁS QUE UN DEPORTE,", f, WHITE + (int(255 * a2),))
            text_center(dl, cx, cy + 285 + off, "UNA MEJOR VERSIÓN DE TI", f, RED + (int(255 * a2),))
            im.paste(layer, (0, 0), layer)
        return im

    def frame_outro(self, t, dur):
        L = self.L
        im = Image.new("RGB", (L.W, L.H), (8, 8, 8))
        cx, cy = L.W / 2, L.H / 2
        a = ease(t / 0.5)
        s = 1.0 + 0.04 * (t / dur)
        lg = logo_img(int(min(L.W - 120, 760) * s)).convert("RGBA")
        lg.putalpha(int(255 * a))
        im.paste(lg, (int(cx - lg.width / 2), int(cy - lg.height - 60)), lg)
        layer = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        a2 = ease((t - 0.4) / 0.5)
        f1 = font(FONT_BLACK, 66)
        f2 = font(FONT_BOLD, 40)
        text_center(d, cx, cy + 20, "UN ESTILO DE VIDA", f1, WHITE + (int(255 * a2),))
        text_center(d, cx, cy + 110, "EST. 2026", f2, (170, 170, 170, int(255 * a2)))
        a3 = ease((t - 1.0) / 0.5)
        if a3 > 0:
            bw, bh = 640, 96
            y0 = cy + 230 + int(20 * (1 - a3))
            d.rounded_rectangle((cx - bw / 2, y0, cx + bw / 2, y0 + bh), radius=48, fill=RED + (int(255 * a3),))
            text_center(d, cx, y0 + 22, "SÍGUENOS · ACTIVA NOTIS", font(FONT_BLACK, 44), WHITE + (int(255 * a3),))
        im.paste(layer, (0, 0), layer)
        im.paste(self.footer, (0, 0), self.footer)
        return im

    def frame_panel(self, seg, t, dur):
        L = self.L
        im = self.bg(seg["src"]).copy()
        src = crop(seg["src"])
        sw, sh = src.size
        # panel frame size
        pw = L.W - 2 * L.margin
        if seg["src"] == "p7":
            ph = int(pw * 0.5)
        else:
            ph = int(pw * sh / sw)
            if ph > L.max_panel_h:
                ph = L.max_panel_h
        aspect = pw / ph
        p = ease(t / dur)
        z = seg["z"][0] + (seg["z"][1] - seg["z"][0]) * p
        (fx0, fy0), (fx1, fy1) = seg["f"]
        fx = fx0 + (fx1 - fx0) * p
        fy = fy0 + (fy1 - fy0) * p
        # crop box with aspect of frame, as large as possible / z
        if sw / sh > aspect:
            ch = sh / z
            cw = ch * aspect
        else:
            cw = sw / z
            ch = cw / aspect
        x0 = min(max(fx * sw - cw / 2, 0), sw - cw)
        y0 = min(max(fy * sh - ch / 2, 0), sh - ch)
        panel = src.resize((pw, ph), Image.BICUBIC, box=(x0, y0, x0 + cw, y0 + ch))
        # entrance: slide up + fade
        a = ease(t / 0.45)
        py = L.panel_top + int(40 * (1 - a))
        if seg["src"] != "p7":
            py += max(0, (L.max_panel_h - ph) // 2)
        px = L.margin
        border = Image.new("RGB", (pw + 8, ph + 8), WHITE)
        shadow = Image.new("RGBA", (pw + 60, ph + 60), (0, 0, 0, 0))
        ImageDraw.Draw(shadow).rectangle((30, 40, pw + 30, ph + 40), fill=(0, 0, 0, 170))
        shadow = shadow.filter(ImageFilter.GaussianBlur(18))
        im.paste(shadow, (px - 30, py - 30), shadow)
        im.paste(border, (px - 4, py - 4))
        im.paste(panel, (px, py))
        # logo top
        im.paste(self.logo, ((L.W - self.logo.width) // 2, L.logo_y), self.logo.convert("RGBA"))
        # caption
        layer = Image.new("RGBA", (L.W, L.H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        ca = ease((t - 0.35) / 0.45)
        if ca > 0:
            cy = (py + ph + 70 if seg["src"] != "p7" else L.panel_top + int(pw * 0.5) + 90) + int(30 * (1 - ca))
            if L.H / L.W <= 1.5:
                cy = min(cy, L.footer_y - 2 * (L.cap_size + 14) - 50)
            lh = L.cap_size + 14
            for i, line in enumerate(seg["cap"]):
                col = WHITE if i == 0 else RED
                text_center(d, L.W / 2, cy + i * lh, line, self.capfont, col + (int(255 * ca),))
            # underline
            uw = int(260 * ease((t - 0.6) / 0.4))
            if uw > 0:
                uy = cy + len(seg["cap"]) * lh + 18
                d.rectangle((L.W / 2 - uw, uy, L.W / 2 + uw, uy + 8), fill=RED + (int(255 * ca),))
        im.paste(layer, (0, 0), layer)
        im.paste(self.footer, (0, 0), self.footer)
        return im

    def seg_frame(self, i, t):
        seg = self.segs[i]
        dur = seg["dur"]
        if seg["kind"] == "intro":
            return self.frame_intro(t, dur)
        if seg["kind"] == "outro":
            return self.frame_outro(t, dur)
        return self.frame_panel(seg, t, dur)

    def total(self):
        return sum(s["dur"] for s in self.segs)

    def frame(self, T):
        start = 0.0
        for i, seg in enumerate(self.segs):
            end = start + seg["dur"]
            if T < end or i == len(self.segs) - 1:
                t = T - start
                cur = self.seg_frame(i, t)
                if i + 1 < len(self.segs) and end - T < XF:
                    nxt = self.seg_frame(i + 1, 0.0 + (XF - (end - T)) * 0.0)
                    cur = Image.blend(cur, nxt, 1 - (end - T) / XF)
                # final fade to black
                if i == len(self.segs) - 1 and seg["dur"] - t < 0.4:
                    cur = Image.blend(cur, Image.new("RGB", cur.size, 0), 1 - (seg["dur"] - t) / 0.4)
                return cur
            start = end


def render(name, W, H, segs):
    L = Layout(W, H)
    R = Renderer(L, segs)
    n = int(R.total() * FPS)
    out = OUT / f"davai_{name}.mp4"
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-shortest", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", str(out),
    ]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for k in range(n):
        p.stdin.write(R.frame(k / FPS).tobytes())
    p.stdin.close()
    p.wait()
    # poster frame
    R.frame(R.segs[0]["dur"] + 2.0).save(OUT / f"davai_{name}_portada.jpg", quality=92)
    print(out, f"{R.total():.1f}s")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    jobs = {
        "reel": (1080, 1920, STORY),
        "feed": (1080, 1350, STORY),
        "teaser": (1080, 1920, TEASER),
    }
    for k, (w, h, s) in jobs.items():
        if which in (k, "all"):
            render(k, w, h, s)
