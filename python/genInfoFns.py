import re
import pandas as pd

def parseGenInfo(genLines):

    dfDict = {}
    
    dfDict['trackName'], dfDict['month'], dfDict['day'], dfDict['year'], dfDict['raceNum'] = parseLine1(genLines[0])
    
    for line in genLines[0:]:
        if re.search('Track Record:', line) is not None:
            dfDict['distance'], dfDict['surface'] = parseDistanceSurface(line)
        elif re.search('Weather: [A-Za-z]+ Track:', line) is not None:
            dfDict['weather'], dfDict['conditions'] = parseWeatherConditions(line)
        elif re.search('Off at: [0-9:]+ Start:', line) is not None:
            dfDict['startTime'], dfDict['startNote'] = parseStart(line)
        elif re.search('Last Raced Pgm', line) is not None:
            dfDict['segment1'], dfDict['segment2'], dfDict['segment3'], dfDict['segment4'], dfDict['segment5'] = parseSegments(line)

    if dfDict['segment3'] == '':
        dfDict['segments'] = 2
    elif dfDict['segment4'] == '':
        dfDict['segments'] = 3
    elif dfDict['segment5'] == '':
        dfDict['segments'] = 4
    else:
        dfDict['segments'] = 5

    genInfoItems = pd.DataFrame(dfDict, index = [0])

    return genInfoItems


def parseLine1(line):

    fullSearch = re.search(r' *([^-]+) - ([^-]+) - (.*)', line)
    trackNameRaw = fullSearch.group(1)
    dateRaw = fullSearch.group(2)
    raceNumRaw = fullSearch.group(3)

    #track name -> abbreviated name
    trackNameFull = re.sub('[^A-Za-z ]', '', trackNameRaw)
    trackName = trackLongToShort[trackNameFull]

    #date
    dateSearch = re.search(r'([A-Za-z]*) (\d?\d), (\d\d\d\d)', dateRaw)
    monthRaw = dateSearch.group(1)
    month = monthNameToNumber[monthRaw]
    day = dateSearch.group(2)
    year = dateSearch.group(3)

    #race number
    raceNum = re.search('\d?\d', raceNumRaw).group(0)

    out = [trackName, int(month), int(day), int(year), int(raceNum)]

    return out

def parseLine2(line):
    breedRaw = re.search(r'- (.*)$', line).group(1)
    breed = re.sub('[^A-Za-z]', '', breedRaw)
    return breed

def parseDistanceSurface(line):
    fullSearch = re.search(r'([ A-Za-z]+)(?=Track)', line).group(0)
    specSearch = re.match(r' (.*) (?=On The)On The ([A-Z][a-z ]*) ', fullSearch)
    distanceRaw, surface = [specSearch.group(1), specSearch.group(2)]

    out = [distanceRaw, surface]

    return out

def parseWeatherConditions(line):
    fullSearch = re.search(r'Weather: ([A-Z][a-z]*) Track: ([A-Z][a-z]*)', line)
    weather = fullSearch.group(1)
    conditions = fullSearch.group(2)

    out = [weather, conditions]

    return out

def parseStart(line):
    fullSearch = re.search(r'Off at: (\d?\d:\d\d) Start: ([A-Z0-9][a-z0-9 ]*)', line)
    startTime = fullSearch.group(1)
    startNote = fullSearch.group(2)

    out = [startTime, startNote]

    return out

def parseSegments(line):

    fullSearch = re.search(r'PP ([A-Za-z0-9/]+) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?([A-Za-z0-9/]*) ?Fin', line)
    segment1 = fullSearch.group(1)
    segment2 = fullSearch.group(2)
    segment3 = fullSearch.group(3)
    segment4 = fullSearch.group(4)
    segment5 = fullSearch.group(5)

    return [segment1, segment2, segment3, segment4, segment5]

trackLongToShort = {}
trackShortToLong = {}
tracksDF = pd.read_csv('./../excel/tracks_v03.csv', delimiter=',', header=None)
for i in range(tracksDF.shape[0]):
    trackLongToShort[tracksDF.iloc[i,1]] = tracksDF.iloc[i,0]
    trackShortToLong[tracksDF.iloc[i,0]] = tracksDF.iloc[i,1]

monthNameToNumber = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October': 10,
    'November': 11,
    'December': 12
}