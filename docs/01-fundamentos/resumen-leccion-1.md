---
title: "Resumen de la lección 1"
tags:
  - resumen
  - leccion-1
  - iot
  - bimrocket
---

# Resumen de la lección 1

## Idea central

En esta lección hemos construido el primer flujo completo entre IoT y BIMROCKET.

```text
sensor/API → dato JSON → objeto BIM → visualización → validación
```

La idea clave:

```text
un objeto BIM no solo tiene geometría;
también puede tener identidad, datos vivos y reglas para saber si esos datos son confiables.
```

## Modelo final de la lección

El archivo final de referencia es:

```text
examples/bimrocket-models/lab-03-dos-salas-iot.brf
```

Contiene:

```text
Edificio_Demo
├── Sala_A-101
└── Sala_A-102
```

Cada sala tiene:

- identidad propia en `userData`;
- un `RestPollController`;
- un `DisplayController`;
- un `ColorController`;
- fórmula de URL dinámica;
- validación `iotMatch`;
- color por confianza del dato.

## Camino completo del dato

Para `Sala_A-102`, el flujo es:

```text
http://127.0.0.1:8001/api/rooms/A-102
  ↓
ctr_0 = RestPollController
  ↓
ctr_0.jsonOutput
  ↓
jsonOutput.co2
jsonOutput.room
jsonOutput.status
  ↓
fórmulas de BIMROCKET
  ↓
DisplayController + ColorController + userData.iotMatch
```

El mismo patrón se repite en `Sala_A-101`.

## Identidad de la sala

Cada sala sabe quién es mediante `userData`.

Ejemplo:

```text
Sala_A-102
├── userData.room = A-102
└── userData.ifcGlobalId = DEMO_IFC_GLOBAL_ID_A102
```

`room` es el identificador humano o funcional de la sala.

`ifcGlobalId` representa el identificador BIM/IFC. En este laboratorio usamos un valor de demostración.

## URL dinámica

La URL del sensor se construye con una fórmula:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room
```

En `Sala_A-101` produce:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

En `Sala_A-102` produce:

```text
http://127.0.0.1:8001/api/rooms/A-102
```

## Fórmulas principales

### URL del sensor

Path:

```text
controllers.ctr_0.url
```

Expression:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room
```

### Valor mostrado en el panel

Path:

```text
controllers.ctr_1.input
```

Expression:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

### Entrada del color

Path:

```text
controllers.co2_color.input
```

Expression:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

### Validación de identidad

Path:

```text
userData.iotMatch
```

Expression:

```javascript
object.userData.room === object.controllers.ctr_0.jsonOutput.room
```

Se lee:

```text
¿la sala BIM seleccionada coincide con la sala que dice la API?
```

## Estados visuales

El modelo final usa esta prioridad:

```text
1. iotMatch = false → morado
2. status = "offline" → gris
3. todo correcto → color según CO₂
```

| Caso | `status` | `iotMatch` | Color |
|---|---|---|---|
| Todo correcto | `online` | `true` | Verde/amarillo/rojo según CO₂ |
| Sensor offline | `offline` | `true` | Gris |
| Identidad incorrecta | `online` | `false` | Morado |

## Fórmulas de color finales

### `minColor`

```javascript
!object.userData.iotMatch ? object.controllers.co2_color.minColor.set(0x8000ff) : object.controllers.ctr_0.jsonOutput.status === "offline" ? object.controllers.co2_color.minColor.set(0x808080) : object.controllers.co2_color.minColor.set(0x00aa00)
```

### `maxColor`

```javascript
!object.userData.iotMatch ? object.controllers.co2_color.maxColor.set(0x8000ff) : object.controllers.ctr_0.jsonOutput.status === "offline" ? object.controllers.co2_color.maxColor.set(0x808080) : object.controllers.co2_color.maxColor.set(0xff0000)
```

## Qué significa cada controlador

| Controlador | Función |
|---|---|
| `RestPollController` | Consulta periódicamente una API REST |
| `DisplayController` | Muestra un valor en un panel |
| `ColorController` | Colorea el objeto según un valor numérico |

En nuestro modelo:

```text
ctr_0 = RestPollController
ctr_1 = DisplayController
co2_color = ColorController
```

## Pruebas realizadas

### Caso normal

```text
status = online
iotMatch = true
color = según CO₂
```

### Caso offline

URL temporal:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room + "?offline=1"
```

Resultado esperado:

```text
status = offline
iotMatch = true
color = gris
```

### Caso de identidad incorrecta

Fórmula temporal:

```javascript
"A-999" === object.controllers.ctr_0.jsonOutput.room
```

Resultado esperado:

```text
iotMatch = false
color = morado
```

Después de la prueba se restauró:

```javascript
object.userData.room === object.controllers.ctr_0.jsonOutput.room
```

## Cómo reanudar la lección

Arranca el sensor:

```powershell
cd C:\ruta\a\bimrocket-iot-learning
.\scripts\start-mock-sensor.ps1
```

Arranca BIMROCKET:

```powershell
cd C:\ruta\a\bimrocket-iot-learning
.\scripts\start-bimrocket-static.ps1
```

Abre:

```text
http://127.0.0.1:8000/app.html
```

Y carga:

```text
examples/bimrocket-models/lab-03-dos-salas-iot.brf
```

## Cierre conceptual

La lección 1 termina con esta idea:

```text
Un gemelo digital no es solo un modelo 3D.
Es geometría + identidad + datos vivos + reglas de confianza.
```

En esta lección todavía usamos un sensor simulado en Python. Más adelante podremos sustituir esa fuente por un dispositivo real, como el kit ESP32 de KEYESTUDIO.
