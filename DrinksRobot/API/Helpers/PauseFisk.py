import time
import random
from DrinksRobot.API.Helpers import RobotState

class PauseFisk:
    def __init__(self, comms):
        self.comms = comms
        self.IDLE_LIMIT = 30
        self.pause_programs = ["pause1.urp", "pause2.urp", "pause3.urp"]

    def monitor_idle(self):

        while True:
            try:
                # Tjek altid om pause.urp er stoppet
                if RobotState.pause_script_active and not self.comms.is_program_running_name("pause.urp"):
                    print("Pause-program stoppet. Klar til ny idle-check.")
                    RobotState.pause_script_active = False

                # Kun hvis pause ikke er aktiv
                if not RobotState.pause_script_active:
                    RobotState.idle_counter += 5
                    print(f"Inaktiv i {RobotState.idle_counter} sekunder...")

                    if RobotState.idle_counter >= self.IDLE_LIMIT:
                        # Vælg et tilfældigt pauseprogram
                        chosen_program = random.choice(self.pause_programs)
                        print(f"Idle tid overskredet. Kører: {chosen_program}")
                        self.comms.load_and_run_program(chosen_program)

                        RobotState.pause_script_active = True
                        RobotState.idle_counter = 0
                        RobotState.pause_script_active = False
                        RobotState.progress_done = 0
            except Exception as e:
                print(f"Fejl i idle monitor: {e}")

            time.sleep(5)