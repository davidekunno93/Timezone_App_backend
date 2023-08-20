# importing app to route different web directories
from app import app
from .myfunctions import TimeZone
from flask import request
from .models import User, City

# if url = localhost:5000/ call this function and return this
@app.route('/')
def index():
    return "Home page"

@app.route('/major-cities')
def majorCities():

    major_cities = []

    london = TimeZone("london")
    major_cities.append(london.to_dict())

    hongkong = TimeZone("hong_kong")
    major_cities.append(hongkong.to_dict())

    houston = TimeZone("houston")
    major_cities.append(houston.to_dict())

    # rome = TimeZone("rome")
    # major_cities.append(rome.to_dict())

    paris = TimeZone("paris")
    major_cities.append(paris.to_dict())

    zurich = TimeZone("zurich")
    major_cities.append(zurich.to_dict())

    # nairobi = TimeZone("nairobi")
    # major_cities.append(nairobi.to_dict())

    # print(major_cities)

    return major_cities

@app.route('/get-city', methods=["POST"])
def getCity():

    data = request.get_json()
    print(data)
    data = data.strip().replace(" ", "_")
    print(data)

    status = "OK"

    cities = []
    try: 
        city = TimeZone(data)
        cities.append(city.to_dict())
        message = "cityFound"
    except:
        message = "noCityFound"


    return {
        "status" : status,
        "message" : message,
        "cities" : cities
    }

@app.route('/add-city', methods=["POST"])
def addCity():

    data = request.get_json()
    print(data)

    # return "done"


    user_id = data["user_id"]
    city_name = data["city_name"].lower()

    city = City.query.filter_by(name=city_name).first()
    if not city:
        print("city to be added to db")
        city = City(city_name)
        city.save_city()
        city = City.query.filter_by(name=city_name).first()

    user = User.query.filter_by(id=user_id).first()
    city.addToWatch(user)

    return {
        "status": "OK",
        "message": "added",
        "data": user.to_dict()
    }

@app.route('/remove-city', methods=["POST"])
def removeCity():

    data = request.get_json()
    print(data)

    user_id = data["user_id"]
    city_name = data["city_name"].lower()

    city = City.query.filter_by(name=city_name).first()

    user = User.query.filter_by(id=user_id).first()
    city.removeFromWatch(user)
    
    return {
        "status": "OK",
        "message": "removed",
        "data": user.to_dict()
        # "cities"
    }


@app.route('/my-cities', methods=["POST"])
def myCities():

    data = request.get_json()
    print(data)

    cities = []
    for d in data:
        city = TimeZone(d)
        cities.append(city.to_dict())

    return {
        "status": "OK",
        "message": "cities returned",
        "data": cities
    }






@app.route('/register', methods=["POST"])
def register():

    data = request.get_json()
    print(data)

    name = data["name"].lower()
    relationship = data["relationship"].lower()

    dup_name = User.query.filter_by(name=name).first()
    if dup_name:
        return {
        "status": "OK",
        "message": "nameExists",
        "data": None
    }
    dup_relationship = User.query.filter_by(relationship=relationship).first()
    if dup_relationship:
        return {
        "status": "OK",
        "message": "relationshipExists",
        "data": None
    }

    user = User(name, relationship)
    user.save_user()
    print("user added")

    return {
        "status": "OK",
        "message": "userCreated",
        "data": user.to_dict()
    }



@app.route('/login', methods=["POST"])
def login():

    data = request.get_json()
    print(data)

    name = data["name"].lower()
    relationship = data["relationship"].lower()

    user = User.query.filter_by(name=name).first()
    if user:
        if user.relationship == relationship:
            print("User found")
            return {
                "status": "OK",
                "message": "userFound",
                "data": user.to_dict()
            }
        else:
            print("Wrong relationship")
            return {
                "status": "OK",
                "message": "relationshipWrong",
                "data": None
            }
    else:
        print("User not found")
        return {
            "status": "OK",
            "message": "userNotFound",
            "data": None
        }