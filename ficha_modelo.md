# Ficha del modelo de riesgo de mala reseña

## 1. ¿Para qué sirve?

El modelo estima la probabilidad de que un pedido reciba una mala reseña de **1 o 2 estrellas** en el momento en que el pedido ya fue entregado.

Su objetivo es ayudar al equipo de atención al cliente de Olist a identificar qué pedidos deberían recibir atención prioritaria, considerando que solo se puede contactar aproximadamente al 10% de los clientes.

El modelo **no debe utilizarse para castigar automáticamente a vendedores**, cancelar pedidos o tomar decisiones sin supervisión humana.

## 2. Datos utilizados

Se utilizaron datos de Olist disponibles en la base de datos del proyecto, con pedidos anteriores al **1 de junio de 2018**.

La tabla final contiene **77,304 pedidos entregados y con reseña conocida**.

Se utilizaron variables relacionadas con:

- fechas del pedido y de entrega;
- ubicación del cliente y del vendedor;
- cantidad de artículos;
- cantidad de vendedores;
- precio y flete;
- peso y fotografías del producto;
- categoría;
- método de pago y cuotas.

No se utilizó información de la reseña como entrada del modelo, ya que esa información todavía no existe al momento de realizar la predicción.

## 3. ¿Qué tan bien funciona?

La evaluación principal se realizó utilizando una división temporal: los pedidos más antiguos se utilizaron para entrenamiento y los más recientes para validación.

La métrica utilizada fue la **precisión dentro del 10% de pedidos con mayor riesgo**.

Los resultados obtenidos fueron:

- Regresión Logística: **44.47%**
- XGBoost: **44.25%**
- Regla basada únicamente en retraso: **33.04%**
- Selección al azar: **11.27%**

La Regresión Logística obtuvo el mejor resultado global y fue seleccionada como modelo final.

En términos simples, de cada 10 clientes priorizados por el modelo, aproximadamente **4 de ellos terminaron dejando una mala reseña** durante el periodo de validación.

El umbral utilizado para considerar un pedido como riesgo alto es aproximadamente **0.6844**.

## 4. Límites conocidos

El desempeño puede cambiar cuando las condiciones futuras son diferentes a las observadas durante el entrenamiento.

Por ejemplo, el modelo puede perder capacidad de discriminación en periodos con muy pocos retrasos, cambios logísticos importantes o nuevas categorías y vendedores.

También pueden existir valores faltantes o situaciones poco frecuentes que dificulten la predicción.

El resultado debe entenderse como una probabilidad de riesgo y no como una certeza.

## 5. ¿A quién puede afectar un error?

Un **falso positivo** ocurre cuando el modelo considera que un pedido tiene alto riesgo, pero finalmente el cliente no deja una mala reseña. Esto podría hacer que el equipo de atención utilice tiempo en un cliente que no necesitaba intervención.

Un **falso negativo** ocurre cuando un pedido no es identificado como riesgo alto, pero posteriormente recibe una mala reseña. En este caso se pierde la oportunidad de atender al cliente antes de que publique su experiencia negativa.

El modelo tampoco debe utilizarse para penalizar directamente a vendedores, ya que algunos problemas pueden depender del transporte u otros factores fuera de su control.

## 6. Recomendación de uso

Se recomienda utilizar el modelo como una herramienta de apoyo para priorizar contactos con clientes.

Las decisiones importantes deben mantener supervisión humana y considerar información adicional sobre el pedido.

También se recomienda revisar periódicamente el desempeño del modelo y volver a entrenarlo cuando existan cambios importantes en el comportamiento de los pedidos, vendedores o procesos logísticos.