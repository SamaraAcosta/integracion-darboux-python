import random
import math
import matplotlib
import numpy

while True:

    grado = int(input("Digite el grado del polinomio: "))

    coef = []
    for i in range(grado + 1):
        c = float(input(f"Coeficiente de x^{grado - i}: "))
        coef.append(c)

    print("\nPolinomio ingresado: ", end="")

    primer_termino = True

    for i in range(grado + 1):
        c = coef[i]
        exp = grado - i

        if c == 0:
            continue

        if not primer_termino:
            if c > 0:
                print(" + ", end="")
            else:
                print(" - ", end="")
        else:
            if c < 0:
                print("-", end="")

        if not (abs(c) == 1 and exp != 0):
            print(abs(c), end="")

        if exp > 0:
            print("x", end="")
            if exp > 1:
                print(f"^{exp}", end="")

        primer_termino = False

    print()

    a, b = map(float, input("\nDigite el dominio [a, b]: ").split())
    epsilon = float(input("Digite la tolerancia (epsilon): "))

    print(f"Dominio: [{a}, {b}]")
    print(f"Epsilon: {epsilon}")

    cantidad_cortes = random.randint(3, 10)

    puntos = [a]

    for _ in range(cantidad_cortes):
        r = random.uniform(a, b)
        puntos.append(r)

    puntos.append(b)

    puntos.sort()

    print("\nCantidad de cortes generados:", cantidad_cortes)
    print("Cortes generados:")
    for p in puntos:
        print(p, end=", ")

    print("\n   Intervalos:")
    for i in range(len(puntos) - 1):
        print(f"[{puntos[i]}, {puntos[i+1]}]")

    n = 1
    iteraciones = 0

    while True:
        sumaMin = 0
        sumaMax = 0

        for i in range(len(puntos) - 1):
            x0 = puntos[i]
            x1 = puntos[i+1]
            h = (x1 - x0) / n

            for k in range(n):
                xi = x0 + k * h
                xi1 = x0 + (k + 1) * h

                f0 = 0
                f1 = 0

                for j in range(grado + 1):
                    f0 += coef[j] * (xi ** (grado - j))
                    f1 += coef[j] * (xi1 ** (grado - j))

                minimo = min(f0, f1)
                maximo = max(f0, f1)

                sumaMin += minimo * h
                sumaMax += maximo * h

        if (sumaMax - sumaMin) < epsilon:
            break
        else:
            n *= 2
            iteraciones += 1

    print("\nRESULTADOS")
    print("Intervalo donde esta la integral:")

    if sumaMin > sumaMax:
        print(f"[{sumaMax}, {sumaMin}]")
        precision = sumaMin - sumaMax
    else:
        print(f"[{sumaMin}, {sumaMax}]")
        precision = sumaMax - sumaMin

    print("Precisión alcanzada:", precision)
    print("Iteraciones usadas:", iteraciones, "=", f"({n})")
    print("Total de subintervalos usados:", (len(puntos) - 1) * n)

    desea = input("\nDesea evaluar otro polinomio? (y/n): ")

    if desea.lower() != 'y':
        break