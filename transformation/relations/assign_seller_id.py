def assign_seller_id(db):
    cars = db["cars"].find({}, {"seller_name":1})
    for car in cars : 
        seller = db["sellers"].find_one({"name":car["seller_name"]},{"_id":1})
        if seller:
            db["cars"].update_one(
                {"_id":car["_id"]},
                {"$set":{"seller_id":seller["_id"]}}
            )   