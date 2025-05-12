from flask import Flask, request
from flask_cors import CORS
from DrinksRobot.API.Helpers.RobotComms import RobotComms
from DrinksRobot.API.BLL.RobotLogic import RobotLogic
from DrinksRobot.API.Helpers.ScriptQueue import ScriptQueue
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from DrinksRobot.API.Controller.DrinksController import DrinksController
from DrinksRobot.API.Controller.BottleController import BottleController
from DrinksRobot.API.Controller.LogController import LogController
from DrinksRobot.API.Controller.RobotController import create_robot_controller
app = Flask(__name__)
CORS(app)  # Tillad requests fra browser
robot_connection = RobotComms("192.168.0.101")
script_queue = ScriptQueue(robot_connection)
robot_logic = RobotLogic(robot_connection, script_queue)


app.register_blueprint(BottleController, url_prefix='/api')
app.register_blueprint(DrinksController, url_prefix='/api')
app.register_blueprint(LogController, url_prefix='/api')
app.register_blueprint(create_robot_controller(robot_logic), url_prefix='/api')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)