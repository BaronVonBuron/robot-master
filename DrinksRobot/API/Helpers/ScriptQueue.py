import time
import threading
from DrinksRobot.API.Helpers.RobotState import RobotState
from DrinksRobot.API.Helpers.logger import get_logger
from DrinksRobot.API.BLL.LogLogic import LogLogic

log = get_logger("ScriptQueue")
log_db = LogLogic()

class ScriptQueue:
    def __init__(self, robot_connection):
        self.robot_connection = robot_connection #socket til robot
        self.queue = [] # kø med scripts
        self.running = False # angiver om kø er i gang

    #når script tilføjes, starter scriptQueue automatisk processen, hvis den ikke er i gang
    def add_script(self, script_text):
        self.queue.append(script_text)
        log.info("Enqueued command: %s (queue_len=%d)", script_text.strip(), len(self.queue))
        if not self.running:
            self._process_next()

    #Tjekker om der er flere script i kø. Hvis ikke stopper den.
    def _process_next(self):
        if not self.queue:
            self.running = False
            log.info("All commands completed. Progress: %d/%d", RobotState.progress_done, RobotState.progress_total)
            try:
                log_db.create_logs("Queue completed", "info")
            except Exception:
                pass
            print("Alle scripts kørt færdigt.")
            return

        # Vent til robotten ikke kører noget før vi sender næste kommando
        while self.robot_connection.is_program_running():
            time.sleep(0.1)

        next_script = self.queue.pop(0)

        if next_script.startswith('load '):
            program_name = next_script.split('load ')[1].strip()
            RobotState.current_program_name = program_name
            log.info("Loading program: %s", program_name)
            try:
                log_db.create_logs(f"Loading program {program_name}", "info")
            except Exception:
                pass
            self.robot_connection.load_program(program_name)
            # Progress for load sendes med det samme
            RobotState.progress_done += 1
            log.debug("Progress after load: %d/%d", RobotState.progress_done, RobotState.progress_total)
            print("Script sendt:", next_script)
            self.running = True
            time.sleep(0.2)
            self._process_next()
            return

        if next_script.strip() == 'play':
            log.info("Playing program: %s", RobotState.current_program_name)
            self.robot_connection.play_program()
            # Vent til programmet er færdigt før vi tæller progress for 'play'
            while self.robot_connection.is_program_running():
                time.sleep(0.2)
            RobotState.progress_done += 1
            try:
                log_db.create_logs(f"Completed program {RobotState.current_program_name}", "info")
            except Exception:
                pass
            log.debug("Progress after play: %d/%d", RobotState.progress_done, RobotState.progress_total)
            print("Script (play) afsluttet:", next_script)
            self.running = True
            time.sleep(0.2)
            self._process_next()
            return

        # Ukendt kommando
        log.warning("Unknown command: %s", next_script)
        print(f"Ukendt kommando: {next_script}")
        time.sleep(0.2)
        self._process_next()
