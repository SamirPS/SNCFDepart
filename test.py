import datetime
import requests

def convertir_en_chaine(dt) :
    ''' on convertit en chaîne de caractères un datetime'''
    return datetime.datetime.strftime(dt, '%Y%m%dT%H%M%S')


def convertir_en_temps(chaine) :
    ''' on convertit en date la chaine de caractères de l API'''
    return datetime.datetime.strptime(chaine.replace('T',''),'%Y%m%d%H%M%S')

now = datetime.datetime.now()

a=requests.get(url=f'https://api.sncf.com/v1/coverage/sncf/stop_areas/stop_area:OCE:SA:87681601/departures?datetime={convertir_en_chaine(now)}'
,headers={"Authorization":"cac438f6-f223-4802-b5eb-cf11ec8098c0"})


for i in a.json()["departures"]:
    depart=convertir_en_temps(i["stop_date_time"]["departure_date_time"])
    nom=i["display_informations"]["direction"].split("(")
    code=requests.get(url=f'https://geo.api.gouv.fr/communes?nom={nom[1][:-1]}&fields=code&format=json&geometry=centre')
    now = datetime.datetime.now()

    b=requests.get(url=f'https://api.sncf.com/v1/coverage/sncf/journeys?from=admin:fr:91174&to=admin:fr:{code.json()[0]["code"]}&datetime={convertir_en_chaine(now)}'
    ,headers={"Authorization":"cac438f6-f223-4802-b5eb-cf11ec8098c0"})

    try:
        session = b.json()['journeys'][0]['sections'][1]
        rows = []

        if "stop_date_times" in session:
            for i in session['stop_date_times']:
                rows.append(i['stop_point']['name'])
    except KeyError:
        pass
    
    
    print("\n")
    print("*** Pour le train direction",nom[1][:-1],"depart à",depart,"***",sep=" ")
    print("Voici les arrêts que vous allez avoir : ")
    print(" ".join(rows))