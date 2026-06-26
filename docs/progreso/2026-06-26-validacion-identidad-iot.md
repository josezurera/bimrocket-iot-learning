---
title: "2026-06-26 — Validación de identidad IoT"
tags:
  - progreso
  - iot
  - validacion
  - formulas
---

# 2026-06-26 — Validación de identidad IoT

En este paso añadimos una comprobación nueva al modelo: no basta con recibir un dato IoT, también queremos saber si ese dato pertenece al objeto BIM correcto.

## Problema

Una sala BIM puede tener esta identidad:

```text
userData.room = A-102
```

Y el sensor puede devolver una lectura como:

```json
{
  "room": "A-102",
  "co2": 677,
  "status": "online"
}
```

En ese caso todo es coherente:

```text
Sala BIM: A-102
Dato IoT: A-102
```

Pero en un sistema real podría haber errores de asociación. Por ejemplo:

```text
Sala BIM: A-102
Dato IoT: A-101
```

La red puede funcionar, el sensor puede estar `online`, y aun así el dato puede no pertenecer al objeto correcto.

## Fórmula creada

Añadimos una fórmula en `Sala_A-102`.

Path:

```text
userData.iotMatch
```

Expression:

```javascript
object.userData.room === object.controllers.ctr_0.jsonOutput.room
```

## Cómo leerla

Parte izquierda:

```javascript
object.userData.room
```

significa:

```text
el código de sala guardado en el objeto BIM actual
```

Parte derecha:

```javascript
object.controllers.ctr_0.jsonOutput.room
```

significa:

```text
el código de sala que llegó desde la API REST
```

El operador:

```javascript
===
```

pregunta:

```text
¿son exactamente iguales?
```

Por tanto, la fórmula completa significa:

```text
¿la sala que soy coincide con la sala del dato recibido?
```

## Resultado

Cuando la sala seleccionada era `Sala_A-102`, la comprobación dio:

```text
iotMatch = true
```

En BIMROCKET aparece como un checkbox marcado en `Propiedades (userData)`.

## Prueba controlada

Para entender el booleano `true/false`, se hizo una prueba temporal cambiando la expresión a:

```javascript
"A-999" === object.controllers.ctr_0.jsonOutput.room
```

Como la API estaba devolviendo:

```text
A-102
```

la comparación real era:

```javascript
"A-999" === "A-102"
```

Resultado:

```text
false
```

Después se restauró la expresión correcta:

```javascript
object.userData.room === object.controllers.ctr_0.jsonOutput.room
```

Y `iotMatch` volvió a quedar en:

```text
true
```

## Diferencia entre `status` e `iotMatch`

Ahora distinguimos dos conceptos:

| Campo | Quién lo decide | Qué significa |
|---|---|---|
| `status` | API / sensor | Si el sensor está online u offline |
| `iotMatch` | BIMROCKET / fórmula | Si el dato pertenece a esta sala |

Esto permite detectar situaciones distintas:

| status | iotMatch | Interpretación |
|---|---|---|
| `online` | `true` | Todo bien |
| `offline` | `true` | Sensor no disponible, pero identidad coherente |
| `online` | `false` | Llega dato, pero parece de otra sala |
| `offline` | `false` | Dato no disponible y además incoherente |

## Idea importante

Antes teníamos:

```text
leer dato → mostrar dato → pintar sala
```

Ahora empezamos a tener:

```text
leer dato → comprobar identidad → mostrar dato → pintar sala
```

Este es un paso hacia un modelo más robusto: no se trata solo de visualizar datos, sino de comprobar si son confiables para el objeto BIM seleccionado.

## Siguiente paso natural

Usar `iotMatch` en las reglas visuales:

- si `status = "offline"`, pintar gris;
- si `iotMatch = false`, pintar con un color de alerta;
- si todo está bien, pintar según el valor de CO₂.
