from bs4 import BeautifulSoup
import requests 
from datetime import datetime
import time
import smtplib
from exts import db
from models import Pharmacy
from main import app



def get_scrapped_data(province = "cankaya"):
    provinces = [
    'altindag', 'ayas', 'bala', 'beypazari', 'cankaya', 'cubuk', 'elmadag',
    'etimesgut', 'evren', 'golbasi', 'gudul', 'haymana', 'kalecik', 'kazan',
    'kecioren', 'kizilcahamam', 'mamak', 'nallihan', 'polatli', 'pursaklar',
    'sereflikochisar', 'sincan'
]

    URL =f"https://www.eczaneler.gen.tr/nobetci-ankara-{province}"
    headers_my = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}
    r = requests.get(URL, headers = headers_my)
    soup = BeautifulSoup(r.content, 'lxml')
    table = soup.find('table')
    rows = table.find_all('tr')[1:]
    pharmacies = []
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 

    for row in rows:
        pharmacy_name = None
        pharmacy_number = None
        adress = None
        adress_description = None
        
        span_name = row.find('span', class_='isim')
        if span_name:
            pharmacy_name = span_name.text.strip()
        
        div_number = row.find('div', class_='col-lg-3 py-lg-2')
        if div_number:
            pharmacy_number = div_number.text.strip()
            
        div_adress = row.find('div', class_='col-lg-6')
        if div_adress:
            adress_names = div_adress.text.strip()

            
            
    
        pharmacy_data = {
                'name': pharmacy_name,
                'adress': adress_names,
                'number': pharmacy_number,
                'scrapped_at': current_datetime,
                'province': province
            }
        pharmacies.append(pharmacy_data)
    for pharmacy in pharmacies:
        print(f"Pharmacy Name: {pharmacy['name']}")
        print(f"Adress: {pharmacy['adress']}")
        print(f"Number: {pharmacy['number']}")
        print(f"scrap_datetime: {pharmacy['scrapped_at']}")
        print(f"province: {pharmacy['province']}")
    return pharmacies

def delete_all_data(): # everyday opened pharmacies are changing so old data become trash so to save memory
    with app.app_context():
        db.session.query(Pharmacy).delete()  # Delete all rows from the Pharmacy table
        db.session.commit()
    
def save_to_db(pharmacies):
    with app.app_context():
        delete_all_data()
        for pharmacy in pharmacies:
            scrapped_at = datetime.strptime(pharmacy['scrapped_at'], '%Y-%m-%d %H:%M:%S')

            new_pharmacy = Pharmacy(
                name=pharmacy['name'],
                adress=pharmacy['adress'],
                number=pharmacy['number'],
                scrapped_at=scrapped_at,
                province=pharmacy['province']
            )
            db.session.add(new_pharmacy)
        db.session.commit()


def scrape_for_all():
    provinces = [
    'altindag', 'ayas', 'bala', 'beypazari', 'cankaya', 'cubuk', 'elmadag',
    'etimesgut', 'evren', 'golbasi', 'gudul', 'haymana', 'kalecik', 'kazan',
    'kecioren', 'kizilcahamam', 'mamak', 'nallihan', 'polatli', 'pursaklar',
    'sereflikochisar', 'sincan'
]
    pharmacies_all = []
    for province in provinces:
        pharmacies = get_scrapped_data(province)
        pharmacies_all.extend(pharmacies)
    save_to_db(pharmacies_all)


if __name__ == "__main__":
    scrape_for_all()



    
    



                 
    
                
                    
            

                