import socket
import time

class RobotComms:
    def __init__(self, robot_ip):
        self.robotIP = robot_ip
        self.DASHBOARD_PORT = 29999
        self.SECONDARY_PORT = 30002

    def load_program(self, program_name):
        try:
            time.sleep(0.5)  # Give robot time between socket calls
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)  # Increase timeout
            s.connect((self.robotIP, self.DASHBOARD_PORT))

            init_response = s.recv(1024).decode().strip()
            print("🔌 Dashboard forbindelse:", init_response)

            s.sendall(f"load {program_name}\n".encode('utf-8'))
            response = s.recv(1024).decode().strip()
            print("Robot load:", response)
            s.close()

            if not response.startswith("Loading program:"):
                print(f"⚠️ Program ikke korrekt indlæst: {response}")
        except Exception as e:
            print(f"❌ Fejl ved load: {e}")

    def play_program(self):
        try:
            time.sleep(0.5)  # Give robot a bit of time between commands
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(10)  # Increase timeout
            s.connect((self.robotIP, self.DASHBOARD_PORT))

            init_response = s.recv(1024).decode().strip()
            print("🔌 Dashboard forbindelse:", init_response)

            s.sendall(b"play\n")
            response = s.recv(1024).decode().strip()
            print("Robot play:", response)
            s.close()

            if not response.startswith("Starting program"):
                print(f"⚠️ Program ikke korrekt startet: {response}")
        except Exception as e:
            print(f"❌ Fejl ved play: {e}")

    def get_program_state(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.DASHBOARD_PORT))
            s.recv(1024)  # Initial hello
            s.sendall(b"programState\n")
            response = s.recv(1024).decode().strip()
            s.close()
            print(f"Current Program State: {response}")  # Debug: print the state
            return response
        except Exception as e:
            print(f"Fejl ved statusforespørgsel: {e}")
            return "Unknown"

    def is_program_running(self):
        state = self.get_program_state()
        return state == "PLAYING"

    def wait_for_program_to_finish(self):
        # Wait for the program to stop before loading the next one
        print("⏳ Venter på at programmet stopper...")
        while self.is_program_running():
            time.sleep(1)  # Wait until the program finishes
        print("✅ Program færdigt!")




