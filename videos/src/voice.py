# Build the wolf voice-over + ambience for one short and write timings JSON.
# usage: python3 voice.py <name> <model.onnx> "line1" "line2" "RULE" "line3" "line4"
import sys, os, json, subprocess, wave
import numpy as np
name, model = sys.argv[1], sys.argv[2]
L1, L2, RULE, L3, L4 = sys.argv[3:8]
OUT = f'voice_{name}'; os.makedirs(OUT, exist_ok=True)
SR = 44100

def run(cmd, inp=None):
    subprocess.run(cmd, input=inp, check=True, capture_output=True)

def synth(i, text, ls=1.0):
    raw, fx = f'{OUT}/{i}_raw.wav', f'{OUT}/{i}.wav'
    run(['piper', '-m', model, '--length_scale', str(ls), '--sentence_silence', '0.15', '--output_file', raw], text.encode())
    # deep wolf voice: pitch down ~3.5 semitones, slightly slower, bass, compression, mountain echo
    af = ('asetrate=22050*0.82,aresample=44100,atempo=1.12,'
          'equalizer=f=120:t=q:w=1:g=5,equalizer=f=3000:t=q:w=1:g=-3,'
          'acompressor=threshold=-18dB:ratio=3:attack=5:release=120,'
          'aecho=0.8:0.6:90|180:0.22|0.12,highpass=f=60,volume=1.6')
    run(['ffmpeg', '-y', '-v', 'error', '-i', raw, '-af', af, '-ar', str(SR), '-ac', '1', fx])
    with wave.open(fx) as w:
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def fit(i, text, maxdur):
    ls = 1.0
    for _ in range(6):
        a = synth(i, text, ls)
        if len(a) / SR <= maxdur: return a
        ls *= max(.82, maxdur / (len(a) / SR) * .98)
    return a

DUR = 16.0
track = np.zeros(int(SR * DUR), np.float32)
def place(a, t):
    s = int(t * SR); e = min(len(track), s + len(a)); track[s:e] += a[:e - s]
    return t, t + (e - s) / SR

# first half: 0.5 .. 5.5 ; rule word at slam 5.95 ; second half 6.6 .. 12.6
a1 = fit(1, L1, 2.3); a2 = fit(2, L2, 5.5 - 0.5 - len(a1) / SR - .25)
t1 = place(a1, .5); t2 = place(a2, t1[1] + .25)
ar = synth(0, RULE, 1.05); tr = place(ar * 1.15, 5.95)
start3 = max(6.6, tr[1] + .1)
a3 = fit(3, L3, 3.2); t3 = place(a3, start3)
a4 = fit(4, L4, 12.6 - t3[1] - .3); t4 = place(a4, t3[1] + .3)
voice = track.copy()

# ambience: wind (filtered noise), low drone, boom on the rule slam and on the end card
rng = np.random.default_rng(3); n = len(track); tt = np.arange(n) / SR
noise = rng.standard_normal(n).astype(np.float32)
k = int(SR * .004); wind = np.convolve(noise, np.ones(k) / k, 'same')
wind *= (0.5 + 0.5 * np.sin(2 * np.pi * tt / 5.3) ** 2) * 0.10
drone = (0.07 * np.sin(2 * np.pi * 55 * tt) + 0.04 * np.sin(2 * np.pi * 82.4 * tt) + 0.025 * np.sin(2 * np.pi * 110 * tt + .5))
drone *= np.clip(tt / 2, 0, 1) * np.clip((DUR - tt) / 1.5, 0, 1)
def boom(t0, amp):
    s = int(t0 * SR); m = int(SR * 1.6); x = np.arange(m) / SR
    f = 70 * np.exp(-x * 2.5) + 35
    b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.2) * amp
    e = min(n, s + m); track[s:e] += b[:e - s].astype(np.float32)
mix = track + wind + drone
track[:] = mix; boom(5.92, .9); boom(12.8, .6)
# duck ambience under voice is implicit (low levels); normalise
peak = np.max(np.abs(track)); track = track / peak * 0.89
with wave.open(f'{OUT}/mix.wav', 'w') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track * 32767).astype(np.int16).tobytes())
# per-video-frame voice envelope (drives the muzzle)
fps = 30; hop = SR // fps
env = [float(np.sqrt(np.mean(voice[i * hop:(i + 1) * hop] ** 2))) for i in range(int(DUR * fps))]
mx = max(env) or 1; env = [round(min(1, e / mx * 1.6), 3) for e in env]
json.dump({'t1': t1, 't2': t2, 'tr': tr, 't3': t3, 't4': t4, 'env': env}, open(f'{OUT}/timing.json', 'w'))
print(name, 'L1', t1, 'L2', t2, 'R', tr, 'L3', t3, 'L4', t4)
