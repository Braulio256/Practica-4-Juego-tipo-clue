import random

# --- Datos base ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Pico de diamante", "Pala de piedra"]
habitaciones = ["Herrería en una aldea", "Patio de Steve", "Pirámide del desierto", "Mansión del bosque", "Portal en ruinas"]

# --- Historias de los personajes ---
historias = {
    "Alex": "Alex estaba ayudando a Steve en la aldea, pero desapareció justo cuando el perro comenzó a ladrar. Dice que fue por madera...",
    "Kai": "Kai es el herrero de confianza de Steve. Siempre tiene un hacha en la mano, y algunos dicen que discutió con Steve hace poco.",
    "Ari": "Ari es una exploradora que pasa tiempo en el bosque cazando con su arco. Llegó tarde a la reunión de Steve.",
    "Noor": "Noor es muy curiosa y le gusta excavar templos del desierto con su pico de diamante. Estaba fuera todo el día, o eso dice.",
    "Sunny": "Sunny estaba reparando un portal en ruinas para viajar al Nether. Siempre parece distraída, pero algo la pone nerviosa..."
}

# --- 5 rutas del crimen ---
rutas = [
    {"asesino": "Alex", "arma": "Espada de madera", "habitacion": "Patio de Steve", "ocultas": ["Pirámide del desierto"]},
    {"asesino": "Kai", "arma": "Hacha de oro", "habitacion": "Herrería en una aldea", "ocultas": ["Portal en ruinas"]},
    {"asesino": "Ari", "arma": "Arco y flecha", "habitacion": "Mansión del bosque", "ocultas": ["Patio de Steve"]},
    {"asesino": "Noor", "arma": "Pico de diamante", "habitacion": "Pirámide del desierto", "ocultas": ["Mansión del bosque"]},
    {"asesino": "Sunny", "arma": "Pala de piedra", "habitacion": "Portal en ruinas", "ocultas": ["Pirámide del desierto"]}
]

ruta_real = random.choice(rutas)

# --- Introducción ---
print("🐕💀 EL MISTERIO DEL PERRO DE STEVE 💀🐕")
print("--------------------------------------------------")
print("Una mañana, Steve encontró a su perro sin vida en su patio.")
print("Reunió a todos sus amigos para descubrir quién fue el culpable.")
print("Solo tú puedes ayudarlo a resolver el misterio...\n")

print("Steve ha convocado a los sospechosos:")
for p in personajes:
    print(f" - {p}")
print("\nSteve te permite hacer 5 preguntas antes de acusar al culpable.")
print("Puedes preguntar por una persona, un arma o una habitación.\n")

# --- Mostrar historia de cada sospechoso ---
input("Presiona ENTER para escuchar las historias de los sospechosos...\n")
for nombre, historia in historias.items():
    print(f"📜 {nombre}: {historia}\n")

input("Presiona ENTER para comenzar la investigación...\n")

