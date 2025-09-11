import pymongo
from relations.assign_manufacturer_id import assign_manufacturer_id
from relations.assign_seller_id import assign_seller_id
import os
from dotenv import load_dotenv

def main():
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DATABASE = os.getenv("MONGO_DATABASE")
    client = pymongo.MongoClient(MONGO_URI)
    db = client[MONGO_DATABASE]
    #Calling the transformation functions
    assign_manufacturer_id(db)
    assign_seller_id(db)
    #Closing the database connection
    client.close()

if __name__ == "__main__":
    main()
