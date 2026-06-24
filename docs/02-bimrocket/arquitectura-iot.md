---
title: Arquitectura IoT de BIMROCKET
tags:
  - arquitectura
  - bimrocket
  - brain4it
---

# Arquitectura IoT de BIMROCKET

BIMROCKET actúa principalmente como consumidor, representación y superficie de
control. La adquisición de dispositivos y los históricos suelen pertenecer a
una plataforma externa.

## Canales de integración principales

| Canal | Entrada | Salida | Uso |
|---|---:|---:|---|
| REST genérico | Sí | Sí | APIs HTTP y gateways |
| Brain4it Watch | Sí | No | Observación de valores remotos |
| Brain4it Post | No | Sí | Envío de datos y órdenes |
| WFS | Sí | Limitada | Información geográfica |
| Scripts | Interna | Interna | Lógica personalizada del modelo |

## Ciclo de eventos

1. Un controlador recibe o genera un cambio.
2. BIMROCKET llama a `notifyObjectsChanged`.
3. Los controladores interesados reciben un evento `nodeChanged`.
4. Se recalculan las fórmulas dependientes.
5. Los controladores actualizan geometría, materiales, paneles o servicios.

