# Vault Holistic Alpha

Conocimiento destilado del podcast Holistic Alpha de Steven Mathis.
Ábrela en Obsidian como vault: la carpeta `holistic-alpha/`.
Empieza por [[Mapa Holistic Alpha]].

## Carpetas
- `fuentes/transcripts/`: un transcript por episodio, cada párrafo con su ancla `^mMMSS`
- `episodios/`: una nota destilada por episodio
- `conceptos/`: el centro, una nota por idea con todas sus apariciones
- `practicas/`: protocolos con pasos
- `mapas/`: índices y rutas de estudio
- `salidas/`: piezas para compartir armadas desde los conceptos
- `plantillas/`: moldes de cada tipo de nota

## Reglas
**Cada idea cita su fuente.**
Un minuto como `06:28` es un enlace al párrafo del transcript que empieza ahí.

**Los conceptos crecen, no se duplican.**
Cuando un tema vuelve en otro episodio, se suma una línea en `## Referencias` con fecha, episodio y minuto.
Un concepto nace si aparece en dos episodios o más, o si es central en uno.

**Lo privado va al final.**
Todo bajo `## Privado` es lectura crítica o notas personales y no se comparte.
`publicable: false` hasta que lo revises.
Las citas textuales van en inglés y cortas.

## Escribir notas nuevas
Escribe las citas con abreviaturas y deja que el script las convierta en enlaces:
- `{4@06:28}` enlaza al minuto 06:28 del episodio 4
- `{E4}` enlaza a la nota del episodio 4
- `{R4@06:28}` arma una referencia completa con fecha, episodio y minuto

Después corre:

```
python3 herramientas/citas.py holistic-alpha
```

El script expande las abreviaturas y verifica que cada cita `> "..."` esté textual en el párrafo que cita.
Falla si un minuto no existe o una cita no coincide.
