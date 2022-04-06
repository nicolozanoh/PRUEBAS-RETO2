"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf
from texttable import Texttable


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def newController(TLTr,TLAr,TLAl):
    """
    Se crea una instancia del controlador
    """
    control = controller.newController(TLTr,TLAr,TLAl)
    return control

def loadData(tamanoListaTracks,tamanoListaArtists,tamanoListaAlbums):
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    tracks, artists, albums,dt,dm = controller.loadData(control,tamanoListaTracks,tamanoListaArtists,tamanoListaAlbums)
    
    return tracks, artists, albums,dt,dm

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1")
    print("3- Requerimiento 2")
    print("4- Requerimiento 3")
    print("5- Requerimiento 4")
    print("6- Requerimiento 5")
    print("7- Requerimiento 6")

catalog = None

def printPrimerosUltimosAlbumes(primeros, ultimos):
    
    table = Texttable()
    table.set_cols_align(["l","c","c","l"])
    table.set_cols_valign(["t","t","t","t"])

    print("Los primeros y últimos 3 álbumes cargados fueron: \n" )
    table.add_row(['name','album_type','release_date','available_markets'])
    
    for i in lt.iterator(primeros):
        table.add_row([i['name'],i['album_type'],i['release_date'],i['available_markets']])
    
    for i in lt.iterator(ultimos):
        table.add_row([i['name'],i['album_type'],i['release_date'],i['available_markets']])
    
    print(table.draw())
    return ""

def printPrimerosUltimosTracks(primeros, ultimos):
    table = Texttable()
    table.set_cols_align(["l","c","c","l"])
    table.set_cols_valign(["t","t","t","t"])
    print("Las primeras y últimas 3 canciones cargadas fueron: \n" )

    table.add_row(["name","duration_ms","track_number","available_markets"])
    
    for i in lt.iterator(primeros): 
        table.add_row([i['name'],i['duration_ms'],i['track_number'],i['available_markets']])
    
    for i in lt.iterator(ultimos):
        table.add_row([i['name'],i['duration_ms'],i['track_number'],i['available_markets']])
       
    print(table.draw())
    
    return ""

def printPrimerosUltimosArtists(primeros, ultimos):
    table = Texttable()
    table.set_cols_align(["l","l","c","c"])
    table.set_cols_valign(["t","t","t","t"])

    table.add_row(["name",'genres','artist_popularity','followers'])

    print("Las primeros y últimos 3 artistas cargados fueron: \n" )
    
    for i in lt.iterator(primeros):
        table.add_row([i['name'],i['genres'],i['artist_popularity'],i['followers']])            
        
    for i in lt.iterator(ultimos):
        table.add_row([i['name'],i['genres'],i['artist_popularity'],i['followers']])   

    print(table.draw())

    return ""

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        tipoListaTracks=input("Escriba ARRAY o SINGLE para elegir el tipo de lista que usará: ")
        tipoListaArtists=tipoListaTracks
        tipoListaAlbums=tipoListaTracks

        if (tipoListaTracks=='SINGLE'):
            tipoListaTracks='SINGLE_LINKED_LIST'
        else:
            tipoListaTracks='ARRAY_LIST'

        if (tipoListaArtists=='SINGLE'):
            tipoListaArtists='SINGLE_LINKED_LIST'
        else:
            tipoListaArtists='ARRAY_LIST'

        if (tipoListaAlbums=='SINGLE'):
            tipoListaAlbums='SINGLE_LINKED_LIST'
        else:   
            tipoListaAlbums='ARRAY_LIST' 

        # Se crea el controlador asociado a la vista
        control = newController(tipoListaTracks, tipoListaArtists, tipoListaAlbums)
        tamanoListaAlbums=input("Escriba: small, 5pct, 10pct,20pct, 30pct, 50pct, 80pct o large dependiendo del tamaño de los datos que desea cargar:")
        tamanoListaTracks=tamanoListaAlbums
        tamanoListaArtists=tamanoListaAlbums

        print("\n\nCargando información de los archivos .... \n")

        tracks, artists, albums,dt,dm=loadData(tamanoListaTracks,tamanoListaArtists,tamanoListaAlbums)
        
        priAlb,ultAlb = controller.primerosUltimosAlbumes(control,3)
        priArt,ultArt = controller.primerosUltimosArtistas(control,3)
        priTra,ultTra = controller.primerosUltimosTracks(control,3)

        print('-------------------------------------------------------------------------------------------------------------------------------------- ')
        print("tracks ID count: "+ str(tracks))
        print("astists ID count: "+ str(artists)) 
        print("albums ID count: "+ str(albums))
        print('-------------------------------------------------------------------------------------------------------------------------------------- ')
        
        print(printPrimerosUltimosTracks(priTra,ultTra))
        
        print(printPrimerosUltimosArtists(priArt,ultArt))
        
        print(printPrimerosUltimosAlbumes(priAlb,ultAlb))

        print("Tiempo [ms]: ", f"{dt:.3f}", "||",
              "Memoria [kB]: ", f"{dm:.3f}")

    elif int(inputs) == 2:
        print("Examinar los álbumes en un año de interés")
        año = int(input('Digite el año que desea consultar'))
        albumesAnio = controller.examinarAlbumesPeriodo(control, año)

        priAlb,ultAlb = controller.primerosUltimosDeLista(albumesAnio,3)
        print(printPrimerosUltimosAlbumes(priAlb,ultAlb))

    elif int(inputs) == 4:
        print("Encontrar las canciones por popularidad")
        popularidad = int(input("Popularidad de las canciones"))
        canciones = controller.encontrarCancionesPopularidad(control, popularidad)

        priTrck,ultTrck = controller.primerosUltimosDeLista(canciones,3)
        print(printPrimerosUltimosTracks(priTrck,ultTrck))


    elif int(inputs) == 6:
        print("Encontrar la discografía de un artista")
        nombre = input("Escriba el nombre del artista")

        albumsArtist, cancionesPopulares, tipoAlbum, tipoSencillo, tipoCompilacion = controller.encontrarDiscografiaArtista(control, nombre)

        priAlb,ultAlb = controller.primerosUltimosDeLista(albumsArtist,3)
        print(printPrimerosUltimosAlbumes(priAlb,ultAlb))

        priTrck,ultTrck = controller.primerosUltimosDeLista(cancionesPopulares,3)
        print(printPrimerosUltimosTracks(priTrck,ultTrck))

    elif int(inputs) == 0:
        sys.exit(0)
