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

- recibir datos en `output` y `jsonOutput`;
- añadir un `DisplayController` como `ctr_1`;
- crear fórmulas para conectar `ctr_0.jsonOutput.co2` con
  `ctr_1.input`;
- mostrar el CO₂ en un panel visual como `ppm`.

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

Usar el valor de CO₂ para colorear la sala.

La conexión visual ya conseguida fue:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

con destino:

```text
controllers.ctr_1.input
```

Objetivo del siguiente tramo:

- añadir un `ColorController`;
- definir una regla de color para distinguir aire correcto, advertencia y
  alarma;
- decidir cómo representar el estado `offline`.

## Conceptos aclarados

La sesión del 25 de junio de 2026 dejó documentados estos conceptos:

- qué es `RestPollController`;
- por qué se usa para consultar APIs REST de IoT;
- qué diferencia hay entre `output` y `jsonOutput`;
- qué significa `object` en una fórmula;
- qué significa el punto `.` como acceso a propiedades;
- qué diferencia hay entre `path` y `expression`;
- por qué los textos llevan comillas y los números no;
- por qué puede ser necesario pulsar `Reconstruir` para evaluar fórmulas.

Ver:

```text
docs/progreso/2026-06-25-restpoll-formulas-display.md
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

## Nota sobre el archivo del modelo

Los modelos del laboratorio ya están versionados en GitHub:

```text
examples/bimrocket-models/lab-01-sensor-rest.brf
examples/bimrocket-models/lab-01-co2-display-color-offline.brf
```

Para continuar desde otro equipo, clona el repositorio, arranca el sensor y
BIMROCKET, y abre el `.brf` correspondiente desde **Abrir del disco local**.
