from fastapi import FastAPI
import uvicorn
import pandas as pd
import function_recommend as fr

df = pd.read_csv("./datasets/movies_processed.csv")

app = FastAPI()

# @app.get("/")
# def root():
#     data = {"word": "Hello Wolrd"}
#     return data

@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma( Idioma: str ):
    ''' Se ingresa un idioma (como están escritos en el dataset, no hay que traducirlos!). 
    Debe devolver la cantidad de películas producidas en ese idioma. '''        
    res = df["original_language"] == Idioma
    return {"idioma": Idioma, "cantidad": str(res.sum())}


@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion( Pelicula: str ):
    ''' Se ingresa una pelicula. Debe devolver la duracion y el año. '''
    res = df[df["title"] == Pelicula]
    return {"pelicula": Pelicula, "duracion": res.runtime.item(), "anio": res.release_year.item()}


@app.get('/franquicia/{franquicia}')
def franquicia( Franquicia: str ):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia
    total y promedio '''
    f = df[df["belongs_to_collection"] == Franquicia]
    cant_pel = len(f)
    ganancia_total = f.revenue.sum()
    promed = ganancia_total / 3
    return {'franquicia':Franquicia, 'cantidad':cant_pel, 'ganancia_total':ganancia_total, 'ganancia_promedio':round(promed, 2)}


@app.get('/peliculas_pais/{pais}')
def peliculas_pais( Pais: str ):
    cantidad = df['production_countries'].str.contains(Pais, case=False).sum()
    datos = dict()
    
    if cantidad > 0:
        datos = {
                  "pais"    : Pais,
                  "cantidad": str(cantidad)
        }
        
    return datos


@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas( Productora: str ):
    '''Se ingresa la productora, entregandote el revenue total y la cantidad
    de peliculas que realizó.'''
    producer = df[df.production_companies.str.contains(Productora)]
    return {
        'productora':Productora,
        'revenue_total': str(producer.revenue.sum()),
        'cantidad':str(producer.title.count())
    }


@app.get('/get_director/{nombre_director}')
def get_director( nombre_director: str ):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma, en formato lista.'''
    director = df.loc[df['crew'].str.contains(nombre_director)]

    revenue_total = sum(director.revenue) / sum(director.budget)
    success_director = {        
        'medicion_exito': revenue_total        
    }
    
    movies = list(director.title)
    rel_years = list(director.release_year)
    ind_returns = list(round(director["return"], 2))
    costs = list(director.budget)
    revs = list(director.revenue)
    
    movie_data = []
    for movie, rel_year, ind_return, cost, rev in zip(movies, rel_years, ind_returns, costs, revs):
        movie_data.append([movie, rel_year, ind_return, cost, rev])
    
    movies_dict = {}
    
    for movie, rel_year, ind_return, cost, rev in movie_data:
        movies_dict[movie] = {
            "año": rel_year,
            "retorno": ind_return,
            "costo": cost,
            "ganancia": rev
    }

    return movies_dict, success_director
    
    
    


# # ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    res = fr.recommend(titulo)
    return res    
