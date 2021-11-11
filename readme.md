# **River station Project**

## **專案說明**
<br>
對比資料時間，相差二十小時以上即向資料網站發出請求取得token後，獲得雨量站資料，並匯入其他資料。連接本地端postgreSQL資料庫，查找到每筆資料庫最新的資料，與api資料做對比，抓取資料進行更新。
<br>
</br>

## **環境說明**
<br>Windows 10 家用版；
<br>Python version 3.6.8

</br>

## **檔案說明**
<br>run.py 為撰寫之主要程式
<br>inser.py 第一次匯入本地資料庫之程式
<br>token.json 透過Postman取得的token
<br>log_result.json 顯示專案結果是否執行
<br>db.json 存放涉及隱私相關的資料；db_template.json為db.json的空模板
<br>basin_rain.json/basin_depth_boudary.json 讀取網站匯入的資料
<br>basin_depth_area.png 讀取網站匯入的圖片
<br>run.bat 執行主程式之批次檔
<br>requirements.txt存放虛擬環境下所設的套件

</br>

## **成果說明**
<br>
在PostgreSQL本地端資料庫匯入api取得的最新資料

![PostgreSQL更新資料](./image/postgreSQL.jpg)