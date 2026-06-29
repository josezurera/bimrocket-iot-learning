# Media — Lección 1

Esta carpeta contiene los artefactos audiovisuales generados para la lección 1.

## Vídeo final

```text
final/leccion-01.mp4
```

Características:

- resolución: 1280 × 720;
- formato: MP4;
- vídeo: H.264;
- audio: AAC;
- duración aproximada: 11 min 29 s;
- sincronización inicial: por bloques de diapositivas.

## Generación

Para regenerar el vídeo:

```powershell
cd C:\Users\josez\bimrocket-iot-learning
.\scripts\build-lesson1-video.ps1 -Force
```

El script usa:

- `slides/leccion-01/leccion-01.md`
- `slides/leccion-01/theme.css`
- `slides/leccion-01/tts/audio/leccion-01-bloque-*-algieba.wav`

## Nota

La carpeta intermedia `media/work/` no se conserva en Git. Se puede regenerar automáticamente.

