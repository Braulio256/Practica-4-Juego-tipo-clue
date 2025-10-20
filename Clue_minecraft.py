import random

# --- Datos base del juego ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Azada de diamante", "Pala de piedra"]
habitaciones = ["Herrería en una aldea", "Patio de Steve", "Pirámide del desierto", "Mansión del bosque", "Portal en ruinas"]

# --- 5 rutas predefinidas del crimen ---
rutas = [
    {
        "asesino": "Alex",
        "arma": "Espada de madera",
        "habitacion": "Patio de Steve",
        "habitaciones_ocultas": ["Pirámide del desierto"]
    },
    {
        "asesino": "Kai",
        "arma": "Hacha de oro",
        "habitacion": "Herrería en una aldea",
        "habitaciones_ocultas": ["Portal en ruinas"]
    },
    {
        "asesino": "Ari",
        "arma": "Arco y flecha",
        "habitacion": "Mansión del bosque",
        "habitaciones_ocultas": ["Herrería en una aldea", "Patio de Steve"]
    },
    {
        "asesino": "Noor",
        "arma": "Azada de diamante",
        "habitacion": "Pirámide del desierto",
        "habitaciones_ocultas": ["Mansión del bosque"]
    },
    {
        "asesino": "Sunny",
        "arma": "Pala de piedra",
        "habitacion": "Portal en ruinas",
        "habitaciones_ocultas": ["Pirámide del desierto"]
    }
]

# --- Elegir una ruta aleatoria ---
ruta_real = random.choice(rutas)

print(" MISTERIO DEL PERRO DE STEVE ")
print("--------------------------------------------------")
print("El perro de Steve ha sido asesinado...")
print("Debes descubrir QUIÉN lo hizo, CON QUÉ ARMA y DÓNDE ocurrió.")
print("\nPersonajes:", ", ".join(personajes))
print("Armas:", ", ".join(armas))
print("Lugares:", ", ".join(habitaciones))
print("--------------------------------------------------")

# --- Lógica del juego ---
intentos = 5
for intento in range(1, intentos + 1):
    print(f"\n Intento #{intento} de {intentos}")

    sospechoso = input("¿Quién crees que fue el asesino? ").strip().capitalize()
    arma_intento = input("¿Con qué arma? ").strip().capitalize()
    lugar_intento = input("¿Dónde ocurrió? ").strip().capitalize()

    # Normalizamos texto para comparar sin errores de mayúsculas
    asesino_correcto = sospechoso.lower() == ruta_real["asesino"].lower()
    arma_correcta = arma_intento.lower() == ruta_real["arma"].lower()
    lugar_correcto = lugar_intento.lower() == ruta_real["habitacion"].lower()

    # Si la habitación está en la lista de ocultas, el jugador no puede verla
    if lugar_intento.lower() in [h.lower() for h in ruta_real["habitaciones_ocultas"]]:
        print(f" No puedes ver bien lo que ocurre en {lugar_intento}. Intenta con otro lugar.")
        continue

    # Si acierta las tres cosas
    if asesino_correcto and arma_correcta and lugar_correcto:
        print("\n ¡HAS RESUELTO EL MISTERIO! ")
        print(f"Fue {ruta_real['asesino']} con la {ruta_real['arma']} en {ruta_real['habitacion']}.")
        print(f"Te tomó {intento} intentos.")
        break

    # Si falla, se le indica en qué se equivocó
    print("\n No es correcto. Pistas:")
    if asesino_correcto:
        print(" El asesino es correcto.")
    else:
        print(" Esa persona no fue el asesino.")
    if arma_correcta:
        print(" El arma es correcta.")
    else:
        print(" Esa no fue el arma usada.")
    if lugar_correcto:
        print(" El lugar es correcto.")
    else:
        print(" Ese no fue el lugar del crimen.")

    if intento == intentos:
        print("\n Se acabaron tus intentos...")
        print(f"La verdad era: {ruta_real['asesino']} con la {ruta_real['arma']} en {ruta_real['habitacion']}.")
        print("El perro de Steve no descansará en paz... ")
