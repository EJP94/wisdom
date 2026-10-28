# Guía: transcripción local con NVIDIA Parakeet TDT 0.6B v3

Guía para que un agente replique, en otro equipo, la transcripción que se hizo en la PC
(Windows 11, RTX 5050 de 8 GB) el 2026-10-22. Es autocontenida: el script completo está
al final y no hace falta nada más de este repositorio.

## 1. Qué se logra

- Transcripción **gratuita y 100 % local** de audios (MP3, M4A, WAV, etc.).
- Modelo: [`nvidia/parakeet-tdt-0.6b-v3`](https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3)
  (licencia CC-BY-4.0), cargado con Hugging Face `transformers` (sin NeMo).
- Por cada audio, un `.txt` con la hora de inicio de cada trozo (`[03:12] texto…`) y un
  `.json` con los tiempos exactos.
- Velocidad medida en una RTX 5050: **un episodio de 16 min en ~10 s**. La primera vez se
  descargan ~2,5 GB del modelo.

### Por qué este modelo

Se compararon Parakeet v3, Bark 3.0 Pro (versión ajustada de Parakeet) y Voxtral Mini 3B con
el mismo episodio de un podcast en inglés. Parakeet fue el que menos se apartó de los otros
dos, transcribe palabra por palabra (conserva "um", "uh", "gonna") y sus errores son
evidentes ("Alpha Mail" por "Alpha Male"), no cambios de sentido. Voxtral "limpia" el
habla y en 8 GB de VRAM tardó 25 min por episodio; Bark tuvo más fallos de formato.

## 2. Requisitos

| | Recomendado | Notas |
|---|---|---|
| GPU | NVIDIA con 4 GB de VRAM o más | El modelo en bf16 ocupa ~1,2 GB. Sin GPU funciona con `--cpu`, más lento (no medido). |
| Driver | Compatible con CUDA 12.8 | Obligatorio para las RTX serie 50 (Blackwell, compute capability 12.0). |
| Python | 3.11 | Es la versión probada. |
| ffmpeg | En el `PATH` | El script lo usa para leer cualquier formato de audio. |
| Disco | ~6 GB | Entorno de Python (~4 GB) + modelo (~2,5 GB). |

Comprobaciones previas:

```bash
nvidia-smi                 # GPU, VRAM y versión del driver
python3.11 --version       # o: py -3.11 --version en Windows
ffmpeg -version
```

## 3. Instalación

