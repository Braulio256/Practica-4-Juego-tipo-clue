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

# --- Introducción narrativa ---
print(" MINECRAFT MISTERIO: ¡El caso del perro de Steve! ")
time.sleep(2)
print("\nSteve regresaba de un largo viaje por el Nether, cargando cofres llenos de recursos.")
time.sleep(2)
print("Al llegar a su casa, esperaba ser recibido por su fiel perro... pero el silencio fue su única bienvenida.")
time.sleep(2)
print("Sobre la puerta encontró un mensaje hecho con tinta de calamar: 'Tu perro está muerto. No busques al culpable.'")
time.sleep(3)
print("\nFurioso y con el corazón roto, Steve llamó a sus amigos más cercanos para una reunión.")
print("Sospecha que uno de ellos cometió el horrible crimen...")
time.sleep(3)

print("\nTienes 5 oportunidades para hacer preguntas antes de acusar a alguien.\n")

# --- Control de nerviosismo ---
# Garantizamos que al menos una persona esté nerviosa
nerviosos_fijos = random.sample(personajes, k=1)
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
        print(f" Te diriges a la {hab}...")
        time.sleep(1.5)

        prob_bloqueada = 0.2  # 20% no se puede revisar
        prob_pista = 0.5  # 50% de encontrar algo útil
        prob_nada = 0.3  # 30% de nada interesante

        if random.random() < prob_bloqueada:
            print(f"La puerta de la {hab.lower()} está bloqueada... no puedes entrar.")
        elif hab == ruta["habitacion"] and random.random() < prob_pista:
            print("Encuentras rastros de pelea... parece que aquí ocurrió algo grave.")
        elif random.random() < prob_nada:
            print("Todo parece en calma, solo polvo y telarañas.")
        else:
            print("Notas algo fuera de lugar, pero no estás seguro de qué.")
        preguntas += 1

    elif eleccion == "2":  # Arma
        arma = menu_opciones(armas, "revisar un arma")
        print(f" Examinas la {arma.lower()} detenidamente...")
        time.sleep(1.5)
        prob_sucia_extra = 0.6  # 60% de que aparezca un arma sucia

        if arma == ruta["arma"]:
            print("La superficie está manchada... parece haber sido usada recientemente.")
        else:
            if random.random() < prob_sucia_extra:
                otra_arma = random.choice([a for a in armas if a != arma])
                print(
                    f"La {arma.lower()} está limpia, pero escuchas que la {otra_arma.lower()} tiene rastros de suciedad...")
            else:
                print("El arma luce impecable, sin rastro de uso reciente.")
        preguntas += 1

    elif eleccion == "3":  # Persona
        persona = menu_opciones(personajes, "interrogar a alguien")
        print(f" Hablas con {persona}...")
        time.sleep(1.5)

        es_asesino = persona == ruta["asesino"]
        nervioso = (persona in nerviosos_fijos) or (random.random() < 0.35)

        if nervioso and not es_asesino:
            print(f"{persona} está inquieto, evita mirarte: 'Yo... no tengo idea, Steve. Estaba ocupado...'")
        elif nervioso and es_asesino and random.random() < 0.5:
            print(f"{persona} parece tranquilo, aunque notas que evita mencionar el perro...")
        elif es_asesino:
            print(f"{persona} dice calmadamente: '{historias[persona]}' pero hay algo en su tono que no encaja.")
        else:
            print(f"{persona} responde: {historias[persona]}")
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
