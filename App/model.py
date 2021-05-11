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
import random
import datetime
import csv

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
    analyzer['char4'] = mp.newMap(numelements=50,
                                     maptype='PROBING',
                                     comparefunction=compareValue)
                                      
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
    artist= False
    if "artisthash" in char:
        char=char.replace("artisthash", "")
        artist= True
    CharValue = track[char]
    if char == "created_at":
        CharValue= datetime.datetime.strptime(CharValue, '%Y-%m-%d %H:%M:%S').time()
    entry = om.get(map, CharValue)
    if entry is None:
        charentry = newDataEntry(track)
        om.put(map, CharValue, charentry)
    else:
        charentry = me.getValue(entry)
    if artist:
        addCharIndex(charentry, track, 'artist_id')
    else:
        addCharIndex(charentry, track, 'track_id')
    return map

def clearChar(analyzer, char):

    analyzer[char] = None
    analyzer[char]=om.newMap(omaptype='RBT',
                                      comparefunction=compareDates)


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
    entry['info'] = mp.newMap(numelements=50,
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

def newGender(analyzer,minTempo,maxTempo):

    tracks=getTracksByRangeChar(analyzer, minTempo, maxTempo, "char")
    artists=indexHashSize(analyzer, minTempo, maxTempo, "char")
    samples=indexHashSamples(analyzer,minTempo, maxTempo, "char")

    return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)
     
