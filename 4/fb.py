from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient


connection_string = 'mongodb://127.0.0.1:27017/facebook'
client = MongoClient(connection_string)
db = client.get_database('facebook')
collection = db.get_collection('facebookdata')

source = requests.get('https://www.facebook.com/public/Guido-van-Rossum').text

soup = BeautifulSoup(source,'lxml')


imgs = soup.find_all('img')
for img in imgs:

    source = {
            'src': img.get('src'),
          }
    response = collection.insert_one(source)
    last_inserted_id = response.inserted_id