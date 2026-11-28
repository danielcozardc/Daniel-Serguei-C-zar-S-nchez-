# CLAUDE.md · Índice del repo

Repo de trabajo de Daniel SERGUEI: contenido de Instagram para su marca **DAVAI Combat Sports** y packs demo para captar clientes (agencia de contenido).

## Cómo hablarle a Daniel
- Español, tono de hermano y de buen rollo, sin tonterías, directo y al grano. Cuando salude: "Daniel SERGUEI". Remate típico: "Davai".

## Estructura

| Ruta | Qué es |
|---|---|
| `instagram/` | Posts de **DAVAI Combat Sports** (01–10, 1080×1350) + `TEXTOS.md` con los textos, el orden de publicación y los hashtags. |
| `clientes/<cliente>/` | Un pack por cliente (real o en prospección). |
| `clientes/jcm-jardineria/` | Demo para **JCM Jardinería** (@jcmjardineria, Sierra de Madrid): 7 posts, textos y mensaje de captación. |

### Plantilla de carpeta de cliente
```
clientes/<cliente>/
  TEXTOS.md        textos de cada post, orden, hashtags, mensaje de captación (DM)
  posts/           PNG finales 1080×1350, numerados 01_, 02_…
  src/build.py     plantillas HTML -> PNG (genera posts/)
  src/img/         fotos y logo del cliente (recortes o originales)
  src/html/        HTML intermedio (ignorado en git)
```

## Flujo para un cliente nuevo ("probamos con un cliente desconocido")
1. Daniel pasa capturas del perfil de Instagram del cliente.
2. Sacar la marca (logo, colores, servicios, zona, contacto) y recortar sus fotos a `src/img/` (quitar los badges del carrusel tipo "1/4").
3. Pack de ~7 posts: presentación · antes/después · servicios · contenido útil y para guardar · nicho rentable · llamada a presupuesto.
4. `TEXTOS.md` con los textos, hashtags locales y un mensaje corto para entrarle al cliente.
5. Avisar: las fotos sacadas de capturas tienen poca resolución (pedir originales) y no se publica nada sin el ok del cliente.

## Generar posts
```
python3 clientes/<cliente>/src/build.py
```
Python escribe el HTML y Playwright en **Node** hace las capturas (el módulo Python `playwright` no está instalado; Chromium ya viene preinstalado). Fuentes de Google Fonts: Montserrat + Playfair Display.

## Git
- Commits en español, con un mensaje corto que diga qué se añade.
- Nada de PR si Daniel no lo pide.
