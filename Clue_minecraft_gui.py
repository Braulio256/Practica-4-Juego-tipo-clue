import pygame
import sys
import random

# --- Lógica de tu juego (CAMBIO EN STRINGS) ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Pico de diamante", "Pala de piedra"]
habitaciones = ["Herreria de la aldea", "Patio de Steve", "Piramide del desierto", "Mansion del bosque",
                "Portal en ruinas"]

rutas = [
    {"asesino": "Alex", "arma": "Espada de madera", "habitacion": "Patio de Steve"},
    {"asesino": "Kai", "arma": "Pala de piedra", "habitacion": "Herreria de la aldea"},
    {"asesino": "Ari", "arma": "Arco y flecha", "habitacion": "Mansion del bosque"},
    {"asesino": "Noor", "arma": "Hacha de oro", "habitacion": "Piramide del desierto"},
    {"asesino": "Sunny", "arma": "Pico de diamante", "habitacion": "Portal en ruinas"}
]

# --- ¡CAMBIO AQUI! ---
# Se reemplazó 'cabaña' por 'refugio'
historias = {
    "Alex": "Estaba combatiendo con mobs cerca de la cueva.",
    "Kai": "Dice que estaba haciendo un hueco para llevar agua a sus cultivos.",
    "Ari": "Afirma haber estado en la feria probando su punteria.",
    "Noor": "Estaba en el bosque talando madera para su nuevo refugio.",  # <-- ¡CAMBIO!
    "Sunny": "Dice que estaba en la mina consiguiendo minerales."
}

# --- Variables del juego que se reinician ---
ruta_solucion = None
preguntas = 0
resultado_final = ""
# --- FIN Lógica de tu juego ---


# --- 1. Configuración de Pygame y Pantalla HD ---
pygame.init()
ANCHO, ALTO = 1280, 720  # Resolución HD
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Minecraft Misterio")
reloj = pygame.time.Clock()

# --- 2. Colores y Fuentes ---
COLOR_BLANCO = (255, 255, 255)
COLOR_NEGRO = (0, 0, 0)
COLOR_GRIS = (100, 100, 100)
COLOR_GRIS_CLARO = (150, 150, 150)
COLOR_TRANSPARENTE = (0, 0, 0, 0)

COLOR_FONDO_MENU = (20, 20, 40)
COLOR_FONDO_JUEGO_BASE = (40, 20, 20)
COLOR_FONDO_FINAL = (20, 40, 20)

# Fuentes
try:
    fuente_titulo = pygame.font.Font("minecraft_font.ttf", 60)
    fuente_normal = pygame.font.Font("minecraft_font.ttf", 25)
    fuente_pequena = pygame.font.Font("minecraft_font.ttf", 18)
except FileNotFoundError:
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_normal = pygame.font.Font(None, 32)
    fuente_pequena = pygame.font.Font(None, 24)

# --- 3. Diccionario de Colores de Escena ---
colores_fondo_escena = {
    "base": COLOR_FONDO_JUEGO_BASE,
    "Herreria de la aldea": (160, 80, 0),
    "Patio de Steve": (0, 100, 20),
    "Piramide del desierto": (210, 200, 100),
    "Mansion del bosque": (30, 60, 30),
    "Portal en ruinas": (80, 0, 140)
}
color_escena_actual = colores_fondo_escena["base"]

# --- 4. Áreas de la Interfaz ---
OPCIONES_ANCHO = 300
TEXTO_ALTO = 200
panel_opciones_rect = pygame.Rect(ANCHO - OPCIONES_ANCHO, 0, OPCIONES_ANCHO, ALTO)
caja_texto_rect = pygame.Rect(20, ALTO - TEXTO_ALTO - 20, ANCHO - 40, TEXTO_ALTO)


# --- 5. Funciones de Ayuda para Dibujar ---
def dibujar_texto(texto, fuente, color, superficie, x, y, centrado=False, x_max=None):
    textobj = fuente.render(texto, True, color)
    textrect = textobj.get_rect()
    if centrado:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    if x_max and textrect.width > x_max:
        textrect.width = x_max
    superficie.blit(textobj, textrect)
    return textrect


def dibujar_texto_envoltura(texto, fuente, color, superficie, rect):
    palabras = texto.split(' ')
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        prueba_linea = linea_actual + palabra + " "
        prueba_ancho = fuente.size(prueba_linea)[0]
        if prueba_ancho < rect.width - 20:
            linea_actual = prueba_linea
        else:
            lineas.append(linea_actual)
            linea_actual = palabra + " "
    lineas.append(linea_actual)
    y = rect.top + 15
    for linea in lineas:
        dibujar_texto(linea, fuente, color, superficie, rect.left + 15, y)
        y += fuente.get_linesize()


