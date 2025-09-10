import socket
import time

class RobotComms:
    def __init__(self, robot_ip):
        self.robotIP = robot_ip
        self.DASHBOARD_PORT = 29999
        self.SECONDARY_PORT = 30002

    def _send_dashboard_cmd(self, cmd: str) -> str:
        """Helper to send a single Dashboard command and return the response text."""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((self.robotIP, self.DASHBOARD_PORT))
        # read greeting
        try:
            _ = s.recv(1024)
        except Exception:
            pass
        s.sendall((cmd + "\n").encode('utf-8'))
        try:
            resp = s.recv(4096).decode('utf-8').strip()
        except Exception:
            resp = ""
        finally:
            s.close()
        return resp

    def load_program(self, program_name):
        """Loader et program uden at starte."""
        try:
            resp = self._send_dashboard_cmd(f"load {program_name}")
            print(resp)
            print(f"{program_name} loaded (klar til at spille)")
        except Exception as e:
            print(f"Fejl ved load program: {e}")

    def play_program(self):
        """Starter det loaded program."""
        try:
            resp = self._send_dashboard_cmd("play")
            print(resp)
            print("Program startet (play).")
        except Exception as e:
            print(f"Fejl ved play program: {e}")

    def pause_program(self) -> bool:
        """Pause the currently running program via Dashboard."""
        try:
            resp = self._send_dashboard_cmd("pause")
            print(f"Pause respons: {resp}")
            return True
        except Exception as e:
            print(f"Fejl ved pause program: {e}")
            return False

    def resume_program(self) -> bool:
        """Resume (play) the currently loaded program via Dashboard."""
        try:
            resp = self._send_dashboard_cmd("play")
            print(f"Resume respons: {resp}")
            return True
        except Exception as e:
            print(f"Fejl ved resume program: {e}")
            return False

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




