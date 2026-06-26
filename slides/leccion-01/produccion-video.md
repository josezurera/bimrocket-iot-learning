# Producción de videotutorial — Lección 1

## Objetivo

Convertir las diapositivas Marp de la lección 1 en un videotutorial monetizable.

La pieza final debería incluir:

- diapositivas limpias;
- locución en español de España;
- ritmo pausado;
- posibles capturas o cortes de BIMROCKET;
- guion alineado con el contenido técnico;
- archivos fuente editables.

## Estructura recomendada de archivos

```text
slides/leccion-01/
├── leccion-01.md              # diapositivas Marp
├── theme.css                  # tema visual
├── narrativa-video.md         # enfoque narrativo
├── guion-locucion.md          # voz por diapositiva
├── produccion-video.md        # esta guía
├── dist/
│   ├── leccion-01.pdf
│   └── leccion-01.html
└── media/
    ├── audio/                 # audios por diapositiva
    ├── video/                 # renders o clips intermedios
    └── final/                 # vídeo final
```

La carpeta `media/` no se ha creado todavía porque conviene decidir antes el método de voz y edición.

## Flujo de trabajo propuesto

### Fase 1 — Guion

Ya tenemos una primera versión:

- `narrativa-video.md`
- `guion-locucion.md`

Antes de grabar o generar voz, conviene hacer una pasada para:

- ajustar el nivel técnico;
- añadir ejemplos orales;
- decidir si el vídeo será más corto o más explicativo;
- marcar dónde se entra en BIMROCKET en directo.

### Fase 2 — Voz

Opciones posibles:

1. Voz humana grabada por el autor.
2. Voz sintética con licencia comercial.
3. Voz sintética local si el equipo tiene una voz española instalada.

Para monetización, la opción más segura es usar voz humana propia o una voz sintética con licencia comercial clara.

Codex puede ayudar a preparar:

- texto final por escena;
- archivos `.txt` o `.ssml`;
- división por diapositiva;
- nombres de archivo consistentes;
- comandos de ensamblado si existe una herramienta de audio/vídeo disponible.

Ejemplo de nombres:

```text
media/audio/slide-01.wav
media/audio/slide-02.wav
media/audio/slide-03.wav
```

### Fase 3 — Imagen

Opciones de vídeo:

1. Exportar cada diapositiva como imagen y montar un vídeo con audio.
2. Grabar la presentación en pantalla.
3. Combinar diapositivas con pequeños clips de BIMROCKET.

La opción más profesional sería:

```text
diapositiva → explicación → breve demostración BIMROCKET → vuelta a diapositiva
```

### Fase 4 — Montaje

Herramientas posibles:

- DaVinci Resolve;
- CapCut;
- Clipchamp;
- OBS para capturas;
- FFmpeg para montaje automatizado.

Con FFmpeg se puede automatizar mucho, pero para monetización conviene revisar manualmente ritmo, silencios y transiciones.

### Fase 5 — Publicación

Formatos recomendados:

- YouTube horizontal: 1920×1080;
- plataforma de cursos: 1920×1080;
- clips cortos promocionales: 1080×1920.

## Decisiones pendientes

Antes de generar la primera versión de vídeo hay que elegir:

- si la voz será humana o sintética;
- si habrá demo en vivo de BIMROCKET o solo slides;
- duración objetivo: 10, 15 o 20 minutos;
- nivel de edición: básico, curso profesional o promocional.

## Recomendación inicial

Para esta primera lección, recomiendo:

- vídeo principal de 12–15 minutos;
- voz pausada española;
- slides como columna vertebral;
- 2 o 3 cortes breves de BIMROCKET;
- cierre preparando el salto al ESP32.

Así queda suficientemente profesional sin complicar demasiado el primer montaje.

