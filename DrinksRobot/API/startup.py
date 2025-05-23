from flask import Flask, request, jsonify
from flask_cors import CORS

from DrinksRobot.API.BLL.RobotLogic import RobotLogic
from DrinksRobot.API.Helpers.ScriptQueue import ScriptQueue
from DrinksRobot.API.Helpers.RobotState import RobotState
from DrinksRobot.API.Helpers.PauseFisk import PauseFisk
from DrinksRobot.API.Helpers.RobotComms import RobotComms

import sys
import os
import threading
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DrinksRobot.API.Controller.DrinksController import DrinksController
from DrinksRobot.API.Controller.BottleController import BottleController
from DrinksRobot.API.Controller.LogController import LogController
from DrinksRobot.API.Controller.RobotController import create_robot_controller

progress_counter = {"done": 0, "total": 1}
app = Flask(__name__)
CORS(app)  # Tillad requests fra browser
robot_connection = RobotComms("192.168.0.101")
script_queue = ScriptQueue(robot_connection)
robot_logic = RobotLogic(robot_connection, script_queue)
idle_checker = PauseFisk(robot_connection)
idle_thread = threading.Thread(target=idle_checker.monitor_idle, daemon=True)
idle_thread.start()

app.register_blueprint(BottleController, url_prefix='/api')
app.register_blueprint(DrinksController, url_prefix='/api')
app.register_blueprint(LogController, url_prefix='/api')
app.register_blueprint(create_robot_controller(robot_logic), url_prefix='/api')

@app.route('/run_drink', methods=['POST'])
def run_drink():
    data = request.get_json()
    print(f"Modtaget data: {data}")

    if 'ingredients' in data:
        ingredients = data['ingredients']
        print(f"Mix Selv valgt: {ingredients}")
        robot_logic.mix_drink(ingredients)
        return "Mix Selv drink startet!", 200

    elif 'drink' in data:
        drink = data['drink']
        print(f"Færdig drink valgt: {drink}")
        robot_logic.run_program(drink)
        return "Færdig drink startet!", 200

    else:
        return "Forkert data sendt!", 400

@app.route('/robot_status', methods=['GET'])
def robot_status():
    is_running = robot_connection.is_program_running()
    return {
        "running": is_running,
        "progress": RobotState.progress_done,
        "total": RobotState.progress_total,
        "current_program": RobotState.current_program_name  # ← send med
    }, 200

@app.route('/robot_progress', methods=['GET'])
def robot_progress():
    return {
        "done": RobotState.progress_done,
        "total": RobotState.progress_total
    }, 200

@app.route('/current_program', methods=['GET'])
def get_current_program():
    name = RobotState.current_program_name
    return jsonify({"program": name})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)