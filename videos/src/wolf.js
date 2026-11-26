// Shared "talking wolf" short. Each page defines CFG before loading this file.
// CFG = { n, rule, icon:[cx,cy], lines:[[start,end,text,pos]], next }
const DUR = 16;
document.getElementById('stage').innerHTML = `
  <img id="img" src="${CFG.frames}/0000.jpg" style="position:absolute;left:0;top:0;width:1080px;height:1080px;transform-origin:0 0">
  <div id="snow" style="position:absolute;inset:0;pointer-events:none"></div><div id="eyeL" class="eye"></div><div id="eyeR" class="eye"></div>
  <div id="gb" style="position:absolute;left:0;right:0;bottom:0;height:900px;background:linear-gradient(to top,rgba(0,0,0,.97) 45%,transparent)"></div>
  <div id="gt" style="position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(to bottom,rgba(0,0,0,.95) 35%,transparent);opacity:0"></div>
  <div id="tag" class="osw" style="position:absolute;left:70px;top:230px;font-size:28px;letter-spacing:8px;color:#bbb">REGLA ${CFG.n} DE 3</div>
  <div id="sub" style="position:absolute;left:70px;right:70px;text-align:center">
    <div class="osw red" style="font-size:28px;letter-spacing:10px;font-weight:600;margin-bottom:14px">🐺 EL LOBO</div>
    <div id="txt" class="anton" style="font-size:88px;line-height:1.02;text-transform:uppercase"></div></div>
  <div id="big" class="abs anton" style="font-size:250px;opacity:0">${CFG.rule}</div>
  <div id="end" style="position:absolute;inset:0;background:rgba(0,0,0,.93);opacity:0">
    <img src="a/v_alpha.png" style="position:absolute;left:50%;top:560px;width:380px;transform:translateX(-50%)">
    <div class="abs osw" style="top:930px;font-size:34px;letter-spacing:12px;color:#bbb">REGLA ${CFG.n}</div>
    <div class="abs anton" style="top:985px;font-size:200px">${CFG.rule}</div>
    <div id="nx" class="abs osw red" style="top:1250px;font-size:36px;letter-spacing:8px;font-weight:600">${CFG.next}</div>
    <div class="handle">@DAVAICOMBATSPORTS</div>
  </div>
  <div id="flash"></div><div id="grain"></div>`;
// camera: [t, cx, cy, scale, screenY]
const W = [540, 235], I = CFG.icon;
const K = [[0, W[0], W[1], 2.45, 470], [5.2, W[0], W[1] + 15, 2.2, 470],
           [6.2, I[0], I[1], 2.25, 1260], [12.6, I[0], I[1] - 10, 2.05, 1260], [16, I[0], I[1] - 10, 2.05, 1260]];
function cam(t) {
  for (let i = 0; i < K.length - 1; i++) { const a = K[i], b = K[i + 1];
    if (t <= b[0]) { let x = cl((t - a[0]) / (b[0] - a[0]));
      if (i === 1) x = x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
      return a.slice(1).map((v, j) => lerp(v, b[j + 1], x)); } }
  return K[K.length - 1].slice(1);
}
// deterministic snow
const FL = []; { let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  for (let i = 0; i < 140; i++) FL.push({ x: rnd() * 1080, y: rnd() * 1920, r: 2 + rnd() * 6, v: 60 + rnd() * 160, w: rnd() * 6.28, o: .25 + rnd() * .6 }); }
$('snow').innerHTML = FL.map(() => '<i style="position:absolute;border-radius:50%;background:#fff"></i>').join('');
const flakes = [...document.querySelectorAll('#snow i')];
async function render(t) {
  const fr = Math.min(479, Math.round(t * 30));
  const im = $('img'), want = `${CFG.frames}/${String(fr).padStart(4, '0')}.jpg`;
  if (!im.src.endsWith(want)) { im.src = want; await im.decode(); }
  flakes.forEach((el, i) => { const f = FL[i]; const y = (f.y + t * f.v) % 1960 - 20, x = f.x + Math.sin(t * 1.3 + f.w) * 25;
    st(el, { left: x + 'px', top: y + 'px', width: f.r + 'px', height: f.r + 'px', opacity: f.o, filter: f.r > 6 ? 'blur(2px)' : 'none' }); });
  const [cx, cy, s, sy] = cam(t);
  const tx = 540 - cx * s, ty = sy - cy * s;
  st('img', { transform: `translate(${tx}px,${ty}px) scale(${s})` });
  // eyes glow while the wolf "speaks"
  const speaking = CFG.lines.some(l => t > l[0] && t < l[1]);
  const pulse = speaking ? .55 + .45 * Math.abs(Math.sin(t * 6)) : .25;
  [['eyeL', 487, 197], ['eyeR', 589, 197]].forEach(([id, ex, ey]) =>
    st(id, { left: `${tx + ex * s - 70}px`, top: `${ty + ey * s - 70}px`, opacity: (pulse * (1 - prog(t, 5.6, .5))).toFixed(3) }));
  const icon = prog(t, 5.6, .6);
  st('gb', { opacity: 1 - icon }); st('gt', { opacity: icon });
  // subtitles: typewriter
  let shown = '', pos = 'bottom';
  CFG.lines.forEach(([a, b, txt, p]) => { if (t >= a && t < b) {
    const n = Math.floor(cl((t - a) / Math.min(1.1, (b - a) * .55)) * txt.length);
    shown = txt.slice(0, n).replace(/\*(.*?)(\*|$)/g, '<span class="red">$1</span>'); pos = p || 'bottom'; } });
  $('txt').innerHTML = shown;
  st('sub', { top: pos === 'top' ? '300px' : '1420px', opacity: shown ? 1 : 0 });
  // rule title slam during the camera move
  const bg = eb(prog(t, 5.9, .35));
  st('big', { top: '330px', opacity: (cl(bg * 1.5) * (1 - prog(t, 7.6, .3))).toFixed(3), transform: `scale(${lerp(2, 1, cl(bg))})` });
  const [kx, ky] = shake(t, 5.95, .35, 18); $('big').style.transform += ` translate(${kx}px,${ky}px)`;
  st('flash', { opacity: (win(t, 5.92, 6.1, .05) * .18).toFixed(3) });
  st('tag', { opacity: (1 - prog(t, 12.6, .3)) * eo(prog(t, .3, .5)) });
  // end card
  st('end', { opacity: eo(prog(t, 12.8, .5)) });
  st('nx', { opacity: eo(prog(t, 13.8, .5)) * (CFG.next ? 1 : 0) });
  grain(t);
}
