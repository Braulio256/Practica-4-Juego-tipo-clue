import random

# --- Datos base ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Azada de diamante", "Pala de piedra"]
habitaciones = ["Herrería en una aldea", "Patio de Steve", "Pirámide del desierto", "Mansión del bosque", "Portal en ruinas"]

# --- Historias de los personajes ---
historias = {
    "Alex": "Alex estaba ayudando a Steve en la aldea, pero desapareció justo cuando el perro comenzó a ladrar. Dice que fue por madera...",
    "Kai": "Kai es el herrero de confianza de Steve. Siempre tiene un hacha en la mano, y algunos dicen que discutió con Steve hace poco.",
    "Ari": "Ari es una exploradora que pasa tiempo en el bosque cazando con su arco. Llegó tarde a la reunión de Steve.",
    "Noor": "Noor es muy curiosa y le gusta excavar templos del desierto con su azada de diamante. Estaba fuera todo el día, o eso dice.",
    "Sunny": "Sunny estaba reparando un portal en ruinas para viajar al Nether. Siempre parece distraída, pero algo la pone nerviosa..."
}

# --- 5 rutas del crimen ---
rutas = [
    {"asesino": "Alex", "arma": "Espada de madera", "habitacion": "Patio de Steve", "ocultas": ["Pirámide del desierto"]},
    {"asesino": "Kai", "arma": "Hacha de oro", "habitacion": "Herrería en una aldea", "ocultas": ["Portal en ruinas"]},
    {"asesino": "Ari", "arma": "Arco y flecha", "habitacion": "Mansión del bosque", "ocultas": ["Patio de Steve"]},
    {"asesino": "Noor", "arma": "Azada de diamante", "habitacion": "Pirámide del desierto", "ocultas": ["Mansión del bosque"]},
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

    if opcion == "1":
        # Preguntar por una persona
        print("\nSospechosos:")
        for i, p in enumerate(personajes, 1):
            print(f"{i}. {p}")
        eleccion = int(input("Elige un sospechoso: "))
        elegido = personajes[eleccion - 1]

        if elegido == ruta_real["asesino"]:
            print(f"🧩 {elegido} parece nervioso... podría ser el culpable.")
        else:
            print(f"🤔 {elegido} parece tener una buena coartada.")
        preguntas_restantes -= 1

    elif opcion == "2":
        # Preguntar por un arma
        print("\nArmas disponibles:")
        for i, a in enumerate(armas, 1):
            print(f"{i}. {a}")
        eleccion = int(input("Elige un arma: "))
        elegido = armas[eleccion - 1]

        if elegido == ruta_real["arma"]:
            print(f"🧩 Has notado que la {elegido} está manchada... podría ser el arma del crimen.")
        else:
            print(f"🔍 La {elegido} parece estar limpia, no muestra señales de uso reciente.")
        preguntas_restantes -= 1

    elif opcion == "3":
        # Preguntar por una habitación
        print("\nLugares:")
        for i, h in enumerate(habitaciones, 1):
            print(f"{i}. {h}")
        eleccion = int(input("Elige una habitación: "))
        elegido = habitaciones[eleccion - 1]

        if elegido in ruta_real["ocultas"]:
            print(f"👀 No puedes ver bien lo que ocurre en {elegido}, parece una zona peligrosa.")
        elif elegido == ruta_real["habitacion"]:
            print(f"🧩 Se perciben rastros del perro en {elegido}... aquí ocurrió algo terrible.")
        else:
            print(f"🔍 Todo parece normal en {elegido}.")
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