def BPMbyGender(analyzer,gen):

    if "Reggae"==gen:
        tracks=getTracksByRangeChar(analyzer, str(60), str(90), "char")
        artists=indexHashSize(analyzer, str(60), str(90), "char")
        samples=indexHashSamples(analyzer,str(60), str(90), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

    if "Down-tempo"==gen:
        tracks=getTracksByRangeChar(analyzer, str(70), str(100), "char")
        artists=indexHashSize(analyzer,str(70), str(100), "char")
        samples=indexHashSamples(analyzer,str(70), str(100), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

    if "Chill-out"==gen:
        tracks=getTracksByRangeChar(analyzer, str(90), str(120), "char")
        artists=indexHashSize(analyzer,  str(90), str(120), "char")
        samples=indexHashSamples(analyzer,str(90), str(120), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)
    
    if "Hip-hop"==gen:
        tracks=getTracksByRangeChar(analyzer, str(85), str(115), "char")
        artists=indexHashSize(analyzer, str(85), str(115), "char")
        samples=indexHashSamples(analyzer,str(85), str(115), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

    if "Jazz and Funk"==gen:
        tracks=getTracksByRangeChar(analyzer, str(120), str(125), "char")
        artists=indexHashSize(analyzer,  str(120), str(125), "char")
        samples=indexHashSamples(analyzer, str(120), str(125), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

    if "Pop"==gen:
        tracks=getTracksByRangeChar(analyzer, str(100), str(130), "char")
        artists=indexHashSize(analyzer, str(100), str(130), "char")
        samples=indexHashSamples(analyzer,str(100), str(130), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)
    
    if "R&B"==gen:
        tracks=getTracksByRangeChar(analyzer, str(60), str(80), "char")
        artists=indexHashSize(analyzer, str(60), str(80), "char")
        samples=indexHashSamples(analyzer,str(60), str(80), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)       

    if "Rock"==gen:

        tracks=getTracksByRangeChar(analyzer, str(110), str(140), "char")
        artists=indexHashSize(analyzer, str(110), str(140), "char")
        samples=indexHashSamples(analyzer,str(110), str(140), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

    if "Metal"==gen:
        tracks=getTracksByRangeChar(analyzer, str(110), str(160), "char")
        artists=indexHashSize(analyzer, str(110), str(160), "char")
        samples=indexHashSamples(analyzer,str(110), str(160), "char")

        return str(tracks)+" reproducciones y "+str(artists)+" artistas. \n Algunos artistas son: "+str(samples)

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

def indexHashSamples(analyzer,minValue, maxValue, char):

    lst=om.keys(analyzer[char], minValue, maxValue)
    aux=[]
    size=0
  
    for value in lt.iterator(lst):   
        charValue = om.get(analyzer[char], value)
        ids = me.getValue(charValue)["info"]
        idValues = m.keySet(ids)

        for key in lt.iterator(idValues):   
            if str(key) not in aux:
                aux.append(key)
                size+=1
        
    if size>10:
        randomIndex=random.choices(aux, k=10)
    else:
        randomIndex=random.choices(aux, k=size)
    return randomIndex


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
    

def getRecommendedSongs(analyzer,minEnergy, maxEnergy,minDance, maxDance):

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

    
    if totSongs>5:
        randomIndex=random.choices(combined, k=5)
    else:
        randomIndex=random.choices(combined, k=totSongs)

    return str(totSongs)+"\n5 pistas aleatorias dentro de los rangos:"+str(randomIndex)

def getGenreByTime(analyzer,begtime,fintime):
    aux= {}
    auxlist= []
    timesongs=om.keys(analyzer["char"], begtime, fintime)
    for value in lt.iterator(timesongs):   
        charValue = om.get(analyzer["char"], value)
        ids = me.getValue(charValue)['lstTracks']        
        for track in lt.iterator(ids):   
            CharValue = track["tempo"]
            entry = om.get(analyzer["char2"], CharValue)
            if entry is None:
                charentry = newDataEntry(track)
                om.put(analyzer["char2"], CharValue, charentry)
            else:
                charentry = me.getValue(entry)
            addCharIndex(charentry, track, 'track_id')
    aux["reggae"]= getTracksByRangeChar(analyzer, str(60), str(90), "char2")
    aux["downtempo"]= getTracksByRangeChar(analyzer, str(70), str(100), "char2")
    aux["chillout"]= getTracksByRangeChar(analyzer, str(90), str(120), "char2")
    aux["hiphop"]= getTracksByRangeChar(analyzer, str(85), str(115), "char2")
    aux["jazzfunk"]= getTracksByRangeChar(analyzer, str(120), str(125), "char2")
    aux["pop"]= getTracksByRangeChar(analyzer, str(100), str(130), "char2")
    aux["rnb"]= getTracksByRangeChar(analyzer, str(60), str(80), "char2")
    aux["rock"]= getTracksByRangeChar(analyzer, str(110), str(140), "char2")
    aux["metal"]= getTracksByRangeChar(analyzer, str(110), str(160), "char2")
    genre= max(aux, key=aux.get)
    print("El genero mas escuchado es "+genre+" con "+str(aux[genre])+" reproducciones")
    if genre == "reggae":
        minValue= 60
        maxValue= 90
    elif genre == "downtempo":
        minValue= 70
        maxValue= 100
    elif genre == "chillout":
        minValue= 90
        maxValue= 120
    elif genre == "hiphop":
        minValue= 85
        maxValue= 115
    elif genre == "jazzfunk":
        minValue= 120
        maxValue= 125
    elif genre == "pop":
        minValue= 100
        maxValue= 130
    elif genre == "rnb":
        minValue= 60
        maxValue= 80
    elif genre == "rock":
        minValue= 110
        maxValue= 140
    elif genre == "metal":
        minValue= 110
        maxValue= 160
    genrelist= om.values(analyzer["char2"], str(minValue), str(maxValue))
    for i in lt.iterator(genrelist):
        for k in lt.iterator(i['lstTracks']):
            if k["track_id"] not in auxlist:
                auxlist.append(k["track_id"])
    songsfile = cf.data_dir + "user_track_hashtag_timestamp-small.csv"
    input_file = csv.DictReader(open(songsfile, encoding="utf-8"),
                                delimiter=",")
    for line in input_file:
        song= line["track_id"]
        entry= om.get(analyzer["char3"], song)
        if entry is None:
            hashtag= []
            hashtag.append(line["hashtag"])
            om.put(analyzer["char3"], song, hashtag)
        else:
            a= me.getValue(entry)
            if line["hashtag"] not in a:              
               a.append(line["hashtag"])
    songsfile2 = cf.data_dir + "sentiment_values.csv"
    input_file2 = csv.DictReader(open(songsfile2, encoding="utf-8"),
                                delimiter=",")
    for line in input_file2:
        hashtag= line["hashtag"]
        if line["vader_avg"] == "" or line["vader_avg"] == " ":
            value= 0
        else:
            value= float(line["vader_avg"])    
        mp.put(analyzer["char4"], hashtag, value)
    
    top10= {}
    tracks= {}
    for i in auxlist:
        vadersum= 0
        cont= 0
        hashtags=om.get(analyzer["char3"], i)
        hashtags=me.getValue(hashtags)
        top10[i]= len(hashtags)
        for k in hashtags:
            k= k.lower()
            vaderval=mp.get(analyzer["char4"], k)
            if vaderval != None:              
                vaderval=me.getValue(vaderval)
                if vaderval > 0:
                    cont+=1
                    vadersum += vaderval 
        if cont != 0: 
          vaderavg= vadersum/ cont
        else:
          vaderavg= 0
        tracks[i]= vaderavg
    cont= 0
    while cont < 10:
       a=max(top10, key=top10.get)
       print("\n TOP "+str(cont+1)+" track: "+a+" with "+str(top10[a])+" hashtags"+" and VADER = "+str(tracks[a]))
       del top10[a]
       cont +=1

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


