from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
from datetime import datetime

cluster = MongoClient("mongodb+srv://admin:jzSQTjPCfobvbwTD@whatsapp.0ycm2se.mongodb.net/")
db = cluster["Slabhouse"]
users = db["Users"]
orders = db["Orders"]

app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text = request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:","")
    response = MessagingResponse()
    user = users.find_one({"number":number})
    if bool(user) == False:
        response.message("Hi, thanks for contacting *Slab House*😊\nPlease choose an option below:\n\n1️⃣ *Contact* Us \n2️⃣ *Slab Table* Categories \n3️⃣ *Operating* Hours \n4️⃣ Our *Location*")
        users.insert_one({"number": number, "status": "main", "messages": []})
    elif user["status"] == "main":
        try:
            option = int(text)
        except:
            response.message("Please use a correct response")
            return str(response)

        if option == 1:
            response.message("You can contact us through \n\n *Phone*: +971526458913 \n *E-mail*: sales@slabhouse.ae")
        elif option == 2:
            response.message("Please choose your preferred *Slab Table*")
            users.update_one({"number" :number}, {"$set": {"status": "category"}})
            response.message("1️⃣ Pre-Made Tables\n2️⃣ Custom Tables\n3️⃣ Restaurant Tables\n0️⃣ Go Back")
        elif option == 3:
            response.message("Our operating hour starts at *8:30am* until *6:30pm*")
        elif option == 4:
            response.message("You can find us here:\n*Dubai Investments Park 1 Dar Global Investment Showroom No S-3 - Dubai*")
        else:
            response.message("Please use a correct response")
    elif user["status"] == "category":
        try:
            option = int(text)
        except:
            response.message("Please use a correct response")
            return str(response)
        if option == 0:
            users.update_one({"number": number}, {"$set": {"status": "main"}})
            response.message("Please choose an option below:\n\n 1️⃣ *Contact* Us \n 2️⃣ *Slab Table* Categories \n 3️⃣ *Operating* Hours \n 4️⃣ Our *Location*")
        elif option == 1:
            response.message("Browse your Pre-Made Tables here:\n https://slabhouse.ae/category/pre-made-tables/")
        elif option == 2:
            response.message("Make your Custom Table here:\n https://slabhouse.ae/category/custom-made-tables/")
        elif option == 3:
            response.message("Browse your Restaurant Tables here:\n https://slabhouse.ae/category/restaurant-table/")
        else:
            response.message("Please use a correct response")
    users.update_one({"number": number}, {"$push": {"messages": {"text": text, "date": datetime.now()}}})
    return str(response)


if __name__ == "__main__":
    app.run()
