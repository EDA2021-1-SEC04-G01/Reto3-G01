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
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
import datetime
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador
    Crea una lista vacia para guardar todas las canciones
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas
    Retorna el analizador inicializado.
    """
    analyzer = {'songs': None,
                'dateIndex': None
                }

    analyzer['songs'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    return analyzer

# Funciones para agregar informacion al catalogo

def addSong(analyzer, song):
    """
    """
    lt.addLast(analyzer['songs'], song)
    updateDateIndex(analyzer['dateIndex'], song)
    return analyzer

def updateDateIndex(map, song):
    """
    Se toma la fecha de la canción y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de canciones
    y se actualiza el indice de tipos de canciones.
    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de canciones
    """
    createdat = song["created_at"]
    songdate = datetime.datetime.strptime(createdat, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, songdate.date())
    if entry is None:
        datentry = newDataEntry(song)
        om.put(map, songdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, song)
    return map

# Funciones para creacion de datos

def addDateIndex(datentry, song):
    """
    Actualiza un indice de caracteristica de contenido.  Este indice tiene una lista
    de canciones y una tabla de hash cuya llave es el hashtag y
    el valor es una lista con las canciones que tienen el hashtag en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstsongs']
    lt.addLast(lst, song)
    hashtagIndex = datentry['hashtagIndex']
    offentry = mp.get(hashtagIndex, song['hashtag'])
    if (offentry is None):
        entry = newHashtagEntry(song['hashtag'], song)
        lt.addLast(entry['lsthashtags'], song)
        mp.put(hashtagIndex, song['hashtag'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lsthashtags'], song)
    return datentry

def newDataEntry(song):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'hashtagIndex': None, 'lstsongs': None}
    entry['hashtagIndex'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareHashtags)
    entry['lstsongs'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newHashtagEntry(hashtaggrp, song):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    hashtagentry = {'hashtag': None, 'lsthashtags': None}
    hashtagentry['hashtag'] = hashtaggrp
    hashtagentry['lsthashtags'] = lt.newList('SINGLELINKED', compareHashtags)
    return hashtagentry

# Funciones de consulta

def songsSize(analyzer):
    """
    Número de crimenes
    """
    return lt.size(analyzer['songs'])

def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['dateIndex'])

def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['dateIndex'])



# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    """
    Compara dos canciones
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareDates(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareHashtags(hashtag1, hashtag2):
    """
    Compara dos hashtags
    """
    hashtag = me.getKey(hashtag2)
    if (hashtag1 == hashtag):
        return 0
    elif (hashtag1 > hashtag):
        return 1
    else:
        return -1

# Funciones de ordenamiento
