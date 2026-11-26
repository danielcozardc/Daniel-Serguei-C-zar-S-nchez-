# Fake "alive" wolf: breathing, head sway/nod, blinks and muzzle motion via image warping.
import sys, os, math
import numpy as np, cv2
src, outdir, fps, dur = sys.argv[1], sys.argv[2], 30, 16
import json
ENV = json.load(open(sys.argv[3]))['env'] if len(sys.argv) > 3 else None
os.makedirs(outdir, exist_ok=True)
img = cv2.imread(src)
H, W = img.shape[:2]
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)

def gauss(cx, cy, rx, ry):
    return np.exp(-(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)).astype(np.float32)

M_body = gauss(540, 250, 260, 250) * (yy < 480)          # whole wolf above the rock
M_body = cv2.GaussianBlur(M_body, (0, 0), 25)
M_head = cv2.GaussianBlur(gauss(540, 230, 190, 175), (0, 0), 15)
M_mouth = gauss(537, 345, 60, 22) * (yy > 322)
M_mouth = cv2.GaussianBlur(M_mouth.astype(np.float32), (0, 0), 6)
EYES = [(487, 197), (589, 197)]
M_eye = sum(gauss(ex, ey - 2, 20, 11) for ex, ey in EYES)
BLINKS = [1.9, 7.3, 11.1, 14.3]
TALK = [(0.5, 2.7), (2.9, 5.4)]                           # muzzle only visible in close-up

def blink(t):
    for b in BLINKS:
        d = abs(t - b)
        if d < .09: return 1 - d / .09
    return 0.0

for f in range(int(fps * dur)):
    t = f / fps
    dx = np.zeros_like(xx); dy = np.zeros_like(yy)
    # breathing: scale body around the rock line
    s = 0.011 * math.sin(2 * math.pi * t / 3.4)
    dx += (xx - 540) * s * M_body; dy += (yy - 470) * s * M_body
    # head tilt + nod around neck
    a = math.radians(1.4 * math.sin(2 * math.pi * t / 5.0) + 0.5 * math.sin(2 * math.pi * t / 1.9))
    cx, cy = 540, 400
    rx = (xx - cx) * math.cos(a) - (yy - cy) * math.sin(a) + cx
    ry = (xx - cx) * math.sin(a) + (yy - cy) * math.cos(a) + cy
    dx += (rx - xx) * M_head; dy += (ry - yy) * M_head
    dy += 2.5 * math.sin(2 * math.pi * t / 2.6 + 1) * M_head
    dx += 3.0 * math.sin(2 * math.pi * t / 6.0) * M_head
    # muzzle "speaking": pull lower muzzle content down
    m = 0.0
    if ENV is not None:
        if t < 5.7: m = 7.0 * ENV[f]
    else:
        for a0, b0 in TALK:
            if a0 < t < b0: m = 5.5 * abs(math.sin((t - a0) * 7.5))
    dy += m * M_mouth
    # blink: drag fur from above over the eyes
    k = blink(t)
    dy += 13 * k * M_eye
    mapx = (xx - dx).astype(np.float32); mapy = (yy - dy).astype(np.float32)
    # note: sampling at p - offset moves content by +offset
    out = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    cv2.imwrite(os.path.join(outdir, f'{f:04d}.jpg'), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
print('frames', f + 1)
