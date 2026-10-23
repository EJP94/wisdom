"""Transcribe audios con NVIDIA Parakeet TDT 0.6B v3 (local, gratis).

Uso:
    python transcribir_parakeet.py <audio o carpeta> [más audios...] [--salida carpeta] [--cpu]

Por cada audio escribe <salida>/<nombre>.txt (con [mm:ss] por trozo) y
<nombre>.json (tiempos exactos). Salta los que ya tienen .txt. El modelo se
carga una sola vez para toda la tanda.
"""

import argparse
import json
import subprocess
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import torch
from transformers import AutoProcessor, ParakeetForTDT

REPO = "nvidia/parakeet-tdt-0.6b-v3"
SR = 16000
MIN_TROZO, MAX_TROZO = 20.0, 40.0  # segundos
EXTENSIONES = {".mp3", ".m4a", ".wav", ".flac", ".ogg", ".opus", ".aac", ".mp4", ".webm"}

warnings.filterwarnings("ignore", message=".*max_length.*")
warnings.filterwarnings("ignore", message=".*RNN module weights.*")


def cargar_audio(ruta: Path) -> np.ndarray:
    """Decodifica con ffmpeg a mono 16 kHz float32."""
    crudo = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(ruta), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
        check=True,
        capture_output=True,
    ).stdout
    return np.frombuffer(crudo, dtype=np.float32).copy()


def cortar(audio: np.ndarray) -> list[tuple[int, int]]:
    """Trozos de 20 a 40 s, cortando en el punto de menor energía (una pausa)."""
    paso = SR // 100  # marcos de 10 ms
    n = len(audio) // paso
    energia = (audio[: n * paso].reshape(n, paso) ** 2).mean(axis=1)
    energia = np.convolve(energia, np.ones(30) / 30, mode="same")  # suavizado de 300 ms
    trozos, inicio = [], 0
    while len(audio) - inicio > MAX_TROZO * SR:
        a = (inicio + int(MIN_TROZO * SR)) // paso
        b = (inicio + int(MAX_TROZO * SR)) // paso
        corte = (a + int(np.argmin(energia[a:b]))) * paso
        trozos.append((inicio, corte))
        inicio = corte
    trozos.append((inicio, len(audio)))
    return trozos


def mmss(s: float) -> str:
    return f"{int(s // 60):02d}:{int(s % 60):02d}"


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("entradas", nargs="+", type=Path)
    p.add_argument("--salida", type=Path, default=Path("transcripciones"))
    p.add_argument("--cpu", action="store_true", help="sin GPU (más lento, float32)")
    args = p.parse_args()

    audios = []
    for e in args.entradas:
        audios += sorted(f for f in e.iterdir() if f.suffix.lower() in EXTENSIONES) if e.is_dir() else [e]
    args.salida.mkdir(parents=True, exist_ok=True)
    pendientes = [a for a in audios if not (args.salida / f"{a.stem}.txt").exists()]
    print(f"{len(audios)} audios, {len(audios) - len(pendientes)} ya transcritos, {len(pendientes)} pendientes", flush=True)
    if not pendientes:
        return

    if args.cpu:
        dispositivo, tipo = "cpu", torch.float32
    else:
        if not torch.cuda.is_available():
            sys.exit("No hay GPU CUDA disponible en PyTorch. Revisa la instalación o usa --cpu.")
        dispositivo, tipo = "cuda", torch.bfloat16
    procesador = AutoProcessor.from_pretrained(REPO)
    modelo = ParakeetForTDT.from_pretrained(REPO, dtype=tipo).to(dispositivo).eval()
    silencio = np.zeros(SR // 4, np.float32)  # 0,25 s de silencio al inicio de cada trozo

    for k, ruta in enumerate(pendientes, 1):
        t0 = time.perf_counter()
        audio = cargar_audio(ruta)
        segmentos = []
        with torch.inference_mode():
            for a, b in cortar(audio):
                entrada = procesador(np.concatenate([silencio, audio[a:b]]), sampling_rate=SR, return_tensors="pt")
                entrada = entrada.to(dispositivo, tipo)
                salida = modelo.generate(**entrada)
                ids = salida.sequences if hasattr(salida, "sequences") else salida
                texto = procesador.batch_decode(ids, skip_special_tokens=True)[0].strip()
                segmentos.append({"inicio": a / SR, "fin": b / SR, "texto": texto})

        datos = {"modelo": REPO, "audio": ruta.name, "duracion_s": len(audio) / SR, "segmentos": segmentos}
        (args.salida / f"{ruta.stem}.json").write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
        texto = "\n\n".join(f"[{mmss(s['inicio'])}] {s['texto']}" for s in segmentos if s["texto"])
        (args.salida / f"{ruta.stem}.txt").write_text(texto + "\n", encoding="utf-8")
        print(f"[{k}/{len(pendientes)}] {ruta.name}: {len(audio) / SR / 60:.1f} min en {time.perf_counter() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
