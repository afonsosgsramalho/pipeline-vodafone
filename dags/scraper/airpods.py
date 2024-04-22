import os
import requests
from datetime import datetime
from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psycopg2
from dotenv import load_dotenv

load_dotenv()

URL_BASE = 'https://www.vodafone.pt/bin/mvc.do/eshop/products/productDetails?pageModel=/loja/'
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = os.getenv('EMAIL')
PASS = os.getenv('PASS')

def _get_current_state(url):
    req = requests.get(url)
    data = req.json()

    stock = int(data["productModel"]["variants"][0]["stock"].split('.')[0])
    product = url.split('/')[-1]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M")

    if stock > 0:
        # Disponivel
        return product, True, stock, current_datetime
    else:
        # Indisponivel
        return product, False, stock, current_datetime
    

def _send_mail(product_name):
    sender_email = EMAIL
    receiver_email = EMAIL
    password = PASS

    subject = f'{product_name} Disponiveis'
    message = 'O produto está finalmente disponivel!'

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_email, password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())
    
    print('Email has been sent to', receiver_email)


def insert_database(row):
    conn = psycopg2.connect(
        host='vodafone_airpods-postgres_vodafone-1',
        user='vodafone',
        dbname='vodafone',
        password='vodafone',
        port='5432'
    )

    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO airpods_2ndgen(product, state, stock, updated_at) VALUES(%s, %s, %s, %s)', row)
        conn.commit()
        cursor.close()
        conn.close()


def vodafone_etl():
    product = 'acessorios/som/apple-airpods-pro-2nd-gen-usb-c.html'
    # product = 'acessorios/som/apple-airpods-3_-geracao.html'
    product_state = _get_current_state(URL_BASE + product)

    if product_state[1]:
        _send_mail(product.split('/')[2].split('.')[0])

    insert_database(product_state)

    return product_state
    
    