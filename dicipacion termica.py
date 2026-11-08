INCERTIDUMBRE_RELATIVA_K = 0.05

NUM_PUNTOS_PERFIL = 200
CARPETA_RESULTADOS = Path('resultados')


def calcular_generacion_volumetrica(potencia_w, area_m2, espesor_m):
    # q''' = P/(A*L), en W/m^3
    return potencia_w / (area_m2 * espesor_m)


def calcular_perfil_temperatura(x_m, potencia_w, area_m2, espesor_m, conductividad_w_mk):
    # theta(x) = (q'''/k) * (L*x - x^2/2)
    q_vol = calcular_generacion_volumetrica(potencia_w, area_m2, espesor_m)
    return (q_vol/conductividad_w_mk) * (espesor_m*x_m - x_m**2/2.0)


def calcular_gradiente(x_m, potencia_w, area_m2, espesor_m, conductividad_w_mk):
    # d(theta)/dx = (q'''/k)*(L-x), en K/m
    q_vol = calcular_generacion_volumetrica(potencia_w, area_m2, espesor_m)
    return (q_vol/conductividad_w_mk) * (espesor_m-x_m)


def calcular_flujo_calor(x_m, potencia_w, area_m2, espesor_m, conductividad_w_mk):
    # Ley de Fourier: q'' = -k*d(theta)/dx
    gradiente = calcular_gradiente(x_m, potencia_w, area_m2, espesor_m, conductividad_w_mk)
    return -conductividad_w_mk * gradiente


def calcular_incremento_maximo(potencia_w, area_m2, espesor_m, conductividad_w_mk):
    # DeltaT_max = P*L/(2*k*A), en grados Celsius
    return potencia_w*espesor_m/(2.0*conductividad_w_mk*area_m2)


def generar_escenarios():
    # La semilla fija permite repetir los mismos 10 escenarios.
    rng = np.random.default_rng(SEMILLA)
    p = rng.normal(POTENCIA_REGION_W, INCERTIDUMBRE_POTENCIA_W, NUM_SIMULACIONES)
    a = rng.normal(AREA_REGION_M2, INCERTIDUMBRE_AREA_M2, NUM_SIMULACIONES)
    L = rng.normal(ESPESOR_SILICIO_M, INCERTIDUMBRE_ESPESOR_M, NUM_SIMULACIONES)
    k = rng.normal(CONDUCTIVIDAD_W_MK, INCERTIDUMBRE_RELATIVA_K*CONDUCTIVIDAD_W_MK, NUM_SIMULACIONES)
    # Evitar valores iguales o inferiores a cero.
    return np.maximum(p, 0.01), np.maximum(a, 1e-12), np.maximum(L, 1e-12), np.maximum(k, 1e-12)


def analizar_incertidumbre():
    p, a, L, k = generar_escenarios()
    delta_t = calcular_incremento_maximo(p, a, L, k)
    flujo = p/a
    gradiente = p/(a*k)
    return {'potencia_W': p, 'area_m2': a, 'espesor_m': L,
            'conductividad_W_mK': k, 'incremento_maximo_C': delta_t,
            'flujo_maximo_W_m2': flujo, 'gradiente_maximo_K_m': gradiente}


