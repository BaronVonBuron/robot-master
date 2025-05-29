import os
from email.policy import default

from flask import Flask, request, jsonify, Blueprint

import json
from DrinksRobot.API.BLL.DrinksLogic import DrinkLogic

drink_logic = DrinkLogic()

DrinksController = Blueprint('DrinksController', __name__)
#app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'Images')  # Images will be stored in 'images' folder
#app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allow image file types


# ROUTES
@DrinksController.route('/get_drinks', methods=['GET'])
def get_drinks():
    drinks = drink_logic.get_drinks()
    return jsonify(drinks)

@DrinksController.route('/add_drink', methods=['POST'])
def create_drink():

    drink_name = request.form.get('drink_name')
    img = request.form.get('img')
    bottles_raw = request.form.get('bottles')
    try:
        bottles = json.loads(bottles_raw)
    except Exception as e:
        return jsonify({"error": "Invalid bottle data"}), 400
    drink_logic.create_drink_with_content(drink_name, img, bottles)
    return jsonify({"status": "success"}), 200

@DrinksController.route('/get_drinks_by_id', methods=['GET'])
def get_drink_by_id():
    drink_id = request.form.get('drink_id')
    drink = drink_logic.get_drink_by_id(drink_id)
    return drink

@DrinksController.route('/add_count_drink', methods=['POST'])
def add_count_drink():
    drink_id = request.form.get('drink_id')
    drink_logic.add_count_drink(drink_id)
    return jsonify({"status": "success"}), 200


