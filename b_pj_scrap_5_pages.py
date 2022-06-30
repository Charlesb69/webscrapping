#coding:utf-8
#Programme Python pour scraper les 5 premières pages 
#de la requête "Assurance Habitation + Lyon" sur les pages jaunes
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
import re
import pandas as pd

URL = "https://www.pagesjaunes.fr/annuaire/lyon-69/assurance-habitation?quoiqui=assurance+habitation+&ou=Lyon"

print ("Lancement du programme avec la requête 'Assurance Habitation + Lyon'...")

#Créer une liste de listes de n éléments: [[Service 0, Adresse 0],..., [Service i, Adresse i],..., [Service n, Adresse n]]
table = [['Service', 'Adresse, Code Postal/Ville']]
for i in range(1,6):
    URL_page_i = URL + "&page=" + str(i)

    r = requests.get(URL_page_i)
    soup = BeautifulSoup(r.content, features="lxml")

    for header in soup.findAll('header', attrs= {'class':'v-card'}):
        entry = []
        for companyName in header.select('[class^="denomination-links"]'):
            entry.append(companyName.text.replace("\n", " "))
        for adress in header.select('[class^="adresse "]'):
            entry.append(adress.text.replace("\n", " "))
        table.append(entry)


#Convertir la liste en dictionnaire pour export en csv:
dic = {}
for elements in table: 
    dic[elements[0]] = elements[1]


#Réaliser l'export:
print ("Exportation des résultats en .csv...")
import csv
with open('pj_cinq_premieres_pages.csv', 'w') as f:
    for key in dic.keys():
        f.write("%s,%s\n"%(key,dic[key]))

print ("Le fichier pj_cinq_premieres_pages.csv a été créé")