def guardar_graficas():
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    x = np.linspace(0.0, ESPESOR_SILICIO_M, NUM_PUNTOS_PERFIL)
    theta = calcular_perfil_temperatura(x, POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)
    grad = calcular_gradiente(x, POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)
    flujo = calcular_flujo_calor(x, POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)

    plt.figure(figsize=(8, 5)); plt.plot(x*1e3, theta, linewidth=2)
    plt.xlabel('Posicion x (mm)'); plt.ylabel('Incremento de temperatura, theta (°C)')
    plt.title('Perfil de temperatura en el silicio'); plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS/'figura_1_perfil_temperatura.png', dpi=300); plt.close()

    plt.figure(figsize=(8, 5)); plt.plot(x*1e3, grad, linewidth=2)
    plt.xlabel('Posicion x (mm)'); plt.ylabel('Gradiente de temperatura (K/m)')
    plt.title('Gradiente de temperatura'); plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS/'figura_2_gradiente.png', dpi=300); plt.close()

    plt.figure(figsize=(8, 5)); plt.plot(x*1e3, flujo/1000.0, linewidth=2)
    plt.xlabel('Posicion x (mm)'); plt.ylabel('Flujo de calor (kW/m²)')
    plt.title('Flujo de calor en el silicio'); plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS/'figura_3_flujo_calor.png', dpi=300); plt.close()

    potencias = np.linspace(5.0, 15.0, 100)
    temperaturas = calcular_incremento_maximo(potencias, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)
    plt.figure(figsize=(8, 5)); plt.plot(potencias, temperaturas, linewidth=2)
    plt.scatter([POTENCIA_REGION_W], [calcular_incremento_maximo(POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)])
    plt.xlabel('Potencia de la region activa (W)'); plt.ylabel('Incremento maximo de temperatura (°C)')
    plt.title('Temperatura maxima frente a potencia'); plt.grid(True, alpha=0.3); plt.tight_layout()
    plt.savefig(CARPETA_RESULTADOS/'figura_4_temperatura_vs_potencia.png', dpi=300); plt.close()


def guardar_csv(r):
    ruta = CARPETA_RESULTADOS/'escenarios_incertidumbre.csv'
    with ruta.open('w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(['simulacion','potencia_W','area_mm2','espesor_mm','conductividad_W_mK','incremento_maximo_C','flujo_maximo_kW_m2','gradiente_maximo_K_m'])
        for i in range(NUM_SIMULACIONES):
            escritor.writerow([i+1, r['potencia_W'][i], r['area_m2'][i]*1e6, r['espesor_m'][i]*1e3,
                               r['conductividad_W_mK'][i], r['incremento_maximo_C'][i],
                               r['flujo_maximo_W_m2'][i]/1000.0, r['gradiente_maximo_K_m'][i]])


def imprimir_resumen(r):
    delta = calcular_incremento_maximo(POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M, CONDUCTIVIDAD_W_MK)
    q_vol = calcular_generacion_volumetrica(POTENCIA_REGION_W, AREA_REGION_M2, ESPESOR_SILICIO_M)
    print('\n===== RESUMEN DEL MODELO TERMICO =====')
    print(f'Conductividad: {CONDUCTIVIDAD_W_MK:.2f} W/(m K)')
    print(f'Generacion volumetrica: {q_vol:.3e} W/m^3')
    print(f'Incremento maximo nominal: {delta:.6f} °C')
    print(f'Flujo maximo nominal: {POTENCIA_REGION_W/AREA_REGION_M2/1000:.2f} kW/m^2')
    print(f'Gradiente maximo nominal: {POTENCIA_REGION_W/(AREA_REGION_M2*CONDUCTIVIDAD_W_MK):.1f} K/m')
    print(f'Numero de escenarios: {NUM_SIMULACIONES}')
    print(f"Rango exploratorio de incremento: {np.min(r['incremento_maximo_C']):.6f} a {np.max(r['incremento_maximo_C']):.6f} °C")
    print(f"Rango exploratorio de flujo: {np.min(r['flujo_maximo_W_m2'])/1000:.2f} a {np.max(r['flujo_maximo_W_m2'])/1000:.2f} kW/m²")
    print(f"Rango exploratorio de gradiente: {np.min(r['gradiente_maximo_K_m']):.1f} a {np.max(r['gradiente_maximo_K_m']):.1f} K/m")
    print('Con 10 escenarios, minimo y maximo son exploratorios; no representan un intervalo de confianza del 95 %.')
    print(f'Resultados guardados en: {CARPETA_RESULTADOS.resolve()}')


def main():
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    resultados = analizar_incertidumbre()
    guardar_graficas()
    guardar_csv(resultados)
    imprimir_resumen(resultados)


if __name__ == '__main__':
    main()
