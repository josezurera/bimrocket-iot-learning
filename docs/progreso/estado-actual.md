---
title: "Estado actual"
tags:
  - progreso
  - checkpoint
  - laboratorio
---

# Estado actual del curso

Última actualización: 25 de junio de 2026.

## Punto alcanzado

Ya se completó la primera conexión práctica entre un sensor REST simulado y
BIMROCKET.

Se consiguió:

- ejecutar una API local en `http://127.0.0.1:8001`;
- obtener lecturas JSON de la sala `A-101`;
- diferenciar estados `online` y `offline`;
- abrir BIMROCKET desde `http://127.0.0.1:8000/app.html`;
- crear una caja que representa la sala `Sala_A-101`;
- añadir un `RestPollController`;
- conectar ese controlador con:

  ```text
  http://127.0.0.1:8001/api/rooms/A-101
  ```

- recibir datos en `output` y `jsonOutput`.

## Nombre real del controlador usado

El controlador quedó con nombre automático:

```text
ctr_0
```

Por tanto, para leer el CO₂ en una fórmula de BIMROCKET hay que usar:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

Si en otro intento el controlador se llama de otra manera, sustituye `ctr_0`
por el nombre real que aparezca en el inspector.

## Siguiente paso

Añadir un `DisplayController` al mismo objeto y alimentar su entrada con:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

Objetivo del siguiente tramo:

- comprobar que el valor de CO₂ ya no solo llega al inspector;
- mostrarlo visualmente en el modelo;
- preparar después una regla de color para distinguir aire correcto, advertencia
  y alarma.

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

## Nota sobre el archivo del modelo

Si existe un archivo `.brf` guardado del laboratorio, se puede cargar y continuar
desde ahí. Si no existe, el estado mínimo se recrea en pocos pasos siguiendo
`Continuar en otro equipo`.
