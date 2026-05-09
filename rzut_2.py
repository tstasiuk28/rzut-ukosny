import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tkinter as tk
from tkinter import messagebox

def trajektoria(v0,fi):
    #dane poczatkowe + podpisy
    g = 9.81
    C = 0.47
    rho = 1.225
    r = 0.05
    m = 0.5
    A = np.pi * r**2
    dt = 0.01

    #rozklad v0 na skladowe
    vx = v0*np.cos(np.radians(fi))
    vy = v0*np.sin(np.radians(fi))
    
    #oddzielnie dla x i y: lista kolejnych polozen p oraz polozenia w danej chwilii
    xp, yp = [0.0], [0.0] 
    x,y = 0.0, 0.0

    while y>=0:
        v = np.sqrt(vx**2 + vy**2) #złożenie składowych
        Fop = 0.5*C*rho*A*v**2 #wzór na siłę oporu

        ax = -(Fop*(vx/v))/m #przyśpieszenie siły wypadkowej na x (proporcjonalne do stosuku skladowej predkosci x do calkowitej)
        ay = -g-(Fop*(vy/v)/m) #analogicznie dla y z dodaniem przyspieszenia ziemskiego g

        #przyrost vx i vy w każdym malutkim przyroście czasu dt (różniczka)
        vx += ax*dt
        vy += ay*dt
        #na podstawie przyrostu prędkości przyrost polozenia x i y
        x += vx*dt
        y += vy*dt
        #i dodaje to do list p
        xp.append(x)
        yp.append(y)
        
        
    return np.array(xp), np.array(yp)

def start():
    global ani
    try:
        #pobranie danych od uzytkownika
        v0 = float(entry_v.get())
        fi = float(entry_a.get())

        #zabezpieczenie
        if v0 <= 0 or not (0 <= fi <= 90):
            raise ValueError
        
        x_rez, y_rez = trajektoria(v0, fi)

        fig, ax = plt.subplots(figsize=(8,5))
        ax.set_xlim(0, max(x_rez)*1.1)
        ax.set_ylim(0, max(y_rez)*1.1)
        ax.set_title(f"Symulacja: v={v0}m/s, kąt={fi}°")
        ax.grid(True, ls='--')

        linia, = ax.plot([], [], 'b-', alpha=0.6)
        punkt, = ax.plot([], [], 'ro', ms=8)

        def update(frame):
            linia.set_data(x_rez[:frame], y_rez[:frame])
            punkt.set_data([x_rez[frame]], [y_rez[frame]])
            return linia, punkt
        
        ani = animation.FuncAnimation(
            fig, update, frames=range(0, len(x_rez), 3), 
            blit=True, interval=10, repeat=False)
        plt.show()
    
    except ValueError:
        messagebox.showerror("Błąd")

root = tk.Tk()
root.title("Symulacja rzutu ukośnego")
root.geometry("300x200")
tk.Label(root, text="Prędkość początkowa (m/s): ").pack(pady=5)
entry_v = tk.Entry(root)
entry_v.insert(0, "50")
entry_v.pack()

tk.Label(root, text ="Kąt [stopnie]:").pack(pady=5)
entry_a = tk.Entry(root)
entry_a.insert(0, "45")
entry_a.pack()  

btn_start = tk.Button(root, text="Start", command=start,
                      bg="lightblue",
                      font=('Arial', 10, 'bold'))
btn_start.pack(pady=20)

root.mainloop()
