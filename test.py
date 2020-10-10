import datetime
import requests
import csv

def convertir_en_chaine(dt) :
    ''' on convertit en chaîne de caractères un datetime'''
    return datetime.datetime.strftime(dt, '%Y%m%dT%H%M%S')

def convertir_en_temps(chaine) :
    ''' on convertit en date la chaine de caractères de l API'''
    return datetime.datetime.strptime(chaine.replace('T',''),'%Y%m%d%H%M%S')

def getthedepart(code):
    with open('ensemble_gares.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile)
        for row in spamreader:
            if code  in row:
                return row[4]
        return "stop_area:OCE:SA:87681601"

#Gare de depart : 

depart=input("donner la ville\n")
GDP=requests.get(url=f'https://geo.api.gouv.fr/communes?nom={depart}&fields=code&format=json&geometry=centre')

now = datetime.datetime.now()

TGDP=requests.get(url=f'https://api.sncf.com/v1/coverage/sncf/stop_areas/{getthedepart(GDP.json()[0]["code"])}/departures?datetime={convertir_en_chaine(now)}'
,headers={"Authorization":"cac438f6-f223-4802-b5eb-cf11ec8098c0"})

for i in TGDP.json()["departures"]:
    
    DGDA=convertir_en_temps(i["stop_date_time"]["departure_date_time"])
    
    Arrivee=i["display_informations"]["direction"].split("(")

    GDA=requests.get(url=f'https://geo.api.gouv.fr/communes?nom={Arrivee[1][:-1]}&fields=code&format=json&geometry=centre')
    
    now = datetime.datetime.now()

    b=requests.get(url=f'https://api.sncf.com/v1/coverage/sncf/journeys?from=admin:fr:{GDP.json()[0]["code"]}&to=admin:fr:{GDA.json()[0]["code"]}&datetime={convertir_en_chaine(now)}'
    ,headers={"Authorization":"cac438f6-f223-4802-b5eb-cf11ec8098c0"})
    

    rows = []
    try:
        session = b.json()['journeys'][0]['sections'][1]
        for i in session['stop_date_times']:
            rows.append(i['stop_point']['name'])
    except KeyError:
        rows=["information manquante"]
    
    
    print("\n")
    print("*** Pour le train direction",Arrivee[1][:-1],"depart à",DGDA,"***",sep=" ")
    print("Voici les arrêts que vous allez avoir : ")
    print(" ".join(rows))