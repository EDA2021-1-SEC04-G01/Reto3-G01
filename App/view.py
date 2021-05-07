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


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""



def printMenu():
    print("Bienvenido")
    print("0- Inicializar analizador")
    print("1- Cargar información en el catálogo")
    print("2- Consultar reproducciones con característica de contenido y un rango")
    print ("3- Encontrar música para festejar")
    print ("4- Encontrar música para estudiar")
    print ("5- Estudiar los géneros musicales")
    print("6- Indicar el género musical más escuchado en el tiempo")
    print("7- Salir")
    print("*******************************************")

catalog = None

songfile = 'context_content_features-small.csv'
cont = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')

    if int(inputs[0]) == 0:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        controller.loadData(cont, songfile)
        print('Eventos de escucha cargados: ' + str(controller.tracksSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol (pistas de audio cargadas) : ' + str(controller.indexSize(cont)))
        print('Artistas cargados: ' + str(controller.artistsSize(cont)))
        print('Primeros 5 eventos de escucha cargados: ' + str(controller.firstTracks(cont)))
        print()
        print('Últimos 5 eventos de escucha cargados: ' + str(controller.lastTracks(cont)))

    #elif int(inputs[0]) == 2:
        #char=input("\nDigite la característica de contenido que desea averiguar: ")
        #print("\nBuscando número de reproducciones con "+char+" en un rango: ")
        #minValue = input("Valor mínimo: ")
        #maxValue = input("Valor máximo: ")
        #totalTracks = controller.getTracksByRangeChar(cont,char, minValue, maxValue)
        #totalArtists=
        #print("Para "+char+"entre "+minValue+" y "+maxValue" :")
        #print("\nTotal de reproducciones: " + str(totalTracks))
        #print("Total de artistas únicos: " + str(totalArtists))
        #pass

    else:
        sys.exit(0)
sys.exit(0)
