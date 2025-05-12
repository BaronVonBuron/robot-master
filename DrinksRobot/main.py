
from DrinksRobot.API.Helpers.PauseFisk import PauseFisk
from DrinksRobot.API.Helpers.DrinksProgrammer import DrinksProgrammer
from DrinksRobot.API.Helpers.RobotComms import RobotComms
from DrinksRobot.API.Logic.RobotLogic import RobotLogic
from DrinksRobot.API.Controller.RobotController import create_robot_controller
import threading

robot_ip = "192.168.0.101"
comms = RobotComms(robot_ip)
robot_logic = RobotLogic(comms)

robot_controller = create_robot_controller(robot_logic)
app.register_blueprint(robot_controller)

# Start PauseFisk i baggrundstråd
pause = PauseFisk(comms)
idle_thread = threading.Thread(target=pause.monitor_idle)
idle_thread.daemon = True
idle_thread.start()

# Start drinks-menu
drinks = DrinksProgrammer(comms)
drinks.menu()
