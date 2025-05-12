import tkinter as tk
from DrinksRobot.API.Helpers.DrinksProgrammer import DrinksProgrammer
from DrinksRobot.API.Helpers.RobotComms import RobotComms
from DrinksRobot.API.Helpers.PauseFisk import PauseFisk
import threading
import time
import socket

robot_ip = "192.168.0.101"
comms = RobotComms(robot_ip)
drinks_programmer = DrinksProgrammer(comms)

# ---- GUI setup ----
root = tk.Tk()
root.title("Drink Robot")
root.geometry("500x500")

# ==== Frames ====
start_frame = tk.Frame(root)
drink_frame = tk.Frame(root)

for frame in (start_frame, drink_frame):
    frame.grid(row=0, column=0, sticky='nsew')

def show_frame(frame):
    frame.tkraise()

# ====== Start Frame ======
btn_choose = tk.Button(start_frame, text="Vælg Drink", width=25, height=3, font=("Arial", 14),
                       command=lambda: show_frame(drink_frame))
btn_choose.pack(pady=50)

btn_mix = tk.Button(start_frame, text="Bland Selv", width=25, height=3, font=("Arial", 14),
                    command=lambda: print("Bland Selv valgt - funktion endnu ikke lavet"))
btn_mix.pack(pady=50)

# ====== Popup funktion ======
def show_popup():
    popup = tk.Toplevel(root)
    popup.title("Vent venligst")
    popup.geometry("500x600+100+100")  # Fast størrelse & position
    popup.attributes("-topmost", True)
    popup.grab_set()
    popup.overrideredirect(True)  # Fjern titelbar
    popup.configure(bg="white")

    label = tk.Label(popup, text="Robotten kører program...\nVent venligst", font=("Arial", 16), bg="white")
    label.place(relx=0.5, rely=0.5, anchor="center")

    # Funktion der både lukker popup og viser startmenu
    def close_popup():
        popup.destroy()
        show_frame(start_frame)  # Gå tilbage til startmenu

    popup.after(5000, close_popup)  # Auto-luk + gå til startmenu


# ====== Monitor program-status ======
def monitor_program():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((robot_ip, comms.DASHBOARD_PORT))
            s.recv(1024)
            s.sendall(b"is program running\n")
            response = s.recv(1024).decode().strip()
            s.close()

            if "false" in response.lower():
                # Robot færdig
                set_buttons_state("normal")
                break
        except Exception as e:
            print(f"Fejl ved tjek af programstatus: {e}")
            break
        time.sleep(1)

# ---- Funktion til at enable/disable knapper ----
def set_buttons_state(state):
    btn1.config(state=state)
    btn2.config(state=state)
    btn3.config(state=state)

# ====== Funktion der starter drink program ======
def run_drink(drink):
    print(f"Kører {drink}")
    show_popup()

    # Start robot i baggrund
    threading.Thread(target=lambda: drinks_programmer.run_program(drink)).start()
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_program)
    monitor_thread.start()

def run_multiple_drinks():
    print("Kører ")
    show_popup()

    # Start robot i baggrund
    threading.Thread(target=lambda: drinks_programmer.run_program_sequence()).start()
    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor_program)
    monitor_thread.start()

# ====== Drink Menu Frame ======
btn1 = tk.Button(drink_frame, text="Rom og Cola", command=lambda: run_drink("rom_og_cola"), width=25, height=3, font=("Arial", 14))
btn1.pack(pady=10)

btn2 = tk.Button(drink_frame, text="Gin Hass", command=lambda: run_drink("gin_hass"), width=25, height=3, font=("Arial", 14))
btn2.pack(pady=10)

btn3 = tk.Button(drink_frame, text="Brandbil", command=lambda: run_drink("brandbil"), width=25, height=3, font=("Arial", 14))
btn3.pack(pady=10)

# Tilbage-knap
back_btn = tk.Button(drink_frame, text="Tilbage", command=lambda: show_frame(start_frame),
                     width=25, height=3, bg="gray", font=("Arial", 14))
back_btn.pack(pady=10)

# Afslut-knap
exit_btn = tk.Button(drink_frame, text="Afslut", command=root.destroy,
                     width=25, height=3, bg="red", fg="white", font=("Arial", 14))
exit_btn.pack(pady=10)

# ----- PauseFisk monitor -----
pause = PauseFisk(comms)
idle_thread = threading.Thread(target=pause.monitor_idle)
idle_thread.daemon = True
idle_thread.start()

# ---- Start med startmenu ----
show_frame(start_frame)

# ---- Start GUI ----
root.mainloop()