# --- 6. Variables de Estado del Juego ---
estado_juego = "menu_principal"
sub_estado_juego = "ninguno"
texto_narrativo = ""
botones_actuales = []
acusacion_final = {}


# Función para (re)iniciar el juego
def iniciar_nuevo_juego():
    global ruta_solucion, preguntas, resultado_final, sub_estado_juego, texto_narrativo, acusacion_final, color_escena_actual
    ruta_solucion = random.choice(rutas)
    preguntas = 0
    resultado_final = ""
    sub_estado_juego = "introduccion"
    texto_narrativo = "Steve regresaba de un largo viaje por el Nether... Al llegar a su casa, encontro un mensaje: 'Tu perro esta muerto. No busques al culpable.'"
    acusacion_final = {"asesino": None, "arma": None, "habitacion": None}
    color_escena_actual = colores_fondo_escena["base"]
    # print(f"SOLUCION (Debug): {ruta_solucion}")


# Función de lógica de investigación (CORREGIDA)
def investigar_item(item_nombre, tipo):
    global texto_narrativo, color_escena_actual

    clave_solucion = tipo
    if tipo == "persona":
        clave_solucion = "asesino"
    elif tipo == "habitacion":
        clave_solucion = "habitacion"

    if tipo == "habitacion":
        if item_nombre in colores_fondo_escena:
            color_escena_actual = colores_fondo_escena[item_nombre]
        else:
            color_escena_actual = colores_fondo_escena["base"]

    if item_nombre == ruta_solucion[clave_solucion]:
        if tipo == "persona":
            texto_narrativo = f"{item_nombre} dice: '{historias[item_nombre]}' Su voz tiembla un poco, pero no puedes estar seguro... (Pista Sospechosa)"
        elif tipo == "arma":
            texto_narrativo = f"Examinas el/la {item_nombre.lower()}. Esta... ¿manchada? Parece que se ha usado recientemente. (Pista Sospechosa)"
        elif tipo == "habitacion":
            texto_narrativo = f"Inspeccionas el/la {item_nombre.lower()}. Hay claros signos de forcejeo y algunos... ¿pelos de perro? (Pista Sospechosa)"
    else:
        if tipo == "persona":
            texto_narrativo = f"{item_nombre} tiene una coartada perfecta. '{historias[item_nombre]}'. Varios testigos lo confirman. ¡Puedes DESCARTAR a {item_nombre}!"
        elif tipo == "arma":
            texto_narrativo = f"El/La {item_nombre.lower()} esta guardada y cubierta de polvo. Es imposible que se usara. ¡Puedes DESCARTAR esta arma!"
        elif tipo == "habitacion":
            texto_narrativo = f"El lugar esta tranquilo, no hay ni una mota de polvo fuera de lugar. El crimen NO ocurrio aqui. ¡Puedes DESCARTAR la {item_nombre}!"


