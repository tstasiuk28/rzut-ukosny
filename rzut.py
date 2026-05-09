import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import messagebox

# --- LOGIKA FIZYCZNA ---
def oblicz_trajektorie(v0, alpha):
    g = 9.81
    C = 0.47
    rho = 1.225
    r = 0.05
    m = 0.5
    A = np.pi * r**2
    dt = 0.01

    vx = v0 * np.cos(np.radians(alpha))
    vy = v0 * np.sin(np.radians(alpha))

    x_pos, y_pos = [0.0], [0.0]
    x, y = 0.0, 0.0
    
    while y >= 0:
        v = np.sqrt(vx**2 + vy**2)
        f_drag = 0.5 * C * rho * A * v**2
        
        ax = -(f_drag * (vx / v)) / m
        ay = -g - (f_drag * (vy / v)) / m
        
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt
        
        x_pos.append(x)
        y_pos.append(y)
        
    return np.array(x_pos), np.array(y_pos)

# --- FUNKCJA URUCHAMIAJĄCA SYMULACJĘ ---
def start_symulacji():
    try:
        # Pobranie danych z pól tekstowych
        v0 = float(entry_v.get())
        alpha = float(entry_a.get())
        
        if v0 <= 0 or not (0 < alpha < 90):
            raise ValueError

        x_rez, y_rez = oblicz_trajektorie(v0, alpha)
        
        # Tworzenie okna wykresu Matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, max(x_rez) * 1.1)
        ax.set_ylim(0, max(y_rez) * 1.1)
        ax.set_title(f"Symulacja: v={v0}m/s, kąt={alpha}°")
        ax.grid(True, ls='--')

        linia, = ax.plot([], [], 'b-', alpha=0.6)
        punkt, = ax.plot([], [], 'ro', ms=8)

        def update(frame):
            linia.set_data(x_rez[:frame], y_rez[:frame])
            punkt.set_data([x_rez[frame]], [y_rez[frame]])
            return linia, punkt

        ani = animation.FuncAnimation(
            fig, update, frames=range(0, len(x_rez), 3),
            blit=True, interval=20, repeat=False
        )
        plt.show()

    except ValueError:
        messagebox.showerror("Błąd", "Wpisz poprawne liczby! (v > 0, kąt 1-89)")

# --- INTERFEJS TKINTER ---
root = tk.Tk()
root.title("Symulator Fizyczny - FZiTF")
root.geometry("300x200")

# Etykiety i pola wprowadzania
tk.Label(root, text="Prędkość początkowa [m/s]:").pack(pady=5)
entry_v = tk.Entry(root)
entry_v.insert(0, "50") # domyślna wartość
entry_v.pack()

tk.Label(root, text="Kąt wyrzutu [stopnie]:").pack(pady=5)
entry_a = tk.Entry(root)
entry_a.insert(0, "45") # domyślna wartość
entry_a.pack()

# Przycisk startu
btn_start = tk.Button(root, text="Uruchom Symulację", command=start_symulacji, 
                      bg="lightblue", font=('Arial', 10, 'bold'))
btn_start.pack(pady=20)

root.mainloop()