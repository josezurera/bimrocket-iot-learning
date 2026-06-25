# Modelos BIMROCKET del curso

Esta carpeta contiene modelos `.brf` usados en los laboratorios.

Los archivos `.brf` son modelos nativos de BIMROCKET. Guardan la geometría, los
controladores y las fórmulas del laboratorio.

## Archivos

### `lab-01-sensor-rest.brf`

Estado base del laboratorio:

- sala `Sala_A-101`;
- caja simple como representación geométrica;
- `ctr_0 = RestPollController`;
- URL del sensor:

  ```text
  http://127.0.0.1:8001/api/rooms/A-101
  ```

### `lab-01-co2-display-color-offline.brf`

Estado completo del laboratorio de CO₂:

- `ctr_0 = RestPollController`;
- `ctr_1 = DisplayController`;
- `co2_color = ColorController`;
- panel visual con CO₂ en `ppm`;
- color de sala según CO₂;
- color gris cuando `status` es `offline`.

## Cómo usarlos

1. Arranca el sensor:

   ```powershell
   .\scripts\start-mock-sensor.ps1
   ```

2. Arranca BIMROCKET:

   ```powershell
   .\scripts\start-bimrocket-static.ps1
   ```

3. Abre:

   ```text
   http://127.0.0.1:8000/app.html
   ```

4. Usa **Abrir del disco local** y selecciona el `.brf`.

5. Si los controladores no arrancan automáticamente, ve al inspector de la sala
   y arráncalos desde el menú contextual.

