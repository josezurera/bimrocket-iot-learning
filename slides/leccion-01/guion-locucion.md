# Guion de locución — Lección 1

Este guion está pensado para una voz española, natural, pausada y didáctica.  
No busca leer las diapositivas palabra por palabra, sino acompañar el razonamiento.

Duración estimada: 12–18 minutos, según ritmo y pausas en BIMROCKET.

---

## Diapositiva 1 — Portada

Bienvenido a esta primera lección de BIMROCKET más IoT.

En esta clase vamos a construir el primer flujo completo: desde una lectura de sensor simulada hasta una sala BIM que muestra, colorea y valida ese dato.

No hace falta que tengas todavía una placa real conectada. Para aprender bien el proceso, vamos a empezar con una API REST simulada. Así nos centramos en lo importante: cómo viaja el dato y cómo lo interpreta el modelo.

---

## Diapositiva 2 — Objetivo de la lección

El objetivo es entender este camino: sensor, dato JSON, objeto BIM, visualización y validación.

Fíjate en que no hablamos solo de ver un número en pantalla. La gracia está en que ese número llegue al objeto correcto y que el modelo pueda reaccionar.

Esa es la base de un gemelo digital: geometría, identidad, datos vivos y reglas.

---

## Diapositiva 3 — Qué vas a construir

En esta lección tenemos una escena sencilla con dos salas: la A-101 y la A-102.

Cada sala consulta su propio dato de CO₂, lo muestra en un panel y cambia de color según el valor recibido.

Además, añadimos dos estados de control: si el sensor está offline, la sala se pone gris; y si el dato no pertenece a esa sala, se pone morada.

Esto último es importante porque nos mete en un tema clave: la confianza del dato.

---

## Diapositiva 4 — El sensor devuelve JSON

Aquí vemos una respuesta típica de nuestra API.

La API devuelve información de una sala concreta: nombre de la sala, identificador IFC simulado, temperatura, CO₂, hora de la medición y estado del sensor.

Este formato se llama JSON. Puedes verlo como una forma ordenada de mandar datos entre sistemas.

Por ahora no necesitamos dominar programación. Solo necesitamos entender que BIMROCKET va a leer estos campos.

---

## Diapositiva 5 — Camino del dato

Este es el flujo completo.

Primero tenemos el sensor simulado. Ese sensor publica datos a través de una API REST.

BIMROCKET llama a esa API mediante un controlador. El controlador recibe JSON. Después, otras partes del objeto usan ese JSON para mostrar valores, cambiar colores o comprobar si el dato es confiable.

Si entiendes este dibujo, entiendes la columna vertebral de la lección.

---

## Diapositiva 6 — Identidad BIM + IoT

Aquí viene una idea muy importante.

No basta con que una API nos dé un número de CO₂. Necesitamos saber a qué objeto BIM pertenece ese número.

Si no, podríamos estar coloreando la sala equivocada.

Por eso hablamos de identidad BIM más identidad IoT.

---

## Diapositiva 7 — A-101: el objeto sabe quién es

En esta captura está seleccionada la sala A-101.

Abajo, en el inspector, vemos sus propiedades propias: `room` e `ifcGlobalId`.

El campo `room` es el que usaremos para pedir el dato correcto a la API.

La idea es sencilla: antes de pedir datos externos, el objeto BIM tiene que saber quién es.

---

## Diapositiva 8 — A-102: misma lógica, otro objeto

Ahora estamos viendo la A-102.

La estructura es la misma, pero los valores son distintos.

Esto es importante porque no queremos construir una solución artesanal para cada sala. Queremos una lógica reutilizable.

La misma regla debe servir para A-101, A-102 y, más adelante, para muchas más salas.

---

## Diapositiva 9 — Leer datos desde la API

En este punto ya tenemos objetos con identidad.

Ahora necesitamos traer datos vivos.

BIMROCKET lo hace preguntando cada cierto tiempo a una dirección web. Esa dirección devuelve el JSON con la lectura actual.

---

## Diapositiva 10 — RestPollController en A-101

Aquí aparece el `RestPollController` de la A-101.

Este controlador consulta una URL concreta: la dirección de la API para la sala A-101.

Fíjate también en el campo `output`. Ahí vemos la respuesta que ha recibido BIMROCKET: sala, identificador, temperatura, CO₂, hora y estado.

Es decir: BIMROCKET ya tiene dentro del objeto la lectura viva del sensor.

---

## Diapositiva 11 — RestPollController en A-102

Ahora vemos lo mismo, pero para la A-102.

La lógica es idéntica. Lo que cambia es la sala consultada.

Esta es una de las ideas más importantes del laboratorio: cada objeto BIM pregunta por su propio dato.

---

## Diapositiva 12 — URL dinámica del sensor

La URL dinámica es una fórmula muy simple.

Tenemos una parte fija, que es la dirección base de la API, y luego añadimos el identificador de la sala actual.

En JavaScript, el símbolo `+` sirve aquí para unir texto.

Así BIMROCKET construye automáticamente la URL correcta para cada objeto.

---

## Diapositiva 13 — Fórmula en BIMROCKET

Aquí ya no estamos viendo solo un dibujo conceptual. Estamos viendo la fórmula real dentro de BIMROCKET.

