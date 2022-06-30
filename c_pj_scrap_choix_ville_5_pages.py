#coding:utf-8
#Programme Python pour scraper les 5 premières pages 
#de la requête de son choix sur les pages jaunes
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlsplit
import re
import pandas as pd

choix_ville = input("Entrez la ville de votre choix: ")
choix_mots_cles = input("Entrez les mots clés de votre recherche séparés par des espaces: ")

list_mots_cles = choix_mots_cles.split(" ")
mots_cles_middle = str()
mots_cles_end = str()
x = 0
for mot in list_mots_cles:
    if x < (len(list_mots_cles) - 1):
        mots_cles_middle += str(mot) + '-'
        mots_cles_end += str(mot) + '+'
        x += 1
    else:
        mots_cles_middle += str(mot)
        mots_cles_end += str(mot)

URL = "https://www.pagesjaunes.fr/annuaire/{}/{}?quoiqui={}".format(choix_ville, mots_cles_middle, mots_cles_end)

print ("Lancement du programme avec la requête '{}'+'{}'...".format(choix_mots_cles, choix_ville))

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
with open('pj_cinq_premieres_pages_{}.csv'.format(choix_ville), 'w') as f:
    for key in dic.keys():
        f.write("%s,%s\n"%(key,dic[key]))

print ("Le fichier pj_cinq_premieres_pages_{}.csv a été créé".format(choix_ville))