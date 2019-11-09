import requests
import pandas as pd
import sys
from playerprofile import PlayerProfile, PlayerSet

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Sec-Fetch-Mode": "cors",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
    "Host": "www.vistagolf.com.ar"
}

import psycopg2
import sys
from datetime import datetime

connection = psycopg2.connect(user = "postgres",
                              password = "egg4592",
                              host = "127.0.0.1",
                              port = "5432",
                              database = "handicap")

cursor = connection.cursor()

def insertRow(player):
    try:
        postgres_insert_query = """ INSERT INTO player_profile (matricula, nombre, validez, handicap) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING"""
        record_to_insert = (player.matricula, str(player.nombre).encode(sys.stdout.encoding, errors='replace').decode('LATIN9'), player.validez, player.handicap)
        cursor.execute(postgres_insert_query, record_to_insert)

        if hasattr(player, 'diferenciales'):
            for index, row in player.diferenciales.iterrows():
                postgres_insert_query = """ INSERT INTO diferenciales (matricula, diferencial, fecha, club, is_dif) VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING"""

                record_to_insert = (row['matricula'], row['Diferenciales'], datetime.strptime(row['Fecha'], '%d/%m/%Y'), str(row['Clubes']).encode(sys.stdout.encoding, errors='replace').decode('LATIN9'), row['is_dif'])
                cursor.execute(postgres_insert_query, record_to_insert)
        count = cursor.rowcount
        #print (count, "Record inserted successfully into mobile table")

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into mobile table", error)
    #finally:
        #closing database connection.
            #if(connection):
                #cursor.close()
                #connection.close()
                #print("PostgreSQL connection is closed")

playerset1 = PlayerSet()
handicap_domain = 'http://www.vistagolf.com.ar/handicap/DiferencialesArg.asp?strCampo=Campo1&strValor='
errors = 0
objects = 0
mat_ids = []
starting_id = 132862
i = 0
while True:
    i += 1
    response = requests.get(handicap_domain + str(starting_id+i), headers=headers)
    if(response.status_code == 200):
        playerInstance = PlayerProfile(response.text)
        if playerInstance.handicap == 999:
            del playerInstance
        else:
            playerset1.newPlayer(playerInstance)
            objects += 1
            insertRow(playerInstance)
    else:
        errors += 1
        mat_ids.append(handicap_domain + str(90100+i))
    if((i % 500) == 0):
        print("errors: ",errors,"objects: ", objects, "\nmat_id's", mat_ids)
        connection.commit()