La sala seleccionada es A-102 y el inspector está en la pestaña de fórmulas.

La clave es que la URL no contiene A-102 escrito a mano. Usa `object.userData.room`.

Eso permite que la misma fórmula funcione también para A-101.

---

## Diapositiva 14 — Mostrar el CO₂

Leer un dato no basta.

Si el usuario no lo ve o el modelo no reacciona, el dato todavía no está aportando valor.

Por eso el siguiente paso es mostrar el CO₂ dentro de BIMROCKET.

---

## Diapositiva 15 — Fórmula para mostrar CO₂

En esta fórmula tomamos el campo `co2` de la respuesta JSON.

`object.controllers.ctr_0.jsonOutput.co2` significa: entra en el controlador REST, mira su salida JSON y toma el valor de CO₂.

Ese valor se envía al controlador que muestra el panel de texto.

---

## Diapositiva 16 — Resultado visible

Aquí ya vemos el resultado en pantalla.

La sala A-101 tiene su panel de CO₂ y muestra la lectura actual en ppm.

Esto parece sencillo, pero conceptualmente es un salto importante: la sala ya no es solo geometría. Ahora está mostrando información viva.

---

## Diapositiva 17 — Validar confianza del dato

Ahora damos un paso más.

Un dato puede llegar correctamente y aun así no ser confiable.

Por ejemplo, imagina que una sala recibe por error la medición de otra sala. El número existe, pero no debemos usarlo para colorear ese objeto.

Por eso añadimos una validación.

---

## Diapositiva 18 — iotMatch

`iotMatch` compara dos cosas.

Por un lado, la sala que el objeto cree ser: `object.userData.room`.

Por otro lado, la sala que viene en la respuesta de la API: `jsonOutput.room`.

Si ambas coinciden, el dato pertenece al objeto. Si no coinciden, marcamos el dato como no confiable.

---

## Diapositiva 19 — iotMatch en A-102

Aquí vemos esa comparación dentro de BIMROCKET.

La fórmula comprueba si la sala guardada en el objeto coincide con la sala recibida desde la API.

Esta comprobación es pequeña, pero conceptualmente es enorme: evita que el modelo acepte cualquier dato sin preguntarse si pertenece al objeto correcto.

---

## Diapositiva 20 — Estados visuales

Usamos tres estados visuales.

Verde a rojo cuando el dato es válido y representa el nivel de CO₂.

Gris cuando el sensor está offline.

Morado cuando la identidad no coincide y, por tanto, no confiamos en el dato.

Esta prioridad evita confusiones.

---

## Diapositiva 21 — Reglas finales de color

La fórmula parece larga, pero la lógica es sencilla.

Primero preguntamos: ¿el dato no coincide con la sala? Si no coincide, morado.

Si sí coincide, preguntamos: ¿el sensor está offline? Si está offline, gris.

Y si ninguna de esas dos cosas ocurre, usamos la escala normal de CO₂.

---

## Diapositiva 22 — Prioridad de confianza

Esta tabla resume la regla.

Primero va la identidad incorrecta, porque es el fallo más grave.

Después va el estado offline, porque no tenemos dato vivo.

Y por último va la escala de CO₂, que solo tiene sentido cuando el dato es válido.

---

## Diapositiva 23 — Pruebas realizadas

No basta con configurar.

Hay que probar los estados importantes.

En sistemas IoT, una parte del trabajo consiste en comprobar qué pasa cuando todo va bien, pero también qué pasa cuando algo falla.

---

## Diapositiva 24 — Prueba 1: caso normal

La primera prueba es el caso normal.

El sensor está online, la identidad coincide y la sala se colorea según el CO₂.

Este es el comportamiento esperado cuando todo funciona.

---

## Diapositiva 25 — Prueba 2: sensor offline

Después forzamos el estado offline añadiendo un parámetro temporal a la URL.

Esto nos permite comprobar que BIMROCKET detecta el estado y cambia el color a gris.

Así sabemos que el modelo no solo responde a valores de CO₂, sino también al estado de disponibilidad del sensor.

---

## Diapositiva 26 — Prueba 3: identidad incorrecta

La tercera prueba fuerza una identidad incorrecta.

Hacemos que la fórmula compare contra una sala falsa, A-999.

El resultado esperado es que `iotMatch` sea falso y la sala se ponga morada.

Esta prueba demuestra que el modelo no acepta cualquier dato sin comprobarlo.

---

## Diapositiva 27 — Modelo final

El archivo final queda guardado como referencia del laboratorio.

Contiene dos salas conectadas, URL dinámica, paneles de CO₂, validación de identidad y reglas visuales.

Este archivo es importante porque nos permite retomar el curso desde otro equipo sin perder el estado del aprendizaje.

---

## Diapositiva 28 — Cierre conceptual

La idea de cierre es esta:

un gemelo digital no es solo un modelo 3D.

Es geometría más identidad, más datos vivos, más reglas de confianza.

En esta lección hemos construido una versión mínima de esa idea.

---

## Diapositiva 29 — Siguiente paso

En la siguiente fase podremos cambiar el sensor simulado por un sensor real con ESP32.

Y esto es lo bonito: la lógica aprendida se mantiene.

Solo cambia la fuente del dato.

Hoy el dato viene de Python. Mañana puede venir de una placa física conectada por WiFi.

