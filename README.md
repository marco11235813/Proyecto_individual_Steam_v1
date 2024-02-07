![Pandas](https://img.shields.io/badge/-Pandas-333333?style=flat&logo=pandas)
![Numpy](https://img.shields.io/badge/-Numpy-333333?style=flat&logo=numpy)
![Matplotlib](https://img.shields.io/badge/-Matplotlib-333333?style=flat&logo=matplotlib)
![Seaborn](https://img.shields.io/badge/-Seaborn-333333?style=flat&logo=seaborn)
![Scikitlearn](https://img.shields.io/badge/-Scikitlearn-333333?style=flat&logo=scikitlearn)
![FastAPI](https://img.shields.io/badge/-FastAPI-333333?style=flat&logo=fastapi)
![Render](https://img.shields.io/badge/-Render-333333?style=flat&logo=render)

# Prueba de concepto para proyecto de Steam

## Introducción

Este proyecto simula el rol de un MLOps Engineer, es decir, la combinación de un Data Engineer y Data Scientist, para la plataforma multinacional de videojuegos Steam. Para su desarrollo, se entregan unos datos y se solicita un Producto Mínimo Viable que muestre una API deployada en un servicio en la nube y la aplicación de dos modelos de Machine Learning, por una lado, un análisis de sentimientos sobre los comentarios de los usuarios de los juegos y, por otro lado, la recomendación de juegos a partir de dar el nombre de un juego y/o a partir de los gustos de un usuario en particular.

## Contexto

Steam es una plataforma de distribución digital de videojuegos desarrollada por Valve Corporation. Fue lanzada en septiembre de 2003 como una forma para Valve de proveer actualizaciones automáticas a sus juegos, pero finalmente se amplió para incluir juegos de terceros. Cuenta con más de 325 millones de usuarios y más de 25.000 juegos en su catálogo. Es importante tener en cuenta que las cifras publicadas por SteamSpy son hasta el año 2017, porque a principios de 2018 Steam limitó la forma de obtener estadísticas, por eso no hay datos tan precisos.

## Datos

Para este proyecto se proporcionaron tres archivos JSON:

* **australian_user_reviews.json** es un dataset que contiene los comentarios que los usuarios realizaron sobre los juegos que consumen, además de datos adicionales como si recomiendan o no ese juego, emoticones de gracioso y estadísticas de si el comentario fue útil o no para otros usuarios. También presenta el id del usuario que comenta con su url del perfil y el id del juego que comenta.

* **australian_users_items.json** es un dataset que contiene información sobre los juegos que juegan todos los usuarios, así como el tiempo acumulado que cada usuario jugó a un determinado juego.

* **output_steam_games.json** es un dataset que contiene datos relacionados con los juegos en sí, como los título, el desarrollador, los precios, características técnicas, etiquetas, entre otros datos.

En el documento [Diccionario de datos](https://github.com/marco11235813/Proyecto_individual_Steam_v1/blob/main/Diccionario_de_datos_STEAM.md) se encuetran los detalles de cada una de las variables de los conjuntos de datos.

## Tareas desarrolladas

### Transformaciones

Se realizó la extracción, transformación y carga (ETL) de los tres conjuntos de datos entregados. Dos de los conjuntos de datos se encontraban anidados, es decir había columnas con diccionarios o listas de diccionarios, por lo que aplicaron distintas estrategias para transformar las claves de esos diccionarios en columnas. Luego se rellenaron algunos nulos de variables necesarias para el proyecto, se borraron columnas con muchos nulos o que no aportaban al proyecto, para optimizar el rendimiento de la API y teneniendo en cuenta las limitaciones de almacenamiento del deploy. Para las transformaciones se utilizó la librería Pandas.

Los detalles del ETL se puede ver en las carpetas [steam_games](https://github.com/marco11235813/Proyecto_individual_Steam_v1/tree/main/steam_games), [users_items](https://github.com/marco11235813/Proyecto_individual_Steam_v1/tree/main/users_items) y [user_reviews](https://github.com/marco11235813/Proyecto_individual_Steam_v1/tree/main/user_reviews).

### Feature engineering

Uno de los pedidos para este proyecto fue aplicar un análisis de sentimiento a los reviews de los usuarios. Para ello se creó una nueva columna llamada 'sentiment_analysis' que reemplaza a la columna que contiene los reviews donde clasifica los sentimientos de los comentarios con la siguiente escala:

* 0 si es malo,
* 1 si es neutral o esta sin review
* 2 si es positivo.

Dado que el objetivo de este proyecto es realizar una prueba de concepto, se realiza un análisis de sentimiento básico utilizando TextBlob que es una biblioteca de procesamiento de lenguaje natural (NLP) en Python. El objetivo de esta metodología es asignar un valor numérico a un texto, en este caso a los comentarios que los usuarios dejaron para un juego determinado, para representar si el sentimiento expresado en el texto es negativo, neutral o positivo. 

Esta metodología toma una revisión de texto como entrada, utiliza TextBlob para calcular la polaridad de sentimiento y luego clasifica la revisión como negativa, neutral o positiva en función de la polaridad calculada. En este caso, se consideraron las polaridades por defecto del modelo, el cuál utiliza umbrales -0.1 y 0.1, siendo polaridades negativas por debajo de -0.1, positivas por encima de 0.1 y neutrales entre medio de ambos.

Por otra parte, y bajo el mismo criterio de optimizar los tiempos de respuesta de las consultas en la API y teniendo en cuenta las limitaciones de almacenamiento en el servicio de nube para deployar la API, se realizaron dataframes auxiliares para cada una de las funciones solicitadas. En el mismo sentido, se guardaron estos dataframes en formato *parquet* que permite una compresión y codificación eficiente de los datos.

Todos los detalles del desarrollo se pueden ver en la carpeta [feature_engineer](https://github.com/marco11235813/Proyecto_individual_Steam_v1/blob/main/feature_engineer/feature_engineer-v1.ipynb
).

### Análisis exploratorio de los datos

Se realizó el EDA a los tres conjuntos de datos sometidos a ETL con el objetivo de identificar las variables que se pueden utilizar en la creación del modelo de recmendación. Para ello se utilizó la librería Pandas para la manipulación de los datos y las librerías Matplotlib y Seaborn para la visualización.

En particular para el modelo de recomendación, se terminó eligiendo construir un dataframe específico con el id del usuario que realizaron reviews, los nombres de los juegos a los cuales se le realizaron comentarios y una columna de rating que se construyó a partir de la combinación del análisis de sentimiento y la recomendación a los juegos.

El desarrollo de este análisis se encuentra en la carpeta EDA, en el archivo .ipynb [EDA](https://github.com/marco11235813/Proyecto_individual_Steam_v1/blob/main/EDA/EDA.ipynb)

### Modelo de aprendizaje automático

 Sistema de Recomendación ítem-ítem: Se desarrolló un modelo que recomienda juegos similares en base a un juego dado, utilizando similitud del coseno. Con CountVectorizer se convirtieron los textos de la columna 'specs' en vectores numéricos para posterior calcular la similitud del coseno.
Se utilizó la métrica de similitud del coseno, ya que mide el coseno del ángulo entre dos vectores. Cuanto más cercano a 1, más similares son los vectores. Este método fue clave para determinar qué tan parecidos son los juegos entre sí. Esto se utiliza para generar recomendaciones, ya que los juegos con vectores similares son considerados como recomendaciones potenciales.

El desarrollo para la creación del modelo se encuentra en la carpeta [modelo_machine_learning](https://github.com/marco11235813/Proyecto_individual_Steam_v1/blob/main/modelo_machine_learning/modelo.ipynb
).

### Desarrollo de API

Para el desarrolo de la API se decidió utilizar el framework FastAPI, creando las siguientes funciones:
* **endpoint1** (developer): En esta función tiene por parametro 'valor'  devuelve la cantidad de items y porcentaje de contenido Free por año según  la empresa desarrolladora
    ingresada.

* **endpoint2** (userdata): Esta función tiene por parámentro 'user_id' y devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendaciones que realizó sobre la cantidad de reviews que se analizan y la cantidad de items que consume el mismo.

* **endpoint3** (UserForGenre): Esta función recibe como parámetro el género de un videojuego y devuelve el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año de lanzamiento.

* **endpoint4** (best_developer_year): Esta función recibe como parámetro un año y Devuelve el top 3 de desarrolladoras con juegos MAS recomendados por usuarios para el año dado.

* **endpoint5** (developer_reviews_analysis): Esta función recibe como parámetro un desarrollador y se devuelve un diccionario con el nombre del desarrollador como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.

* **endpoint6** (item_recomendacion): Esta funcion toma como parametro el id de un juego (item) y realiza una busqueda de similitud
    para encontrar juegos similares
    esta busqueda se basa en un modelo de recomendacion centrado en la similitud del coseno
    devuelve una lista de los 5 juegos recomendados mas similares al juego ingresado

El desarrollo de las funciones se puede ver en el script [funciones_api]().

El código para generar la API se encuentra en el archivo [main.py](https://github.com/marco11235813/Proyecto_individual_Steam_v1/blob/main/main.py). 
En caso de querer ejecutar la API desde localHost se deben seguir los siguientes pasos:

- Clonar el proyecto haciendo `git clone https://github.com/IngCarlaPezzone/PI1_MLOps_videojuegos.git`.
- Preparación del entorno de trabajo en Visual Studio Code:
    * Crear entorno `Python -m venv env`
    * Ingresar al entorno haciendo `venv\Scripts\activate`
    * Instalar dependencias con `pip install -r requirements.txt`
- Ejecutar el archivo main.py desde consola activando uvicorn. Para ello, hacer `uvicorn main:app --reload`
- Hacer Ctrl + clic sobre la dirección `http://XXX.X.X.X:XXXX` (se muestra en la consola).
- Una vez en el navegador, agregar `/docs` para acceder a ReDoc.
- En cada una de las funciones hacer clic en *Try it out* y luego introducir el dato que requiera o utilizar los ejemplos por defecto. Finalmente Ejecutar y observar la respuesta.

### Deployment
Se desplegó el modelo de recomendación como parte de la API.
Para el deploy de la API se seleccionó la plataforma Render que es una nube unificada para crear y ejecutar aplicaciones y sitios web, permitiendo el despliegue automático desde GitHub.
El servicio queda corriendo [aqui](https://proyecto-individual-v1.onrender.com)

### Video

