"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

mtpe='PROBING'
lfct=0.90

def newCatalog(TLTr='ARRAY_LIST',TLAr='ARRAY_LIST',TLAl='ARRAY_LIST'):
    """
    Inicializa el catálogo de canciones. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {'tracks': None,
               'artists': None,
               'albums': None,
               'genres': None,
               'years': None,
               'popularityArtists': None,
               'popularityTracks': None,
               'artistsNames': None,
               'countries': None,
               'idArtists': None,
               'idTracks': None,
               'idAlbum': None,
               
               }

    """
    lsitas
    """
    catalog['tracks'] = lt.newList(TLTr)
    catalog['artists'] = lt.newList(TLAr)
    catalog['albums'] = lt.newList(TLAl)
    catalog['gl'] = lt.newList(TLAl)

    """
    mapas
    """
    catalog['genres'] = mp.newMap(2470,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapGenres)

    catalog['years'] = mp.newMap(100,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapYears)

    catalog['popularityArtists'] = mp.newMap(110,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapPopularityArtists)

    catalog['popularityTracks'] = mp.newMap(110,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapPopularityTracks)

    catalog['artistsNames'] = mp.newMap(56150,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapArtistsNames)

    catalog['countriesTracks'] = mp.newMap(200,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapCountriesTracks)

    catalog['idArtists'] = mp.newMap(56150,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapIdArtists)                               

    catalog['idTracks'] = mp.newMap(102000,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapIdTracks) 

    catalog['idAlbums'] = mp.newMap(75550,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=compareMapIdAlbums)                         

    return catalog

# Funciones para agregar informacion al catalogo

def addTrack(catalog, track):
    #
    lt.addLast(catalog['tracks'], track)
     
    popularity=float(track['popularity'])
    if mp.contains(catalog['popularityTracks'],popularity):
        ent=mp.get(catalog['popularityTracks'],popularity)
        popu=me.getValue(ent)
    else:
        popu=lt.newList('ARRAY_LIST')
        mp.put(catalog['popularityTracks'],popularity,popu)
    lt.addLast(popu,track)

    mp.put(catalog['idTracks'], track['id'], track)
    
    if track['available_markets'] != "[]":
        countries=track['available_markets'].strip('"[]"').split(",")
        for i in countries:
            i.strip(" ").strip("'")
            addCountryTrack(catalog, i, track)

    return catalog

def addArtist(catalog, artist):
    # 
    lt.addLast(catalog['artists'], artist)

    if artist['genres'] != "[]":
        genres=artist['genres'].strip('"[]"').split(",")
        for i in genres:
            addGenre(catalog, i, artist)
    
    popularity=float(artist['artist_popularity'])
    if mp.contains(catalog['popularityArtists'],popularity):
        ent=mp.get(catalog['popularityArtists'],popularity)
        popu=me.getValue(ent)
    else:
        popu=lt.newList('ARRAY_LIST')
        mp.put(catalog['popularityArtists'],popularity,popu)
    lt.addLast(popu,artist)
    

    mp.put(catalog['artistsNames'], artist['name'], artist)

    mp.put(catalog['idArtists'], artist['id'], artist)
    
    return catalog

def addAlbum(catalog, album):
    # 
    lt.addLast(catalog['albums'], album)

    if album['release_date_precision'] == "month":
        year=int("19"+album['release_date'][-2:])
    else:
        year=int(album['release_date'][0:4])
    if mp.contains(catalog['years'],year):
        ent=mp.get(catalog['years'],year)
        ye=me.getValue(ent)
    else:
        ye=lt.newList('ARRAY_LIST')
        mp.put(catalog['years'],year,ye)
    lt.addLast(ye,album) 

    mp.put(catalog['idAlbums'], album['id'], album)

    return catalog

def addGenre(catalog, genre, artist):
    # 
    genre=genre.strip(" ").strip("'")
    
    
    if mp.contains(catalog['genres'],genre):
        ent=mp.get(catalog['genres'],genre)
        gen=me.getValue(ent)
    else:
        lt.addLast(catalog['gl'],genre)
        gen=lt.newList('ARRAY_LIST')
        mp.put(catalog['genres'],genre,gen)
    lt.addLast(gen,artist)
    return None

def addCountryTrack(catalog, country, track):
    # 

    if mp.contains(catalog['countriesTracks'],country):
        ent=mp.get(catalog['countriesTracks'],country)
        co=me.getValue(ent)
    else:
        co=lt.newList('ARRAY_LIST')
        mp.put(catalog['genres'],country,co)
    lt.addLast(co,track)
    return None


def printGen(catalog):
    input(catalog['genres'])
    return None

# Funciones para creacion de datos

# Funciones de consulta



def trackSize(catalog):
    #mesort.sort(catalog['tracks'],cmpTracksByPopularity)
    return lt.size(catalog['tracks'])

def artistSize(catalog):
    return lt.size(catalog['artists'])

def albumSize(catalog):
    return lt.size(catalog['albums'])

def primerosUltimosAlbumes(catalog, numero):
    return primerosUltimosDeLista(catalog['albums'], numero)
    
def primerosUltimosArtistas(catalog, numero):
    return primerosUltimosDeLista(catalog['artists'], numero)
        
def primerosUltimosTracks(catalog, numero):
    return primerosUltimosDeLista(catalog['tracks'], numero)

def primerosUltimosDeLista(l, numero):
    primeros=lt.newList()
    ultimos=lt.newList()
    for cont in range(1, numero+1):
        item=lt.getElement(l,cont)
        lt.addLast(primeros,item)
    for cont in range(lt.size(l),lt.size(l)-numero,-1):
        item=lt.getElement(l,cont)
        lt.addFirst(ultimos,item)    
    return primeros, ultimos

def buscarArtistasPopularidad(catalog, popularity):
    popularity=float(popularity)
    aa=mp.get(catalog['popularityArtists'],popularity)
    a=me.getValue(aa)
    input(a)
    return a



# Funciones utilizadas para comparar elementos dentro de una lista

def compareMapGenres(genre, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    genreentry = me.getKey(entry)
    if (genre == genreentry):
        return 0
    elif ((genre) > (genreentry)):
        return 1
    else:
        return -1

def compareMapYears(year, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    yearentry = me.getKey(entry)
    if (int(year) == int(yearentry)):
        return 0
    elif (int(year) > int(yearentry)):
        return 1
    else:
        return -1

def compareMapPopularityArtists(popularity, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    popularityentry = me.getKey(entry)
    if (int(popularity) == int(popularityentry)):
        return 0
    elif (int(popularity) > int(popularityentry)):
        return 1
    else:
        return -1

def compareMapPopularityTracks(popularity, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    popularityentry = me.getKey(entry)
    if (int(popularity) == int(popularityentry)):
        return 0
    elif (int(popularity) > int(popularityentry)):
        return 1
    else:
        return -1

def compareMapArtistsNames(name, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    nameentry = me.getKey(entry)
    if (name == nameentry):
        return 0
    elif (name > nameentry):
        return 1
    else:
        return -1

def compareMapCountriesTracks(name, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    nameentry = me.getKey(entry)
    if (name == nameentry):
        return 0
    elif (name > nameentry):
        return 1
    else:
        return -1

def compareMapIdArtists(id, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareMapIdTracks(id, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def compareMapIdAlbums(id, entry):
    """
    Compara dos géneros, id es un identificador
    y entry una pareja llave-valor
    """
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1




# Funciones de ordenamiento

