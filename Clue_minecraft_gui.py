import pygame
import sys
import random
import os


# --- ### Función Resource Path ### ---
def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para desarrollo y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# --- ### FIN FUNCION ### ---


# --- Lógica de tu juego ---
personajes = ["Alex", "Kai", "Ari", "Noor", "Sunny"]
armas = ["Espada de madera", "Hacha de oro", "Arco y flecha", "Pico de diamante", "Pala de piedra"]
habitaciones = ["Herreria en una aldea", "Patio de Steve", "Piramide del desierto", "Mansion del bosque",
                "Portal en ruinas"]

articulos_armas = {
    "Espada de madera": "la", "Hacha de oro": "el", "Arco y flecha": "el",
    "Pico de diamante": "el", "Pala de piedra": "la"
}
articulos_habitaciones = {
    "Herreria en una aldea": "la", "Patio de Steve": "el", "Piramide del desierto": "la",
    "Mansion del bosque": "la", "Portal en ruinas": "el"
}

rutas = [
    {"asesino": "Alex", "arma": "Espada de madera", "habitacion": "Patio de Steve"},
    {"asesino": "Kai", "arma": "Pala de piedra", "habitacion": "Herreria en una aldea"},
    {"asesino": "Ari", "arma": "Arco y flecha", "habitacion": "Mansion del bosque"},
    {"asesino": "Noor", "arma": "Hacha de oro", "habitacion": "Piramide del desierto"},
    {"asesino": "Sunny", "arma": "Pico de diamante", "habitacion": "Portal en ruinas"}
]

historias = {
    "Alex": "Estaba combatiendo con mobs cerca de la cueva.",
    "Kai": "Dice que estaba haciendo un hueco para llevar agua a sus cultivos.",
    "Ari": "Afirma haber estado en el campo de tiro probando su punteria.",
    "Noor": "Estaba en el bosque talando madera para su nuevo refugio.",
    "Sunny": "Dice que estaba en la mina consiguiendo minerales."
}

# --- Variables del juego ---
ruta_solucion = None
preguntas = 0
resultado_final = ""
# --- FIN Lógica ---


# --- 1. Configuración de Pygame ---
pygame.init()
ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Clue MINECRAFT")
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

try:
    ruta_fuente = resource_path("assets/minecraft_font.ttf")
    fuente_titulo = pygame.font.Font(ruta_fuente, 60)
    fuente_normal = pygame.font.Font(ruta_fuente, 28)
    fuente_pequena = pygame.font.Font(ruta_fuente, 22)
except FileNotFoundError:
    print("ADVERTENCIA: Fuente no encontrada en 'assets/'. Usando fuente por defecto.")
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_normal = pygame.font.Font(None, 32)
    fuente_pequena = pygame.font.Font(None, 24)

# --- 3. Colores de Escena (Fallback) ---
colores_fondo_escena = {
    "base": COLOR_FONDO_JUEGO_BASE,
    "Herreria en una aldea": (160, 80, 0), "Patio de Steve": (0, 100, 20),
    "Piramide del desierto": (210, 200, 100), "Mansion del bosque": (30, 60, 30),
    "Portal en ruinas": (80, 0, 140)
}
color_escena_actual = colores_fondo_escena["base"]

