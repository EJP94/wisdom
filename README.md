# Wisdom

Conocimiento destilado de libros, podcasts, videos y cursos, en vaults de Obsidian.
La primera vault es el podcast Holistic Alpha de Steven Mathis.

## Capas

1. **Transcripts** (`holistic-alpha/transcripts/`): los 809 episodios tal como salieron de Parakeet. No se editan
2. **Recaps** (`holistic-alpha/recaps/`): un Recap por episodio. Es la fuente de todo lo demás
3. Vistas sacadas de los Recaps: notas por tema, manual por problema, contenido. Todavía no existen

## Dónde está cada cosa

- `holistic-alpha/recap-instructions.md`: las instrucciones de recap, la única regla de cómo se escribe un Recap
- `holistic-alpha/episodes.csv`: un renglón por episodio. Lo genera `tools/build_episodes.py` desde `INVENTARIO.csv`
- `holistic-alpha/golden/`: la lista del set de oro (`set.txt`) y la clave para medir revisores. El set de oro no tiene copias: son Recaps de `recaps/`
- `holistic-alpha/logs/`: hallazgos de revisión, reportes del checker y calibración
- `tools/`: scripts gratis (Python, sin dependencias) para armar la tabla, planear bloques, revisar formato, puntuar revisores y medir el costo
- `tools/transcription/`: descarga y transcripción de audios nuevos
- `.claude/skills/recaps/`: el skill `/recaps` que corre el pipeline

## Procesar episodios

En Claude Code, desde la raíz del repo: `/recaps 801-813`.
El skill explica cada paso. Las reglas para agentes están en `AGENTS.md`.

El contenido de la vault va en inglés.
