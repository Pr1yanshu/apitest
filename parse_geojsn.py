#This script pasrses the geojson file and copies all its content to a postgresql table named geo_table.
import geojson
import psycopg2
conn = psycopg2.connect(dbname="apitest", user="Priyanshu", password="pr1yanshu")
with open("C:/apitest/Database/map.geojson","r") as f:
        gj = geojson.load(f)
for feature in gj["features"]:
	name = feature["properties"]["name"]
	for coordinate in feature["geometry"]["coordinates"][0]:
		latitude = coordinate[0]
		longitude = coordinate[1]
		command = "insert into geo_table values("+"\'"+name+"\'"+","+str(latitude)+","+str(longitude)+")"
		cur = conn.cursor()
		cur.execute(command)
		conn.commit()