# --- 4. Carga de Imágenes ---
usar_colores_fallback = False
try:
    def sanitizar_nombre(nombre):
        return nombre.lower().replace(" ", "_").replace("á", "a").replace("é", "e").replace("í", "i").replace("ó",
                                                                                                              "o").replace(
            "ú", "u")


    fondo_menu = pygame.image.load(resource_path("assets/fondo_menu.png")).convert()
    fondo_intro = pygame.image.load(resource_path("assets/fondo_intro.png")).convert()
    fondo_juego_base = pygame.image.load(resource_path("assets/fondo_juego_base.png")).convert()
    fondo_ganaste = pygame.image.load(resource_path("assets/fondo_ganaste.png")).convert()
    fondo_perdiste = pygame.image.load(resource_path("assets/fondo_perdiste.png")).convert()

    fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))
    fondo_intro = pygame.transform.scale(fondo_intro, (ANCHO, ALTO))
    fondo_juego_base = pygame.transform.scale(fondo_juego_base, (ANCHO, ALTO))
    fondo_ganaste = pygame.transform.scale(fondo_ganaste, (ANCHO, ALTO))
    fondo_perdiste = pygame.transform.scale(fondo_perdiste, (ANCHO, ALTO))

    imagenes_personajes = {
        p: pygame.transform.scale(pygame.image.load(resource_path(f"assets/{sanitizar_nombre(p)}.png")).convert_alpha(),
                                  (ANCHO, ALTO)) for p in personajes}
    imagenes_armas = {
        a: pygame.transform.scale(pygame.image.load(resource_path(f"assets/{sanitizar_nombre(a)}.png")).convert_alpha(),
                                  (ANCHO, ALTO)) for a in armas}
    imagenes_armas_culpables = {a: pygame.transform.scale(
        pygame.image.load(resource_path(f"assets/{sanitizar_nombre(a)}_culpable.png")).convert_alpha(), (ANCHO, ALTO))
                                for a in armas}
    imagenes_locaciones = {
        l: pygame.transform.scale(pygame.image.load(resource_path(f"assets/{sanitizar_nombre(l)}.png")).convert(),
                                  (ANCHO, ALTO)) for l in habitaciones}

    imagen_escena_actual = fondo_intro
except FileNotFoundError as e:
    print(f"¡ADVERTENCIA! No se pudo cargar una imagen: {e}")
    print("Asegurate de que todos los archivos esten en la carpeta 'assets'.")
    print("Se usaran los fondos de color solido en su lugar.")
    usar_colores_fallback = True
# --- FIN Carga de Imágenes ---


# --- 5. Áreas de la Interfaz ---
OPCIONES_ANCHO = 320
TEXTO_ALTO = 200
panel_opciones_rect = pygame.Rect(ANCHO - OPCIONES_ANCHO, 0, OPCIONES_ANCHO, ALTO)
caja_texto_rect = pygame.Rect(20, ALTO - TEXTO_ALTO - 20, ANCHO - 40, TEXTO_ALTO)


# --- 6. Funciones de Ayuda para Dibujar ---
def dibujar_texto(texto, fuente, color, superficie, x, y, centrado=False, x_max=None):
    textobj = fuente.render(texto, True, color)
    textrect = textobj.get_rect()

    if centrado:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)

    superficie.blit(textobj, textrect)
    return textrect


def dibujar_texto_envoltura(texto_completo, fuente, color, superficie, rect, indice_visible):
    palabras = texto_completo.split(' ')
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
    caracteres_contados = 0
    for linea in lineas:
        caracteres_restantes = indice_visible - caracteres_contados
        if caracteres_restantes <= 0:
            break

        texto_a_dibujar = ""
        if caracteres_restantes >= len(linea):
            texto_a_dibujar = linea
        else:
            texto_a_dibujar = linea[:caracteres_restantes]

        dibujar_texto(texto_a_dibujar, fuente, color, superficie, rect.left + 15, y)
        caracteres_contados += len(linea)
        y += fuente.get_linesize()


# --- 7. Variables de Estado del Juego ---
estado_juego = "menu_principal"
sub_estado_juego = "ninguno"
texto_narrativo = ""
botones_actuales = []
acusacion_final = {}

indice_texto = 0
contador_tiempo_texto = 0
TIEMPO_LETRA = 30  # Milisegundos por letra


def iniciar_nuevo_juego():
    global ruta_solucion, preguntas, resultado_final, sub_estado_juego, texto_narrativo, acusacion_final, color_escena_actual, imagen_escena_actual, indice_texto
    ruta_solucion = random.choice(rutas)
    preguntas = 0
    resultado_final = ""
    sub_estado_juego = "introduccion"
    texto_narrativo = "Steve regresaba de un largo viaje por el Nether... Al llegar a su casa, encontro un mensaje: 'Tu perro esta muerto. No busques al culpable.'"
    indice_texto = 0
    acusacion_final = {"asesino": None, "arma": None, "habitacion": None}

    if usar_colores_fallback:
        color_escena_actual = colores_fondo_escena["base"]
    else:
        imagen_escena_actual = fondo_intro


