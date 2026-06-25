---
title: "Continuar en otro equipo"
tags:
  - setup
  - entorno
  - reanudacion
---

# Continuar el curso en otro equipo

Esta guía deja el curso preparado para retomarlo desde cualquier equipo con
Git, Python y un navegador moderno.

## 1. Clonar los repositorios

El curso y BIMROCKET viven en repositorios distintos. Lo más cómodo es clonarlos
como carpetas hermanas:

```powershell
mkdir bimrocket-workspace
cd bimrocket-workspace

git clone https://github.com/josezurera/bimrocket-iot-learning.git
git clone https://github.com/bimrocket/bimrocket.git
```

La estructura esperada queda así:

```text
bimrocket-workspace/
├─ bimrocket-iot-learning/
└─ bimrocket/
```

## 2. Comprobar el entorno

Desde el repositorio del curso:

```powershell
cd bimrocket-iot-learning
.\scripts\check-environment.ps1
```

El script comprueba que existen `git`, `python` y el repositorio de BIMROCKET
en la ubicación esperada.

Si PowerShell bloquea la ejecución de scripts, usa esta forma:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\check-environment.ps1
```

## 3. Arrancar el sensor REST simulado

En el primer terminal:

```powershell
cd bimrocket-iot-learning
.\scripts\start-mock-sensor.ps1
```

El sensor queda disponible en:

```text
http://127.0.0.1:8001/api/rooms/A-101
```

Para simular una sala sin dato disponible:

```text
http://127.0.0.1:8001/api/rooms/A-101?offline=1
```

## 4. Arrancar BIMROCKET

En un segundo terminal:

```powershell
cd bimrocket-iot-learning
.\scripts\start-bimrocket-static.ps1
```

Abre:

```text
http://127.0.0.1:8000/app.html
```

## 5. Punto actual del laboratorio

El último punto completado fue conectar un `RestPollController` de BIMROCKET
con el sensor REST local.

Estado conseguido:

- objeto de ejemplo: `Sala_A-101`;
- controlador REST generado automáticamente como `ctr_0`;
- URL del controlador:

  ```text
  http://127.0.0.1:8001/api/rooms/A-101
  ```

- el controlador recibe lecturas en `output` y `jsonOutput`.

Siguiente paso:

```javascript
object.controllers.ctr_0.jsonOutput.co2
```

Esa expresión se usará como entrada de un `DisplayController` para mostrar el
CO₂ de la sala dentro de BIMROCKET.

## 6. Si no existe el modelo guardado

Si no tienes un archivo `.brf` guardado del laboratorio anterior, recrea el
estado mínimo:

1. abre BIMROCKET;
2. crea una caja;
3. renómbrala como `Sala_A-101`;
4. añade un `RestPollController`;
5. si no permite nombrarlo manualmente, deja que BIMROCKET genere `ctr_0`;
6. configura la URL del sensor REST;
7. confirma los campos editados con `Enter`;
8. inicia el controlador desde el menú contextual de su encabezado.

Detalles aprendidos:

- `started` es un indicador de solo lectura;
- los campos editables necesitan confirmación con `Enter`;
- si la URL queda vacía, el controlador puede consultar la página actual de
  BIMROCKET en vez del sensor;
- el nombre generado `ctr_0` es válido y reutilizable en fórmulas.
