import pandas as pd
import numpy as np


# df_sentimiento_x_desarrollador = pd.read_parquet('Proyecto_Individual_1-v1/data/df_sentimiento_x_desarrollador.parquet')
# df_dev_free = pd.read_parquet('Proyecto_Individual_1-v1/data/df_dev_free.parquet')
# df_games_reviews = pd.read_parquet('Proyecto_Individual_1-v1/data/df_games_reviews.parquet')
# df_playtime_user_final = pd.read_parquet('Proyecto_Individual_1-v1/data/df_playtime_user_final.parquet')
# df_user_recom_dev_pos_unido = pd.read_parquet('Proyecto_Individual_1-v1/data/df_user_recom_dev_pos.parquet')
# df_recomendaciones = pd.read_parquet('Proyecto_Individual_1-v1/data/recomendaciones_item_item.parquet')

df_sentimiento_x_desarrollador = pd.read_parquet('data/df_dev_free.parquet')
df_dev_free = pd.read_parquet('data/df_dev_free.parquet')
df_games_reviews = pd.read_parquet('data/df_games_reviews.parquet')
df_playtime_user_final = pd.read_parquet('data/df_playtime_user_final.parquet')
df_user_recom_dev_pos_unido = pd.read_parquet('data/df_user_recom_dev_pos.parquet')
df_recomendaciones = pd.read_parquet('data/recomendaciones_item_item.parquet')

def developer(valor: str) -> str|int:

    """ Esta funcion devuelve la cantidad de items y porcentaje de contenido Free por año según  la empresa desarrolladora
    ingresada
    """
    data = df_dev_free
    data['Cantidad_de_items'] = data['Cantidad_de_items'].astype(int)

    # transformamos en minuscula los caracteres de valor y lo guardamos en una variable
    developer = valor.lower()

    # atrapamos los valores de developers con formato de escritura diferente(mayusculas,minusculas..alternadas o no) pero con los mismos caracteres y disposicion de ellos.
    if developer not in df_dev_free['developer'].str.lower().unique():
        return 'No se encuentran registros del developer ingresado'
    
    # filtramos valores por la consulta
    consulta= df_dev_free[df_dev_free['developer'].str.lower() == developer]

    
    return consulta


def userdata(User_id : str):

    """Debe devolver cantidad de dinero gastado por el usuario, el porcentaje de recomendación que
     dio ese usuario y la cantidad de items que intervinieron en estos valores (dinero gastado y recomendaciones)
    
    
    """
    data = df_games_reviews

    # transformamos en minuscula los caracteres de valor y lo guardamos en una variable
    usuario = User_id.lower()

    # atrapamos los valores de developers con formato de escritura diferente(mayusculas,minusculas..alternadas o no) pero con los mismos caracteres y disposicion de ellos.
    if usuario not in df_games_reviews['user_id'].str.lower().unique():
        return 'No se encuentran registros del usuario ingresado'

    resultado = data[data['user_id'].str.lower() == usuario]
    
    return f'Usuario: {resultado["user_id"].iloc[0]}, Cantidad de items: {resultado["Cantidad_items"].iloc[0]}, Cantidad de dinero gastado: {resultado["Dinero_gastado"].iloc[0]}, Porcentaje de recomendacion: {resultado["Recomendacion (%)"].iloc[0]}'





def UserForGenre(valor: str) -> str|int:

    """Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista 
    de la acumulación de horas jugadas por año.
    
    """
    # transformamos en minuscula los caracteres de valor y lo guardamos en una variable llamada genero
    genero = valor.lower()

    # atrapamos los valores de genres con formato de escritura diferente(mayusculas,minusculas..alternadas o no) pero con los mismos caracteres y disposicion de ellos.
    if genero not in df_playtime_user_final['genres'].str.lower().unique():
        return 'No se encuentran registros del developer ingresado'
    
    # realizamos el filtrado de registros que coinciden con el genero
    data= df_playtime_user_final[df_playtime_user_final['genres'].str.lower() == genero]
    user = data['user_id'].unique()[0]


    ## obtenemos el nombre real del genero como sale escrito en el registro, por lo que reiniciamos la variable genero
    genero = data['genres'].unique()[0]

    # creamos la cadena que retornaremos con los datos de la consulta que se nos pidio
    resultado = f'Usuario con más horas jugadas para Género {genero} : {user}, Horas jugadas:'

    # agregaremos a la cadena de la variable resultado, cadenas correspondientes a los valores de cada año registrado y el tiempo acumulado segun se consultó
    for year, time in zip(data['release_date'],data['playtime_hours']):
        resultado += f' [Año: {year}, {time} horas]--'

    return resultado