def investigar_item(item_nombre, tipo):
    global texto_narrativo, color_escena_actual, imagen_escena_actual, indice_texto

    clave_solucion = tipo
    if tipo == "persona":
        clave_solucion = "asesino"
    elif tipo == "habitacion":
        clave_solucion = "habitacion"

    if usar_colores_fallback:
        if tipo == "habitacion": color_escena_actual = colores_fondo_escena.get(item_nombre,
                                                                                colores_fondo_escena["base"])
    else:
        if tipo == "habitacion":
            imagen_escena_actual = imagenes_locaciones.get(item_nombre, fondo_juego_base)
        elif tipo == "persona":
            imagen_escena_actual = imagenes_personajes.get(item_nombre, fondo_juego_base)
        elif tipo == "arma":
            if item_nombre == ruta_solucion[clave_solucion]:
                imagen_escena_actual = imagenes_armas_culpables.get(item_nombre, fondo_juego_base)
            else:
                imagen_escena_actual = imagenes_armas.get(item_nombre, fondo_juego_base)

    if item_nombre == ruta_solucion[clave_solucion]:
        if tipo == "persona":
            texto_narrativo = f"{item_nombre} dice: '{historias[item_nombre]}' Su voz tiembla un poco, pero no puedes estar seguro... (Pista Sospechosa)"
        elif tipo == "arma":
            texto_narrativo = f"Examinas {articulos_armas[item_nombre]} {item_nombre.lower()}. Esta... ¿manchada? Parece que se ha usado recientemente. (Pista Sospechosa)"
        elif tipo == "habitacion":
            texto_narrativo = f"Inspeccionas {articulos_habitaciones[item_nombre]} {item_nombre.lower()}. Hay claros signos de forcejeo y algunos... ¿pelos de perro? (Pista Sospechosa)"
    else:
        if tipo == "persona":
            texto_narrativo = f"{item_nombre} tiene una coartada perfecta. '{historias[item_nombre]}'. Varios testigos lo confirman. ¡Puedes DESCARTAR a {item_nombre}!"
        elif tipo == "arma":
            texto_narrativo = f"{articulos_armas[item_nombre].capitalize()} {item_nombre.lower()} esta guardada y cubierta de polvo. Es imposible que se usara. ¡Puedes DESCARTAR esta arma!"
        elif tipo == "habitacion":
            texto_narrativo = f"El lugar esta tranquilo, no hay ni una mota de polvo fuera de lugar. El crimen NO ocurrio aqui. ¡Puedes DESCARTAR {articulos_habitaciones[item_nombre]} {item_nombre}!"

    indice_texto = 0