# --- 7. Bucle Principal del Juego ---
running = True
while running:

    mouse_pos = pygame.mouse.get_pos()

    # --- Lógica de Botones Movida ARRIBA ---
    botones_actuales.clear()

    if estado_juego == "jugando" or estado_juego == "acusando":
        y_offset = 50
        x_botones = ANCHO - (OPCIONES_ANCHO // 2)
        ancho_botones = OPCIONES_ANCHO - 40

        lista_opciones_actual = []

        if estado_juego == "jugando":
            if sub_estado_juego == "introduccion":
                lista_opciones_actual = ["Continuar"]
            elif sub_estado_juego == "eligiendo_categoria":
                lista_opciones_actual = ["Investigar Persona", "Investigar Arma", "Investigar Habitacion", "---",
                                         "HACER ACUSACION"]
            elif sub_estado_juego == "eligiendo_persona":
                lista_opciones_actual = personajes + ["---", "Volver"]
            elif sub_estado_juego == "eligiendo_arma":
                lista_opciones_actual = armas + ["---", "Volver"]
            elif sub_estado_juego == "eligiendo_habitacion":
                lista_opciones_actual = habitaciones + ["---", "Volver"]
            elif sub_estado_juego == "mostrando_pista":
                lista_opciones_actual = ["Continuar"]

        elif estado_juego == "acusando":
            if sub_estado_juego == "acusando_persona":
                lista_opciones_actual = personajes
            elif sub_estado_juego == "acusando_arma":
                lista_opciones_actual = armas
            elif sub_estado_juego == "acusando_habitacion":
                lista_opciones_actual = habitaciones

        # Calcular los rects de los botones y guardarlos
        for texto_opcion in lista_opciones_actual:
            if texto_opcion == "---":
                y_offset += 20
                continue

            boton_rect = pygame.Rect(x_botones - (ancho_botones // 2), y_offset, ancho_botones, 40)
            botones_actuales.append((texto_opcion, boton_rect))
            y_offset += 50

            # --- 7.1. Manejo de Eventos ---
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:
                if estado_juego == "menu_principal":
                    if 'boton_jugar_rect' in locals() and boton_jugar_rect.collidepoint(mouse_pos):
                        iniciar_nuevo_juego()
                        estado_juego = "jugando"
                    if 'boton_salir_rect' in locals() and boton_salir_rect.collidepoint(mouse_pos):
                        running = False

                elif estado_juego == "jugando" or estado_juego == "acusando":
                    for (texto_opcion, rect) in botones_actuales:
                        if rect.collidepoint(mouse_pos):
                            if estado_juego == "jugando":

                                if sub_estado_juego == "introduccion":
                                    if texto_opcion == "Continuar":
                                        sub_estado_juego = "eligiendo_categoria"
                                        texto_narrativo = f"Steve te reune. Tienes {5 - preguntas} oportunidades para investigar. ¿Por donde empiezas?"

                                elif sub_estado_juego == "eligiendo_categoria":
                                    if texto_opcion == "Investigar Persona":
                                        sub_estado_juego = "eligiendo_persona"
                                    elif texto_opcion == "Investigar Arma":
                                        sub_estado_juego = "eligiendo_arma"
                                    elif texto_opcion == "Investigar Habitacion":
                                        sub_estado_juego = "eligiendo_habitacion"
                                    elif texto_opcion == "HACER ACUSACION":
                                        estado_juego = "acusando"
                                        sub_estado_juego = "acusando_persona"
                                        texto_narrativo = "Es el momento. ¿A quien acusas de ser el ASESINO?"

                                elif sub_estado_juego in ["eligiendo_persona", "eligiendo_arma",
                                                          "eligiendo_habitacion"]:
                                    if texto_opcion == "Volver":
                                        sub_estado_juego = "eligiendo_categoria"
                                        texto_narrativo = f"¿Que deseas investigar ahora? (Preguntas restantes: {5 - preguntas})"
                                        color_escena_actual = colores_fondo_escena["base"]
                                    else:
                                        # Aquí determinamos el 'tipo' para la función investigar_item
                                        if sub_estado_juego == "eligiendo_persona":
                                            tipo_investigacion = "persona"
                                        elif sub_estado_juego == "eligiendo_arma":
                                            tipo_investigacion = "arma"
                                        elif sub_estado_juego == "eligiendo_habitacion":
                                            tipo_investigacion = "habitacion"

                                        investigar_item(texto_opcion, tipo_investigacion)
                                        sub_estado_juego = "mostrando_pista"

                                elif sub_estado_juego == "mostrando_pista":
                                    if texto_opcion == "Continuar":
                                        preguntas += 1
                                        color_escena_actual = colores_fondo_escena["base"]
                                        if preguntas >= 5:
                                            estado_juego = "acusando"
                                            sub_estado_juego = "acusando_persona"
                                            texto_narrativo = "Se acabaron tus preguntas. Debes hacer una acusacion. ¿Quien es el ASESINO?"
                                        else:
                                            sub_estado_juego = "eligiendo_categoria"
                                            texto_narrativo = f"¿Que deseas investigar ahora? (Preguntas restantes: {5 - preguntas})"

                            elif estado_juego == "acusando":
                                if sub_estado_juego == "acusando_persona":
                                    acusacion_final["asesino"] = texto_opcion
                                    sub_estado_juego = "acusando_arma"
                                    texto_narrativo = f"Acusas a {acusacion_final['asesino']}. ¿Que ARMA uso?"
                                elif sub_estado_juego == "acusando_arma":
                                    acusacion_final["arma"] = texto_opcion
                                    sub_estado_juego = "acusando_habitacion"
                                    texto_narrativo = f"Acusas a {acusacion_final['asesino']} con la {acusacion_final['arma'].lower()}. ¿En que HABITACION?"
                                elif sub_estado_juego == "acusando_habitacion":
                                    acusacion_final["habitacion"] = texto_opcion

                                    if acusacion_final["asesino"] == ruta_solucion["asesino"] and \
                                            acusacion_final["arma"] == ruta_solucion["arma"] and \
                                            acusacion_final["habitacion"] == ruta_solucion["habitacion"]:
                                        resultado_final = "Ganaste"
                                    else:
                                        resultado_final = "Perdiste"
                                    estado_juego = "pantalla_final"

                            break

                elif estado_juego == "pantalla_final":
                    if 'boton_jugar_de_nuevo_rect' in locals() and boton_jugar_de_nuevo_rect.collidepoint(mouse_pos):
                        iniciar_nuevo_juego()
                        estado_juego = "jugando"
                    elif 'boton_menu_principal_rect' in locals() and boton_menu_principal_rect.collidepoint(mouse_pos):
                        estado_juego = "menu_principal"
                    elif 'boton_salir_rect' in locals() and boton_salir_rect.collidepoint(mouse_pos):
                        running = False

    # --- 7.2. Lógica y Dibujo basado en el Estado ---

    # --- PANTALLA: Menú Principal ---
    if estado_juego == "menu_principal":
        pantalla.fill(COLOR_FONDO_MENU)
        dibujar_texto("Minecraft Misterio", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150, centrado=True)

        boton_jugar_rect = pygame.draw.rect(pantalla, COLOR_GRIS, [ANCHO // 2 - 100, 300, 200, 50])
        boton_salir_rect = pygame.draw.rect(pantalla, COLOR_GRIS, [ANCHO // 2 - 100, 400, 200, 50])

        if boton_jugar_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton_jugar_rect)
        if boton_salir_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton_salir_rect)

        dibujar_texto("Jugar", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 325, centrado=True)
        dibujar_texto("Salir", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 425, centrado=True)

    # --- PANTALLA: Jugando o Acusando ---
    elif estado_juego == "jugando" or estado_juego == "acusando":

        pantalla.fill(color_escena_actual)

        panel_opciones_surf = pygame.Surface((OPCIONES_ANCHO, ALTO), pygame.SRCALPHA)
        panel_opciones_surf.fill((0, 0, 0, 180))
        pantalla.blit(panel_opciones_surf, (ANCHO - OPCIONES_ANCHO, 0))

        caja_texto_surf = pygame.Surface((caja_texto_rect.width, caja_texto_rect.height), pygame.SRCALPHA)
        caja_texto_surf.fill((0, 0, 0, 200))
        pantalla.blit(caja_texto_surf, caja_texto_rect.topleft)
        pygame.draw.rect(pantalla, COLOR_BLANCO, caja_texto_rect, 2)

        dibujar_texto_envoltura(texto_narrativo, fuente_normal, COLOR_BLANCO, pantalla, caja_texto_rect)

        # Dibujar los botones
        for (texto_opcion, boton_rect) in botones_actuales:
            color_boton = COLOR_GRIS
            if boton_rect.collidepoint(mouse_pos):
                color_boton = COLOR_GRIS_CLARO

            pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=5)
            dibujar_texto(texto_opcion, fuente_pequena, COLOR_BLANCO, pantalla,
                          boton_rect.centerx, boton_rect.centery,
                          centrado=True, x_max=boton_rect.width - 10)

    # --- PANTALLA: Final ---
    elif estado_juego == "pantalla_final":

        pantalla.fill(COLOR_FONDO_FINAL)

        if resultado_final == "Ganaste":
            dibujar_texto("¡Has resuelto el caso!", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150,
                          centrado=True)
            sol_texto_1 = f"¡Era {ruta_solucion['asesino']} con la {ruta_solucion['arma'].lower()}"
            sol_texto_2 = f"en la {ruta_solucion['habitacion'].lower()}!"
            dibujar_texto(sol_texto_1, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 250, centrado=True)
            dibujar_texto(sol_texto_2, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 290, centrado=True)
        else:
            dibujar_texto("¡El asesino escapo!", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150, centrado=True)
            sol_texto_1 = f"La respuesta correcta era: {ruta_solucion['asesino']}"
            sol_texto_2 = f"con la {ruta_solucion['arma'].lower()} en la {ruta_solucion['habitacion'].lower()}."
            dibujar_texto(sol_texto_1, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 250, centrado=True)
            dibujar_texto(sol_texto_2, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 290, centrado=True)

        # Definimos los TRES rects
        boton_jugar_de_nuevo_rect = pygame.draw.rect(pantalla, COLOR_GRIS, [ANCHO // 2 - 100, 350, 200, 50])
        boton_menu_principal_rect = pygame.draw.rect(pantalla, COLOR_GRIS, [ANCHO // 2 - 100, 450, 200, 50])
        boton_salir_rect = pygame.draw.rect(pantalla, COLOR_GRIS, [ANCHO // 2 - 100, 550, 200, 50])

        # Efectos hover
        if boton_jugar_de_nuevo_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton_jugar_de_nuevo_rect)
        if boton_menu_principal_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton_menu_principal_rect)
        if boton_salir_rect.collidepoint(mouse_pos):
            pygame.draw.rect(pantalla, COLOR_GRIS_CLARO, boton_salir_rect)

        # Textos de los botones
        dibujar_texto("Jugar de Nuevo", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 375, centrado=True)
        dibujar_texto("Menu Principal", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 475, centrado=True)
        dibujar_texto("Salir", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 575, centrado=True)

    # --- 7.3. Actualizar la pantalla ---
    pygame.display.flip()

    # --- 7.4. Controlar los FPS ---
    reloj.tick(30)

# --- Salir de Pygame ---
pygame.quit()
sys.exit()