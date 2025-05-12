from flask import Blueprint, request, jsonify
from DrinksRobot.API.BLL.BottleLogic import BottleLogic
bottle_logic = BottleLogic()

BottleController = Blueprint('BottleController', __name__)

@BottleController.route('/bottles/<int:bottle_id>', methods=['DELETE'])
def delete_bottles(bottle_id):
    bottle_logic.delete_bottle(bottle_id)


# --- GET alle flasker ---
@BottleController.route('/bottles', methods=['GET'])
def get_bottles():
    bottles = bottle_logic.get_bottles()
    return jsonify(bottles)


# --- POST ny flaske ---
@BottleController.route('/add_bottles', methods=['POST'])
def add_bottle():
    try:
        placement_id = int(request.form['position'])  # Convert from string to int
        title = request.form['name']
        type_ = request.form['type']
        urscript_get = request.form['urscript_get']
        urscript_pour = request.form['urscript_pour']
        urscript_back = request.form['urscript_back']
        image = request.form['image']

        bottles = bottle_logic.get_bottles()

        for bottle in bottles:
            if bottle["bottle_position"] == placement_id:
                return Exception(f"Position '{placement_id}' is already in use!")

        # Now use the parsed variables
        bottle_logic.add_bottle(placement_id, urscript_get, urscript_pour, urscript_back, image, title, type_)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        # Handle exceptions by returning an error message
        return jsonify({"error": str(e)}), 400

@BottleController.route('/delete_bottle', methods=['DELETE', 'OPTIONS'])
def delete_bottle():
    if request.method == 'OPTIONS':
        # Preflight request
        return '', 200

    data = request.get_json()
    bottle_id = data.get('bottle_id')
    if bottle_id is None:
        return jsonify({"error": "Missing bottle_id"}), 400

    success = bottle_logic.delete_bottle(bottle_id)
    if success:
        return jsonify({"message": "Bottle deleted"}), 200
    else:
        return jsonify({"error": "Bottle not found"}), 404

@BottleController.route('/counts', methods=['POST'])
def add_count(bottle_id):
    bottle_logic.add_count(bottle_id)
    return jsonify({"status": "success"}), 200

@BottleController.route('/bottles_alch', methods=['GET'])
def get_bottles_alch():
    bottles = bottle_logic.get_alch_bottles()
    return jsonify(bottles)

@BottleController.route('/bottles_nonalch', methods=['GET'])
def get_bottles_nonalch():
    bottles = bottle_logic.get_nonalch_bottles()
    return jsonify(bottles)