def best_developer_year(año: int ) -> str|None:

    """Devuelve el top 3 de desarrolladoras con juegos MAS recomendados por usuarios para el año dado.
    
    """

    # llamamos al dataframe y lo guardamos en una variable data, transformamos el parametro año en str para que coincida con el tipo de dato de la columna reviews_posted
    año = str(año)
    data = df_user_recom_dev_pos_unido

    # evaluzamos si el valor de año esta dentro de los valores que componen los datos correspondientes a años en nuestro dataframe
    if año not in list(data['reviews_posted'].unique()):
        return 'Error: Año no registrado'

    try:
        # filtramos los registros por el año que nos interesa
        filtro = data[data['reviews_posted'] == año].index

        # obtenemos los valores de desarrolladores de los registros filtrados (los valores de recomendacion estan previamente segmentados y conservan un ordenamiento descendente)
        consulta= data['developer'].iloc[filtro].reset_index(drop= True)
    except Exception as e:
        return f'No se pudo completar la consulta:\n{e}'
    
    
    return f'Ranking desarrolladores de juegos mas recomendados: "Puesto 1": {consulta[0]}, "Puesto 2": {consulta[1]}, "Puesto 3": {consulta[2]}'


def developer_reviews_analysis(valor: str) -> dict:


    """Esta funcion es utilizada para obtener el registro de reseñas de usuarios para una desarrolladora determinada, 
    que se encuentren categorizados con un análisis de sentimiento como valor.
    
    
    """
    data = df_sentimiento_x_desarrollador

    # transformamos en minuscula los caracteres de valor y lo guardamos en una variable
    desarrollador = valor.lower()

    # atrapamos los valores de developers con formato de escritura diferente(mayusculas,minusculas..alternadas o no) pero con los mismos caracteres y disposicion de ellos.
    if desarrollador not in df_dev_free['developer'].str.lower().unique():
        return 'No se encuentran registros del developer ingresado'
    
    # iniciamos una serie de contadores donde vamos a acumular los valores
    negative = 0
    positive = 0

    # obtenemos la muestra del desarrollador que nos interesa
    consulta = df_sentimiento_x_desarrollador[df_sentimiento_x_desarrollador['developer'].str.lower() == desarrollador]

    # realizamos la evaluacion de valores
    for x in consulta['sentiment_analysis']:
        if x == 0:
            negative += 1
        elif x == 2:
            positive += 1
        else:
            continue

    ## obtenemos el nombre real del desarrollador como sale escrito en el registro
    desarrollador = consulta['developer'].unique()

    # creamos un diccionario al que le asignamos el nombre del desarrollador y los valores acumulados de sentiment_analysis de acuerdo a su valor
    dicc = {desarrollador[0]: f'Negative= {negative}, Positive= {positive}'}
    

    # return f'{desarrollador}: {dicc[desarrollador]}'
    return dicc



def item_recomendation(item):

    """ Esta funcion toma como parametro el id de un juego (item) y realiza una busqueda de similitud
    para encontrar juegos similares

    esta busqueda se basa en un modelo de recomendacion centrado en la similitud del coseno

    devuelve una lista de los 5 juegos recomendados mas similares al juego ingresado 
    
    """
    
    data = df_recomendaciones  # 

    if item not in list(data['item_id']):
        return 'No se encuentran registros del item ingresado'

    consulta= data[data['item_id'] == item]['Recomendaciones'].iloc[0]

    return f'Juegos recomendados: {consulta}'


    

