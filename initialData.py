import http.client, urllib.request, urllib.parse, urllib.error, base64
import keys
import json

headers = {
    # Request headers
    'api_key': keys.keys["PrimaryKey"],
}

params = urllib.parse.urlencode({})

def getStations():
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jStations?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        jData = json.loads(data)
        with open("stations.json", 'w') as fObj:
            json.dump(jData, fObj, indent=2)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getLines():
    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jLines?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        jData = json.loads(data)
        with open("lines.json", 'w') as fObj:
            json.dump(jData, fObj, indent=2)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def getPaths():
    params = urllib.parse.urlencode({
        # Request parameters
        'FromStationCode': 'C15',
        'ToStationCode': 'E06',
    })

    try:
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Rail.svc/json/jPath?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        jData = json.loads(data)
        with open("YellowLine.json", 'w') as fObj:
            json.dump(jData, fObj, indent=2)
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

def changeStations():
    stations = {}
    stationNameToCode = {}

    with open("stations.json", 'r') as fObj:
        stationData = json.load(fObj)
        for s in stationData["Stations"]:
            stations[s["Code"]] = s
            if s["Name"] in stationNameToCode:
                stationNameToCode[s["Name"]].append(s["Code"])
            else:
                stationNameToCode[s["Name"]] = [s["Code"]]
    return stations, stationNameToCode

def readLine(lines):
    lineData = json.load(open("./BlueLine.json"))
    lines["BL"]["Path"] = lineData["Path"]
    lineData = json.load(open("./GreenLine.json"))
    lines["GR"]["Path"] = lineData["Path"]
    lineData = json.load(open("./OrangeLine.json"))
    lines["OR"]["Path"] = lineData["Path"]
    lineData = json.load(open("./RedLine.json"))
    lines["RD"]["Path"] = lineData["Path"]
    lineData = json.load(open("./SilverLine.json"))
    lines["SV"]["Path"] = lineData["Path"]
    lineData = json.load(open("./YellowLine.json"))
    lines["YL"]["Path"] = lineData["Path"]

    return lines

def changeLines():
    lines = {}
    lineData = json.load(open("./lines.json"))
    for l in lineData["Lines"]:
        lines[l["LineCode"]] = l
    lines = readLine(lines)
    return lines

def writeToFile(file, dict):
    with open(file, 'w') as fObj:
        json.dump(dict, fObj, indent=2)

if __name__ == "__main__":
    # getStations()
    # getLines()
    # getPaths()
    stations = {}
    stationNameToCode = {}
    lines = {}
    lines = changeLines()

    stations, stationNameToCode = changeStations()

    writeToFile("./data/lines.json", lines)
    writeToFile("./data/stations.json", stations)
    writeToFile("./data/StationNameToCode.json", stationNameToCode)

