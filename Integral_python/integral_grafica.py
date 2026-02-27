import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.cm as cm
import random
import math

def leer_numero(mensaje):
    expresion = input(mensaje)

    valores_permitidos = {
        "pi": math.pi,
        "e": math.e,
        "sqrt": math.sqrt,
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "log": math.log,
        "exp": math.exp
    }

    try:
        return eval(expresion, {"__builtins__": {}}, valores_permitidos)
    except:
        print("Entrada inválida. Intente nuevamente.")
        return leer_numero(mensaje)

grado = int(input("Digite el grado del polinomio: "))
print("\nPuede ingresar números normales o:")
print("  pi")
print("  e")
print("  sqrt(2)")
print("  2*pi")
print("  pi/4")
print("  3*sqrt(5)/2")
print("Usar sqrt(x) para raíces.")

coef = []
for i in range(grado + 1):
    c = leer_numero(f"Coeficiente de x^{grado - i}: ")
    coef.append(c)

print("\nPolinomio ingresado:")
polinomio_str = ""
for i in range(grado + 1):
    c = coef[i]
    exp = grado - i

    if c == 0:
        continue

    if c > 0 and polinomio_str != "":
        polinomio_str += " + "
    elif c < 0:
        polinomio_str += " - "

    if abs(c) != 1 or exp == 0:
        polinomio_str += str(abs(c))

    if exp > 0:
        polinomio_str += "x"
        if exp > 1:
            polinomio_str += "^" + str(exp)

print(polinomio_str)

print("\nIngrese el dominio [a, b]:")
a = leer_numero("\nDigite a: ")
b = leer_numero("Digite b: ")
if a > b:
    a, b = b, a
epsilon = leer_numero("Digite epsilon: ")

print("\nDominio:", [a, b])
print("Epsilon:", epsilon)


cantidad_cortes = random.randint(3, 10)
puntos = [a]

for _ in range(cantidad_cortes):
    puntos.append(random.uniform(a, b))

puntos.append(b)
puntos.sort()

print("\nCantidad de cortes generados:", cantidad_cortes)
print("Cortes generados:", puntos)

print("\nIntervalos:")
for i in range(len(puntos)-1):
    print(f"[{puntos[i]}, {puntos[i+1]}]")

def evaluar(x):
    resultado = 0
    for j in range(grado + 1):
        resultado += coef[j] * (x ** (grado - j))
    return resultado

fig, ax = plt.subplots()
x_suave = np.linspace(a, b, 600)
y_suave = [evaluar(x) for x in x_suave]

n = 1
iteraciones = 0

colores = cm.plasma(np.linspace(0.2, 0.9, len(puntos)-1))

def actualizar(frame):
    global n, iteraciones

    ax.clear()
    ax.plot(x_suave, y_suave, color="black", linewidth=2)

    suma_min = 0
    suma_max = 0

    for i in range(len(puntos)-1):

        color_intervalo = colores[i]

        x0 = puntos[i]
        x1 = puntos[i+1]
        h = (x1 - x0) / n

        for k in range(n):

            xi = x0 + k*h
            xi1 = x0 + (k+1)*h

            f0 = evaluar(xi)
            f1 = evaluar(xi1)

            minimo = min(f0, f1)
            maximo = max(f0, f1)

            suma_min += minimo * h
            suma_max += maximo * h

            # Rectángulo mínimo
            ax.fill_between([xi, xi1], minimo,
                            color=color_intervalo,
                            alpha=0.3)

            # Rectángulo máximo
            ax.fill_between([xi, xi1], maximo,
                            color=color_intervalo,
                            alpha=0.6)

    if suma_min > suma_max:
        suma_min, suma_max = suma_max, suma_min

    diferencia = abs(suma_max - suma_min)

    ax.set_title(f"Iteración {iteraciones}  |  n = {n}  |  Epsilon = {diferencia:.6f}")
    ax.grid(True)

    if diferencia < epsilon:
        ani.event_source.stop()

        print("RESULTADOS FINALES")
        print("                   ")
        print("Intervalo de la integral:")
        print("[", suma_min, ",", suma_max, "]")
        print("Precisión alcanzada:", diferencia)
        print("Iteraciones:", iteraciones)
        print("Total subintervalos:", (len(puntos)-1) * n)
    else:
        n *= 2
        iteraciones += 1

ani = animation.FuncAnimation(fig, actualizar, interval=200)

plt.show()