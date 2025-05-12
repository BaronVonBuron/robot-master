import time
from DrinksRobot.API.Helpers import RobotState

class PauseFisk:
    def __init__(self, comms):
        self.comms = comms
        self.IDLE_LIMIT = 30

    def monitor_idle(self):
        while True:
            try:
                RobotState.idle_counter += 5
                print(f"Inaktiv i {RobotState.idle_counter} sekunder...")

                if RobotState.idle_counter >= self.IDLE_LIMIT and not RobotState.pause_script_active:
                    print("Idle tid overskredet. Loader pause program...")
                    self.comms.load_and_run_program("pause.urp")  # Load fra robotten
                    RobotState.pause_script_active = True
                    RobotState.idle_counter = 0

            except Exception as e:
                print(f"Fejl i idle monitor: {e}")

            time.sleep(5)
