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
 """
import time
import tracemalloc
import config as cf
import model
import csv
csv.field_size_limit(2147483647)

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def newController(TLTr,TLAr,TLAl):
    """
    Crea una instancia del modelo
    """
    if (TLTr==2):TLTr='SINGLE_LINKED'
    else: TLTr='ARRAY_LIST'
    if (TLAr==2):TLAr='SINGLE_LINKED'
    else: TLAr='ARRAY_LIST'
    if (TLAl==2): TLAl='SINGLE_LINKED'
    else: TLAl='ARRAY_LIST' 

    control = {
        'model': None
    }
    control['model'] = model.newCatalog(TLTr,TLAr,TLAl)
    return control

# Funciones para la carga de datos

def loadData(control,tamaño):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    tracemalloc.start()
    
    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    if tamaño == 1: stamaño = 'small'
    if tamaño == 2: stamaño = '10pct'
    if tamaño == 3: stamaño = '20pct'
    if tamaño == 4: stamaño = '30pct'
    if tamaño == 5: stamaño = '50pct'
    if tamaño == 6: stamaño = '80pct'
    if tamaño == 7: stamaño = 'large'

    catalog = control['model']
    tracks = loadTracks(catalog,stamaño)
    artists = loadArtists(catalog,stamaño)
    albums = loadAlbums(catalog,stamaño)
    
    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()
    # finaliza el proceso para medir memoria
    tracemalloc.stop()

    dt = deltaTime(stop_time, start_time)
    dm = deltaMemory(stop_memory, start_memory)
    
    return tracks, artists, albums,dt,dm

def loadTracks(catalog, tamano='small'):
    """
    Carga todos las canciones del archivo y las agrega a la lista de canciones
    """
    tracksfile = cf.data_dir + 'Spotify/spotify-tracks-utf8-'+tamano+'.csv'
    input_file = csv.DictReader(open(tracksfile, encoding='utf-8'))
    for track in input_file:
        model.addTrack(catalog, track)
    return model.trackSize(catalog)

def loadArtists(catalog,tamano='small'):
    """
    Carga todos los artistas del archivo y los agrega a la lista de artistas
    """
    artistsfile = cf.data_dir + 'Spotify/spotify-artists-utf8-'+tamano+'.csv'
    input_file = csv.DictReader(open(artistsfile, encoding='utf-8'))
    for artist in input_file:
        model.addArtist(catalog, artist)
    return model.artistSize(catalog)

def loadAlbums(catalog,tamano='small'):
    """
    Carga todos los albumes del archivo y los agrega a la lista de albumes
    """
    albumsfile = cf.data_dir + 'Spotify/spotify-albums-utf8-'+tamano+'.csv'
    input_file = csv.DictReader(open(albumsfile, encoding='utf-8'))
    for album in input_file:
        model.addAlbum(catalog, album)
    return model.albumSize(catalog)

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def primerosUltimosAlbumes (control, numero):
    return model.primerosUltimosAlbumes(control['model'],numero)

def primerosUltimosArtistas (control, numero):
    return model.primerosUltimosArtistas(control['model'],numero)

def primerosUltimosTracks (control, numero):
    return model.primerosUltimosTracks(control['model'],numero)    

def primerosUltimosDeLista(l, numero):
    return model.primerosUltimosDeLista(l, numero)

def buscarArtistasPopularidad(control,popularidad):
    return model.buscarArtistasPopularidad(control['model'],popularidad)

def examinarAlbumesPeriodo(control, año):
    return model.examinarAlbumesPeriodo(control['model'], año)

def encontrarDiscografiaArtista(control, nombre):
    return model.encontrarDiscografiaArtista(control['model'], nombre)

def encontrarCancionesPopularidad(control, popularidad):
    return model.encontrarCancionesPopularidad(control['model'], popularidad)

def getDataPrint(lista, control,  req, numPrim, numUlt, tipo = None):
    primeros = None
    ultimos = None
    data = None
    if numPrim != -1:
        primeros = model.getPrimeros(lista, numPrim)
    
    if numUlt != -1:
        ultimos = model.getUltimos(lista, numUlt)

    if primeros != None or ultimos != None:
        data =  model.getDataPrint(req, control['model'], primeros, ultimos, tipo)

    return data

# Funciones para medir tiempos de ejecucions

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funciones para medir la memoria utilizada

def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory

