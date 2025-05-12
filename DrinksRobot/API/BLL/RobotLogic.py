import threading
import time
from DrinksRobot.API.DAL.BottleContext import BottleContext
from DrinksRobot.API.Helpers.RobotState import RobotState


bottle_context = BottleContext()

class RobotLogic:

    def __init__(self, comms, script_queue):
        self.comms = comms
        self.script_queue = script_queue
        self.program_map = []

    def run_program(self, bottle_ids):
        bottles = bottle_context.get_Bottles_with_id(bottle_ids)

        for bottle in bottles:
            for script in [bottle.urscript_get, bottle.urscript_pour, bottle.urscript_back]:
                if script:
                    self.program_map.append(script)
                    self.queue_program(script)

            RobotState.idle_counter = 0
            RobotState.pause_script_active = False
            print("Idle counter reset efter valg!")
        else:
            print(f"Ukendt drink navn: ")

    def mix_drink(self, ingredients):
        RobotState.progress_done = 0
        RobotState.progress_total = len(ingredients) * 2
        for ingredient in ingredients:
            mapped_name = self.name_mapping.get(ingredient, None)
            if mapped_name and mapped_name in self.program_map:
                program_name = self.program_map[mapped_name]
                self.queue_program(program_name)
            else:
                print(f"Ukendt ingrediens: {ingredient}")

    def queue_program(self, program_name):
        # Hver program består af load + play kommandoer
        load_command = f'load {program_name}\n'
        play_command = 'play\n'

        # Tilføj load og play til køen
        self.script_queue.add_script(load_command)
        self.script_queue.add_script(play_command)











