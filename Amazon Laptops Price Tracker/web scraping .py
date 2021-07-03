from _typeshed import NoneType
import requests 
from bs4 import BeautifulSoup
import pandas as pd 
from datetime import date
import sqlite3



def data_entry(con,code,name,price,date):
    command = con.cursor()
    table_detail = command.execute(""" SELECT * FROM  "Product Code Details" """)
    table_rows = table_detail.fetchall()

    
    if (name,code) not in table_rows:
        command2 = con.cursor()
        command2.execute(""" INSERT INTO "Product Code Details" VALUES(?,?)""",(name,code))
        con.commit()
        command3 = con.cursor()
        command3.execute(""" CREATE TABLE {}("Date" DATE,"Product Price" INTEGER) """.format(code))
        con.commit()
        command4 = con.cursor()
        command4.execute(""" INSERT INTO {} VALUES(?,?)""".format(code),(date,price))
        con.commit()
    else:
        command4 = con.cursor()
        command4.execute(""" INSERT INTO {} VALUES(?,?)""".format(code),(date,price))
        con.commit()



def dacorator_for_productname(name):
    name = str(name)
    name = name.replace("\n","")
    name = name.split(",")
    code = name[-1].split("-")
    
    return "".join(map(str,code)) , " ".join([str(e) for e in name[0:-1]])



def dacorator_for_productprice(price):
    price = str(price)
    price = price.split("-")
    if len(price) == 1:
        if "₹" in price[0]:
            price = price[0].replace("₹","")
            price = price.replace(",","")
            return float(price)
        elif "$" in price[0]:
            price = price[0].replace("$","")
            return 74.19*float(price)
    elif len(price)==2:
        if "₹" in price[0] and "₹" in price[1]:
            price0 = price[0].replace("₹","")
            price0 = price0.replace(",","")
            price1 = price[1].replace("₹","")
            price1 = price1.replace(",","")
            return (float(price0)+float(price1))/2
        elif "$" in price[0]:
            price0 = price[0].replace("$","")
            price1 = price[0].replace("$","")
            return ((74.19*float(price0))+(74.19*float(price1)))/2


def product_price_ids():
    ids = ["priceblock_ourprice","priceblock_dealprice"]
    for ID in ids:
        price = soup.find(id=ID).get_text()

        if price is not NoneType:
            return str(ID)




URL = "https://www.amazon.in/ASUS-i7-10750H-ScreenPad-Celestial-UX581LV-XS74T/dp/B08D941WH6/ref=pd_sbs_7/258-1968671-9530502?pd_rd_w=zTJNT&pf_rd_p=18688541-e961-44b9-b86a-bd9b8fa83027&pf_rd_r=8S1D8FT6AVF007ZE0M4W&pd_rd_r=d138c222-d7ff-47b7-ae3c-df5f12848aa8&pd_rd_wg=GpR5H&pd_rd_i=B08D941WH6&psc=1"
Headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"}
page = requests.get(URL,headers= Headers)
soup = BeautifulSoup(page.content , "html.parser")
con = sqlite3.connect("C:\\Users\\evil1\\Desktop\\customer\\product data vise price details.db")


product_name = soup.find(id="productTitle").get_text()
product_price = soup.find(id=product_price_ids).get_text()
todaydates = date.today()
product_code , product_name = dacorator_for_productname(product_name)
product_price = dacorator_for_productprice(product_price)

data_entry(con,product_code,product_name,product_price,todaydates)