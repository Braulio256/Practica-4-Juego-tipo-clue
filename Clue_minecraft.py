import random
import time

# --- Datos base ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Pico de diamante", "Pala de piedra"]
habitaciones = ["Herrería en una aldea", "Patio de Steve", "Pirámide del desierto", "Mansión del bosque",
                "Portal en ruinas"]

# 5 rutas predefinidas (asesino, arma, habitación)
rutas = [
    {"asesino": "Alex", "arma": "Espada de madera", "habitacion": "Patio de Steve"},
    {"asesino": "Kai", "arma": "Pala de piedra", "habitacion": "Herrería en una aldea"},
    {"asesino": "Ari", "arma": "Arco y flecha", "habitacion": "Mansión del bosque"},
    {"asesino": "Noor", "arma": "Hacha de oro", "habitacion": "Pirámide del desierto"},
    {"asesino": "Sunny", "arma": "Pico de diamante", "habitacion": "Portal en ruinas"}
]

# Historias de los personajes
historias = {
    "Alex": "Estaba entrenando con sus ovejas cerca del río cuando escuchó la noticia. Dice que no tenía motivos para dañar al perro.",
    "Kai": "Afirma que estaba reparando su casa tras una explosión de creepers. Nadie lo vio, pero dice que tiene las manos llenas de madera.",
    "Ari": "Dice que estaba cazando esqueletos para conseguir flechas, aunque no recuerda en qué dirección fue exactamente.",
    "Noor": "Mencionó que exploraba la pirámide del desierto buscando tesoros. No parece muy afectada por el incidente.",
    "Sunny": "Comentó que estaba minando diamantes cerca del portal en ruinas. Juró que ni siquiera sabía que el perro de Steve existía."
}

# Elegir ruta aleatoria
ruta = random.choice(rutas)

# --- Introducción ---
print(" MINECRAFT MISTERIO: ¡El caso del perro de Steve! ")
print("\nSteve ha descubierto que su fiel perro ha sido asesinado...")
print("Ha llamado a los sospechosos a una reunión para descubrir al culpable.")
time.sleep(2)

print("\nTienes 5 oportunidades para hacer preguntas antes de acusar a alguien.")

preguntas = 0

# --- Función para mostrar opciones tipo menú ---
def menu_opciones(lista, texto):
    for i, item in enumerate(lista, 1):
        print(f"{i}. {item}")
    while True:
        try:
            opcion = int(input(f"\nElige un número para {texto}: "))
            if 1 <= opcion <= len(lista):
                return lista[opcion - 1]
            else:
                print("Opción inválida.")
        except ValueError:
            print("Por favor, elige un número válido.")


# --- Bucle de preguntas ---
while preguntas < 5:
    print("\n¿Qué deseas investigar?")
    print("1. Habitación")
    print("2. Arma")
    print("3. Persona")
    print("4. Terminar preguntas y acusar")

    eleccion = input(" Opción: ")
    print()

    if eleccion == "1":  # Habitación
        hab = menu_opciones(habitaciones, "investigar una habitación")
        print(f"🔍 Revisas la {hab}...")
        time.sleep(1.5)
        # Posibilidad de pista real o confusa
        if random.random() < 0.6 and hab == ruta["habitacion"]:
            print("Encuentras rastros de pelea... algo ocurrió aquí.")
        elif random.random() < 0.3:
            print("Parece que una de las armas fue usada aquí, pero no hay nadie alrededor.")
        else:
            print("Todo parece tranquilo, sin señales del crimen.")
        preguntas += 1

    elif eleccion == "2":  # Arma
        arma = menu_opciones(armas, "revisar un arma")
        print(f" Examinas el arma: {arma}")
        time.sleep(1.5)
        if arma == ruta["arma"]:
            print("El arma está manchada... parece haber sido usada recientemente.")
        else:
            # Aleatoriamente otra arma puede parecer sospechosa
            if random.random() < 0.4:
                otra_arma = random.choice([a for a in armas if a != arma])
                print(f"Esta está limpia, pero oyes que la {otra_arma.lower()} parece estar sucia...")
            else:
                print("El arma parece completamente limpia.")
        preguntas += 1

    elif eleccion == "3":  # Persona
        persona = menu_opciones(personajes, "interrogar a alguien")
        print(f" Hablas con {persona}...")
        time.sleep(1.5)
        nervioso = random.random() < 0.3  # 30% de nerviosismo
        es_asesino = persona == ruta["asesino"]
        if nervioso and not es_asesino:
            print(
                f"{persona} parece nervioso, responde de manera vaga: 'Yo... no sé nada, estuve ocupado con mis cosas...'")
        elif nervioso and es_asesino and random.random() < 0.5:
            print(f"{persona} mantiene la calma, aunque algo en su mirada te hace dudar...")
        else:
            print(f"{persona} te dice: {historias[persona]}")
        preguntas += 1

    elif eleccion == "4":
        break
    else:
        print("Opción inválida.")

# --- Fase final: acusación ---
print("\n Ha llegado el momento de decidir...")
asesino = menu_opciones(personajes, "acusar al asesino")
arma_final = menu_opciones(armas, "elegir el arma del crimen")
hab_final = menu_opciones(habitaciones, "decidir la habitación del crimen")

print("\nSteve escucha tu veredicto...")
time.sleep(2)

if asesino == ruta["asesino"] and arma_final == ruta["arma"] and hab_final == ruta["habitacion"]:
    print(
        f" ¡Correcto! {asesino} usó la {arma_final.lower()} en la {hab_final.lower()} para acabar con el perro de Steve. ¡Has resuelto el caso!")
else:
    print(" No lograste resolver el caso.")
    if asesino != ruta["asesino"]:
        print(f"El asesino real era {ruta['asesino']}.")
    if arma_final != ruta["arma"]:
        print(f"El arma usada fue la {ruta['arma'].lower()}.")
    if hab_final != ruta["habitacion"]:
        print(f"El crimen ocurrió en la {ruta['habitacion'].lower()}.")
    print("\n Steve te mira decepcionado... el asesino escapó.")

