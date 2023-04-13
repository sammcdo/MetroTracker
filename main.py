import http.client, urllib.request, urllib.parse, urllib.error, base64
import json
import time
import keys

headers = {
    # Request headers
    'api_key': keys.keys["PrimaryKey"],
}

params = urllib.parse.urlencode({
})

def updateTracker():
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/StationPrediction.svc/json/GetPrediction/All?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data

def transformPredictions(predictions):
    stationPredictions = {}
    for t in predictions:
        loc = t["LocationCode"]
        if loc not in stationPredictions:
            stationPredictions[loc] = [t]
        else:
            stationPredictions[loc].append(t)
    return stationPredictions

def stationSetup(last, predictions):
    entry = input("Enter a station name or Q to quit:\n")
    if time.time()-last > 10:
        predictions = updateTracker()
        last = time.time()
    predictions = transformPredictions(predictions["Trains"])
    return entry, predictions, last

def getPredictions(trainList):
    #Car #\tLine #\t Dest \tMin
    print("Car\tLine\tDest\tMin")
    gr1=""
    gr2=""
    for item in trainList:
        if item["Group"] == "1":
            gr1+=item["Car"]+"\t"+item["Line"]+"\t"+item["Destination"]+"\t"+item["Min"]+"\n"
        else:
            gr2+=item["Car"]+"\t"+item["Line"]+"\t"+item["Destination"]+"\t"+item["Min"]+"\n"
    print(gr1[:-1])
    print("-----------------------------------------")
    print(gr2[:-1])

def main():
    lines = json.load(open("./data/lines.json"))
    stations = json.load(open("./data/stations.json"))
    stationNameToCode = json.load(open("./data/StationNameToCode.json"))

    lineCodeToFull = {
        "RD": "Red",
        "GR": "Green",
        "YL": "Yellow",
        "SV": "Silver",
        "OR": "Orange",
        "BL": "Blue",
    }

    predictions = {}
    stationList = []
    last = 0
    entry = ""

    for name in stationNameToCode:
        stationList.append(name)

    entry, predictions, last = stationSetup(last, predictions)

    while entry != "Q":
        if entry not in stationList:
            print("Station not in Station List - Please try again.")
        else:
            print("\nNext trains at "+entry+" are: ")
            stationCodes = stationNameToCode[entry]
            if len(stationCodes) == 2:
                for code in stationCodes:
                    stationObj = stations[code]
                    possibleLines = [stationObj["LineCode1"], stationObj["LineCode2"], stationObj["LineCode3"]]
                    servicedLines = []

                    for pl in possibleLines:
                        if pl:
                            servicedLines.append(lineCodeToFull[pl])


                    if len(servicedLines) == 3:
                        servicedLines[-1] = "and " + servicedLines[-1]
                        servicedLines = ', '.join(servicedLines)
                    elif len(servicedLines) == 2:
                        servicedLines[-1] = "and " + servicedLines[-1]
                        servicedLines = ' '.join(servicedLines)
                    else:
                        servicedLines = ' '.join(servicedLines)
                    print("On the platform servicing the "+servicedLines+"lines:")
                    getPredictions(predictions[code])
            else:
                code = stationCodes[0]
                getPredictions(predictions[code])

            entry, predictions, last = stationSetup(last, predictions)


if __name__ == "__main__":
    main()