# --- Fase de investigación ---
preguntas_restantes = 5
while preguntas_restantes > 0:
    print(f"\n🔎 Tienes {preguntas_restantes} preguntas restantes.")
    print("¿Sobre qué quieres preguntar?")
    print("1. Persona")
    print("2. Arma")
    print("3. Habitación")
    print("4. Terminar investigación")
    opcion = input("Elige una opción (1-4): ")

    # --- Preguntar por persona ---
    if opcion == "1":
        print("\nSospechosos:")
        for i, p in enumerate(personajes, 1):
            print(f"{i}. {p}")
        try:
            eleccion = int(input("Elige un sospechoso: "))
            elegido = personajes[eleccion - 1]
        except:
            print("❌ Opción inválida.")
            continue

        # Posibilidad de falso nerviosismo
        nervioso_extra = random.choice([p for p in personajes if p != ruta_real["asesino"]])
        if elegido == ruta_real["asesino"] or (random.random() < 0.3 and elegido == nervioso_extra):
            print(f"😰 {elegido} parece nervioso... tal vez oculta algo.")
        else:
            print(f"😐 {elegido} mantiene la calma, parece decir la verdad.")
        preguntas_restantes -= 1

    # --- Preguntar por arma ---
    elif opcion == "2":
        print("\nArmas disponibles:")
        for i, a in enumerate(armas, 1):
            print(f"{i}. {a}")
        try:
            eleccion = int(input("Elige un arma: "))
            elegido = armas[eleccion - 1]
        except:
            print("❌ Opción inválida.")
            continue

        # Arma real o arma falsa con pista aleatoria
        arma_sucia = random.choice([a for a in armas if a != elegido])
        if elegido == ruta_real["arma"]:
            print(f"🧩 Has notado que la {elegido.lower()} tiene manchas extrañas... podría ser el arma del crimen.")
        elif random.random() < 0.3:
            print(f"🤔 La {arma_sucia.lower()} cercana parece estar sucia... ¿será una pista falsa?")
        else:
            print(f"🔍 La {elegido.lower()} parece estar limpia y sin uso reciente.")
        preguntas_restantes -= 1

    # --- Preguntar por habitación ---
    elif opcion == "3":
        print("\nLugares:")
        for i, h in enumerate(habitaciones, 1):
            print(f"{i}. {h}")
        try:
            eleccion = int(input("Elige una habitación: "))
            elegido = habitaciones[eleccion - 1]
        except:
            print("❌ Opción inválida.")
            continue

        # Si la habitación está oculta
        if elegido in ruta_real["ocultas"]:
            print(f"👀 No puedes ver bien lo que ocurre en {elegido}, parece una zona peligrosa.")
        elif elegido == ruta_real["habitacion"]:
            print(f"🧩 Se perciben rastros del perro en {elegido}... aquí ocurrió algo terrible.")
            # Posibilidad de encontrar un arma en la habitación
            if random.random() < 0.6:
                arma_encontrada = random.choice(armas)
                print(f"🔪 También ves una {arma_encontrada.lower()} tirada cerca.")
        else:
            print(f"🔍 Todo parece normal en {elegido}.")
            if random.random() < 0.4:
                arma_encontrada = random.choice(armas)
                print(f"🔎 Sin embargo, notas una {arma_encontrada.lower()} apoyada en una esquina.")
        preguntas_restantes -= 1

    elif opcion == "4":
        print("Decides terminar la investigación antes de tiempo.")
        break
    else:
        print("❌ Opción inválida, intenta de nuevo.")

# --- Fase de acusación ---
print("\n⚖️ Es hora de hacer tu acusación final...")
print("Solo tienes una oportunidad, elige con cuidado.\n")

print("Sospechosos:")
for i, p in enumerate(personajes, 1):
    print(f"{i}. {p}")
asesino = personajes[int(input("Elige al asesino: ")) - 1]

print("\nArmas:")
for i, a in enumerate(armas, 1):
    print(f"{i}. {a}")
arma = armas[int(input("Elige el arma: ")) - 1]

print("\nLugares:")
for i, h in enumerate(habitaciones, 1):
    print(f"{i}. {h}")
lugar = habitaciones[int(input("Elige el lugar: ")) - 1]

# --- Evaluar acusación ---
if asesino == ruta_real["asesino"] and arma == ruta_real["arma"] and lugar == ruta_real["habitacion"]:
    print(f"\n🎉 ¡Has resuelto el misterio! 🎉")
    print(f"Fue {ruta_real['asesino']} con la {ruta_real['arma']} en {ruta_real['habitacion']}.")
    print("Steve te agradece por hacer justicia a su perro 🐕💚.")
else:
    print("\n💀 Has fallado en tu acusación...")
    print(f"El verdadero culpable era {ruta_real['asesino']} con la {ruta_real['arma']} en {ruta_real['habitacion']}.")
    print("El asesino escapó y el perro de Steve no tendrá justicia 😢.")

