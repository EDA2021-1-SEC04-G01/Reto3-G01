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
    -canciones
    -artistas
    Retorna el analizador inicializado.
    """
    analyzer = {'tracks': None,
                'songs': None,
                'artists': None
                }

    analyzer['tracks'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['songs'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareSongs)
    analyzer['artists'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareArtists)
    return analyzer

# Funciones para agregar informacion al catalogo

def addTrack(analyzer, track):
    """
    """
    lt.addLast(analyzer['tracks'], track)
    updateSongs(analyzer['songs'], track)
    updateArtists(analyzer['artists'], track)
    return analyzer

def updateSongs(map, track):
    """
    Se toma el id de la canción y se busca si ya existe en el arbol
    dicha cancion.  Si es asi, se adiciona a su lista de reproducciones
    y se actualiza el indice de canciones.
    Si no se encuentra creado un nodo para esa cancion en el arbol
    se crea y se actualiza el indice de canciones
    """
    songId = track["track_id"]
    entry = om.get(map, songId)
    if entry is None:
        songentry = newDataEntry(track)
        om.put(map, songId, songentry)
    else:
        songentry = me.getValue(entry)
    return map

def updateArtists(map, track):
    """
    """
    artistId = track["artist_id"]
    entry = om.get(map, artistId)
    if entry is None:
        artistentry = newDataEntry(track)
        om.put(map, artistId, artistentry)
    else:
        artistentry = me.getValue(entry)
    
    return map

# Funciones para creacion de datos

def newDataEntry(track):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'artist': None, 'lsttracks': None}
    entry['artist'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareHashtags)
    entry['lsttracks'] = lt.newList('SINGLE_LINKED', compareSongs)
    return entry



# Funciones de consulta

def tracksSize(analyzer):
    """
    Número de reproducciones
    """
    return lt.size(analyzer['tracks'])

def indexHeight(analyzer):
    """
    Altura del arbol
    """
    return om.height(analyzer['songs'])

def indexSize(analyzer):
    """
    Numero de elementos en el indice
    """
    return om.size(analyzer['songs'])

def firstTracks(analyzer):
    """
    5 primeros eventos cargados 
    """
    return lt.subList(analyzer['tracks'],0,4)

def lastTracks(analyzer):
    """
    5 últimos eventos cargados 
    """
    
    final=int(tracksSize(analyzer))
    inicio=final-3

    return lt.subList(analyzer['tracks'],inicio,4)

def artistsSize(analyzer):
    """
    Numero de artistas
    """
    return om.size(analyzer['artists'])

def getTracksByRangeChar(analyzer,char, minValue, maxValue):
    """
    Retorna el numero de registros de eventos de escucha en un rango de una 
    característica de contenido dada.
    """
    lst = om.values(analyzer[char], minValue, maxValue)
    totTracks = 0
    for lstchar in lt.iterator(lst):
        totTracks += lt.size(lstdate['lstTracks'])
    return totTracks


# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(id1, id2):
    """
    Compara dos tracks
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareSongs(song1, song2):
    """
    Compara dos canciones (ids)
    """
    if (song1 == song2):
        return 0
    elif (song1 > song2):
        return 1
    else:
        return -1

def compareArtists(artist1, artist2):
    """
    Compara dos artistas
    """
    if (artist1 == artist2):
        return 0
    elif (artist1 > artist2):
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
