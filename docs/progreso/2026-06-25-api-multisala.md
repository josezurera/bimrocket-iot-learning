---
title: "2026-06-25 — API IoT multisala"
tags:
  - progreso
  - api
  - iot
  - sensor
---

# 2026-06-25 — API IoT multisala

En este paso ampliamos el sensor REST simulado para que no represente una sola sala, sino varias.

Antes solo existía:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

Ahora el mismo patrón de URL sirve para varias habitaciones:

```text
http://127.0.0.1:8001/api/rooms/A-101
http://127.0.0.1:8001/api/rooms/A-102
http://127.0.0.1:8001/api/rooms/A-103
```

## Por qué hacemos esto

En un sistema IoT real no queremos escribir una URL completamente distinta para cada objeto BIM.

Queremos un patrón:

```text
/api/rooms/{room}
```

Y que cada objeto BIM aporte su parte variable:

```javascript
object.userData.room
```

Así, si una sala tiene:

```text
userData.room = A-102
```

la URL generada será:

```text
http://127.0.0.1:8001/api/rooms/A-102
```

## Qué cambió en el sensor simulado

El archivo:

```text
examples/mock-sensor/server.py
```

ahora contiene un diccionario `ROOMS`:

```python
ROOMS = {
    "A-101": {...},
    "A-102": {...},
    "A-103": {...},
}
```

Cada sala tiene:

- un `ifcGlobalId` de demostración;
- una temperatura simulada;
- un CO₂ simulado;
- una variación distinta para que no todas las salas parezcan iguales.

## Nueva ruta de consulta de salas

También se añadió:

```text
http://127.0.0.1:8001/api/rooms
```

Esta ruta devuelve la lista de salas simuladas:

```json
{
  "rooms": ["A-101", "A-102", "A-103"]
}
```

## Importante: reiniciar el servidor

Si el sensor ya estaba arrancado antes de este cambio, seguirá usando la versión antigua.

Para cargar el código nuevo:

1. vuelve a la terminal donde está corriendo el sensor;
2. pulsa `Ctrl+C`;
3. arráncalo otra vez:

   ```powershell
   .\scripts\start-mock-sensor.ps1
   ```

## Pruebas rápidas

Desde PowerShell:

```powershell
Invoke-RestMethod http://127.0.0.1:8001/api/rooms
Invoke-RestMethod http://127.0.0.1:8001/api/rooms/A-101
Invoke-RestMethod http://127.0.0.1:8001/api/rooms/A-102
Invoke-RestMethod http://127.0.0.1:8001/api/rooms/A-103
```

Cada sala debe devolver su propio `room`, su propio `ifcGlobalId` y valores distintos de CO₂.

## Relación con BIMROCKET

Este cambio prepara el siguiente ejercicio en BIMROCKET:

- duplicar o crear varias salas;
- asignar a cada una su `userData.room`;
- reutilizar la fórmula:

  ```javascript
  "http://127.0.0.1:8001/api/rooms/" + object.userData.room
  ```

Con esto veremos el salto importante: el controlador ya no está “pegado” a `A-101`, sino al identificador de la sala.
