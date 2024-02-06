# Desarrollo API: se disponibilizan los datos de la empresa usando el framework FastAPI. 
# Se crean  6 funciones para los endpoints que se consumirán en la API,con un decorador por cada una (@app.get(‘/’))

# importamos las librerias
import numpy as np
import pandas as pd

from fastapi import FastAPI

from fastapi.responses import JSONResponse
from fastapi import HTTPException
import traceback  
from funciones_api import developer, UserForGenre, userdata, best_developer_year, developer_reviews_analysis, item_recomendation


# Link para API y nombramiento de la visualización web.
app = FastAPI(title='STEAM', description='Revisa los datos de interés sobre esos videojuegos que quieres adquirir o aquellos a los que tanto juegas desde reseñas de usuarios y recomendaciones, hasta horas jugadas por otros usuarios')



# uvicorn main:app --reload
# http://127.0.0.1:8000 

# importamos los datasets que vamos a utilizar


#Función de Bienvenida.
# ### Root



@app.get("/")
async def root():
    """
    Proyecto FastAPI - Sistema de Recomendaciones

    Versión: 1.0.0

    ---

    """
    return {"Mensaje": "Proyecto Individual N° 1 - Marco Caro"}


# ### Endpoint 1



@app.get("/developer/{desarrollador}", tags=['developer'])
async def endpoint1(desarrollador: str):
    """
    Descripción: Devuelve cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.
    
    Parámetros:
        - desarrollador (str): Desarrollador para el cual se busca la cantidad de items y porcentaje de contenido Free por año. 
        Debe ser un string, ejemplo: .M.Y.W.
    
    Ejemplo de retorno: 

         Año	     Cantidad de Items	Contenido Free
        2023	          50	          27%
        2022	          45	          25%
        xxxx	          xx              xx%
    """
    try:
        # Validación adicional para asegurarse de que el desarrollador no sea nulo o esté vacío
        if not desarrollador or not desarrollador.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'desarrollador' no puede ser nulo o estar vacío.")

        result = developer(desarrollador)

        # Convertir DataFrame a un formato nativo de Python
        result_dict = result.to_dict(orient='records')

        return JSONResponse(content=result_dict)
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo df_dev_free.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# ### Endpoint 2



@app.get("/UserForGenre/{genero}", tags=['UserForGenre'])
async def endpoint2(genero: str):
    """
    Descripción: Retorna el usuario que acumula más horas jugadas para un género dado y una lista de la acumulación de horas jugadas por año.

    Parámetros:
        - genero (str): Género para el cual se busca el usuario con más horas jugadas. Debe ser un string, ejemplo: Adventure

    Ejemplo de retorno: {"Usuario con más horas jugadas para Género Adventure": Evilutional, Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, 
    {Año: 2011, Horas: 23}]}
    """
    try:
        # Validación adicional para asegurarse de que el género no sea nulo o esté vacío
        if not genero or not genero.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'genero' no puede ser nulo o estar vacío.")

        result = UserForGenre(genero)
        
        # Validación para verificar si el género existe en los datos
        if not result:
            raise HTTPException(status_code=404, detail=f"No se encontró información para el género '{genero}'.")
            
        return result
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo df_playtime_user_final.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# ### Endpoint 3



@app.get("/userdata/{user}", tags=['userdata'])
async def endpoint3(user: str):
    """
    Descripción: Devuelve la cantidad de dinero gastado por el usuario, el porcentaje de recomendación que
     dio ese usuario y la cantidad de items que intervinieron en estos valores (dinero gastado y recomendaciones)
    
    Parámetros:
        - user (str): Usuario para el cual se busca el cantidad de dinero gastado, el porcentaje de recomendación y cantidad de items.
        Debe ser un string, ejemplo: zyr0n1c

    Ejemplo de retorno: 'Usuario: zyr0n1c, Cantidad de items: 225, Cantidad de dinero gastado: 19113.75, Porcentaje de recomendacion: 7'
    """
    try:
        usuario = str(user)
    
        # Validación adicional para asegurarse de que el género no sea nulo o esté vacío
        if not usuario or not usuario.strip():
            raise HTTPException(status_code=422, detail="El parámetro 'usuario' no puede ser nulo o estar vacío.")
        
        result = userdata(usuario)

        # Validación para verificar si el género existe en los datos
    
        if result:
            return result
        else:
            #raise HTTPException(status_code=404, detail=f"No se encontraron recomendaciones para el año {year}.")
            error_message = f"No se encontraron datos para el usuario {user} {str(e)}"
            return JSONResponse(status_code=500, content={"error": error_message})

    except FileNotFoundError as e:
        error_message = f"Error al cargar el archivo df_games_reviews.parquet: {str(e)}"
        return JSONResponse(status_code=500, content={"error": error_message})

    except Exception as e:
        error_message = f"Error interno del servidor: {str(e)}"
        return JSONResponse(status_code=500, content={"error": error_message})



# ### Endpoint 4



@app.get("/best_developer_year/{year}", tags=['best_developer_year'])
async def endpoint4(year: str):
    """
    Descripción: Retorna el top 3 de desarrolladoras con juegos MAS recomendados por usuarios para el año dado.
    
    Parámetros:
        - year (str): Año para el cual se busca el top 3 de desarrolladoras mas recomendadas. Debe ser número de 4 digitos, ejemplo: 2015


    Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]
    """
    try:
        year = int(year)
        result = best_developer_year(year)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo df_user_recom_dev_pos.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# ### Endpoint 5



@app.get("/developer_reviews_analysis/{empresa_desarrolladora}", tags=['sentiment_analysis'])
async def endpoint5(empresa_desarrolladora: str):
    """
    Descripción: Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
    
    Parámetros:
        - empresa_desarrolladora (str): Nombre de la empresa desarrolladora para la cual se realiza el análisis de sentimiento. Debe ser un string, ejemplo: Valve
    
    Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}
    """
    try:
        result = developer_reviews_analysis(empresa_desarrolladora)
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=f"Error al cargar el archivo df_sentimiento_x_desarrollador.parquet: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# ### Sistema de recomendación item-item



@app.get("/item_recomendacion/{item_id}", tags=['recomendacion_usuario item_item'])
async def item(item_id: int):
    """
    Descripción: Ingresando el id de producto, devuelve una lista con 5 juegos recomendados similares al ingresado.
    
    Parámetros:
        - item_id (str): Id del producto para el cual se busca la recomendación. Debe ser un número, ejemplo: 761140
        
    Ejemplo de retorno: "['弹炸人2222', 'Uncanny Islands', 'Beach Rules', 'Planetarium 2 - Zen Odyssey', 'The Warrior Of Treasures']"

    """
    try:
        item_id = int(item_id) 
        resultado= item_recomendation(item_id)
        return resultado
    except Exception as e:
        return {"error":str(e)}