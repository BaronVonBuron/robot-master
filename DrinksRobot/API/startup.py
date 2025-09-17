import sys
import os
from pathlib import Path
import threading

# Ensure repository root is on sys.path before importing DrinksRobot package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS


from DrinksRobot.API.Helpers.RobotComms import RobotComms
from DrinksRobot.API.BLL.RobotLogic import RobotLogic
from DrinksRobot.API.Helpers.ScriptQueue import ScriptQueue

from DrinksRobot.API.Helpers.RobotState import RobotState
from DrinksRobot.API.Helpers.logger import get_logger

from DrinksRobot.API.Controller.DrinksController import DrinksController
from DrinksRobot.API.Controller.BottleController import BottleController
from DrinksRobot.API.Controller.LogController import LogController
from DrinksRobot.API.Controller.RobotController import create_robot_controller
from DrinksRobot.API.Controller.MenuController import MenuController
from DrinksRobot.API.Helpers.db_migrations import ensure_db_schema

log = get_logger("startup")


def load_robot_config():
    cfg_path = Path(__file__).resolve().parent / 'Helpers' / 'ip_og_ports.txt'
    cfg = {}
    try:
        with open(cfg_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    # convert to int when possible
                    if v.isdigit():
                        cfg[k] = int(v)
                    else:
                        cfg[k] = v
    except Exception as e:
        log.warning(f"Could not read robot config: {e}")
    return cfg

progress_counter = {"done": 0, "total": 1}
app = Flask(__name__)
CORS(app)  # Tillad requests fra browser

# Ensure DB schema is up-to-date
ensure_db_schema()

_cfg = load_robot_config()
robot_ip = _cfg.get('robotIP', '192.168.0.101')
log.info(f"Starting with robot IP: {robot_ip}")
robot_connection = RobotComms(robot_ip)
# Override ports if present in cfg
if 'DASHBOARD_PORT' in _cfg:
    robot_connection.DASHBOARD_PORT = _cfg['DASHBOARD_PORT']
if 'SECONDARY_PORT' in _cfg:
    robot_connection.SECONDARY_PORT = _cfg['SECONDARY_PORT']

script_queue = ScriptQueue(robot_connection)
robot_logic = RobotLogic(robot_connection, script_queue)

app.register_blueprint(BottleController, url_prefix='/api')
app.register_blueprint(DrinksController, url_prefix='/api')
app.register_blueprint(LogController, url_prefix='/api')
app.register_blueprint(create_robot_controller(robot_logic), url_prefix='/api')
app.register_blueprint(MenuController, url_prefix='/api')

@app.route('/run_drink', methods=['POST'])
def run_drink():
    data = request.get_json()
    log.info(f"/run_drink payload: {data}")

    if 'ingredients' in data:
        ingredients = data['ingredients']
        log.info(f"Mix Selv valgt: {ingredients}")

        robot_logic.mix_drink(ingredients)
        return "Mix Selv drink startet!", 200

    elif 'drink' in data:
        drink = data['drink']
        log.info(f"Færdig drink valgt: {drink}")

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
        "current_program": RobotState.current_program_name
    }, 200

@app.route('/robot_progress', methods=['GET'])
def robot_progress():
    log.debug(f"Progress: {RobotState.progress_done}/{RobotState.progress_total}")
    return {
        "done": RobotState.progress_done,
        "total": RobotState.progress_total
    }, 200

@app.route('/current_program', methods=['GET'])
def get_current_program():
    name = RobotState.current_program_name
    return jsonify({"program": name})


if __name__ == '__main__':
    log.info("Backend starting on 0.0.0.0:5001")
    app.run(host='0.0.0.0', port=5001)