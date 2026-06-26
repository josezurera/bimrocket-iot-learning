# Narrativa audiovisual — Lección 1

## Idea central

Esta lección no va de “pintar una caja en BIMROCKET”.

Va de entender una idea mucho más potente:

> un modelo BIM empieza a comportarse como gemelo digital cuando sus objetos tienen identidad, reciben datos vivos y aplican reglas de confianza.

La historia de la clase debe sentirse como una transición:

```text
modelo 3D estático
→ objeto BIM identificado
→ dato IoT recibido
→ visualización útil
→ validación de confianza
```

## Promesa para el alumno

Al terminar la lección, el alumno debería poder explicar con sus propias palabras:

- qué papel cumple una API REST en un sistema IoT;
- por qué el dato llega en formato JSON;
- cómo BIMROCKET lee ese dato;
- por qué una sala necesita identidad propia;
- cómo se muestra el CO₂ dentro del modelo;
- cómo se colorea una sala según el estado del sensor;
- por qué no basta con recibir datos: hay que validar que pertenecen al objeto correcto.

## Tono de la clase

Tono recomendado:

- español de España, natural y pausado;
- técnico, pero no académico;
- cercano, como si el profesor estuviera acompañando al alumno dentro del proceso;
- sin vender humo: lo importante es que el alumno entienda el mecanismo.

Frase guía:

> “Vamos despacio, porque aquí está la base de casi todo lo que haremos después.”

## Estructura narrativa

### 1. Abrir con el problema

Los modelos BIM suelen verse como geometría: salas, muros, puertas, instalaciones.

Pero en operación de edificios necesitamos saber qué está pasando ahora.

La pregunta inicial es:

> ¿cómo hago que una sala BIM reciba una lectura de un sensor y reaccione visualmente?

### 2. Presentar el flujo mínimo

Antes de usar hardware real, usamos un sensor simulado.

Esto no es una trampa: es una forma limpia de aprender.

> “Primero aprendemos el flujo del dato. Más adelante cambiaremos la fuente por una placa ESP32 real.”

### 3. Convertir la sala en un objeto conectado

La sala no puede ser solo una caja.

Tiene que tener identidad:

- `room`, para hablar con la API;
- `ifcGlobalId`, para representar la identidad BIM/IFC.

Idea clave:

> “Si el dato no sabe a qué objeto pertenece, no tenemos un gemelo digital; tenemos números sueltos.”

### 4. Leer el dato vivo

BIMROCKET usa `RestPollController` como cliente que pregunta periódicamente a la API.

Explicación sencilla:

> “Cada cierto tiempo, BIMROCKET llama a una dirección web local y recibe una pequeña respuesta en JSON.”

### 5. Mostrar y colorear

Una vez llega el CO₂:

- `DisplayController` lo muestra como texto;
- `ColorController` lo convierte en una señal visual.

Esto convierte el dato en algo operativo:

> “Ya no necesito abrir una tabla para saber qué sala está peor. El modelo me lo dice visualmente.”

### 6. Introducir confianza

La lección gana fuerza cuando aparece el problema de confianza:

> “Que llegue un dato no significa que debamos creérnoslo automáticamente.”

Por eso probamos:

- caso normal;
- sensor offline;
- identidad incorrecta.

La prioridad visual queda así:

```text
identidad incorrecta → morado
offline → gris
CO₂ válido → verde/rojo
```

### 7. Cerrar conectando con el futuro

La lección termina preparando el salto a hardware real:

> “Cuando pasemos al ESP32, la lógica no cambia. Solo cambia quién produce el dato.”

Ese cierre da continuidad al curso y prepara la siguiente etapa.

## Mensaje comercial de fondo

Esta lección debe vender una idea sin decirla de forma agresiva:

> BIM + IoT no es una moda. Es una metodología para conectar el modelo digital con el comportamiento real del edificio.

## Frase final recomendada

> “Hoy hemos conectado una sala a un sensor simulado. En la siguiente fase, esa misma lógica empezará a salir del ordenador y entrará en el mundo físico.”

