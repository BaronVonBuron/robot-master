import time
import threading
from DrinksRobot.API.Helpers.RobotState import RobotState


class ScriptQueue:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection  # socket til robot
        self.queue = []  # kø med scripts
        self.running = False  # angiver om kø er i gang

    def add_script(self, script_text):
        self.queue.append(script_text)
        if not self.running:
            self._process_next()

    #Tjekker om der er flere script i kø. Hvis ikke stopper den.
    def _process_next(self):
        if not self.queue:
            self.running = False
            print("Alle scripts kørt færdigt.")
            return

        next_script = self.queue.pop(0).strip()

        if next_script.startswith('load '):
            program_name = next_script.split('load ')[1].strip()
            RobotState.current_program_name = program_name
            print(f"Loading program: {program_name}")
            self.robot_connection.load_program(program_name)

            # Vent lidt før vi kører videre
            time.sleep(0.5)

        elif next_script == 'play':
            print("Starting program")
            self.robot_connection.play_program()

            # Vent på at programmet er færdigt
            while self.robot_connection.is_program_running():
                time.sleep(0.1)

            RobotState.progress_done += 1
            print(f"Script færdigt, fremdrift: {RobotState.progress_done}/{RobotState.progress_total}")

        else:
            print(f"Ukendt kommando: {next_script}")

        self.running = True

        # Vent lidt mellem hvert sæt (valgfrit)
        time.sleep(0.3)

        # Start næste trin i en ny tråd så vi ikke blokerer
        threading.Thread(target=self._process_next, daemon=True).start()
