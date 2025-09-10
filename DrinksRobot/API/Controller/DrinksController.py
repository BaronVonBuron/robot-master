import os
from email.policy import default

from flask import Flask, request, jsonify, Blueprint

import json
from DrinksRobot.API.BLL.DrinksLogic import DrinkLogic
from DrinksRobot.API.DAL.DrinkContext import DrinkContext
from DrinksRobot.API.Helpers.logger import get_logger

drink_logic = DrinkLogic()

drinks_context = DrinkContext()
log = get_logger("DrinksController")

DrinksController = Blueprint('DrinksController', __name__)
#app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'Images')  # Images will be stored in 'images' folder
#app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}  # Allow image file types


# ROUTES
@DrinksController.route('/get_drinks', methods=['GET'])
def get_drinks():
    drinks = drink_logic.get_drinks()
    log.debug("Returning %d drinks", len(drinks))
    return jsonify(drinks)

@DrinksController.route('/add_drink', methods=['POST'])
def create_drink():

    drink_name = request.form.get('drink_name')
    img = request.form.get('img')
    bottles_raw = request.form.get('bottles')
    script_name = request.form.get('script_name')  # optional
    try:
        bottles = json.loads(bottles_raw)
    except Exception as e:
        log.warning("Invalid bottle data on add_drink")
        return jsonify({"error": "Invalid bottle data"}), 400
    log.info("Creating drink name=%s script=%s bottles=%s", drink_name, script_name, bottles)
    drink_logic.create_drink_with_content(drink_name, img, bottles, script_name)
    return jsonify({"status": "success"}), 200

@DrinksController.route('/get_drinks_by_id', methods=['GET'])
def get_drink_by_id():
    # Accept drink_id as query parameter
    drink_id = request.args.get('drink_id')
    if not drink_id:
        return jsonify({"error": "Missing 'drink_id' query parameter"}), 400
    drink = drink_logic.get_drink_by_id(drink_id)
    if not drink:
        return jsonify({"error": "Drink not found"}), 404
    # Map DB row to JSON if it's a tuple
    if isinstance(drink, (list, tuple)):
        # Assuming schema: DrinkId, DrinkName, Img, UseCount, ScriptName
        mapped = {
            "drink_id": drink[0],
            "drink_name": drink[1],
            "drink_image": drink[2],
            "use_count": drink[3],
            "script_name": drink[4] if len(drink) > 4 else None
        }
        return jsonify(mapped), 200
    return jsonify(drink), 200

@DrinksController.route('/drinks/<int:drink_id>/script', methods=['PUT'])
def update_drink_script(drink_id: int):
    data = request.get_json(silent=True) or {}
    script_name = data.get('script_name')
    if script_name is None:
        return jsonify({"error": "Missing 'script_name' in body"}), 400
    ok = drink_logic.update_script_name(drink_id, script_name)
    if ok:
        log.info("Updated ScriptName for drink=%s to %s", drink_id, script_name)
        return jsonify({"status": "updated"}), 200
    return jsonify({"error": "Drink not found"}), 404

@DrinksController.route('/drinks/<int:drink_id>', methods=['DELETE'])
def delete_drink(drink_id: int):
    ok = drinks_context.delete_drink(drink_id)
    if ok:
        log.info("Drink deleted id=%s", drink_id)
        return jsonify({"status": "deleted"}), 200
    log.warning("Drink not found id=%s", drink_id)
    return jsonify({"error": "Drink not found"}), 404

@DrinksController.route('/add_count_drink', methods=['POST'])
def add_count_drink():
    drink_id = request.get_json().get('drink_id')
    log.info("Increment drink count for drink_id=%s", drink_id)
    drink_logic.add_drink_count(drink_id)
    return jsonify({"status": "success"}), 200


