import sys, json, time, torch, torchaudio, numpy as np, librosa
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
torch.set_num_threads(4)
out = sys.argv[1]; lines = json.load(open(sys.argv[2])); idx = [int(i) for i in sys.argv[3].split(',')] if len(sys.argv) > 3 else range(len(lines))
ref = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != '-' else None
t0 = time.time(); m = ChatterboxMultilingualTTS.from_pretrained(device="cpu"); print("load", round(time.time()-t0, 1), flush=True)
for i in idx:
    t0 = time.time()
    wav = m.generate(lines[i]["text"], language_id="tr", audio_prompt_path=ref, exaggeration=0.6, cfg_weight=0.5, temperature=0.75)
    torchaudio.save(f"{out}/n{i}.wav", wav, m.sr)
    y = wav.numpy()[0]; f0, vf, _ = librosa.pyin(y, fmin=60, fmax=400, sr=m.sr, frame_length=2048)
    print(i, "dur", round(len(y)/m.sr, 2), "gen", round(time.time()-t0, 1), "f0 median", round(float(np.nanmedian(f0)), 1), flush=True)
