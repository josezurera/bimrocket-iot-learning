# Bloques de locución — Lección 1

Estos archivos dividen el guion de locución en bloques pequeños para generar audio con Google AI Studio usando la voz `Algieba`.

## Voz seleccionada

```text
Herramienta: Google AI Studio
Modelo: Gemini 3.1 Flash TTS Preview
Voz: Algieba
```

## Bloques

| Archivo | Diapositivas | Uso |
|---|---:|---|
| `bloque-01-slides-01-05.txt` | 1–5 | Introducción y flujo general |
| `bloque-02-slides-06-10.txt` | 6–10 | Identidad BIM/IoT y REST A-101 |
| `bloque-03-slides-11-15.txt` | 11–15 | REST A-102, URL dinámica y CO2 |
| `bloque-04-slides-16-20.txt` | 16–20 | Resultado visible, iotMatch y estados |
| `bloque-05-slides-21-25.txt` | 21–25 | Reglas de color y pruebas 1–2 |
| `bloque-06-slides-26-29.txt` | 26–29 | Prueba 3, modelo final y cierre |

## Instrucciones

### Opción A — Manual desde Google AI Studio

1. Copia un bloque completo.
2. Pégalo en Google AI Studio TTS.
3. Selecciona la voz `Algieba`.
4. Genera el audio.
5. Descárgalo como WAV.
6. Guárdalo con el mismo número de bloque:

```text
audio/leccion-01-bloque-01-algieba.wav
audio/leccion-01-bloque-02-algieba.wav
audio/leccion-01-bloque-03-algieba.wav
audio/leccion-01-bloque-04-algieba.wav
audio/leccion-01-bloque-05-algieba.wav
audio/leccion-01-bloque-06-algieba.wav
```

### Opción B — Automática por API

Desde la raíz del repositorio:

```powershell
cd C:\Users\josez\bimrocket-iot-learning
$env:GEMINI_API_KEY="TU_API_KEY"
python scripts/generate_tts_gemini.py
```

Para regenerar solo un bloque:

```powershell
python scripts/generate_tts_gemini.py --only 01 --force
```

La API key se lee desde la variable de entorno local `GEMINI_API_KEY`.  
No debe guardarse en archivos del repositorio.

## Nota de pronunciación

En los textos se usa `CO dos` en algunos puntos para evitar que la voz lea mal `CO₂`.
