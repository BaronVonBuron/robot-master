import socket
import time

class RobotComms:
    def __init__(self, robot_ip):
        self.robotIP = robot_ip
        self.DASHBOARD_PORT = 29999
        self.SECONDARY_PORT = 30002

    def load_program(self, program_name):
        """Loader et program uden at starte."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.DASHBOARD_PORT))
            s.recv(1024)
            s.sendall(f"load {program_name}\n".encode('utf-8'))
            print(s.recv(1024).decode().strip())
            s.close()
            print(f"{program_name} loaded (klar til at spille)")
        except Exception as e:
            print(f"Fejl ved load program: {e}")

    def play_program(self):
        """Starter det loaded program."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.DASHBOARD_PORT))
            s.recv(1024)
            s.sendall(b"play\n")
            print(s.recv(1024).decode().strip())
            s.close()
            print("Program startet (play).")
        except Exception as e:
            print(f"Fejl ved play program: {e}")

    def load_and_run_program(self, program_name):
        """(Brugt i færdige drinks menu)"""
        self.load_program(program_name)
        self.play_program()

    def send_pause_script(self, script_file):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.SECONDARY_PORT))
            with open(script_file, "r") as f:
                script = f.read()
            s.sendall(script.encode('utf-8'))
            s.close()
            print("Pause script sendt.")
        except Exception as e:
            print(f"Fejl ved pause script: {e}")

    def is_program_running(self):
        """Tjekker om robotten kører et program lige nu."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.DASHBOARD_PORT))
            s.recv(1024)
            s.sendall(b"programState\n")
            response = s.recv(1024).decode('utf-8')
            s.close()
            print(f"ProgramState respons: {response.strip()}")
            return "PLAYING" in response or "running" in response.lower()
        except Exception as e:
            print(f"Fejl ved tjek af programState: {e}")
            return False

    def is_program_running_name(self, expected_name):
        """Tjekker om et specifikt program kører baseret på navnet."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((self.robotIP, self.DASHBOARD_PORT))
            s.recv(1024)
            s.sendall(b"programState\n")
            response = s.recv(1024).decode('utf-8')
            s.close()
            print(f"ProgramState respons: {response.strip()}")
            return expected_name.lower() in response.lower()
        except Exception as e:
            print(f"Fejl ved programState-navnetjek: {e}")
            return False