# --- 8. Bucle Principal del Juego ---
running = True
while running:

    mouse_pos = pygame.mouse.get_pos()
    botones_actuales.clear()

    if indice_texto < len(texto_narrativo):
        delta_tiempo = reloj.get_time()
        contador_tiempo_texto += delta_tiempo
        if contador_tiempo_texto >= TIEMPO_LETRA:
            indice_texto += 1
            contador_tiempo_texto = 0

    if estado_juego == "jugando" or estado_juego == "acusando":
        y_offset = 50
        x_botones = ANCHO - (OPCIONES_ANCHO // 2)
        ancho_botones = OPCIONES_ANCHO - 10

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

        for texto_opcion in lista_opciones_actual:
            if texto_opcion == "---":
                y_offset += 20
                continue
            boton_rect = pygame.Rect(x_botones - (ancho_botones // 2), y_offset, ancho_botones, 40)
            botones_actuales.append((texto_opcion, boton_rect))
            y_offset += 50

    # --- 8.1. Manejo de Eventos ---
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            running = False

        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:

                if (estado_juego == "jugando" or estado_juego == "acusando") and indice_texto < len(texto_narrativo):
                    indice_texto = len(texto_narrativo)

                else:
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
                                            indice_texto = 0
                                            if not usar_colores_fallback:
                                                imagen_escena_actual = fondo_juego_base
                                            else:
                                                color_escena_actual = colores_fondo_escena["base"]
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
                                            indice_texto = 0
                                    elif sub_estado_juego in ["eligiendo_persona", "eligiendo_arma",
                                                              "eligiendo_habitacion"]:
                                        if texto_opcion == "Volver":
                                            sub_estado_juego = "eligiendo_categoria"
                                            texto_narrativo = f"¿Que deseas investigar ahora? (Preguntas restantes: {5 - preguntas})"
                                            indice_texto = 0
                                            if not usar_colores_fallback:
                                                imagen_escena_actual = fondo_juego_base
                                            else:
                                                color_escena_actual = colores_fondo_escena["base"]
                                        else:
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
                                            if not usar_colores_fallback:
                                                imagen_escena_actual = fondo_juego_base
                                            else:
                                                color_escena_actual = colores_fondo_escena["base"]
                                            if preguntas >= 5:
                                                estado_juego = "acusando"
                                                sub_estado_juego = "acusando_persona"
                                                texto_narrativo = "Se acabaron tus preguntas. Debes hacer una acusacion. ¿Quien es el ASESINO?"
                                            else:
                                                sub_estado_juego = "eligiendo_categoria"
                                                texto_narrativo = f"¿Que deseas investigar ahora? (Preguntas restantes: {5 - preguntas})"
                                            indice_texto = 0
                                elif estado_juego == "acusando":
                                    if sub_estado_juego == "acusando_persona":
                                        acusacion_final["asesino"] = texto_opcion
                                        sub_estado_juego = "acusando_arma"
                                        texto_narrativo = f"Acusas a {acusacion_final['asesino']}. ¿Que ARMA uso?"
                                        indice_texto = 0
                                    elif sub_estado_juego == "acusando_arma":
                                        acusacion_final["arma"] = texto_opcion
                                        sub_estado_juego = "acusando_habitacion"
                                        texto_narrativo = f"Acusas a {acusacion_final['asesino']} con {articulos_armas[acusacion_final['arma']]} {acusacion_final['arma'].lower()}. ¿En que HABITACION?"
                                        indice_texto = 0
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
                        if 'boton_jugar_de_nuevo_rect' in locals() and boton_jugar_de_nuevo_rect.collidepoint(
                                mouse_pos):
                            iniciar_nuevo_juego()
                            estado_juego = "jugando"
                        elif 'boton_menu_principal_rect' in locals() and boton_menu_principal_rect.collidepoint(
                                mouse_pos):
                            estado_juego = "menu_principal"
                        elif 'boton_salir_rect' in locals() and boton_salir_rect.collidepoint(mouse_pos):
                            running = False

    # --- 8.2. Lógica y Dibujo ---

    # --- PANTALLA: Menú Principal ---
    if estado_juego == "menu_principal":
        if usar_colores_fallback:
            pantalla.fill(COLOR_FONDO_MENU)
        else:
            pantalla.blit(fondo_menu, (0, 0))

        dibujar_texto("Clue MINECRAFT", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150, centrado=True)

        boton_ancho = 300
        boton_alto = 50
        boton_espacio = 50
        boton_y = ALTO - 200

        total_ancho = (boton_ancho * 2) + boton_espacio
        inicio_x = (ANCHO - total_ancho) // 2

        boton_jugar_x = inicio_x
        boton_salir_x = inicio_x + boton_ancho + boton_espacio

        boton_jugar_rect = pygame.Rect(boton_jugar_x, boton_y, boton_ancho, boton_alto)
        boton_salir_rect = pygame.Rect(boton_salir_x, boton_y, boton_ancho, boton_alto)

        color_jugar = COLOR_GRIS
        if boton_jugar_rect.collidepoint(mouse_pos): color_jugar = COLOR_GRIS_CLARO
        pygame.draw.rect(pantalla, color_jugar, boton_jugar_rect, border_radius=10)

        color_salir = COLOR_GRIS
        if boton_salir_rect.collidepoint(mouse_pos): color_salir = COLOR_GRIS_CLARO
        pygame.draw.rect(pantalla, color_salir, boton_salir_rect, border_radius=10)

        dibujar_texto("Jugar", fuente_normal, COLOR_BLANCO, pantalla, boton_jugar_rect.centerx,
                      boton_jugar_rect.centery, centrado=True)
        dibujar_texto("Salir", fuente_normal, COLOR_BLANCO, pantalla, boton_salir_rect.centerx,
                      boton_salir_rect.centery, centrado=True)

    # --- PANTALLA: Jugando o Acusando ---
    elif estado_juego == "jugando" or estado_juego == "acusando":

        if usar_colores_fallback:
            pantalla.fill(color_escena_actual)
        else:
            pantalla.blit(imagen_escena_actual, (0, 0))

        caja_texto_surf = pygame.Surface((caja_texto_rect.width, caja_texto_rect.height), pygame.SRCALPHA)
        caja_texto_surf.fill((0, 0, 0, 200))
        pantalla.blit(caja_texto_surf, caja_texto_rect.topleft)
        pygame.draw.rect(pantalla, COLOR_BLANCO, caja_texto_rect, 2)

        dibujar_texto_envoltura(texto_narrativo, fuente_normal, COLOR_BLANCO, pantalla, caja_texto_rect, indice_texto)

        if indice_texto >= len(texto_narrativo):
            for (texto_opcion, boton_rect) in botones_actuales:
                color_boton = COLOR_GRIS
                if boton_rect.collidepoint(mouse_pos):
                    color_boton = COLOR_GRIS_CLARO

                pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=5)
                dibujar_texto(texto_opcion, fuente_pequena, COLOR_BLANCO, pantalla,
                              boton_rect.centerx, boton_rect.centery,
                              centrado=True)

                # --- ### PANTALLA FINAL ACTUALIZADA ### ---
    elif estado_juego == "pantalla_final":

        if usar_colores_fallback:
            pantalla.fill(COLOR_FONDO_FINAL)
        else:
            if resultado_final == "Ganaste":
                pantalla.blit(fondo_ganaste, (0, 0))
            else:
                pantalla.blit(fondo_perdiste, (0, 0))

        if resultado_final == "Ganaste":
            dibujar_texto("¡Has resuelto el caso!", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150,
                          centrado=True)

            articulo_arma_sol = articulos_armas[ruta_solucion['arma']]
            articulo_hab_sol = articulos_habitaciones[ruta_solucion['habitacion']]
            sol_texto_1 = f"¡Era {ruta_solucion['asesino']} con {articulo_arma_sol} {ruta_solucion['arma'].lower()}"
            sol_texto_2 = f"en {articulo_hab_sol} {ruta_solucion['habitacion'].lower()}!"
            dibujar_texto(sol_texto_1, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 250, centrado=True)
            dibujar_texto(sol_texto_2, fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 290, centrado=True)

        else:
            dibujar_texto("¡El asesino escapo!", fuente_titulo, COLOR_BLANCO, pantalla, ANCHO // 2, 150, centrado=True)
            dibujar_texto("Steve te mira decepcionado...", fuente_normal, COLOR_BLANCO, pantalla, ANCHO // 2, 200,
                          centrado=True)

            # Logica de feedback
            if acusacion_final["asesino"] == ruta_solucion["asesino"]:
                texto_asesino = "Asesino: Correcto"
            else:
                texto_asesino = "Asesino: Incorrecto"

            if acusacion_final["arma"] == ruta_solucion["arma"]:
                texto_arma = "Arma: Correcto"
            else:
                texto_arma = "Arma: Incorrecto"

            if acusacion_final["habitacion"] == ruta_solucion["habitacion"]:
                texto_habitacion = "Habitacion: Correcto"
            else:
                texto_habitacion = "Habitacion: Incorrecto"

            # --- ### CAMBIO: Dibujar el feedback horizontalmente ### ---
            y_feedback = 250  # Misma altura para todos

            # Posicion X 1 (1/4 de la pantalla)
            x_asesino = ANCHO // 5
            dibujar_texto(texto_asesino, fuente_normal, COLOR_BLANCO, pantalla, x_asesino, y_feedback, centrado=True)

            # Posicion X 2 (Centro de la pantalla)
            x_arma = ANCHO // 2
            dibujar_texto(texto_arma, fuente_normal, COLOR_BLANCO, pantalla, x_arma, y_feedback, centrado=True)

            # Posicion X 3 (3/4 de la pantalla)
            x_habitacion = (ANCHO // 5) * 4
            dibujar_texto(texto_habitacion, fuente_normal, COLOR_BLANCO, pantalla, x_habitacion, y_feedback,
                          centrado=True)
            # --- ### FIN CAMBIO ### ---

        # --- Logica de 3 botones horizontales ---
        boton_ancho_final = 300
        boton_alto_final = 50
        boton_espacio_final = 40

        # Ajustar la altura de los botones
        if resultado_final == "Ganaste":
            boton_y_final = 600
        else:
            # Mas abajo para dejar espacio al texto de feedback
            boton_y_final = 600

        total_ancho_final = (boton_ancho_final * 3) + (boton_espacio_final * 2)
        inicio_x_final = (ANCHO - total_ancho_final) // 2

        boton_jdn_x = inicio_x_final
        boton_mp_x = inicio_x_final + boton_ancho_final + boton_espacio_final
        boton_s_x = inicio_x_final + (boton_ancho_final * 2) + (boton_espacio_final * 2)

        boton_jugar_de_nuevo_rect = pygame.Rect(boton_jdn_x, boton_y_final, boton_ancho_final, boton_alto_final)
        boton_menu_principal_rect = pygame.Rect(boton_mp_x, boton_y_final, boton_ancho_final, boton_alto_final)
        boton_salir_rect = pygame.Rect(boton_s_x, boton_y_final, boton_ancho_final, boton_alto_final)

        color_jdn = COLOR_GRIS
        if boton_jugar_de_nuevo_rect.collidepoint(mouse_pos): color_jdn = COLOR_GRIS_CLARO
        pygame.draw.rect(pantalla, color_jdn, boton_jugar_de_nuevo_rect, border_radius=10)

        color_mp = COLOR_GRIS
        if boton_menu_principal_rect.collidepoint(mouse_pos): color_mp = COLOR_GRIS_CLARO
        pygame.draw.rect(pantalla, color_mp, boton_menu_principal_rect, border_radius=10)

        color_s = COLOR_GRIS
        if boton_salir_rect.collidepoint(mouse_pos): color_s = COLOR_GRIS_CLARO
        pygame.draw.rect(pantalla, color_s, boton_salir_rect, border_radius=10)

        dibujar_texto("Jugar de Nuevo", fuente_normal, COLOR_BLANCO, pantalla, boton_jugar_de_nuevo_rect.centerx,
                      boton_jugar_de_nuevo_rect.centery, centrado=True)
        dibujar_texto("Menu Principal", fuente_normal, COLOR_BLANCO, pantalla, boton_menu_principal_rect.centerx,
                      boton_menu_principal_rect.centery, centrado=True)
        dibujar_texto("Salir", fuente_normal, COLOR_BLANCO, pantalla, boton_salir_rect.centerx,
                      boton_salir_rect.centery, centrado=True)
    # --- ### FIN PANTALLA FINAL ACTUALIZADA ### ---

    # --- 8.3. Actualizar la pantalla ---
    pygame.display.flip()

    # --- 8.4. Controlar los FPS ---
    reloj.tick(30)

# --- Salir de Pygame ---
pygame.quit()
sys.exit()