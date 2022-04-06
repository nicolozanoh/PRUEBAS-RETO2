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

def loadData(tamaño):
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    tracks, artists, albums,dt,dm = controller.loadData(control,tamaño)
    
    return tracks, artists, albums,dt,dm

def printMenu():
    print("\nBienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1")
    print("3- Requerimiento 2")
    print("4- Requerimiento 3")
    print("5- Requerimiento 4")
    print("6- Requerimiento 5")
    print("7- Requerimiento 6")

def menuTamaños():
    print("\nEscoga el tamaño del archivo para continuar:")
    print("1- Small")
    print("2- 5pct")
    print("3- 10pct")
    print("4- 20pct")
    print("5- 30pct")
    print("6- 50pct")
    print("7- 80pct")
    print("8- Large")

def menuTipoLista():
    print("\nEscoga el tipo de lista:")
    print("1- Array List")
    print("2- Single Linked List")

catalog = None

def printData(headers, data, col_width = [0]):
    columns = len(headers)
    table = Texttable()
    table._max_width = 180
    table._header = headers
    table._row_size = columns
    if col_width[0] != 0:
        table.set_cols_width(col_width)
    table.set_cols_align = (["l"] +["c"]*(columns-1))
    table._rows = data
    print(table.draw())

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        menuTamaños()
        tamaño= int(input())
        menuTipoLista()
        tipoListaTracks = int(input())
        tipoListaArtists=tipoListaTracks
        tipoListaAlbums=tipoListaTracks

        control = newController(tipoListaTracks, tipoListaArtists, tipoListaAlbums)

        print("\n\nCargando información de los archivos .... \n")

        tracks, artists, albums,dt,dm=loadData(tamaño)
        
        albumPrint = controller.getDataPrint(control['model']['albums'],control,0, 3, 3, 'ALBUMS')
        artistsPrint = controller.getDataPrint(control['model']['artists'],control,0, 3, 3, 'ARTISTS')
        tracksPrint = controller.getDataPrint(control['model']['tracks'],control,0, 3, 3, 'TRACKS')

        print('-' * 30 + ' ')
        print("astists ID count: "+ str(artists))
        print("albums ID count: "+ str(albums))
        print("tracks ID count: "+ str(tracks))
        print('-' * 30 + ' \n')
        
        print("\nLos primeros y últimos 3 artistas cargados fueron: " )
        printData(['NOMBRE','GENEROS', 'POPULARIDAD', 'SEGUIDORES'], artistsPrint['elements'])
        print("\nLos primeros y últimos 3 álbumes cargados fueron: " )
        printData(['NOMBRE','TIPO DEL ALBUM','MERCADOS', 'FECHA DE LANZAMIENTO'], albumPrint['elements'])
        print("\nLas primeras y últimas 3 canciones cargadas fueron: " )
        printData(['NOMBRE','DURACION','NUMERO DE LA CANCION','MERCADOS','ARTISTA(S)','POPULARIDAD', 'LINK REFERENCIA'], tracksPrint['elements'])

        print("Tiempo [ms]: ", f"{dt:.3f}", "||",
              "Memoria [kB]: ", f"{dm:.3f}")

    elif int(inputs) == 2:
        print("\nExaminar los álbumes en un año de interés\n")
        print('='*30+' Req No. 1 Inputs '+'='*30)
        año = int(input('Digite el año que desea consultar '))
        print('\n'+'='*30+' Req No. 1 Answer '+'='*30)
        albumesAnio = controller.examinarAlbumesPeriodo(control, año)
        print("Se lanzaron " + str(albumesAnio['size']) + " albumes en el " + str(año) + "\n")
        print("Los primeros y últimos 3 albumes lanzados en "+ str(año) + " son: ")

        dataPrint = controller.getDataPrint(albumesAnio,control, 1, 3, 3)
        printData(['NOMBRE', 'FECHA DE LANZAMIENTO', 'TIPO DE ALBUM', 'ARTISTA', 'NUMERO DE CANCIONES'], dataPrint['elements'])

    elif int(inputs) == 4:
        print("\nEncontrar las canciones por popularidad\n")
        print('='*30+' Req No. 3 Inputs '+'='*30)
        popularidad = int(input("Popularidad de las canciones"))
        print('\n'+'='*30+' Req No. 3 Answer '+'='*30)
        canciones = controller.encontrarCancionesPopularidad(control, popularidad)
        print("Hay " + str(canciones['size']) + " con una popularidad de " + str(popularidad) + "\n")
        print("Las primeras y últimas 3 canciones con popularidad de "+ str(popularidad) + " son: ")

        dataPrint = controller.getDataPrint(canciones,control,3,3,3)
        printData(['NOMBRE', 'ALBUM', 'ARTISTAS', 'POPULARIDAD', 'DURACION', 'ENLACE', 'LYRICS'], dataPrint['elements'])
        

    elif int(inputs) == 6:
        print("\nEncontrar la discografía de un artista\n")
        print('='*30+' Req No. 5 Inputs '+'='*30)
        nombre = input("Escriba el nombre del artista")
        print('\n'+'='*30+' Req No. 5 Answer '+'='*30)

        albumsArtist, cancionesPopulares, tipoAlbum, tipoSencillo, tipoCompilacion, totalAlbums = controller.encontrarDiscografiaArtista(control, nombre)

        print("Numero de albumes tipo 'compilaciones': " + str(tipoCompilacion))
        print("Numero de albumes tipo 'sencillos': " + str(tipoSencillo))
        print("Numero de albumes tipo 'album': " + str(tipoAlbum))
        print("Total de albumes: " + str(totalAlbums) + "\n")
        print("Los primeros y últimos 3 albumes de "+ str(nombre) + " son: ")

        dataPrintAlbums = controller.getDataPrint(albumsArtist, control, 5, 3, 3, 'ALBUM')
        dataPrintTracks = controller.getDataPrint(cancionesPopulares, control, 5, 3, 3, 'TRACKS')

        printData(['FECHA DE LANZAMIENTO', 'NOMBRE','NUMERO DE CANCIONES', 'TIPO DE ALBUM', 'ARTISTA'], dataPrintAlbums['elements'])
        
        for cancion in dataPrintTracks['elements']:
                print('\nCanción más popular en \'' + cancion[0]+ '\': ')
                printData(['NOMBRE', 'ARTISTA(S)', 'DURACION', 'POPULARIDAD', 'PREVIEW ', 'LYRICS'], [cancion[1]], [15,15,15,15,15,15])


    elif int(inputs) == 0:
        sys.exit(0)
