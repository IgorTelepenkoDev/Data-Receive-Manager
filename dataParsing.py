import json
from datetime import datetime
import re   # needed for text modification of some data values

from dataReceiving import LOCAL_TEMP_FILE_FOR_PROCESSING

def needed_json_data_blocks(searchedType, file=LOCAL_TEMP_FILE_FOR_PROCESSING):
    resData = []    # separate result list of needed data
    jsonFile = open(file)
    if jsonFile:
        jsonDict = json.load(jsonFile)
        for checkedBlock in jsonDict:
            if checkedBlock['type'] == searchedType:
                # to store current datatime for 'songs':
                if searchedType == "song":  # better to be optimized in the future
                    checkedBlock['data']['ingestion_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                resData.append(checkedBlock['data'])

        jsonFile.close()
    return resData


def get_all_values_certain_type_from_processed_file(searchedType, file=LOCAL_TEMP_FILE_FOR_PROCESSING):
    resAllValuesFound = []   # separate result list
    allPiecesData = needed_json_data_blocks(searchedType, file)
    if searchedType == 'song':  # in order to use proper functions
        for dataBlock in allPiecesData:
            foundValues = prepared_values_song(dataBlock)
            resAllValuesFound.append(foundValues)
    if searchedType == 'movie':   # in order to use proper functions
        for dataBlock in allPiecesData:
            foundValues = prepared_values_movie(dataBlock)
            resAllValuesFound.append(foundValues)
    if searchedType == 'app':   # in order to use proper functions
        for dataBlock in allPiecesData:
            foundValues = prepared_values_app(dataBlock)
            resAllValuesFound.append(foundValues)

    return resAllValuesFound


def prepared_values_song(blockData):
    artName = None
    title = None
    year = None
    release = None
    ingTime = None
    if 'artist_name' in blockData:
        artName = blockData['artist_name']
    if 'title' in blockData:
        title = blockData['title']
    if 'year' in blockData:
        year = blockData['year']
    if 'release' in blockData:
        release = blockData['release']
    if 'ingestion_time' in blockData:
        ingTime = blockData['ingestion_time']

    resTouple = (artName, title, year, release, ingTime)
    return resTouple


def prepared_values_movie(blockData):
    origTitle = None
    origLang = None
    budget = None
    isAdult = None
    releaseDate = None

    if 'original_title' in blockData:
        origTitle = blockData['original_title']
    if 'original_language' in blockData:
        origLang = blockData['original_language']
    if 'budget' in blockData:
        budget = blockData['budget']
    if 'is_adult' in blockData:
        isAdult = blockData['is_adult']
    if 'release_date' in blockData:
        releaseDate = blockData['release_date']

    origTitleNorm = removing_wrong_chars(origTitle)   # according to the task - original_title_normalized

    resTouple = (origTitle, origLang, budget, isAdult, releaseDate, origTitleNorm)
    return resTouple


def prepared_values_app(blockData):
    name = None
    genre = None
    rate = None
    vers = None
    size = None

    if 'name' in blockData:
        name = blockData['name']
    if 'genre' in blockData:
        genre = blockData['genre']
    if 'rating' in blockData:
        rate = blockData['rating']
    if 'version' in blockData:
        vers = blockData['version']
    if 'size_bytes' in blockData:
        size = blockData['size_bytes']

    # isAwesome is TRUE when rating >= 4.5, or >=4 and general major version (for most cases - 1st digit) is <=2:
    isAwesome = rate >= 4.5 or (rate >= 4 and int(re.findall(r'\d+', vers)[0]) <= 2)

    resTouple = (name, genre, rate, vers, size, isAwesome)
    return resTouple


def removing_wrong_chars(strName):
    if strName:
        strName = strName.lower()
        strName = re.sub("[^a-z0-9 ]+", "", strName)
        strName = re.sub(" ", "_", strName)
    return strName
