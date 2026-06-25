---
title: "Lección 1: del sensor al modelo"
tags:
  - fundamentos
  - sensor
  - controlador
  - rest
status: completada
---

# Lección 1: del sensor al modelo

## Objetivo

Comprender el recorrido completo de un dato IoT en BIMROCKET antes de escribir
código o conectar un dispositivo físico.

## Conocimientos previos

No se requiere experiencia con Java, Three.js, IFC, MQTT o Brain4it. Solo
necesitamos reconocer que un sensor produce un valor, por ejemplo una
temperatura de `24.5 °C`.

## Las cinco piezas

### 1. Sensor

Mide una magnitud física: temperatura, humedad, concentración de CO₂,
presencia, consumo eléctrico o estado de una máquina.

### 2. Gateway o plataforma IoT

Recibe el protocolo del dispositivo y presenta el dato de una forma que una
aplicación web pueda consumir. BIMROCKET no implementa directamente un broker
MQTT, un servidor BACnet ni un historiador de series temporales.

### 3. Controlador de entrada

Un controlador pertenece a un objeto de la escena. `RestPollController`
consulta periódicamente una URL, conserva la respuesta y comunica a la escena
que el objeto ha cambiado.

### 4. Fórmula

Una fórmula conecta la salida de un controlador con la entrada de otro. Por
ejemplo, puede enviar el valor de CO₂ al controlador encargado del color.

### 5. Controlador visual o de actuación

`ColorController` interpola un valor entre dos colores. `DisplayController`
muestra un número y sus unidades. Otros controladores pueden mover objetos,
encender luces o enviar órdenes a servicios externos.

## Ejemplo conceptual

Una API entrega:

```json
{
  "room": "A-101",
  "temperature": 24.5,
  "co2": 1250
}
```

El recorrido del CO₂ sería:

```text
jsonOutput.co2
→ fórmula
→ controllers.color.input
→ interpolación entre 400 y 1500 ppm
→ color del espacio IFC
```

## Comprobación de comprensión

Antes del laboratorio debemos poder responder:

1. ¿Por qué BIMROCKET no necesita hablar directamente MQTT con el sensor?
2. ¿Qué función cumple `RestPollController`?
3. ¿Qué pieza relaciona la salida REST con el color?
4. ¿Cambiar el color modifica el valor físico del sensor?

## Conclusiones

- El campo `room` puede identificar la sala y `co2` contiene la medición.
- Un `ifcGlobalId` es más fiable que un nombre porque identifica de manera
  única al objeto IFC.
- Con un intervalo de *polling* de 10 segundos, el retraso máximo esperado es
  aproximadamente de 10 segundos.
- Una misma lectura puede alimentar varios controladores sin repetir la
  consulta a la API.
- Un valor antiguo procedente de un sensor desconectado debe representarse
  como estado desconocido, no como una medición actual válida.

## Siguiente paso

En el primer laboratorio construiremos una API local que simule temperatura y
CO₂. Después conectaremos BIMROCKET a esa API sin utilizar todavía hardware.

## Referencias al código

- [`Controller.js`](https://github.com/bimrocket/bimrocket/blob/bc04faafd3b1bf3f53ad004a73241325bd30d237/bimrocket-webapp/src/main/webapp/js/controllers/Controller.js)
- [`RestPollController.js`](https://github.com/bimrocket/bimrocket/blob/bc04faafd3b1bf3f53ad004a73241325bd30d237/bimrocket-webapp/src/main/webapp/js/controllers/RestPollController.js)
- [`ColorController.js`](https://github.com/bimrocket/bimrocket/blob/bc04faafd3b1bf3f53ad004a73241325bd30d237/bimrocket-webapp/src/main/webapp/js/controllers/ColorController.js)
- [`Formula.js`](https://github.com/bimrocket/bimrocket/blob/bc04faafd3b1bf3f53ad004a73241325bd30d237/bimrocket-webapp/src/main/webapp/js/formula/Formula.js)
