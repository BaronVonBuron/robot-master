import time
import random

from DrinksRobot.API.Helpers.RobotState import RobotState


class PauseFisk:
    def __init__(self, comms, script_queue):
        self.comms = comms

        self.script_queue = script_queue
        self.IDLE_LIMIT = 60
        self.pause_programs = ["pause1.urp", "pause2.urp", "pause3.urp"]

    def monitor_idle(self):
        while True:
            try:
                # Tjek om pause.urp er færdig
                if RobotState.pause_script_active and not self.comms.is_program_running_name("pause.urp"):
                    print("Pause-program stoppet. Klar til ny idle-check.")
                    RobotState.pause_script_active = False

                # Tjek om robot og kø er inaktiv
                robot_still_running = self.comms.is_program_running()
                queue_still_running = self.script_queue.running

                if not RobotState.pause_script_active and not robot_still_running and not queue_still_running:
                    RobotState.idle_counter += 5
                    print(f"Inaktiv i {RobotState.idle_counter} sekunder...")

                    if RobotState.idle_counter >= self.IDLE_LIMIT:
                        chosen_program = random.choice(self.pause_programs)
                        print(f"Idle tid overskredet. Kører: {chosen_program}")
                        self.comms.load_and_run_program(chosen_program)

                        RobotState.pause_script_active = True
                        RobotState.idle_counter = 0
                        RobotState.progress_done = 0
                else:
                    # Reset hvis robotten er aktiv eller køen er i gang
                    RobotState.idle_counter = 0

            except Exception as e:
                print(f"Fejl i idle monitor: {e}")

            time.sleep(5)


