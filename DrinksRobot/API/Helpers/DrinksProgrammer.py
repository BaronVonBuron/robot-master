from DrinksRobot.API.Helpers.RobotState import RobotState

class DrinksProgrammer:
    def __init__(self, comms):
        self.comms = comms
        self.program_map = {
            "rom_og_cola": "rom_og_cola.urp",
            "gin_hass": "gin_hass.urp",
            "brandbil": "brandbil.urp",
            "solstang": "solstang.urp"
        }

    def menu(self):
        while True:
            print("\nVælg din drink:")
            print("1 - Rom og Cola")
            print("2 - Gin Hass")
            print("3 - Brandbil")
            print("4 - Exit")

            choice = input("Indtast valg (1/2/3/4): ")

            if choice == "1":
                self.run_program("rom_og_cola")
            elif choice == "2":
                self.run_program("gin_hass")
            elif choice == "3":
                self.run_program_sequence(["gin_hass", "rom_og_cola", "brandbil"])
            elif choice == "4":
                print("Farvel!")
                break
            else:
                print("Ugyldigt valg. Prøv igen.")

    def run_program(self, drink_name):
        program = self.program_map[drink_name]
        print(f"Kører {drink_name} program...")
        self.comms.load_and_run_program(program)

        RobotState.idle_counter = 0
        RobotState.pause_script_active = False
        print("Idle counter reset efter valg!")

    def run_program_sequence(self, drink_names):
        # Konverter drinks-navne til filnavne
        programs = [self.program_map[name] for name in drink_names if name in self.program_map]
        print(f"\n➡️ Kører sekvens: {', '.join(drink_names)}")
        self.comms.run_program_sequence(programs)