Con [`uv`](https://docs.astral.sh/uv/) (lo que se usó). Linux/macOS:

```bash
uv venv .venv --python 3.11
uv pip install -p .venv torch --index-url https://download.pytorch.org/whl/cu128
uv pip install -p .venv transformers numpy librosa
```

Windows (PowerShell): los mismos comandos; el intérprete queda en `.venv\Scripts\python.exe`.

Sin `uv`: `python3.11 -m venv .venv` y luego `.venv/bin/pip install …` con los mismos paquetes
y el mismo `--index-url` para `torch`.

Sin GPU NVIDIA: instalar `torch` sin `--index-url` (versión CPU) y usar `--cpu` al transcribir.

Versiones probadas: `torch 2.11.0+cu128`, `transformers 5.20.2`, `numpy 2.3.5`.
`ParakeetForTDT` requiere una versión reciente de `transformers`; con una vieja falla el import.

### Verificación (no saltarla)

```bash
.venv/bin/python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0)); from transformers import ParakeetForTDT; print('ok')"
```

Debe mostrar una versión terminada en `+cu128`, `True` y el nombre de la GPU.

**Trampa conocida:** instalar `transformers` con `-U` (o en el mismo comando que otras
dependencias) puede reemplazar el `torch` con CUDA por uno de PyPI **sin GPU**. Síntoma:
`AssertionError: Torch not compiled with CUDA enabled` o `cuda.is_available()` en `False`.
Solución:

```bash
uv pip install -p .venv torch --index-url https://download.pytorch.org/whl/cu128 --reinstall-package torch
```

## 4. Uso

Guardar el script de la sección 8 como `transcribir_parakeet.py` y ejecutar:

```bash
# Una carpeta completa (o varios archivos sueltos)
.venv/bin/python transcribir_parakeet.py audios/ --salida transcripciones/

# Sin GPU
.venv/bin/python transcribir_parakeet.py audios/ --salida transcripciones/ --cpu
```

- Carga el modelo **una sola vez** para toda la tanda.
- **Salta** los audios que ya tienen su `.txt` en la carpeta de salida: se puede cortar (incluso
  por un corte de luz) y volver a correr, o agregar audios nuevos y correrlo de nuevo. Cada archivo
  se escribe completo o no se escribe, así que nunca queda una transcripción a medias.
- Cada resultado lleva el mismo nombre que el audio: `audios/012 - Título.mp3` →
  `transcripciones/012 - Título.txt` y `.json`.
- Para tandas largas, correrlo en segundo plano y guardar la salida en un log.

## 5. Cómo funciona (decisiones y por qué)

1. **Decodificación con ffmpeg** a mono, 16 kHz, float32: es el formato que espera el modelo y
   así acepta cualquier entrada.
2. **Corte en trozos de 20 a 40 s, en pausas.** Dentro de cada ventana se corta en el punto de
   menor energía (suavizada a 300 ms), para no partir palabras. Pasar un episodio entero de
   una vez dispara el uso de memoria de la atención; con trozos cortos 8 GB sobran. El corte
   depende solo del audio, así que es reproducible.
3. **0,25 s de silencio al inicio de cada trozo**, la convención con la que se evalúan estos
   modelos (tomada de la ficha de Bark 3.0, derivado de Parakeet).
4. **bf16 en GPU** (float32 en CPU) y decodificación codiciosa (`generate()` por defecto).
5. **Idioma automático.** Parakeet v3 reconoce 25 idiomas europeos, incluido el español; no se
   le indica el idioma. Las pruebas de esta guía fueron solo en inglés.

## 6. Qué esperar del resultado

- **Palabra por palabra:** conserva muletillas y repeticiones; no resume ni "limpia".
- **Números en cifras** ("20%", "8020") y con puntuación y mayúsculas.
- **Errores típicos:** nombres propios y palabras que suenan igual ("Alpha Mail"). Conviene
  darle al agente que use el texto una nota con los nombres correctos.
- **El último trozo puede salir vacío** cuando el audio termina con música: es normal. El
  `.txt` lo omite y el `.json` lo conserva con texto vacío.
- **No distingue quién habla** y este script solo da tiempos por trozo, no por palabra.

## 7. Problemas encontrados y soluciones

| Síntoma | Causa | Solución |
|---|---|---|
| `Torch not compiled with CUDA enabled` | `torch` reemplazado por la versión CPU | Reinstalar `torch` desde el índice cu128 (sección 3) |
| Aviso de *symlinks* de Hugging Face (Windows) | Windows sin modo desarrollador | Inofensivo; se silencia con `HF_HUB_DISABLE_SYMLINKS_WARNING=1` |
| `UnicodeEncodeError` al imprimir (Windows) | Consola en cp1252 | El script ya llama a `sys.stdout.reconfigure(encoding="utf-8")` |
| Avisos de `max_length` y de `RNN module weights` | Avisos internos de `transformers`/PyTorch | Inofensivos; el script los filtra |
| `No hay GPU CUDA disponible` | Driver, `torch` sin CUDA o equipo sin NVIDIA | Revisar la verificación de la sección 3, o usar `--cpu` |
| `ffmpeg` no encontrado | No está en el `PATH` | Instalarlo (Windows: `winget install Gyan.FFmpeg`; Debian/Ubuntu: `apt install ffmpeg`) |

## 8. El script

```python
"""Transcribe audios con NVIDIA Parakeet TDT 0.6B v3 (local, gratis).

Uso:
    python transcribir_parakeet.py <audio o carpeta> [más audios...] [--salida carpeta] [--cpu]

Por cada audio escribe <salida>/<nombre>.txt (con [mm:ss] por trozo) y
<nombre>.json (tiempos exactos). Salta los que ya tienen .txt. El modelo se
carga una sola vez para toda la tanda.
"""

import argparse
import json
import os
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


def escribir(ruta: Path, contenido: str) -> None:
    """Escribe completo o nada: si se corta la luz, no queda un archivo a medias."""
    temporal = ruta.with_name(ruta.name + ".tmp")
    with open(temporal, "w", encoding="utf-8") as f:
        f.write(contenido)
        f.flush()
        os.fsync(f.fileno())
    temporal.replace(ruta)


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
        # El .txt va último: su existencia marca el audio como terminado
        escribir(args.salida / f"{ruta.stem}.json", json.dumps(datos, ensure_ascii=False, indent=2))
        texto = "\n\n".join(f"[{mmss(s['inicio'])}] {s['texto']}" for s in segmentos if s["texto"])
        escribir(args.salida / f"{ruta.stem}.txt", texto + "\n")
        print(f"[{k}/{len(pendientes)}] {ruta.name}: {len(audio) / SR / 60:.1f} min en {time.perf_counter() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
```

## 9. Comprobación final

1. Transcribir un audio corto que alguien pueda escuchar y revisar 2 o 3 trozos al oído.
2. Al terminar una tanda, revisar que cada audio tenga su `.txt` y que los trozos vacíos
   estén solo al final (música).
3. Correr el script de nuevo: debe decir `0 pendientes`.
