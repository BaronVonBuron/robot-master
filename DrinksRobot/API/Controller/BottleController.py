from flask import Blueprint, request, jsonify
from DrinksRobot.API.BLL.BottleLogic import BottleLogic
from DrinksRobot.API.DAL.BottleContext import Bottle
from DrinksRobot.API.DAL.DrinkContext import DrinkContext
from DrinksRobot.API.Helpers.logger import get_logger

bottle_logic = BottleLogic()
log = get_logger("BottleController")

BottleController = Blueprint('BottleController', __name__)

@BottleController.route('/bottles/<int:bottle_id>', methods=['DELETE'])
def delete_bottles(bottle_id):
    ok = bottle_logic.delete_bottle(bottle_id)
    if ok:
        log.info("Bottle deleted id=%s", bottle_id)
        return jsonify({"status": "deleted"}), 200
    log.warning("Bottle not found id=%s", bottle_id)
    return jsonify({"error": "Bottle not found"}), 404

# --- GET alle flasker ---
@BottleController.route('/bottles', methods=['GET'])
def get_bottles():
    bottles = bottle_logic.get_bottles()
    log.debug("Returning %d bottles", len(bottles))
    return jsonify(bottles)

# --- POST ny flaske ---
@BottleController.route('/add_bottles', methods=['POST'])
def add_bottle():
    try:
        placement_id = int(request.form['position'])
        title = request.form['name']
        type_ = request.form['type']
        urscript_get = request.form['urscript_get']
        urscript_pour = request.form['urscript_pour']
        urscript_back = request.form.get('urscript_back')
        image = request.form['image']

        bottles = bottle_logic.get_bottles()
        for bottle in bottles:
            if int(bottle.get("bottle_position", -1)) == placement_id:
                log.warning("Position conflict for bottle position=%s", placement_id)
                return jsonify({"error": f"Position '{placement_id}' is already in use!"}), 409

        bottle_logic.add_bottle(placement_id, urscript_get, urscript_pour, urscript_back, image, title, type_)
        log.info("Bottle added pos=%s title=%s type=%s", placement_id, title, type_)
        return jsonify({"status": "created"}), 201
    except Exception as e:
        log.exception("Error adding bottle")
        return jsonify({"error": str(e)}), 400

@BottleController.route('/delete_bottle', methods=['DELETE', 'OPTIONS'])
def delete_bottle():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.get_json(silent=True) or {}
    bottle_id = data.get('bottle_id')
    if bottle_id is None:
        return jsonify({"error": "Missing bottle_id"}), 400

    success = bottle_logic.delete_bottle(bottle_id)
    if success:
        log.info("Bottle deleted id=%s", bottle_id)
        return jsonify({"message": "Bottle deleted"}), 200
    else:
        log.warning("Bottle not found id=%s", bottle_id)
        return jsonify({"error": "Bottle not found"}), 404

@BottleController.route('/add_bottle_counts', methods=['POST'])
def add_count():
    bottle_ids = request.get_json().get('bottles', [])
    log.info("Increment counts for bottles=%s", bottle_ids)
    bottle_logic.add_count(bottle_ids)
    return jsonify({"status": "success"}), 200

@BottleController.route('/bottles_alch', methods=['GET'])
def get_bottles_alch():
    bottles = bottle_logic.get_alch_bottles()
    return jsonify(bottles)

@BottleController.route('/bottles_nonalch', methods=['GET'])
def get_bottles_nonalch():
    bottles = bottle_logic.get_nonalch_bottles()
    return jsonify(bottles)

@BottleController.route('/drink_urscripts/<int:drink_id>', methods=['GET'])
def get_drink_urscripts(drink_id):
    try:
        drink_context = DrinkContext()
        bottle_ids = drink_context.get_bottle_ids_by_drink_id(drink_id)
        urscripts = [drink_context.get_urscripts_by_bottle_id(bottle_id) for bottle_id in bottle_ids]
        return jsonify(urscripts), 200
    except Exception as e:
        log.exception("Error fetching drink UR scripts")
        return jsonify({"error": str(e)}), 500

@BottleController.route('/drink_bottles/<int:drink_id>', methods=['GET'])
def get_drink_bottles(drink_id):
    try:
        drink_context = DrinkContext()
        bottle_ids = drink_context.get_bottle_ids_by_drink_id(drink_id)
        bottles = [bottle_logic.get_bottle_by_id(bottle_id) for bottle_id in bottle_ids]
        return jsonify(bottles), 200
    except Exception as e:
        log.exception("Error fetching drink bottles")
        return jsonify({"error": str(e)}), 500