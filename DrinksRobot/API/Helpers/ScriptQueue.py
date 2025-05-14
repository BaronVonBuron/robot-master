import time
import threading
from DrinksRobot.API.Helpers.RobotState import RobotState

class ScriptQueue:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection
        self.queue = []
        self.lock = threading.Lock()
        self.thread = threading.Thread(target=self._process_queue, daemon=True)
        self.running = False
        self.thread.start()

    def add_script(self, script_text):
        with self.lock:
            self.queue.append(script_text)

    def _process_queue(self):
        while True:
            if not self.queue:
                time.sleep(1)
                continue

            # Vent til robotten ikke kører noget
            while self.robot_connection.is_program_running():
                time.sleep(1)

            with self.lock:
                next_script = self.queue.pop(0)

            if next_script.startswith('load '):
                program_name = next_script.split('load ')[1].strip()
                RobotState.current_program_name = program_name
                self.robot_connection.load_program(program_name)

            elif next_script.strip() == 'play':
                self.robot_connection.play_program()

                # VENT til programmet starter (går i PLAYING)

                timeout = 10


                waited = 0
                while not self.robot_connection.is_program_running() and waited < timeout:
                    print("⏳ Venter på at program går i gang...")
                    time.sleep(0.5)
                    waited += 0.1

                if waited >= timeout:
                    print("❌ Program startede aldrig.")
                    continue


                # VENT til programmet bliver færdigt
                while self.robot_connection.is_program_running():
                    print("▶️ Program kører...")
                    time.sleep(0.5)

                print("✅ Program færdigt!")

            else:
                print(f"Ukendt kommando: {next_script}")

            RobotState.progress_done += 1
            print("✅ Script sendt:", next_script)

            time.sleep(1)  # Lidt pause mellem scripts