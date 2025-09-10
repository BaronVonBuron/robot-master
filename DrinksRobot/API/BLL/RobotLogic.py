import threading
import time
from DrinksRobot.API.DAL.BottleContext import BottleContext
from DrinksRobot.API.Helpers.RobotState import RobotState
from DrinksRobot.API.Helpers.logger import get_logger


bottle_context = BottleContext()
log = get_logger("RobotLogic")

class RobotLogic:

    def __init__(self, comms, script_queue):
        self.comms = comms
        self.script_queue = script_queue
        self.program_map = {}  # maps ingredient name → [script1, script2, script3]

    def run_program(self, bottle_ids):
        log.info("run_program called with bottle_ids=%s", bottle_ids)

        if RobotState.pause_script_active:
            log.info("Pause script active; waiting to finish")
            print("Pause-program er i gang. Venter på det afsluttes...")
            while self.comms.is_program_running_name("pause"):
                time.sleep(0.5)
            RobotState.pause_script_active = False
            log.info("Pause script finished")
            print("Pause-program færdig – starter drink.")

        bottles = bottle_context.get_Bottles_with_id(bottle_ids)
        log.info("Resolved %d bottles", len(bottles))
        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        RobotState.progress_done = 0

        total_scripts = 0
        for bottle in bottles:
            scripts = []
            for script in [bottle.urscript_get, bottle.urscript_pour, bottle.urscript_back]:
                if script:
                    scripts.append(script)
            if scripts:
                self.program_map[bottle.title] = scripts
                total_scripts += len(scripts)
                log.info("Queueing %d scripts for %s", len(scripts), bottle.title)
                self.queue_scripts_for_bottle(scripts)

        # Each script corresponds to 2 queue commands (load + play)
        RobotState.progress_total = max(1, total_scripts * 2)
        log.info("Queued total_scripts=%d, progress_total=%d", total_scripts, RobotState.progress_total)
        print("✅ Alle flasker queued! Total scripts:", total_scripts)

    def queue_scripts_for_bottle(self, script_list):
        for script in script_list:
            log.debug("Queue single program: %s", script)
            self.queue_program(script)

    def mix_drink(self, ingredients):
        log.info("mix_drink called with ingredients=%s", ingredients)

        if RobotState.pause_script_active:
            log.info("Pause script active; waiting to finish")
            print("Pause-program er i gang. Venter på det afsluttes...")
            while self.comms.is_program_running_name("pause"):
                time.sleep(0.5)
            RobotState.pause_script_active = False
            log.info("Pause script finished")
            print("Pause-program færdig – starter drink.")

        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        RobotState.progress_done = 0
        # Each ingredient triggers 3 scripts × 2 commands (legacy assumption)
        RobotState.progress_total = max(1, len(ingredients) * 3 * 2)
        log.info("Set progress_total=%d (legacy estimate)", RobotState.progress_total)

        for ingredient in ingredients:
            if ingredient in self.program_map:
                scripts = self.program_map[ingredient]
                log.info("Queueing %d scripts for ingredient=%s", len(scripts), ingredient)
                self.queue_scripts_for_bottle(scripts)
            else:
                log.warning("Unknown ingredient: %s", ingredient)
                print(f"⚠️ Ukendt ingrediens: {ingredient}")

    def queue_program(self, program_path):
        load_command = f'load {program_path}\n'
        play_command = 'play\n'
        self.script_queue.add_script(load_command)
        self.script_queue.add_script(play_command)

    # New: Pause/resume wrappers for RobotController
    def pause(self):
        log.info("Pausing robot")
        return self.comms.pause_program()

    def resume(self):
        log.info("Resuming robot")
        return self.comms.resume_program()

    # Optional: run a single UR program directly (can be used for self-mix later)
    def run_single_program(self, program_path):
        log.info("run_single_program: %s", program_path)
        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        RobotState.progress_done = 0
        RobotState.progress_total = 2  # load + play
        self.queue_program(program_path)











