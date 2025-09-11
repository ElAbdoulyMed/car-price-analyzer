def assign_manufacturer_id(db):
    cars = db["cars"].find({}, {"manufacturer_id":1})
    for car in cars : 
        manufacturer = db["manufacturers"].find_one({"name":car["manufacturer_id"]},{"_id":1})
        if manufacturer:
            db["cars"].update_one(
                {"_id":car["_id"]},
                {"$set":{"manufacturer_id":manufacturer["_id"]}}
            )
