# BIMROCKET IoT Learning

Curso práctico y base de conocimiento sobre la integración de IoT en edificios
mediante BIMROCKET.

El contenido se escribe en Markdown y se publica como documentación navegable
con Material for MkDocs.

## Continuar desde otro equipo

Este repositorio está preparado para poder retomar el curso sin depender de la
sesión original de Codex.

```powershell
git clone https://github.com/josezurera/bimrocket-iot-learning.git
git clone https://github.com/bimrocket/bimrocket.git
```

Recomendación de carpetas:

```text
tu-carpeta-de-trabajo/
├─ bimrocket-iot-learning/
└─ bimrocket/
```

Después puedes arrancar el sensor simulado y BIMROCKET con:

```powershell
cd bimrocket-iot-learning
.\scripts\start-mock-sensor.ps1
```

En otro terminal:

```powershell
cd bimrocket-iot-learning
.\scripts\start-bimrocket-static.ps1
```

Abre BIMROCKET en:

```text
http://127.0.0.1:8000/app.html
```

El punto exacto de reanudación está en
`docs/progreso/estado-actual.md`.

Si PowerShell bloquea los scripts, ejecútalos con:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\nombre-del-script.ps1
```

## Uso local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
mkdocs serve
```

La documentación estará disponible en `http://127.0.0.1:8000`.

## Principios del curso

- Aprender cada concepto antes de utilizarlo.
- Recorrer datos reales desde el sensor hasta el modelo 3D.
- Vincular las explicaciones con código concreto de BIMROCKET.
- Conservar ejercicios reproducibles y preguntas pendientes.
