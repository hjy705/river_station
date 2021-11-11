import psycopg2,api

conn = psycopg2.connect(database="river_station", user="postgres", password="890705", host="127.0.0.1", port="5432")

cur = conn.cursor()

token_use = api.request_token()
data = api.request_data(token_use)
for value in data:
    # 單一測站最新一筆欄位資料
    stationid = value["StationId"]
    timevalue = value["Measurements"][0]["TimeStamp"]
    levelvalue = value["Measurements"][0]["Value"]
    if levelvalue == "NaN":
        levelvalue = 'null'
    cur.execute("INSERT INTO public.river_station (stationid, time, level)VALUES ('{a}','{b}',{c});".format(a= stationid, b=timevalue, c=str(levelvalue)))


conn.commit()
conn.close()