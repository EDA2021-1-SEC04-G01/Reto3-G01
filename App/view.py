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
import model
import datetime
import time
import tracemalloc

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

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
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
        char= char+"artisthash"
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        controller.loadDataChar(cont, songfile, char, key)
        
        
        char=char.replace("artisthash", "")
        print("\nBuscando número de reproducciones con "+char+" en un rango: ")
        minValue = input("Valor mínimo: ")
        maxValue = input("Valor máximo: ")
        totalTracks = controller.getTracksByRangeChar(cont, minValue, maxValue, key)
        totalArtists=controller.indexHashSize(cont, minValue, maxValue, key)
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nPara "+char+" entre "+minValue+" y "+maxValue+":")
        print("Total de reproducciones: " + str(totalTracks))
        print("Total de artistas únicos: " + str(totalArtists))
        controller.clearChar(cont,key)
        print("Tiempo [ms]: ", f"{delta_time:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{delta_memory:.3f}")

    elif int(inputs[0]) == 3:
        energy="energy"
        danceability="danceability"
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        controller.loadDataChar(cont, songfile, energy, "char2")
        controller.loadDataChar(cont, songfile, danceability, "char3")
        minEnergy=input("\nDigite el valor mínimo de la característica Energy: ")
        maxEnergy=input("Digite el valor máimo de la característica Energy: ")
        minDance=input("Digite el valor mínimo de la característica Danceability: ")
        maxDance=input("Digite el valor máximo de la característica Danceability: ")
        print("\nBuscando música para festejar: ")
        totalSongs=controller.getRecommendedSongs(cont,minEnergy, maxEnergy,minDance, maxDance)
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nPara Energy (Energía) entre "+minEnergy+" y "+maxEnergy+" y Danceability (Capacidad de Baile) entre "+minDance+" y "+maxDance+":")
        print("Total de pistas únicas: " + str(totalSongs))
        print("Tiempo [ms]: ", f"{delta_time:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{delta_memory:.3f}")
        controller.clearChar(cont,"char2")
        controller.clearChar(cont,"char3")
        

    elif int(inputs[0]) == 4:
        instrumentalness="instrumentalness"
        tempo="tempo"
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        controller.loadDataChar(cont, songfile, instrumentalness, "char2")
        controller.loadDataChar(cont, songfile, tempo, "char3")
        minIns=input("\nDigite el valor mínimo de la característica Instrumentalness: ")
        maxIns=input("Digite el valor máximo de la característica Instrumentalness: ")
        minTempo=input("Digite el valor mínimo de la característica Tempo: ")
        maxTempo=input("Digite el valor máximo de la característica Tempo: ")
        print("\nBuscando música para estudiar: ")
        totalSongs=controller.getRecommendedSongs(cont,minIns, maxIns,minTempo, maxTempo)
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        print("\nPara Instrumentalness entre "+minIns+" y "+maxIns+" y Tempo entre "+minTempo+" y "+maxTempo+":")
        print("Total de pistas únicas: " + str(totalSongs))
        print("Tiempo [ms]: ", f"{delta_time:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{delta_memory:.3f}")
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
            delta_time = -1.0
            delta_memory = -1.0
            tracemalloc.start()
            start_time = getTime()
            start_memory = getMemory()
            controller.loadDataChar(cont, songfile, "tempo", "char")
            totals=controller.BPMbyGender(cont,str(gender))
            stop_memory = getMemory()
            stop_time = getTime()
            tracemalloc.stop()
            delta_time = stop_time - start_time
            delta_memory = deltaMemory(start_memory, stop_memory)
            print("\nTotal de reproducciones en "+str(gender)+" y el total de artistas únicos: " + str(totals))
            print("Tiempo [ms]: ", f"{delta_time:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{delta_memory:.3f}")
            controller.clearChar(cont,"char")

        #totalTracks= #es desde el tempo mas chiquito hasta el mas grande
        #print("\nTotal de reproducciones: " + str(totalTracks))


    elif int(inputs[0]) == 6:
        begtime= input("Ingrese la hora de inicio del rango(H:M:S): ")
        fintime= input("Ingrese la hora de fin del rango(H:M:S): ")
        begtime= datetime.datetime.strptime(begtime, '%H:%M:%S').time()
        fintime= datetime.datetime.strptime(fintime, '%H:%M:%S').time()
        delta_time = -1.0
        delta_memory = -1.0
        tracemalloc.start()
        start_time = getTime()
        start_memory = getMemory()
        controller.loadDataChar(cont, songfile, "created_at", "char")
        stop_memory = getMemory()
        stop_time = getTime()
        tracemalloc.stop()
        delta_time = stop_time - start_time
        delta_memory = deltaMemory(start_memory, stop_memory)
        model.getGenreByTime(cont,begtime,fintime)
        print("Tiempo [ms]: ", f"{delta_time:.3f}", "  ||  ",
              "Memoria [kB]: ", f"{delta_memory:.3f}")
        controller.clearChar(cont,"char")
        controller.clearChar(cont,"char2")
        controller.clearChar(cont,"char3")
        


    else:
        sys.exit(0)
sys.exit(0)

        

