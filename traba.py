import pygame, sys

#Inicialización de Pygame
pygame.init()

# Obtener resolución de pantalla para pantalla completa nativa
info_pantalla = pygame.display.Info()
ANCHO = info_pantalla.current_w
ALTO = info_pantalla.current_h

pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Animación de Caminata con Gravedad")

clock = pygame.time.Clock()

# 2. Cargar y escalar imágenes
try:
    # Escalar imágenes del personaje
    escala = max(1, 200 // 200)

    # Cargar fondo y escalarlo a la pantalla completa
    img_fondo = pygame.image.load("fondo.gif").convert()
    img_fondo = pygame.transform.scale(img_fondo, (ANCHO, ALTO))

    # Cargar imagen de personaje quieto y escalarla
    img_quieto_raw = pygame.image.load("norm_d_r.gif").convert_alpha()
    img_quieto_der = pygame.transform.scale(img_quieto_raw, (img_quieto_raw.get_width() * escala, img_quieto_raw.get_height() * escala))
    img_quieto_izq = pygame.transform.flip(img_quieto_der, True, False) # Para que mire hacia donde estaba caminando

    # Cargar frames de animación
    frames_der_raw = [pygame.image.load(f).convert_alpha() for f in ["c_d1_r.gif", "c_d2_r.gif", "c_d3_r.gif", "c_d4_r.gif"]]
    frames_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["c_i1_r.gif", "c_i2_r.gif", "c_i3_r.gif", "c_i4_r.gif"]]

    puño_der = [pygame.image.load(f).convert_alpha() for f in ["g1_d_r.gif"]]
    puño_izq = [pygame.image.load(f).convert_alpha() for f in ["g1_i_r.gif"]]

    # Cargar imagen de salto y escalarla
    img_salto_raw = pygame.image.load("salt_d_r.gif").convert_alpha()
    img_salto_der = pygame.transform.scale(img_salto_raw, (img_salto_raw.get_width() * escala, img_salto_raw.get_height() * escala))

    # Opcional: Si querés que mire a la izquierda al saltar hacia la izquierda
    img_salto_izq = pygame.transform.flip(img_salto_der, True, False)

    frames_derecha = [
        pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
        for img in frames_der_raw
    ]
    frames_izquierda = [
        pygame.transform.scale(img, (img.get_width() * escala, img.get_height() * escala))
        for img in frames_izq_raw
    ]

except Exception as e:
    print(f"Error imágenes{e}")
    pygame.quit()
    sys.exit()

# 3. Variables del Personaje y Fisicas
ancho_pj = frames_derecha[0].get_width()
alto_pj = frames_derecha[0].get_height()

pos_x = ANCHO // 2 - ancho_pj // 2
suelo_y = ALTO - 120 - alto_pj  # Ajuste equivalente a la altura del piso
pos_y = suelo_y

ancho_hitbox = int(ancho_pj * 0.5)
alto_hitbox = int(alto_pj * 0.8)

# centra la hitbox
offset_x = (ancho_pj - ancho_hitbox) // 2
offset_y = (alto_pj - alto_hitbox) // 2

hb_r = pygame.Rect(pos_x + offset_x, pos_y + offset_y, ancho_hitbox, alto_hitbox)

velocidad_x = 7
velocidad_y = 0
gravedad = 0.6          # Positiva porque crece hacia abajo
potencia_salto = -14     # Negativa para subir
esta_saltando = False

# Variables de animación
mirando_derecha = True
indice_frame = 0
ultimo_cambio = 0
cooldown_animacion = 200

# 4. Game Loop Principal
ejecutando = True

while ejecutando:
    dt = clock.tick(60)  # Limitar a 60 FPS y obtener tiempo delta
    tiempo_actual = pygame.time.get_ticks()

    # --- A. Manejo de Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            if (evento.key == pygame.K_UP or evento.key == pygame.K_SPACE) and not esta_saltando:
                velocidad_y = potencia_salto
                esta_saltando = True

    # --- B. Manejo del Teclado (Movimiento Continuo) ---
    teclas = pygame.key.get_pressed()
    se_mueve = False
    puño = teclas[pygame.K_z]

    if teclas[pygame.K_RIGHT]:
        if pos_x + velocidad_x < ANCHO - ancho_pj:
            pos_x += velocidad_x
        mirando_derecha = True
        se_mueve = True

    if teclas[pygame.K_LEFT]:
        if pos_x - velocidad_x > 0:
            pos_x -= velocidad_x
        mirando_derecha = False
        se_mueve = True

    # --- C. Animación del Personaje ---
    if se_mueve:
        if tiempo_actual - ultimo_cambio > cooldown_animacion:
            indice_frame = (indice_frame + 1) % len(frames_derecha)
            ultimo_cambio = tiempo_actual
    else:
        indice_frame = 0  # Frame de reposo cuando está quieto

    # --- D. Física (Gravedad y Salto) ---
    velocidad_y += gravedad
    pos_y += velocidad_y

    hb_r.x = pos_x + offset_x
    hb_r.height = alto_hitbox
    hb_r.y = pos_y + offset_y

    # Colisión con el piso
    if pos_y >= suelo_y:
        pos_y = suelo_y
        velocidad_y = 0
        esta_saltando = False

    # --- E. Renderizado (Dibujar en pantalla) ---
    pantalla.blit(img_fondo, (0, 0))

    pygame.draw.rect(pantalla, (255, 0, 0), hb_r, 2)

    if esta_saltando:
        frame_actual = img_salto_der if mirando_derecha else img_salto_izq
    elif se_mueve:
        frame_actual = frames_derecha[indice_frame] if mirando_derecha else frames_izquierda[indice_frame]
    elif puño:
        frame_actual = puño_der[0] if mirando_derecha else puño_izq[0]
    else:
        frame_actual = img_quieto_der if mirando_derecha else img_quieto_izq

    # Dibujar al personaje
    pantalla.blit(frame_actual, (pos_x, pos_y))
    pygame.display.flip()

pygame.quit()
sys.exit()