from flask import request


import socket
# Din robot info

ROBOT_IP = "192.168.0.101"
DASHBOARD_PORT = 29999

def send_robot_command(program_name):
    try:
        # Opret socket forbindelse til Dashboard porten
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((ROBOT_IP, DASHBOARD_PORT))
        s.recv(1024)  # Modtag velkomst fra robot

        # Send load kommando
        s.sendall(f"load {program_name}\n".encode('utf-8'))
        load_response = s.recv(1024).decode()
        print(f"Load response: {load_response}")

        # Send play kommando
        s.sendall(b"play\n")
        play_response = s.recv(1024).decode()
        print(f"Play response: {play_response}")

        s.close()
        return f"Kører program: {program_name}"
    except Exception as e:
        print(f"Fejl ved kommunikation med robot: {e}")
        return f"Fejl: {e}"

@app.route('/run_drink', methods=['POST'])
def run_drink():
    data = request.get_json()
    drink = data.get('drink')
    print(f"Modtaget request: {drink}")
    # Kald socket-funktion
    return send_robot_command(f"{drink}.urp"), 200


