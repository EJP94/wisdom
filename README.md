# Wisdom

Conocimiento destilado de libros, podcasts, videos y cursos, en vaults de Obsidian.
La primera vault es el podcast Holistic Alpha de Steven Mathis.

## Capas

1. **Transcripts** (`holistic-alpha/transcripts/`): los 809 episodios tal como salieron de Parakeet. No se editan
2. **Recaps** (`holistic-alpha/recaps/`): un Recap por episodio. Es la fuente de todo lo demás
3. **Temas**, en dos pasos. El paso A parte cada Recap en afirmaciones (`holistic-alpha/claims/`). El paso B arma una nota por tema con sus afirmaciones (`holistic-alpha/topics/`), en 6 áreas. Los 57 Recaps ya tienen afirmaciones. La primera nota completa será la del frío
4. **Vistas** sacadas de los temas: pensum, manual por problema, programa de transformación, grafo de ideas. Todavía no existen
5. **Piezas**: lo que se publica. Esteban verifica los datos de cada pieza antes de publicarla

## Dónde está cada cosa

- `STATUS.md`: dónde estamos, qué sigue y qué se decidió. Empieza por aquí
- `holistic-alpha/recap-instructions.md`: las instrucciones de recap, la única regla de cómo se escribe un Recap
- `holistic-alpha/topic-instructions.md`: las instrucciones de tema, la única regla de cómo se escribe una nota de tema
- `holistic-alpha/topics.csv`: la lista cerrada de temas, con su área, explicitud y palabras clave
- `holistic-alpha/topic-episodes.csv`: los episodios de cada tema. Lo genera `tools/topic_episodes.py`
- `holistic-alpha/episodes.csv`: un renglón por episodio. Lo genera `tools/build_episodes.py` desde `INVENTARIO.csv`
- `holistic-alpha/logs/`: lo crean las corridas: planes, reportes del checker y hallazgos de revisión
- `tools/`: scripts gratis (Python, sin dependencias) para armar la tabla, planear bloques, revisar formato, puntuar revisores y medir el costo
- `tools/transcription/`: descarga y transcripción de audios nuevos
- `.claude/skills/recaps/`: el skill `/recaps` que corre el pipeline

## Procesar episodios

En Claude Code, desde la raíz del repo: `/recaps 801-813`.
El skill explica cada paso. Las reglas para agentes están en `AGENTS.md`.

El contenido de la vault va en inglés.
