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
import DISClib.Algorithms.Sorting.mergesort as merge
assert cf
import datetime

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
               'albumsArtistsId': None,
               'tracksAlbumsId': None,
               'countries': None,
               'idArtists': None,
               'idTracks': None,
               'idAlbum': None,
               }

    """
    listas
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

    catalog['albumsArtistsId'] = mp.newMap(56150,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=cmpMapalbumsArtistsId)

    catalog['tracksAlbumsId'] = mp.newMap(75550,
                                   maptype=mtpe,
                                   loadfactor=lfct,
                                   comparefunction=cmpMaptracksAlbumsId)

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

    if mp.contains(catalog['tracksAlbumsId'], track['album_id']):
        trackAlbum = me.getValue(mp.get(catalog['tracksAlbumsId'],track['album_id']))

    else:
        trackAlbum = lt.newList('ARRAY_LIST')
        mp.put(catalog['tracksAlbumsId'], track['album_id'], trackAlbum)
    
    lt.addLast(trackAlbum, track)

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
        year=int(datetime.datetime.strptime(album['release_date'], '%b-%y').year)

    elif album['release_date_precision'] == "year":
        year=int(album['release_date'])

    elif album['release_date_precision'] == "day":
        year = int(datetime.datetime.strptime(album['release_date'], '%Y-%m-%d').year)

    if mp.contains(catalog['years'],year):
        ent=mp.get(catalog['years'],year)
        ye=me.getValue(ent)

    else:
        ye=lt.newList('ARRAY_LIST')
        mp.put(catalog['years'],year,ye)

    lt.addLast(ye,album)

    if mp.contains(catalog['albumsArtistsId'], album['artist_id']):
        albumsArtist=me.getValue(mp.get(catalog['albumsArtistsId'],album['artist_id']))

    else:
        albumsArtist = lt.newList('ARRAY_LIST')
        mp.put(catalog['albumsArtistsId'], album['artist_id'], albumsArtist)
    
    lt.addLast(albumsArtist, album)

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

def getPrimeros(data, numero):
    lista = lt.newList('ARRAY_LIST')
    for i in range(1, numero+1):
        lt.addLast(lista, (lt.getElement(data, i)))
    
    return lista

def getUltimos(data, numero):
    numero = numero -1
    lista = lt.newList('ARRAY_LIST')
    for i in range(numero, -1, -1):
        lt.addLast(lista, (lt.getElement(data, int(lt.size(data))-i)))
    return lista

def getDataPrint(req, catalog, primeros, ultimos = None, tipo = None):
    if req ==1:
        data = getDataReq1(primeros, ultimos, catalog)
    elif req == 2:
        data = getDataReq1()
    elif req == 3:
        data = getDataReq1(primeros, ultimos, catalog)
    elif req == 4:
        data = getDataReq1()
    elif req == 5:
        data = getDataReq1()
    elif req == 6:
        data = getDataReq1()
    return data

def getDataReq1(primeros, ultimos, catalog):
    dataPrint = lt.newList("ARRAY_LIST")
    for i in primeros['elements']:
        album = (i['name'], i['release_date'], i['album_type'], me.getValue(mp.get(catalog['idArtists'], i['artist_id']))['name'],i['total_tracks'])
        lt.addLast(dataPrint, album)
    
    for j in ultimos['elements']:
        album = (j['name'], j['release_date'], j['album_type'], me.getValue(mp.get(catalog['idArtists'], j['artist_id']))['name'],j['total_tracks'])
        lt.addLast(dataPrint, album)
    
    return dataPrint

def getDataReq2():
    pass

def getDataReq3(primeros, ultimos, catalog):
    dataPrint = lt.newList("ARRAY_LIST")
    for i in primeros['elements']:
        artistas=[]
        cod_artistas = str(i['artists_id'])
        cod_artistas = cod_artistas.replace("[","")
        cod_artistas = cod_artistas.replace("]","")
        cod_artistas = cod_artistas.replace("'","")
        lista_art = cod_artistas.split(', ')
        
        for k in lista_art:
            artist = me.getValue(mp.get(catalog['idArtists'], i[k]))
            if artist == None:
                artist = ''
            artistas.append(artist)
        
        str_artistas = (((str(artistas).replace("[","")).replace("]",""))).replace("'","")

        if i['lyrics'] == '-99':
            lyrics = 'Letra de la canción NO disponible'
        else:
            lyrics = i['lyrics'][:80] + "..."

        track = (i['name'], me.getValue(mp.get(catalog['idAlbums'], i['album_id']))['name'], str_artistas, i['popularity'], i['duration_ms'],i['href'], lyrics)
        lt.addLast(dataPrint, track)

    for j in ultimos['elements']:
        artistas=[]
        cod_artistas = str(j['artists_id'])
        cod_artistas = cod_artistas.replace("[","")
        cod_artistas = cod_artistas.replace("]","")
        cod_artistas = cod_artistas.replace("'","")
        lista_art = cod_artistas.split(', ')
        
        for k in lista_art:
            artist = me.getValue(mp.get(catalog['idArtists'], j[k]))
            if artist == None:
                artist = ''
            artistas.append(artist)
        
        str_artistas = (((str(artistas).replace("[","")).replace("]",""))).replace("'","")

        if j['lyrics'] == '-99':
            lyrics = 'Letra de la canción NO disponible'
        else:
            lyrics = j['lyrics'][:80] + "..."

        track = (j['name'], me.getValue(mp.get(catalog['idAlbums'], j['album_id']))['name'], str_artistas, j['popularity'], j['duration_ms'],j['href'], lyrics)
        lt.addLast(dataPrint, track)

    return dataPrint

def getDataReq4():
    pass

def getDataReq5(primeros, ultimos, catalog, tipo):
    
    dataPrint = lt.newList('ARRAY_LIST')
    
    if tipo == 'ALBUM':
        dataPrint = lt.newList("ARRAY_LIST")
        for i in primeros['elements']:
            album = (i['release_date'], i['name'], i['total_tracks'], i['album_type'], me.getValue(mp.get(catalog['idArtists'], i['artist_id']))['name'])
            lt.addLast(dataPrint, album)
        
        for j in ultimos['elements']:
            album = (j['release_date'], j['name'], j['total_tracks'], j['album_type'], me.getValue(mp.get(catalog['idArtists'], j['artist_id']))['name'])
            lt.addLast(dataPrint, album)
    
    elif tipo == 'TRACKS':
        for i in primeros['elements']:
            artistas=[]
            cod_artistas = str(i['artists_id'])
            cod_artistas = cod_artistas.replace("[","")
            cod_artistas = cod_artistas.replace("]","")
            cod_artistas = cod_artistas.replace("'","")
            lista_art = cod_artistas.split(', ')
            
            for k in lista_art:
                artist = me.getValue(mp.get(catalog['idArtists'], i[k]))
                if artist == None:
                    artist = ''
                artistas.append(artist)
            
            str_artistas = (((str(artistas).replace("[","")).replace("]",""))).replace("'","")

            if i['lyrics'] == '-99':
                lyrics = 'Letra de la canción NO disponible'
            else:
                lyrics = i['lyrics'][:80] + "..."

            track = (me.getValue(mp.get(catalog['idAlbums'], i['album_id']))['name'], (i['name'], str_artistas, i['duration_ms'], i['popularity'],i['preview_url'], lyrics))

            lt.addLast(dataPrint, track)

            for j in ultimos['elements']:
                artistas=[]
                cod_artistas = str(j['artists_id'])
                cod_artistas = cod_artistas.replace("[","")
                cod_artistas = cod_artistas.replace("]","")
                cod_artistas = cod_artistas.replace("'","")
                lista_art = cod_artistas.split(', ')
                
                for k in lista_art:
                    artist = me.getValue(mp.get(catalog['idArtists'], j[k]))
                    if artist == None:
                        artist = ''
                    artistas.append(artist)
                
                str_artistas = (((str(artistas).replace("[","")).replace("]",""))).replace("'","")

                if j['lyrics'] == '-99':
                    lyrics = 'Letra de la canción NO disponible'
                else:
                    lyrics = j['lyrics'][:80] + "..."

                track = (me.getValue(mp.get(catalog['idAlbums'], j['album_id']))['name'], (j['name'], str_artistas, j['duration_ms'], j['popularity'],j['preview_url'], lyrics))
                lt.addLast(dataPrint, track)
    
    return dataPrint

def getDataReq6():
    pass

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

def examinarAlbumesPeriodo(catalog, año):
    albumesAnio = me.getValue(mp.get(catalog['years'],año))
    callMergeSort(albumesAnio, cmpAlbumsByName)

    return albumesAnio

def encontrarDiscografiaArtista(catalog, nombre):
    id = (me.getValue(mp.get(catalog['artistsNames'], nombre)))['id']
    albumsArtist = me.getValue(mp.get(catalog['albumsArtistsId'], id))
    callMergeSort(albumsArtist, cmpAlbumsByYearDESC)
    cancionesPopulares = lt.newList('ARRAY_LIST')
    posicion = 1

    while posicion <= lt.size(albumsArtist):
        album = lt.getElement(albumsArtist, posicion)
        tipoAlbum = 0
        tipoSencillo = 0
        tipoCompilacion = 0

        if album['album_type'] == 'album':
            tipoAlbum +=1
        if album['album_type'] == 'compilation':
            tipoCompilacion +=1
        if album['album_type'] == 'single':
            tipoSencillo +=1
        
        cancionesAlbum = me.getValue(mp.get(catalog['tracksAlbumsId'], album['id']))

        callMergeSort(cancionesAlbum, cmpTracks)

        lt.addLast(cancionesPopulares, lt.getElement(cancionesAlbum, 1))
        
        posicion += 1
    
    return albumsArtist, cancionesPopulares, tipoAlbum, tipoSencillo, tipoCompilacion

def encontrarCancionesPopularidad(catalog, popularidad):
    canciones = me.getValue(mp.get(catalog['popularityTracks'], popularidad))

    callMergeSort(canciones, cmpTracks2)

    return canciones

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

def cmpMaptracksAlbumsId(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def cmpMapalbumsArtistsId(id, entry):
    identry = me.getKey(entry)
    if (id == identry):
        return 0
    elif (id > identry):
        return 1
    else:
        return -1

def cmpAlbumsByName(album1, album2):
    if album1['name'] < album2['name']:
        return True
    else:
        return False

def cmpAlbumsByYearDESC(album1, album2):
    if album1['release_date_precision'] == 'day':
        releaseYear1 = datetime.datetime.strptime(album1['release_date'], '%Y-%m-%d').year

    elif album1['release_date_precision'] == 'year':
        releaseYear1 = int(album1['release_date'])
    
    elif album1['release_date_precision'] == 'month':
        releaseYear1 = datetime.datetime.strptime(album1['release_date'], '%b-%y').year
    
    if album2['release_date_precision'] == 'day':
        releaseYear2 = datetime.datetime.strptime(album2['release_date'], '%Y-%m-%d').year

    elif album2['release_date_precision'] == 'year':
        releaseYear2 = int(album2['release_date'])

    elif album2['release_date_precision'] == 'month':
        releaseYear2 = datetime.datetime.strptime(album2['release_date'], '%b-%y').year
        
    if int(releaseYear1) >= int(releaseYear2):
        return True
    else:
        return False

def cmpTracks(track1, track2):
    if float(track1['popularity']) > float(track2['popularity']):
        return True
    elif (float(track1['duration_ms']) > float(track2['duration_ms'])) and(float(track1['popularity']) == float(track2['popularity'])):
        return True
    elif ((track1['name']) > (track2['name']))and(float(track1['popularity']) == float(track2['popularity'])) and (float(track1['duration_ms']) == float(track2['duration_ms'])) and ((track1['name']) > (track2['name'])):
        return True
    else:
        return False

def cmpTracks2(track1, track2):
    if (float(track1['duration_ms']) > float(track2['duration_ms'])) and(float(track1['popularity']) == float(track2['popularity'])):
        return True
    elif ((track1['name']) > (track2['name']))and(float(track1['popularity']) == float(track2['popularity'])) and (float(track1['duration_ms']) == float(track2['duration_ms'])) and ((track1['name']) > (track2['name'])):
        return True
    else:
        return False

# Funciones de ordenamiento

def callMergeSort(lista, cmpfunction):
    merge.sort(lista, cmpfunction)