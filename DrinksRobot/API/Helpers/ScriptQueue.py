import time
from DrinksRobot.API.Helpers.RobotState import RobotState

class ScriptQueue:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection
        self.queue = []
        self.running = False

    def add_script(self, script_text):
        self.queue.append(script_text)
        if not self.running:
            self._process_next()

    def _process_next(self):
        if not self.queue:
            self.running = False
            print("Alle scripts kørt færdigt.")
            return

        # Vent til robotten ikke kører noget
        while self.robot_connection.is_program_running():
            time.sleep(0.1)

        next_script = self.queue.pop(0)

        # Bestem hvad vi sender
        if next_script.startswith('load '):
            program_name = next_script.split('load ')[1].strip()

            RobotState.current_program_name = program_name

            self.robot_connection.load_program(program_name)
        elif next_script.strip() == 'play':
            self.robot_connection.play_program()
        else:
            print(f"Ukendt kommando: {next_script}")

        RobotState.progress_done += 1

        print("Script sendt:", next_script)
        self.running = True

        time.sleep(0.5)
        self._process_next()