from flask import Blueprint


api = Blueprint('api', __name__, url_prefix='/api')

@api.get('/major-cities')
def major_cities():
    pass
