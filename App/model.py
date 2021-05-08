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
from DISClib.ADT import map as m

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
                'artists': None,
                'char': None,
                'char2': None,
                'char3': None,
                }

    analyzer['tracks'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['songs'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['artists'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['char'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['char2'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
    analyzer['char3'] = om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)
                                      
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

def addTrackChar(analyzer, track, char, key):
    """
    """
    updateChar(analyzer[key], track, char)
    return analyzer

def updateChar(map, track, char):
    """
    """
    CharValue = track[char]
    entry = om.get(map, CharValue)
    if entry is None:
        charentry = newDataEntry(track)
        om.put(map, CharValue, charentry)
    else:
        charentry = me.getValue(entry)
    
    if char=="char":
        addCharIndex(charentry, track, 'artist_id')
    else:
        addCharIndex(charentry, track, 'track_id')
    return map

def addCharIndex(charentry, track, indexChosen):
    """
    Actualiza un indice de artistas.  Este indice tiene una lista
    de tracks y una tabla de hash cuya llave es el artista y
    el valor es una lista con los tracks de dicho artista en el valor de la característica que
    se está consultando (dada por el nodo del arbol)
    """
    lst = charentry['lstTracks']
    lt.addLast(lst, track)
    index = charentry['info']
    artistentry = m.get(index, track[indexChosen])
    if (artistentry is None):
        entry = newArtistEntry(track[indexChosen], track)
        lt.addLast(entry['lstindex'], track)
        m.put(index, track[indexChosen], entry)
    else:
        entry = me.getValue(artistentry)
        lt.addLast(entry['lstindex'], track)
    return charentry
# Funciones para creacion de datos

def newDataEntry(track):
    """
    """
    entry = {'info': None, 'lstTracks': None}
    entry['info'] = mp.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareValue)
    entry['lstTracks'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry

def newArtistEntry(artist, track):
    """
    Crea una entrada en el indice por artista, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    artentry = {'index': None, 'lstindex': None}
    artentry['index'] = artist
    artentry['lstindex'] = lt.newList('SINGLELINKED', compareValue)
    return artentry

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

def getTracksByRangeChar(analyzer, minValue, maxValue, char):
    """
    Retorna el numero de registros de eventos de escucha en un rango de una 
    característica de contenido dada.
    """
    lst = om.values(analyzer[char], minValue, maxValue)
    totTracks = 0
    for lstchar in lt.iterator(lst):
        totTracks += lt.size(lstchar['lstTracks'])
    return totTracks


def indexHashSize(analyzer,minValue, maxValue, char):

    lst=om.keys(analyzer[char], minValue, maxValue)
    size=0
    aux=[]
  
    for value in lt.iterator(lst):   
        charValue = om.get(analyzer[char], value)
        ids = me.getValue(charValue)["info"]
        idValues = m.keySet(ids)

        for key in lt.iterator(idValues):   
            if str(key) not in aux:
                aux.append(key)
                size+=1
            
    return size
    

def getPartySongs(analyzer,minEnergy, maxEnergy,minDance, maxDance):

    energyAux=[]
    energySongs=om.keys(analyzer["char2"], minEnergy, maxEnergy)
    s1=0

    for value in lt.iterator(energySongs):   
        charValue = om.get(analyzer["char2"], value)
        ids = me.getValue(charValue)["info"]
        idValues = m.keySet(ids)

        for key in lt.iterator(idValues):   
            if str(key) not in energyAux:
                energyAux.append(key)
                s1+=1

    danceAux=[]
    danceSongs=om.keys(analyzer["char3"], minDance, maxDance)
    s2=0
    for value in lt.iterator(danceSongs):   
        charValue = om.get(analyzer["char3"], value)
        ids = me.getValue(charValue)["info"]
        idValues = m.keySet(ids)

        for key in lt.iterator(idValues):   
            if str(key) not in danceAux:
                danceAux.append(key)
                s2+=1

    ##comparando las dos listas

    combined=combinedList(energyAux,danceAux)

    totSongs=0
   
    for i in combined:
        totSongs+=1

    return totSongs

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

def compareDates(date1, date2):
    """
    Compara dos datos
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareValue(value1, value2):
    """
    Compara dos tipos de valor de una característica
    """
    value = me.getKey(value2)
    if (value1 == value):
        return 0
    elif (value1 > value):
        return 1
    else:
        return -1

# Funciones utilizadas para comparar elementos entre dos listas

def combinedList(list1,list2):
    result=[]
    for element in list1:
        if element in list2:
            result.append(element)
    return result
    
    pass
