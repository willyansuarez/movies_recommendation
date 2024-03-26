from fastapi import FastAPI
import uvicorn
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException
import os

# df = pd.read_csv("/home/willian/modelo_recomendacion_peliculas/movies_recommendation/datasets/movies_processed.csv")
# df_2 = pd.read_parquet("/home/willian/modelo_recomendacion_peliculas/movies_recommendation/datasets/movies_with_recommendations.parquet")

# df = pd.read_csv("./datasets/movies_processed.csv")
# df = pd.read_csv("datasets/movies_processed.csv") # 1
# df = pd.read_csv("movies_recommendation/datasets/movies_processed.csv") # 2
df = pd.read_csv("./datasets/movies_processed.csv") # 3
# df_2 = pd.read_parquet("./datasets/movies_with_recommendations.parquet")

app = FastAPI()

# para permitir peticiones desde fuera del servidor
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O puedes especificar los dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/")
# def root():
#     # ruta_absoluta = os.path.abspath('movies_processed.csv')
#     ruta = os.getcwd()
#     # print(ruta_absoluta)
#     data = {"word": "Hello World", "ruta": ruta}
#     return data
# #   os.path retorna: {"word":"Hello World","ruta":"/opt/render/project/src/movies_processed.csv"} 
# #   os.getcwd retorna {"word":"Hello World","ruta":"/opt/render/project/src"}

@app.get('/peliculas_idioma/{idioma}')
async def peliculas_idioma( Idioma: str ):
    ''' Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). 
    Debe devolver la cantidad de películas producidas en ese idioma. '''        
    # df = pd.read_csv("movies_processed.csv")
    res = df["original_language"] == Idioma
    return {"idioma": Idioma, "cantidad": str(res.sum())}


# @app.get('/peliculas_duracion/{pelicula}')
# async def peliculas_duracion( Pelicula: str ):
#     ''' Se ingresa una pelicula. Debe devolver la duracion y el año. '''
#     df = pd.read_csv("movies_processed.csv")
#     res = df[df["title"] == Pelicula]
#     return {"pelicula": Pelicula, "duracion": res.runtime.item(), "anio": res.release_year.item()}


# @app.get('/franquicia/{franquicia}')
# async def franquicia( Franquicia: str ):
#     '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia
#     total y promedio '''
#     df = pd.read_csv("movies_processed.csv")
#     f = df[df["belongs_to_collection"] == Franquicia]
#     cant_pel = len(f)
#     ganancia_total = f.revenue.sum()
#     promed = ganancia_total / 3
#     return {'franquicia':Franquicia, 'cantidad':cant_pel, 'ganancia_total':ganancia_total, 'ganancia_promedio':round(promed, 2)}


# @app.get('/peliculas_pais/{pais}')
# async def peliculas_pais( Pais: str ):
#     df = pd.read_csv("movies_processed.csv")
#     cantidad = df['production_countries'].str.contains(Pais, case=False).sum()
#     datos = dict()
    
#     if cantidad > 0:
#         datos = {
#                   "pais"    : Pais,
#                   "cantidad": str(cantidad)
#         }
        
#     return datos


# @app.get('/productoras_exitosas/{productora}')
# async def productoras_exitosas( Productora: str ):
#     '''Se ingresa la productora, entregandote el revenue total y la cantidad
#     de peliculas que realizó.'''
#     df = pd.read_csv("movies_processed.csv")
#     producer = df[df.production_companies.str.contains(Productora)]
#     return {
#         'productora':Productora,
#         'revenue_total': str(producer.revenue.sum()),
#         'cantidad':str(producer.title.count())
#     }


# @app.get('/get_director/{nombre_director}')
# async def get_director( nombre_director: str ):
#     ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.'''
#     df = pd.read_csv("movies_processed.csv")
#     director = df.loc[df['crew'].str.contains(nombre_director)]

#     revenue_total = sum(director.revenue) / sum(director.budget)
#     success_director = {        
#         'medicion_exito': revenue_total        
#     }
    
#     movies = list(director.title)
#     rel_years = list(director.release_year)
#     ind_returns = list(round(director["return"], 2))
#     costs = list(director.budget)
#     revs = list(director.revenue)
    
#     movie_data = []
#     for movie, rel_year, ind_return, cost, rev in zip(movies, rel_years, ind_returns, costs, revs):
#         movie_data.append([movie, rel_year, ind_return, cost, rev])
    
#     movies_dict = {}
    
#     for movie, rel_year, ind_return, cost, rev in movie_data:
#         movies_dict[movie] = {
#             "año": rel_year,
#             "retorno": ind_return,
#             "costo": cost,
#             "ganancia": rev
#     }

#     return movies_dict, success_director
    
    
    


# # # ML
# @app.get('/recomendacion/{titulo}')
# async def recomendacion(titulo:str):
#     '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
#     df_2 = pd.read_parquet("movies_with_recommendations.parquet")
#     res = tuple(df_2[df_2["movie"] == titulo]["recommended"].item())
    
#     return {res}    
