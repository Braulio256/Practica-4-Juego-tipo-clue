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

# --- CAMBIO #1: Historias de los personajes actualizadas ---
historias = {
    "Alex": "Estaba combatiendo con mobs cerca de la cueva.",
    "Kai": "Dice que estaba haciendo un hueco para llevar agua a sus cultivos.",
    "Ari": "Afirma haber estado en la feria probando su puntería.",
    "Noor": "Estaba en el bosque talando madera para su nueva cabaña.",
    "Sunny": "Dice que estaba en la mina consiguiendo minerales."
}

# Elegir ruta aleatoria (La SOLUCIÓN SECRETA)
ruta_solucion = random.choice(rutas)

# --- Introducción narrativa ---
print(" MINECRAFT MISTERIO: ¡El caso del perro de Steve! ")
time.sleep(1)
print("\nSteve regresaba de un largo viaje por el Nether...")
print("Al llegar a su casa, encontró un mensaje: 'Tu perro está muerto. No busques al culpable.'")
time.sleep(2)
print("\nFurioso, Steve llamó a sus amigos. Sospecha que uno de ellos cometió el crimen...")
time.sleep(2)
print("\nTu objetivo: Usar tus 5 preguntas para DESCARTAR sospechosos, armas y lugares.")
print("Lleva tus propias notas... ¡La deducción corre por tu cuenta!\n")

preguntas = 0


# --- Función para mostrar opciones tipo menú (sin cambios) ---
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


# --- CAMBIO #2: Bucle de preguntas con lógica de ELIMINACIÓN DE OBJETOS ---
# Ya no se menciona el "bloc de notas" ni las "rutas".
while preguntas < 5:
    print(f"\n--- Preguntas restantes: {5 - preguntas} ---")
    print("¿Qué deseas investigar?")
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

        # Pregunta: ¿La habitación investigada es la de la SOLUCIÓN?
        if hab == ruta_solucion["habitacion"]:
            # Pista ambigua (como pediste)
            print("Encuentras rastros de pelea... parece que aquí ocurrió algo grave. (Pista Sospechosa)")
        else:
            # Pista de eliminación (100% segura)
            print(f"Revisas la {hab.lower()} y está impecable. No hay señales de nada.")
            print(f"¡Puedes DESCARTAR la {hab} como el lugar del crimen!")
        preguntas += 1

    elif eleccion == "2":  # Arma
        arma = menu_opciones(armas, "revisar un arma")
        print(f" Examinas la {arma.lower()} detenidamente...")
        time.sleep(1.5)

        # Pregunta: ¿El arma investigada es la de la SOLUCIÓN?
        if arma == ruta_solucion["arma"]:
            # Pista ambigua
            print(f"La {arma.lower()} está manchada... parece haber sido usada recientemente. (Pista Sospechosa)")
        else:
            # Pista de eliminación (100% segura)
            print(f"El arma está limpia y guardada bajo llave. Esta arma NO se usó.")
            print(f"¡Puedes DESCARTAR la {arma} como el arma del crimen!")
        preguntas += 1

    elif eleccion == "3":  # Persona
        persona = menu_opciones(personajes, "interrogar a alguien")
        print(f" Hablas con {persona}...")
        time.sleep(1.5)

        # Pregunta: ¿La persona investigada es la de la SOLUCIÓN?
        if persona == ruta_solucion["asesino"]:
            # Pista ambigua
            print(
                f"{persona} dice calmadamente: '{historias[persona]}' pero hay algo en su tono que no encaja... (Pista Sospechosa)")
        else:
            # Pista de eliminación (100% segura)
            print(f"{persona} tiene una coartada perfecta. '{historias[persona]}'. Varios testigos lo confirman.")
            print(f"¡Puedes DESCARTAR a {persona} como sospechoso!")
        preguntas += 1

    elif eleccion == "4":
        break
    else:
        print("Opción inválida.")

# --- CAMBIO #3: Fase final: acusación por partes ---
# El jugador debe elegir cada elemento por separado.
print("\n Ha llegado el momento de decidir...")
asesino_final = menu_opciones(personajes, "acusar al asesino")
arma_final = menu_opciones(armas, "elegir el arma del crimen")
hab_final = menu_opciones(habitaciones, "decidir la habitación del crimen")

print("\nSteve escucha tu veredicto...")
time.sleep(2)

# Se compara la acusación del jugador con la solución secreta
if asesino_final == ruta_solucion["asesino"] and arma_final == ruta_solucion["arma"] and hab_final == ruta_solucion[
    "habitacion"]:
    print(
        f" ¡Correcto! {asesino_final} usó la {arma_final.lower()} en la {hab_final.lower()} para acabar con el perro de Steve. ¡Has resuelto el caso!")
else:
    print(" No lograste resolver el caso.")
    # Le decimos al jugador cuál era la respuesta correcta
    print(f"El asesino real era {ruta_solucion['asesino']}.")
    print(f"El arma usada fue la {ruta_solucion['arma'].lower()}.")
    print(f"El crimen ocurrió en la {ruta_solucion['habitacion'].lower()}.")
    print("\n Steve te mira decepcionado... el asesino escapó.")