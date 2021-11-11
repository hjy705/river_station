import json, psycopg2, os, api
from datetime import datetime

with open('db.json','r', encoding = 'utf-8') as f:
    db = json.load(f)

now_time = datetime.now()
log_result = {
    "time": "",
    "status": ""
}

try:
    token_use = ""
    if os.path.isfile("token.json"):
        with open('token.json',encoding='utf-8')as f:
            token_file = json.load(f)
        # 就去抓資料時間
        if (now_time - datetime(int(token_file["now_time"][0:4]), int(token_file["now_time"][5:7]), int(token_file["now_time"][8:10]), int(token_file["now_time"][11:13]), int(token_file["now_time"][14:16]), int(token_file["now_time"][17:19]))).total_seconds() > 72000:
            # 檔案時間跟現在時間差如果大於20小時
            token_use = api.request_token()
        else:
            # 使用token.json的token
            token_use = token_file["token"]
    else:
        # 沒有檔案的話就直接去打token api
        token_use = api.request_token()
        

    # 取URL資料
    data = api.request_water_level(token_use)
    api.request_basin_rain(token_use)
    api.request_basin_rain_area(token_use)
    api.request_basin_depth_boundary(token_use)
    

    # 資料庫連線
    conn = psycopg2.connect(database=db["database"], user=db["user"] , password=db["password"], host=db["host"], port=db["port"])
    cur = conn.cursor()

    # 查找在資料庫中全部測站的最新一筆資料
    cur.execute("SELECT stationid, Max(time) FROM river_station GROUP BY stationid;")
    lastest_data_in_local_db = cur.fetchall()
    lastest_data_in_local_db_container = {}
    for eachStation in lastest_data_in_local_db:
        stationid = eachStation[0]
        time = eachStation[1]
        lastest_data_in_local_db_container[stationid] = time

    # 比對api資料以及資料庫資料
    sql_string = ""
    for value in data:
        # 單一測站最新一筆欄位資料
        stationid = value["StationId"]
        timevalue = value["Measurements"][0]["TimeStamp"]
        levelvalue = value["Measurements"][0]["Value"]
        # 判斷時間是否相同以及該測站目前有資料
        if stationid not in lastest_data_in_local_db_container.keys() :
            if levelvalue == "NaN":
                levelvalue = 'null'
            sql_string += "INSERT INTO public.river_station (stationid, time, level) VALUES ('{a}','{b}',{c});".format(a= stationid, b=timevalue, c=str(levelvalue))
        else:
            # api資料時間跟db資料時間
            if  timevalue != lastest_data_in_local_db_container[stationid]:
                if levelvalue == "NaN":
                    levelvalue = 'null'
                sql_string += "INSERT INTO public.river_station (stationid, time, level) VALUES ('{a}','{b}',{c});".format(a= stationid, b=timevalue, c=str(levelvalue))          
            else:
                pass
    else:
        pass

    # 執行insert
    if len(sql_string) > 0:
        cur.execute(sql_string)
        conn.commit()
    else:
        pass
    conn.close()

    log_result["status"] = "執行成功"
    log_result["time"] = str(now_time)
except:
    log_result["status"] = "執行失敗"
    log_result["time"] = str(now_time)

with open ('log_result.json', 'w', encoding='utf-8') as outfile:
    json.dump(log_result, outfile, ensure_ascii=False, indent=4 )
