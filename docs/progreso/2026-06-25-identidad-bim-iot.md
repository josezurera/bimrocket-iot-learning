---
title: "2026-06-25 — Identidad BIM y URL dinámica del sensor"
tags:
  - progreso
  - bim
  - iot
  - formulas
---

# 2026-06-25 — Identidad BIM y URL dinámica del sensor

En este paso convertimos la conexión del sensor en algo más parecido a un flujo BIM + IoT real.

Hasta ahora la URL del sensor estaba escrita de forma fija:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

Eso funciona para una prueba, pero no escala bien. Si mañana tenemos muchas salas, no queremos copiar y modificar manualmente la URL de cada controlador. Queremos que cada sala tenga su propia identidad y que el controlador construya la URL a partir de esa identidad.

## Idea principal

La sala BIM debe saber quién es.

En BIMROCKET podemos guardar datos propios del objeto dentro de `userData`. Para nuestra sala:

```text
Sala_A-101
└── userData
    ├── room: A-101
    └── ifcGlobalId: DEMO_IFC_GLOBAL_ID_A101
```

Así, el objeto ya no es solo una caja geométrica. También representa una entidad del edificio.

## Fórmulas añadidas

### Identificador de sala

Path:

```text
userData.room
```

Expression:

```javascript
"A-101"
```

Esto guarda el código funcional de la sala.

### Identificador BIM / IFC

Path:

```text
userData.ifcGlobalId
```

Expression:

```javascript
"DEMO_IFC_GLOBAL_ID_A101"
```

En un modelo real, este valor vendría del IFC. En el laboratorio usamos un valor de demostración.

### URL dinámica del sensor

Path:

```text
controllers.ctr_0.url
```

Expression:

```javascript
"http://127.0.0.1:8001/api/rooms/" + object.userData.room
```

## Cómo leer esta fórmula si no sabes JavaScript

Esta parte:

```javascript
"http://127.0.0.1:8001/api/rooms/"
```

es un texto fijo.

Esta parte:

```javascript
object.userData.room
```

significa:

```text
objeto actual → datos propios → room
```

Y el signo `+` une textos.

Por tanto, si `object.userData.room` vale:

```text
A-101
```

la URL final queda:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

## Por qué esto importa

Este cambio parece pequeño, pero es muy importante:

- la sala BIM tiene identidad propia;
- el sensor se vincula a esa identidad;
- el controlador ya no depende de una URL escrita a mano para una sala concreta;
- el mismo patrón puede repetirse para muchas salas;
- nos acercamos al concepto de gemelo digital: geometría + identidad + datos vivos.

## Archivo BIMROCKET guardado

El estado de este paso queda guardado en:

```text
examples/bimrocket-models/lab-02-identidad-dinamica-url.brf
```

Este archivo contiene:

- sala `Sala_A-101`;
- `RestPollController`;
- `DisplayController`;
- `ColorController`;
- colores por CO₂;
- gris cuando el sensor está offline;
- `userData.room`;
- `userData.ifcGlobalId`;
- URL dinámica construida desde `object.userData.room`.

## Siguiente paso natural

Duplicar la sala para simular varias habitaciones:

- `A-101`;
- `A-102`;
- `A-103`.

Entonces veremos por qué esta fórmula empieza a ser útil de verdad: cada sala podrá usar el mismo patrón, cambiando solo su identidad.
