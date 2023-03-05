"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = [{
        "family": members
    }]

    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET','DELETE'])
def get_id(member_id):
    if request.method=='GET' :
        search = jackson_family.get_member(member_id)
        if search != None:
            return jsonify(search), 200
        else:
            return 'No se ha encontrado', 404
    else:
        search = jackson_family.delete_member(member_id)
        if search != None:
            return f'la familia {member_id} ha sido eliminado con exito!', 200
        else:
            return 'Un error ha ocurrido, upps!', 500


@app.route('/member', methods=['POST'])
def post_members():
    body = request.json
    if "first_name" not in body:
        return 'No tiene first_name!', 400
    if "age" not in body:
        return 'No tiene age', 400
    if "lucky_numbers" not in body:
        return 'No tiene lucky_numbers', 400
    else:
        new_row = jackson_family.add_member(body)
        if new_row == None:
            return 'Un error ha ocurrido, upps!', 500
        else:
            return jsonify(new_row), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)