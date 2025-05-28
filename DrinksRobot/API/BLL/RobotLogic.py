import threading
import time
from DrinksRobot.API.DAL.BottleContext import BottleContext
from DrinksRobot.API.Helpers.RobotState import RobotState


bottle_context = BottleContext()

class RobotLogic:

    def __init__(self, comms, script_queue):
        self.comms = comms
        self.script_queue = script_queue
        self.program_map = {}  # maps ingredient name → [script1, script2, script3]

    def run_program(self, bottle_ids):

        if RobotState.pause_script_active:
            print("Pause-program er i gang. Venter på det afsluttes...")
            while self.comms.is_program_running_name("pause"):
                time.sleep(0.5)
            RobotState.pause_script_active = False
            print("Pause-program færdig – starter drink.")

        bottles = bottle_context.get_Bottles_with_id(bottle_ids)
        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        RobotState.progress_done = 0
        RobotState.progress_total = len(bottles) * 3

        for bottle in bottles:
            scripts = []


            for script in [bottle.urscript_get, bottle.urscript_pour, bottle.urscript_back]:
                if script:
                    scripts.append(script)

            if scripts:
                self.program_map[bottle.title] = scripts
                self.queue_scripts_for_bottle(scripts)

        print("✅ Alle flasker queued!")


    def queue_scripts_for_bottle(self, script_list):
        for script in script_list:
            self.queue_program(script)

    def mix_drink(self, ingredients):

        if RobotState.pause_script_active:
            print("Pause-program er i gang. Venter på det afsluttes...")
            while self.comms.is_program_running_name("pause"):
                time.sleep(0.5)
            RobotState.pause_script_active = False
            print("Pause-program færdig – starter drink.")

        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        RobotState.progress_done = 0
        RobotState.progress_total = len(ingredients) * 3

        for ingredient in ingredients:
            if ingredient in self.program_map:
                scripts = self.program_map[ingredient]
                self.queue_scripts_for_bottle(scripts)
            else:
                print(f"⚠️ Ukendt ingrediens: {ingredient}")

    def queue_program(self, program_path):
        load_command = f'load {program_path}\n'
        play_command = 'play\n'
        self.script_queue.add_script(load_command)
        self.script_queue.add_script(play_command)











