# Runpod — paling senang (untuk kau)

Runpod = **sewa komputer GPU dalam internet**. Mac kau **tak kuat** untuk AI suara.

---

## Apa aku (AI) boleh buat

| Boleh | Tak boleh |
|-------|-----------|
| Start / Stop pod dari Cursor (MCP) | Klik browser untuk kau |
| Buat pod baru | Taip dalam Web Terminal **untuk** kau |
| Ingatkan jimat credit | Dengar WAV dalam telinga kau |

**Satu benda kau kena buat sendiri:** buka **Web Terminal** → **paste 1 command** → Enter.

---

## 3 perkataan je

1. **Pods** = mesin GPU  
2. **Connect** = cara masuk  
3. **Web Terminal** = tempat paste command  

---

## Flow setiap kali (gambaran)

```
Runpod website → Pods → modeon-week1 → Connect → Web Terminal
→ paste command → tunggu → Stop pod
```

---

## Command tunggal (F5 compare — lepas pod RUNNING)

Paste **semua** sekali gus:

```bash
cd /workspace/modeOn && git pull origin main
test -f /workspace/voices/default/reference.wav || echo "MISSING reference.wav - upload dulu"
chmod +x scripts/runpod_setup_f5.sh && ./scripts/runpod_setup_f5.sh
source .venv-f5/bin/activate
python3 scripts/week1_validate_f5.py --ref-audio /workspace/voices/default/reference.wav --auto-transcribe --limit 10 --output-dir /workspace/samples/week1-f5
```

(`--auto-transcribe` = tak payah taip transkrip manual)

---

## Pod tak start?

Maksud: GPU penuh. Cuba **10–30 minit** lagi, atau message aku **"start pod"** — aku cuba dari sini.

---

## Jangan risau salah

- Terminal Mac ≠ Runpod  
- Stop pod = jimat duit  
- Terminate = padam mesin (elakkan kalau nak keep data)
