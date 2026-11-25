// Shared helpers: every scene is a pure function of time t (seconds)
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const prog = (t, s, d) => cl((t - s) / d);
const eo = x => 1 - Math.pow(1 - x, 3);            // ease out cubic
const eb = x => { const c = 1.70158; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); }; // back
const lerp = (a, b, x) => a + (b - a) * x;
const $ = id => document.getElementById(id);
function st(el, o) { if (typeof el === 'string') el = $(el); for (const k in o) el.style[k] = o[k]; }
// visible window with fade in/out
function win(t, s, e, f = .15) { return cl(Math.min((t - s) / f, (e - t) / f)); }
// deterministic shake
function shake(t, s, d, amp) { const p = prog(t, s, d); if (p <= 0 || p >= 1) return [0, 0]; const k = (1 - p) * amp; return [Math.sin(t * 97) * k, Math.cos(t * 83) * k]; }
// grain overlay seeded by frame
function grain(t) { const g = $('grain'); if (g) g.style.backgroundPosition = `${(t * 1237) % 300}px ${(t * 877) % 300}px`; }
