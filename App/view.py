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

    elif int(inputs[0]) == 2:  
        key="char" 
        char=input("\nDigite la característica de contenido que desea averiguar: ")
        controller.loadDataChar(cont, songfile, char, key)
        print("\nBuscando número de reproducciones con "+char+" en un rango: ")
        minValue = input("Valor mínimo: ")
        maxValue = input("Valor máximo: ")
        totalTracks = controller.getTracksByRangeChar(cont, minValue, maxValue, key)
        totalArtists=controller.indexHashSize(cont, minValue, maxValue, key)
        print("\nPara "+char+" entre "+minValue+" y "+maxValue+":")
        print("Total de reproducciones: " + str(totalTracks))
        print("Total de artistas únicos: " + str(totalArtists))
        controller.clearChar(cont,key)
        print()

    elif int(inputs[0]) == 3:
        energy="energy"
        danceability="danceability"
        controller.loadDataChar(cont, songfile, energy, "char2")
        controller.loadDataChar(cont, songfile, danceability, "char3")
        minEnergy=input("\nDigite el valor mínimo de la característica Energy: ")
        maxEnergy=input("Digite el valor mánimo de la característica Energy: ")
        minDance=input("Digite el valor mínimo de la característica Danceability: ")
        maxDance=input("Digite el valor mánimo de la característica Danceability: ")
        print("\nBuscando música para festejar: ")
        totalSongs=controller.getRecommendedSongs(cont,minEnergy, maxEnergy,minDance, maxDance)
        print("\nPara Energy (Energía) entre "+minEnergy+" y "+maxEnergy+" y Danceability (Capacidad de Baile) entre "+minDance+" y "+maxDance+":")
        print("Total de pistas únicas: " + str(totalSongs))
        controller.clearChar(cont,"char2")
        controller.clearChar(cont,"char3")
        print()

    elif int(inputs[0]) == 4:
        instrumentalness="instrumentalness"
        tempo="tempo"
        controller.loadDataChar(cont, songfile, instrumentalness, "char2")
        controller.loadDataChar(cont, songfile, tempo, "char3")
        minIns=input("\nDigite el valor mínimo de la característica Instrumentalness: ")
        maxIns=input("Digite el valor mánimo de la característica Instrumentalness: ")
        minTempo=input("Digite el valor mínimo de la característica Tempo: ")
        maxTempo=input("Digite el valor mánimo de la característica Tempo: ")
        print("\nBuscando música para estudiar: ")
        totalSongs=controller.getRecommendedSongs(cont,minIns, maxIns,minTempo, maxTempo)
        print("\nPara Instrumentalness entre "+minIns+" y "+maxIns+" y Tempo entre "+minTempo+" y "+maxTempo+":")
        print("Total de pistas únicas: " + str(totalSongs))
        controller.clearChar(cont,"char2")
        controller.clearChar(cont,"char3")

    elif int(inputs[0]) == 5:
        genderLst=input("\nDigite la lista de géneros musicales que se desea buscar. (ej.: Reggae, Hip-hop, Pop): ")
        newGender=int(input("Si desea agregar un nuevo género musical en la búsqueda presione 1, de lo contrario, 0: "))
        if newGender==1:
            print("\ndigite las siguientes variables para el nuevo género musical: ")
            name=input("Nombre único para el nuevo género musical: ")
            minTempo=input("Valor mínimo del Tempo del nuevo género musical: ")
            maxTempo=input("Valor máximo del Tempo del nuevo género musical: ")
            print("\nSe ha creado el nuevo género musical")
            controller.loadDataChar(cont, songfile, "tempo", "char")
            newGenTotals=controller.newGender(cont,minTempo,maxTempo)
            print("\n(Total de reproducciones en "+name+" y el total de artistas únicos) y algunos artistas: " + str(newGenTotals))

            controller.clearChar(cont,"char")
        
        genLst=genderLst.split(", ")

        for gender in genLst:
    
            controller.loadDataChar(cont, songfile, "tempo", "char")
            totals=controller.BPMbyGender(cont,str(gender))
            print("\nTotal de reproducciones en "+str(gender)+" y el total de artistas únicos: " + str(totals))
            controller.clearChar(cont,"char")

        #totalTracks= #es desde el tempo mas chiquito hasta el mas grande
        #print("\nTotal de reproducciones: " + str(totalTracks))

    elif int(inputs[0]) == 6:

        pass

    else:
        sys.exit(0)
sys.exit(0)

        

