import csv, string
from pymongo import MongoClient


connection_string = 'mongodb://127.0.0.1:27017/pycsvdb'
client = MongoClient(connection_string)
db = client.get_database('pycsvdb')
collection = db.get_collection('csv')


with open('test.csv') as csv_file:

    csv_reader = csv.reader(csv_file, delimiter=',')

    for row in csv_reader:
        third_row = row[2][0]
        if third_row.startswith(tuple(string.ascii_letters)):

            print(f'Starts with letter in third row : {row}')    

        else:

            post = {
                
                    'one':  row[0],
                    'two':  row[1],
                    'three':row[2],
                    'four': row[3],
                    'five': row[4],
                    'six':  row[5]

                    }


            response = collection.insert_one(post)
            last_inserted_id = response.inserted_id
            

        
    
