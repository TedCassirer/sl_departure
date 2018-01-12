import requests
import api_keys

station_id_cache = {}

def get_departures(from_station="Vårdcentralen (Värmdö)",
                   end_station="Slussen"):
    parameters = {
        "key" : api_keys.reseplanerare,
        "originId" : get_station_id(from_station),
        "destId" : get_station_id(end_station),
        "searchForArrival" : 0,
        "maxChange" : 0,
    }
    get_url = "http://api.sl.se/api2/TravelplannerV3/trip.json?" + \
              get_parameter_string(parameters)
    get_data = requests.get(get_url)
    js = get_data.json()
    if get_data.status_code == 200 and "Trip" in js:
        return js["Trip"]
    else:
        raise Exception(js)


def get_station_id(station_name, cache=station_id_cache):
    if station_name in cache:
        return cache[station_name]
    parameters = {
        "searchstring" : station_name,
        "stationsonly" : True,
        "key" : api_keys.platsuppslag,
    }
    get_url = "http://api.sl.se/api2/typeahead.json?" + get_parameter_string(parameters)
    get_data = requests.get(get_url)
    js = get_data.json()
    if get_data.status_code == 200:
        station_id = js["ResponseData"][0]["SiteId"]
        cache[station_name] = station_id
        return station_id
    else:
        raise Exception(js)


def get_parameter_string(parameters):
    res = [str(k) + "=" + str(v) for k, v in parameters.items()]
    return "&".join(res)