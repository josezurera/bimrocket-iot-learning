---
title: "2026-06-25 — Dos salas BIM conectadas al sensor"
tags:
  - progreso
  - bim
  - iot
  - multisala
---

# 2026-06-25 — Dos salas BIM conectadas al sensor

En este paso pasamos de una sala aislada a un pequeño modelo con dos salas:

```text
Edificio_Demo
├── Sala_A-101
└── Sala_A-102
```

Cada sala tiene su propia identidad:

```text
Sala_A-101
└── userData.room = A-101

Sala_A-102
└── userData.room = A-102
```

## Lo importante

Las dos salas usan el mismo patrón de fórmula para construir la URL del sensor:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room
```

La fórmula es igual, pero el resultado cambia porque `object` es distinto en cada sala.

En `Sala_A-101`:

```javascript
object.userData.room
```

vale:

```text
A-101
```

Por tanto la URL final es:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

En `Sala_A-102`, la misma fórmula produce:

```text
http://127.0.0.1:8001/api/rooms/A-102
```

## Por qué esto es un salto conceptual

Hasta ahora habíamos conectado un objeto BIM a un dato IoT.

Ahora empezamos a ver el patrón de escalado:

- cada objeto BIM tiene identidad;
- la API IoT responde por esa identidad;
- las fórmulas no necesitan reescribirse completamente;
- el mismo tipo de controlador puede repetirse en muchos espacios;
- el modelo empieza a comportarse como un conjunto de entidades conectadas, no como una maqueta suelta.

## Archivo BIMROCKET guardado

El estado de este paso queda guardado en:

```text
examples/bimrocket-models/lab-03-dos-salas-iot.brf
```

Este archivo contiene:

- un grupo raíz `Edificio_Demo`;
- dos salas: `Sala_A-101` y `Sala_A-102`;
- un `RestPollController` por sala;
- un `DisplayController` por sala;
- un `ColorController` por sala;
- fórmula dinámica de URL en cada sala;
- color por CO₂;
- gris cuando el sensor devuelve `status = "offline"`.

## Qué mirar en BIMROCKET

Cuando abras el archivo, selecciona cada sala y revisa:

- su pestaña de propiedades;
- su `userData.room`;
- su controlador `ctr_0`;
- la URL generada;
- el valor de `jsonOutput.co2`;
- el color resultante de la sala.

La comprobación clave es que cada sala consulta una ruta distinta de la API usando la misma fórmula.
