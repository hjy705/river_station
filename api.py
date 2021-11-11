import requests, json
from datetime import datetime


def request_token():
    payload = 'grant_type=client_credentials'
    headers = {
        'Authorization': 'Basic cG0rRHEzUGxmaEdQUS8xRk9LL1lkbStpT295TE9MRkVqMFZ1aHB6Tng1QT06UnFuL3BQVno1SWFySFJCcTAyY090Q0pFbVFtNVIyVzMrRUUxTFB1cFI3VT0=',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", "https://iot.wra.gov.tw/Oauth2/token", headers=headers, data=payload).json()
    container = {
        "token": response["access_token"],
        "now_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    result = container["token"]
    with open('token.json','w', encoding = 'utf-8') as outfile:
        json.dump(container , outfile , ensure_ascii=False , indent=4)
    return result

def request_water_level(token):
    headers = {
        'Authorization': 'Bearer' + ' ' + token,
    }
    response = requests.request(
        "GET", "https://iot.wra.gov.tw/river/stations?countyCode=65000", headers=headers).json()
    return response

def request_basin_rain(token):
    headers = {
        'Authorization': 'Bearer' + ' ' + token,
    }

    response = requests.request(
        "GET", "https://iot.wra.gov.tw/precipitation/basins", headers=headers).json()

    with open('basin_rain.json','w' , encoding='utf-8') as outfile:
        json.dump(response, outfile, ensure_ascii=False, indent=4)

def request_basin_rain_area(token):
    headers = {
        'Authorization': 'Bearer' + ' ' + token,
    }

    response = requests.get("https://iot.wra.gov.tw/rasterMap/inundation?region=peipeikeelung&forecastHours=0")
    headers=headers

    file = open("basin_depth_area.png", "wb")
    file.write(response.content)
    file.close()

def request_basin_depth_boundary(token):
    headers = {
        'Authorization': 'Bearer' + ' ' + token,
    }

    response = requests.request(
        "GET", "https://iot.wra.gov.tw/rasterMap/inundation/rasetMapMetaData?region=peipeikeelung&forecastHours=0", headers=headers).json()

    with open('basin_depth_boundary.json','w' , encoding='utf-8')as outfile:
        json.dump(response,outfile, ensure_ascii=False, indent=4)