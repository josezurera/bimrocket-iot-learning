---
title: "Estado actual"
tags:
  - progreso
  - checkpoint
  - laboratorio
---

# Estado actual del curso

Última actualización: 26 de junio de 2026.

## Punto alcanzado

Ya se completó la conexión práctica entre un sensor REST simulado y BIMROCKET.

Se consiguió:

- ejecutar una API local en `http://127.0.0.1:8001`;
- obtener lecturas JSON de varias salas;
- diferenciar estados `online` y `offline`;
- abrir BIMROCKET desde `http://127.0.0.1:8000/app.html`;
- crear un modelo con dos salas dentro de `Edificio_Demo`;
- añadir un `RestPollController` por sala;
- añadir un `DisplayController` por sala;
- añadir un `ColorController` por sala;
- mostrar el CO₂ en paneles visuales como `ppm`;
- colorear cada sala según el CO₂;
- representar el estado `offline` con color gris;
- validar que el dato IoT recibido pertenece a la sala BIM correcta.

## Punto actual

El mejor punto de partida actual es:

```text
examples/bimrocket-models/lab-03-dos-salas-iot.brf
```

Ese modelo contiene:

```text
Edificio_Demo
├── Sala_A-101
└── Sala_A-102
```

Cada sala tiene identidad propia:

```text
userData.room
userData.ifcGlobalId
```

Y la URL del `RestPollController` se construye desde esa identidad:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room
```

## API simulada disponible

La API simulada soporta estas rutas:

```text
http://127.0.0.1:8001/api/rooms/A-101
http://127.0.0.1:8001/api/rooms/A-102
http://127.0.0.1:8001/api/rooms/A-103
```

También existe:

```text
http://127.0.0.1:8001/api/rooms
```

para listar las salas simuladas.

Si el sensor estaba arrancado antes de los últimos cambios, hay que reiniciarlo.

## Validación de identidad IoT

El modelo ya incluye esta fórmula en `A-101` y `A-102`:

```javascript
object.userData.room === object.controllers.ctr_0.jsonOutput.room
```

El resultado se guarda en:

```text
userData.iotMatch
```

Interpretación:

```text
iotMatch = true  -> el dato recibido pertenece a la sala
iotMatch = false -> el dato recibido no coincide con la identidad de la sala
```

## Regla visual actual

El color de cada sala sigue esta prioridad:

```text
iotMatch false -> morado
status offline -> gris
todo correcto -> color según CO₂
```

Esto significa que la confianza del dato tiene prioridad sobre el valor de CO₂.

## Nombre real de los controladores usados

En cada sala se usan estos nombres:

```text
ctr_0 = RestPollController
ctr_1 = DisplayController
co2_color = ColorController
```

Para leer el CO₂ en una fórmula:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

Para leer la sala recibida desde la API:

```javascript
object.controllers.ctr_0.jsonOutput.room
```

## Conceptos aclarados

Ya se han documentado estos conceptos:

- qué es `RestPollController`;
- qué diferencia hay entre `output` y `jsonOutput`;
- qué significa `object` en una fórmula;
- qué diferencia hay entre `path` y `expression`;
- qué es `userData`;
- cómo construir una URL desde `object.userData.room`;
- cómo usar `===` para comprobar identidad;
- qué significa `true` y `false`;
- qué diferencia hay entre `status` e `iotMatch`;
- cómo usar `? :` como `if` compacto;
- cómo priorizar reglas visuales: morado, gris, CO₂.

Ver:

```text
docs/progreso/2026-06-25-restpoll-formulas-display.md
docs/progreso/2026-06-25-identidad-bim-iot.md
docs/progreso/2026-06-25-api-multisala.md
docs/progreso/2026-06-25-dos-salas-iot.md
docs/progreso/2026-06-26-validacion-identidad-iot.md
```

## Comandos para reanudar

Terminal 1:

```powershell
cd C:\ruta\a\bimrocket-iot-learning
.\scripts\start-mock-sensor.ps1
```

Terminal 2:

```powershell
cd C:\ruta\a\bimrocket-iot-learning
.\scripts\start-bimrocket-static.ps1
```

Navegador:

```text
http://127.0.0.1:8000/app.html
```

## Archivos del modelo

Modelos disponibles:

```text
examples/bimrocket-models/lab-01-sensor-rest.brf
examples/bimrocket-models/lab-01-co2-display-color-offline.brf
examples/bimrocket-models/lab-02-identidad-dinamica-url.brf
examples/bimrocket-models/lab-03-dos-salas-iot.brf
```
