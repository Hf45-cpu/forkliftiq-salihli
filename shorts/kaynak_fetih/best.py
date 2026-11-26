import sys, json, re, difflib, torch, torchaudio, librosa
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
from faster_whisper import WhisperModel
torch.set_num_threads(4)
L = json.load(open(sys.argv[1])); idx = [int(i) for i in sys.argv[2].split(',')]; ref = sys.argv[3]
REFD = {0: "1453 21 yaşında bir sultan 1100 yıllık bir şehre karşı", 2: "20 metreyi aşan hendek 2 kat sur ve 96 kule",
        4: "nisanın altısında kuşatma başladı 50 ile 80 bin osmanlı askerine karşı şehirde yalnızca 7 bin savunmacı vardı",
        5: "ve büyük sürpriz şahi topu 8 metrelik namlu 540 kiloluk gülle", 7: "22 nisanda 70 kadar gemi karadan tepeden aşırılarak haliçe indirildi",
        3: "önce boğazı kesti rumeli hisarı"}
norm = lambda s: re.sub(r"[^a-zçğıöşü0-9 ]", "", s.replace('İ','i').replace('I','ı').lower().replace("'", "")).split()
tts = ChatterboxMultilingualTTS.from_pretrained(device="cpu"); asr = WhisperModel("small", device="cpu", compute_type="int8")
for i in idx:
    best = (-1, None, "")
    for k in range(3):
        torch.manual_seed(100 + k * 7 + i)
        wav = tts.generate(L[i]["text"], language_id="tr", audio_prompt_path=ref, exaggeration=0.55, cfg_weight=0.55, temperature=0.7)
        a = librosa.resample(wav.numpy()[0], orig_sr=tts.sr, target_sr=16000)
        hyp = " ".join(s.text.strip() for s in asr.transcribe(a, language="tr", beam_size=5)[0])
        r = difflib.SequenceMatcher(None, norm(REFD[i]), norm(hyp)).ratio()
        print(i, k, f"{r:.2f}", hyp, flush=True)
        if r > best[0]: best = (r, wav, hyp)
        if r > .95: break
    torchaudio.save(f"out/n{i}.wav", best[1], tts.sr); print("BEST", i, f"{best[0]:.2f}", best[2], flush=True)
