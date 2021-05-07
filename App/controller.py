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

import config as cf
from App import model
import datetime
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # catalog es utilizado para interactuar con el modelo
    analyzer = model.newAnalyzer()
    return analyzer

def loadData(analyzer, songsfile):
    """
    Carga los datos de los archivos CSV en el modelo
    """
    songsfile = cf.data_dir + songsfile
    input_file = csv.DictReader(open(songsfile, encoding="utf-8"),
                                delimiter=",")
    for track in input_file:
        model.addTrack(analyzer, track)
    return analyzer

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def tracksSize(analyzer):
    """
    Numero de crimenes leidos
    """
    return model.tracksSize(analyzer)


def indexHeight(analyzer):
    """
    Altura del indice (arbol)
    """
    return model.indexHeight(analyzer)

def indexSize(analyzer):
    """
    Numero de nodos en el arbol
    """
    return model.indexSize(analyzer)

def firstTracks(analyzer):
    """
    La menor llave del arbol
    """
    return model.firstTracks(analyzer)

def lastTracks(analyzer):
    """
    La menor llave del arbol
    """
    return model.lastTracks(analyzer)

def artistsSize(analyzer):
    """
    Numero de artistas
    """
    return model.artistsSize(analyzer)

def getTracksByRangeChar(analyzer,char,minValue, maxValue):
    
    return model.getTracksByRangeChar(analyzer,minValue, maxValue)





