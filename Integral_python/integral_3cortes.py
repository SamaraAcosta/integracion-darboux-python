import math
import random
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def evaluar_polinomio(coeficientes, grado, x):
    valor = 0
    for i in range(grado + 1):
        valor += coeficientes[i] * (x ** (grado - i))
    return valor

def mostrar_polinomio(coeficientes, grado):
    texto = ""
    primer_termino = True
    for i in range(grado + 1):
        coef = coeficientes[i]
        exp  = grado - i
        if coef == 0:
            continue
        if not primer_termino:
            texto += " + " if coef > 0 else " - "
        else:
            if coef < 0:
                texto += "-"
        if not (abs(coef) == 1 and exp > 0):
            texto += str(abs(coef))
        if exp > 0:
            texto += "x"
            if exp > 1:
                texto += f"^{exp}"
        primer_termino = False
    return texto if texto else "0"

def graficar(coeficientes, grado, a, b, corte1, corte2,
            intervalo1, intervalo2, intervalo3,
            intv, intv2, intv3,
            suma_min, suma_max, intervalos):

    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    fig.patch.set_facecolor('#0f0f1a')

    xs = np.linspace(a, b, 800)
    ys = np.array([evaluar_polinomio(coeficientes, grado, xv) for xv in xs])

    for ax in axes:
        ax.set_facecolor('#1a1a2e')
        ax.tick_params(colors='#cccccc')
        for spine in ax.spines.values():
            spine.set_color('#555')
        ax.grid(True, color='#2a2a3e', linewidth=0.5, linestyle='--', alpha=0.6)

    m = min(suma_min, suma_max)
    M = max(suma_min, suma_max)
    nombre_poly = f"f(x) = {mostrar_polinomio(coeficientes, grado)}"

    MAX_RECT = 60

    def submuestrear(n_int, delta, origen):
        """Si hay demasiados intervalos, agrupa varios en uno para graficar."""
        if n_int <= MAX_RECT:
            return n_int, delta, origen
        paso = max(1, n_int // MAX_RECT)
        n_graf = n_int // paso
        delta_graf = (delta * n_int) / n_graf  
        return n_graf, delta_graf, origen

    colores_izq = ['#3a7bd5', '#2ecc71', '#9b59b6']
    bordes_izq  = ['#a8d4ff', '#a8f5c8', '#d7a8f7']
    colores_der = ['#d53a7b', '#e67e22', '#16a085']
    bordes_der  = ['#ffaad4', '#f5c28a', '#76d7c4']

    segmentos_orig = [
        (intervalo1, intv,  a,      0),
        (intervalo2, intv2, corte1, 1),
        (intervalo3, intv3, corte2, 2),
    ]

    ax1 = axes[0]
    ax1.set_title("g_izq  —  Suma Inferior  (mínimos)",
                color='#7eb8f7', fontsize=12, pad=12, fontweight='bold')

    for (n_int, delta, origen, idx) in segmentos_orig:
        n_graf, delta_graf, _ = submuestrear(n_int, delta, origen)
        for j in range(n_graf):
            aj  = origen + j * delta_graf
            aj1 = origen + (j + 1) * delta_graf

            puntos = np.linspace(aj, aj1, 5)
            vals   = [evaluar_polinomio(coeficientes, grado, p) for p in puntos]
            minimo = min(vals)
            y_base = min(0.0, minimo)
            altura = abs(minimo)
            rect = plt.Rectangle(
                (aj, y_base), delta_graf, altura,
                color=colores_izq[idx], alpha=0.6,
                linewidth=1.2, edgecolor=bordes_izq[idx]
            )
            ax1.add_patch(rect)

    ax1.plot(xs, ys, color='#f7c948', linewidth=2.5, label=nombre_poly, zorder=5)
    ax1.axhline(0, color='#888', linewidth=0.8)
    ax1.axvline(corte1, color='#ff6b6b', linewidth=1.8, linestyle='--',
                alpha=0.9, label=f"c₁ = {corte1:.3f}")
    ax1.axvline(corte2, color='#ff9f43', linewidth=1.8, linestyle='--',
                alpha=0.9, label=f"c₂ = {corte2:.3f}")

    ax1.axvspan(a,      corte1, alpha=0.05, color=colores_izq[0])
    ax1.axvspan(corte1, corte2, alpha=0.05, color=colores_izq[1])
    ax1.axvspan(corte2, b,      alpha=0.05, color=colores_izq[2])

    ax1.set_xlim(a, b)
    ax1.set_xlabel("x", color='#cccccc', fontsize=11)
    ax1.set_ylabel("y", color='#cccccc', fontsize=11)
    ax1.text(0.03, 0.97, f"∫ g_izq dx ≈ {m:.6f}", transform=ax1.transAxes,
            color='#7eb8f7', fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#0f0f1a', alpha=0.8))

    handles_izq = [
        plt.Line2D([0], [0], color='#f7c948', linewidth=2, label=nombre_poly),
        plt.Line2D([0], [0], color='#ff6b6b', linewidth=1.5, linestyle='--', label=f"c₁ = {corte1:.3f}"),
        plt.Line2D([0], [0], color='#ff9f43', linewidth=1.5, linestyle='--', label=f"c₂ = {corte2:.3f}"),
        mpatches.Patch(color=colores_izq[0], alpha=0.7, label=f"Seg 1: [{a:.2f}, {corte1:.2f}]  n={intervalo1}"),
        mpatches.Patch(color=colores_izq[1], alpha=0.7, label=f"Seg 2: [{corte1:.2f}, {corte2:.2f}]  n={intervalo2}"),
        mpatches.Patch(color=colores_izq[2], alpha=0.7, label=f"Seg 3: [{corte2:.2f}, {b:.2f}]  n={intervalo3}"),
    ]
    ax1.legend(handles=handles_izq, facecolor='#1a1a2e',
            labelcolor='#cccccc', fontsize=8, loc='upper left')

    ax2 = axes[1]
    ax2.set_title("g_der  —  Suma Superior  (máximos)",
                color='#f77eb8', fontsize=12, pad=12, fontweight='bold')

    for (n_int, delta, origen, idx) in segmentos_orig:
        n_graf, delta_graf, _ = submuestrear(n_int, delta, origen)
        for j in range(n_graf):
            aj  = origen + j * delta_graf
            aj1 = origen + (j + 1) * delta_graf
            puntos = np.linspace(aj, aj1, 5)
            vals   = [evaluar_polinomio(coeficientes, grado, p) for p in puntos]
            maximo = max(vals)
            y_base = min(0.0, maximo)
            altura = abs(maximo)
            rect = plt.Rectangle(
                (aj, y_base), delta_graf, altura,
                color=colores_der[idx], alpha=0.6,
                linewidth=1.2, edgecolor=bordes_der[idx]
            )
            ax2.add_patch(rect)

    ax2.plot(xs, ys, color='#f7c948', linewidth=2.5, label=nombre_poly, zorder=5)
    ax2.axhline(0, color='#888', linewidth=0.8)
    ax2.axvline(corte1, color='#ff6b6b', linewidth=1.8, linestyle='--',
                alpha=0.9, label=f"c₁ = {corte1:.3f}")
    ax2.axvline(corte2, color='#ff9f43', linewidth=1.8, linestyle='--',
                alpha=0.9, label=f"c₂ = {corte2:.3f}")

    ax2.axvspan(a,      corte1, alpha=0.05, color=colores_der[0])
    ax2.axvspan(corte1, corte2, alpha=0.05, color=colores_der[1])
    ax2.axvspan(corte2, b,      alpha=0.05, color=colores_der[2])

    ax2.set_xlim(a, b)
    ax2.set_xlabel("x", color='#cccccc', fontsize=11)
    ax2.text(0.03, 0.97, f"∫ g_der dx ≈ {M:.6f}", transform=ax2.transAxes,
            color='#f77eb8', fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#0f0f1a', alpha=0.8))

    handles_der = [
        plt.Line2D([0], [0], color='#f7c948', linewidth=2, label=nombre_poly),
        plt.Line2D([0], [0], color='#ff6b6b', linewidth=1.5, linestyle='--', label=f"c₁ = {corte1:.3f}"),
        plt.Line2D([0], [0], color='#ff9f43', linewidth=1.5, linestyle='--', label=f"c₂ = {corte2:.3f}"),
        mpatches.Patch(color=colores_der[0], alpha=0.7, label=f"Seg 1: [{a:.2f}, {corte1:.2f}]  n={intervalo1}"),
        mpatches.Patch(color=colores_der[1], alpha=0.7, label=f"Seg 2: [{corte1:.2f}, {corte2:.2f}]  n={intervalo2}"),
        mpatches.Patch(color=colores_der[2], alpha=0.7, label=f"Seg 3: [{corte2:.2f}, {b:.2f}]  n={intervalo3}"),
    ]
    ax2.legend(handles=handles_der, facecolor='#1a1a2e',
            labelcolor='#cccccc', fontsize=8, loc='upper left')

    fig.suptitle(
        f"Integral por Definición  —  ∫[{a}, {b}] f(x) dx\n"
        f"Intervalo: [{m:.6f},  {M:.6f}]   |   "
        f"Precisión ε = {M - m:.2e}   |   "
        f"Intervalos usados: {intervalos}",
        color='white', fontsize=12, fontweight='bold', y=1.01
    )

    plt.tight_layout()
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafica_integral.png")
    plt.savefig(ruta, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()
    plt.close()
    print(f"\n  Grafica guardada en: {ruta}")

def main():
    desea = 'y'
    while desea == 'y':
        print("\n" + "="*50)
        print("   INTEGRAL POR DEFINICION — SUMAS DE RIEMANN")
        print("="*50)

        grado = int(input("\nDigite el grado del polinomio: "))

        coeficientes = []
        for i in range(grado + 1):
            c = float(input(f"  Digite el coeficiente de x^{grado - i}: "))
            coeficientes.append(c)

        print(f"\nSu polinomio es: f(x) = {mostrar_polinomio(coeficientes, grado)}")

        dominio = input("\nDigite el dominio [a, b] (separados por espacio): ")
        a, b = map(float, dominio.split())
        print(f"El intervalo de integracion es: [{a}, {b}]")

        epsilon = float(input("Digite la tolerancia de precision (epsilon): "))

        corte1 = a + random.random() * (b - a)
        corte2 = a + random.random() * (b - a)
        if corte1 > corte2:
            corte1, corte2 = corte2, corte1

        intervalo1 = max(math.ceil((corte1 - a)      / epsilon), 1)
        intervalo2 = max(math.ceil((corte2 - corte1) / epsilon), 1)
        intervalo3 = max(math.ceil((b - corte2)      / epsilon), 1)

        suma_min = suma_max = 0.0
        intv = intv2 = intv3 = 0.0

        while True:
            intv  = (corte1 - a)      / intervalo1
            intv2 = (corte2 - corte1) / intervalo2
            intv3 = (b - corte2)      / intervalo3

            suma_min1 = suma_max1 = 0.0
            for j in range(intervalo1):
                aj  = a + j * intv
                aj1 = a + (j + 1) * intv
                v1 = evaluar_polinomio(coeficientes, grado, aj)
                v2 = evaluar_polinomio(coeficientes, grado, aj1)
                suma_min1 += min(v1, v2) * intv
                suma_max1 += max(v1, v2) * intv

            suma_min2 = suma_max2 = 0.0
            for j in range(intervalo2):
                aj  = corte1 + j * intv2
                aj1 = corte1 + (j + 1) * intv2
                v1 = evaluar_polinomio(coeficientes, grado, aj)
                v2 = evaluar_polinomio(coeficientes, grado, aj1)
                suma_min2 += min(v1, v2) * intv2
                suma_max2 += max(v1, v2) * intv2

            suma_min3 = suma_max3 = 0.0
            for j in range(intervalo3):
                aj  = corte2 + j * intv3
                aj1 = corte2 + (j + 1) * intv3
                v1 = evaluar_polinomio(coeficientes, grado, aj)
                v2 = evaluar_polinomio(coeficientes, grado, aj1)
                suma_min3 += min(v1, v2) * intv3
                suma_max3 += max(v1, v2) * intv3

            suma_min = suma_min1 + suma_min2 + suma_min3
            suma_max = suma_max1 + suma_max2 + suma_max3

            if (suma_max - suma_min) < epsilon:
                break
            else:
                intervalo1 += 1
                intervalo2 += 1
                intervalo3 += 1

        m = min(suma_min, suma_max)
        M = max(suma_min, suma_max)
        intervalos = intervalo1 + intervalo2 + intervalo3

        print(f"\n{'─'*45}")
        print(f"  La integral esta en el intervalo: [{m:.6f}, {M:.6f}]")
        print(f"  Cantidad de intervalos usados   : {intervalos}")
        print(f"  Precision (M - m)               : {M - m:.2e}")
        print(f"{'─'*45}")

        ver = input("\n¿Desea ver la grafica? (y/n): ").strip().lower()
        if ver == 'y':
            graficar(coeficientes, grado, a, b, corte1, corte2,
                    intervalo1, intervalo2, intervalo3,
                    intv, intv2, intv3,
                    suma_min, suma_max, intervalos)

        desea = input("\n¿Desea evaluar otro polinomio? (y/n): ").strip().lower()

if __name__ == "__main__":
    main()