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
    print("2- Cargar listado de albums")
    print("3- Listar artistas mas populares")
    print("4- Listar canciones más populares")
    print("5- Cancion más popular de tu artista favorito")
    print("6- Ordenar artistas por cantidad de seguidores")
    print("7- Discografia de tu artista favorito")
    print("8- Canciones con mayor distribución")

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
    if int(inputs[0]) == 1:
        tipoListaTracks=input("Escriba ARRAY o SINGLE para elegir el tipo de lista de las canciones: ")
        tipoListaArtists=input("Escriba ARRAY o SINGLE para elegir el tipo de lista de los artistas: ")
        tipoListaAlbums=input("Escriba ARRAY o SINGLE para elegir el tipo de lista de los álbumes: ")
        
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

        tamanoListaTracks=input("Escriba: small, 5pct, 10pct,20pct, 30pct, 50pct, 80pct o large dependiendo del tamaño de los datos que desea cargar para la lista de canciones:")
        tamanoListaArtists=input("Escriba: small, 5pct, 10pct,20pct, 30pct, 50pct, 80pct o large dependiendo del tamaño de los datos que desea cargar para la lista de artistas:")
        tamanoListaAlbums=input("Escriba: small, 5pct, 10pct,20pct, 30pct, 50pct, 80pct o large dependiendo del tamaño de los datos que desea cargar para la lista de álbumes:")

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

    elif int(inputs[0]) == 2:
        pass

    elif int(inputs[0]) == 1:
        ti=controller.getTime()
        numTop = input('Ingrese el número de canciones que desea que se muestren en el TOP de canciones más populares:')

        print("----------------- Iputs de requerimiento número 3-------------------")
        print("TOP "+numTop+" canciones más populares\n")
        print("----------------- Respuesta de requerimiento número 3-------------------")
        print("Las primeras y últimas 3 canciones del TOP "+numTop +" son: \n" )
        Top, pri, ult=controller.topCancionesMasPopulares(control,numTop)
        printTopPrimerosUltimosTracks(pri,ult,Top)
        tf = controller.getTime()
        delta_time = controller.deltaTime(ti, tf)
        print("=============TIEMPO DE      "+str(delta_time))
        
        
        
    elif int(inputs[0]) == 2:
        anoin = input('Ingrese el limite inferior del año que quiere analizar: ')
        anofin = input('Ingrese el limite superior del año que quiere analizar: ')
        albumsDate = controller.albumsCrono(control, anoin, anofin)
        print(printAlbumsCrono(albumsDate))

    elif int(inputs[0]) == 3:
        top = int(input("Escriba el top de artistas que desee respecto a su popularidad: "))
        top_list = controller.sortArtistsReq(control, 1, top)
        print(printsortArtistsTop(top_list))

    elif int(inputs[0]) == 5:
        art = str(input("Ingrese el nombre del artista del cual quiere conocer su cancion mas popular: "))
        pais = str(input("Ingrese el nombre del pais (en mayusculas) en donde crea que sea mas popular: "))
        print("_________________________________________________________________________________ \n")

        sumaTracksart, sumaAlbumsart, miArtista = controller.AlbumsAndArtists(control, art, pais)

        top_tracks = controller.sortTracksPopularity(control)
        #print(top_tracks)
        print(printAlbumsAndArtists(art, sumaTracksart, sumaAlbumsart, top_tracks, miArtista))

        
        
    elif int(inputs[0]) == 6:
        
        AlgoritmoOrdenamiento=input("Escriba: merge, quick shell, insertion o selection dependiendo del algoritmo de ordenamiento que desee usar:")
        listaOrdenada=controller.sortArtistsByFollowers(control, AlgoritmoOrdenamiento)
        delta_time = f"{listaOrdenada[1]:.3f}"
        listaO = listaOrdenada[0]
        print("-----------\n-----------\n-----------")
        print("Para", str(listaOrdenada[2]), "elementos, con ordenamiento",AlgoritmoOrdenamiento ,"delta tiempo:", str(delta_time))
        print("-----------\n-----------\n-----------")

    elif int(inputs[0]) == 7:
        ti = controller.getTime()
        artista=input("Escribe el nombre del artista para ver su discografía:")
        print("-----Inputs Requerimiento 5--------")
        print("Medidores de discografía de: "+artista+"\n\n")
       
        numA, numS, numC, listaDeAlbumbes, priAlb, ultAlb=controller.Requerimiento5(control,artista)
        a=numA+ numS+ numC
        print("-----Respuesta de Requerimiento 5--------")
        print("Número de compilaciones: "+str(numC))
        print("Número de sencillos: "+str(numS))
        print("Número de álbumes: "+str(numA))
        print("Número total de álbumes: "+str(a)+"\n")
        print("----Detalles de los álbumes----\nLos 3 primeros y últimos álbumes del rango")

        printRequerimiento5(priAlb,ultAlb)
        tf = controller.getTime()
        delta_time = controller.deltaTime(ti, tf)
        print("=============TIEMPO DE      "+str(delta_time))

    elif int(inputs[0]) == 8:
        ti = controller.getTime()
        fechaI=input("Seleccione el año inicial (en formato AAAA): ")
        fechaF=input("Seleccione el año final (en formato AAAA): ")
        nTop=input("Escriba cuantas canciones desea clasificar: ")
        lista=controller.Requerimiento6(control,fechaI,fechaF,nTop)
        printRequerimiento6(lista[0])
        tf = controller.getTime()
        delta_time = controller.deltaTime(ti, tf)
        print("=============TIEMPO DE      "+str(delta_time))
