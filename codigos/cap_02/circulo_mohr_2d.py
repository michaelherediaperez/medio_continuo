"""
Graficación animada del círculo de Mohr en 2D

por: Michael Heredia Pérez
email: mherediap@unal.edu.co
fecha: julio 15, 2022

Animación basada en la función de Sukhbinder
https://sukhbinder.wordpress.com/2021/09/15/comet-plot-in-python/

"""

"""
On windows: un
pip inststall numpy
pip install matplotlib
pip install imageio
"""
import numpy as np                 # Librería para cálculo algebráico.
import matplotlib.pyplot as plt    # Librería para graficar.
#import imageio.v2 as imageio      # Librería para hacer GIFs.
#import os                                   

"""
SOLAMENTE MODIFIQUE EL ESTADO DE ESFUERZOS
"""
# -----------------------------------------------------------------------------
# Ingrese el estado de esfuerzos [Pa]. (ejemplo es sx = 5, sy = -1, txy = 4)
sx  = 5
sy  = -1
txy = -4    

# -----------------------------------------------------------------------------
# Cálculo de esfuerzos principales y ángulos.

# Se construye la matriz de tensiones (esfuerzos).
sigma = np.array([[sx, txy], 
                  [txy, sy]])

# Cálculo de valores y vectores propios.
valp, vecp = np.linalg.eigh(sigma) 

# Recuerde que los valores propios se presentan en orden algebráico.
s2, s1 = valp 
n2, n1 = vecp.T

# El cortante máximo, radio de la circunferencia.
tmax_xy = np.sqrt( ((sx-sy)/2)**2 + txy**2 ) 

# Ángulo theta 1
t1 = np.rad2deg(np.arctan2(2*txy, sx-sy)) / 2

# -----------------------------------------------------------------------------
# Resultados.

print("\nDATOS DE ENTRADA\n")
print(f"+ Esfuerzo normal en x, sigma_x = {sx} Pa ")
print(f"+ Esfuerzo normal en y, sigma_x = {sy} Pa ")
print(f"+ Esfuerzo cortante xy, tau_xy  = {txy} Pa ")
print("\nRESULTADOS\n")
print(f"+ Esfuerzo principal 1, sigma_1      = {round(s1, 2)} Pa ")
print(f"+ Esfuerzo principal 2, sigma_2      = {round(s2, 2)} Pa ")
print(f"+ Esfuerzo máximo xy,   (tau)_max_xy = {tmax_xy.round(2)} Pa ")
print(f"+ Ángulo 1,             theta_1      = {t1.round(2)}  °\n")

# -----------------------------------------------------------------------------
# Cálculos para el círculo de Mohr.

# El círculo de mohr tiene dominio [0, 180°), esto lo calculo pero en radianes:
tt = np.linspace(0, np.pi, 100)  

# Realizo el cálculo de las ecuaciones (2.31) y (2.32). 
ssn_t = ( sx+sy )/2 + ( sx-sy )/2*np.cos( 2*tt ) + txy*np.sin( 2*tt )
ttn_t = txy*np.cos( 2*tt ) - ( sx-sy )/2*np.sin( 2*tt )

# -----------------------------------------------------------------------------
# Gráfico interactivo del círuclo de Mohr en 2D.

# Defino un tamaño de fuente y tamaño del lienzo.
plt.rcParams.update({'font.size': 14})
#plt.rcParams["figure.figsize"] = (8,8)  # Tamaño en pulgadas.

# Inicio el lienzo y lo configuro.
fig = plt.figure()
plt.axis("equal")       # que una unidad en x mida lo mismo que en y.

# Dibujo la recta que pasa por los puntos C y A.
plt.plot((sy, sx), (-txy, txy), "--g")

plt.plot(sy, -txy, "*r")  
plt.plot(sx, txy,  "*r")  

plt.text(sy, -txy*1.1, r"$( \sigma_y, -\tau_{xy} )=$" + f"({sy}, {-txy})")  
plt.text(sx, txy*0.95,  r"$( \sigma_x, \tau_{xy} )=$" + f"({sx}, {txy} )")  

# Marco el centro de la circunferencia O.
plt.plot((sx+sy)/2, 0, "*r")
plt.text((sx+sy)/2, 0,  "O")

# Ubico los esfuerzos sx, sy 
plt.plot(sx, 0, "*r")
plt.text(sx, 0.1, r"$\sigma_x = $" + f"{sx}")
plt.plot(sy, 0, "*r")
plt.text(sy, 0.1, r"$\sigma_y = $" + f"{sy}")

# Ubico los esfuerzos principales s1, s2 
plt.plot(s1, 0, "*r")
plt.text(s1, 0.1, r"$(\sigma_1)_{xy} = $" + f"{round(s1, 2)}")
plt.plot(s2, 0, "*r")
plt.text(s2, 0.1, r"$(\sigma_2)_{xy} = $" + f"{round(s2, 2)}")

# Indico el esfuerzo cortante máximo.
plt.plot((sx+sy)/2, tmax_xy, "*r")
plt.text((sx+sy)/2, 1.1*tmax_xy, r"$(\tau_{max})_{xy} = $" + f"{round(tmax_xy, 2)}")

# Nombre de los ejes.
plt.xlabel("Esfuerzo normal " + r"$\sigma_n$ [Pa]" )
plt.ylabel("Esfuerzo cortante " + r"$\tau_n$ [Pa]")

# Configuro parámetros del lienzo.
plt.grid(which='major', linestyle='-')

# Para la circunferencia, defino el timpo que tarda en graficar cada punto.
time = 0.05

# Inicio el modo interactivo de matplotlib. 
plt.ion()

# Grafico los primeros datos y tomo la primera línea.
plot = plt.plot(ssn_t[0], ssn_t[0])[0]

# filename container to create the gif.
#filenames = []

# Por cada punto del dominio.
for i in range(len(tt)+1):
    # Defino las líneas a graficar 
    plot.set_data(ssn_t[0:i], ttn_t[0:i])
    # Hago el gráfico
    plt.draw()
    # Hago pausas cada "time".
    plt.pause(time)

    # create file name and append it to a list
    #filename = f'{i}.png'
    #filenames.append(filename)
    
    # save frame
    #plt.savefig(filename)
    
# Cierro el modo interactivo
plt.ioff()

# -----------------------------------------------------------------------------
# Build GIF
#with imageio.get_writer('mygif.gif', mode='I') as writer:
#    for filename in filenames:
#        image = imageio.imread(filename)
#        writer.append_data(image)
        
# Remove files
#for filename in set(filenames):
#    os.remove(filename)

# Fin :)