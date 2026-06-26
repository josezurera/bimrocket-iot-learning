# Diapositivas — Lección 1

Esta carpeta contiene la versión en diapositivas de la lección 1 del curso BIMROCKET + IoT.

## Archivos principales

- `leccion-01.md`: fuente Marp de la presentación.
- `theme.css`: tema visual inspirado en BIM Ingenieros.
- `narrativa-video.md`: enfoque narrativo para convertir la lección en videotutorial.
- `guion-locucion.md`: guion de voz por diapositiva.
- `produccion-video.md`: flujo recomendado para producir el vídeo.
- `images/`: capturas y diagramas usados por las slides.
- `dist/`: exportaciones generadas en PDF y HTML.

## Exportar PDF

```powershell
npx @marp-team/marp-cli slides/leccion-01/leccion-01.md --theme slides/leccion-01/theme.css --pdf --allow-local-files --output slides/leccion-01/dist/leccion-01.pdf
```

## Exportar HTML

```powershell
npx @marp-team/marp-cli slides/leccion-01/leccion-01.md --theme slides/leccion-01/theme.css --html --allow-local-files --output slides/leccion-01/dist/leccion-01.html
```

## Siguiente paso audiovisual

Antes de generar vídeo, revisar:

1. `narrativa-video.md`
2. `guion-locucion.md`
3. `produccion-video.md`

Después decidir si el videotutorial será:

- solo slides con voz;
- slides con cortes de BIMROCKET;
- clase grabada completa con demo en vivo.
