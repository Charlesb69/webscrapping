#coding:utf-8
#Programme Python pour scraper les adresses mail
#présentes dans une liste de pages web extraite d'un .csv 
from bs4 import BeautifulSoup
import requests
import re
from email_scraper import scrape_emails

urls = "{}".format(input("Entrez une liste d'url séparées par une virgule: url1,url2,url3... ")).split(",")
results = {}

for url in urls:
	r = requests.get(url)
	cast = str(r.content, encoding='utf-8', errors = 'replace')
	mails = list(scrape_emails(cast))
	if mails != list():
		results[url] = mails
	else:
		results[url] = None 

print (results)




