import pygame, sys

pygame.init()

info_pantalla = pygame.display.Info()
ANCHO = info_pantalla.current_w
ALTO = info_pantalla.current_h

pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption("Animación de Dos Personajes con Gravedad")

clock = pygame.time.Clock()

try:
    escala = 0.25
    escrf = 0.15

    img_fondo = pygame.image.load("fondo.gif").convert()
    img_fondo = pygame.transform.scale(img_fondo, (ANCHO, ALTO))

    # ==========================================
    # PERSONAJE 1 (Usa las mismas imágenes originales)
    # ==========================================
    img_q1_raw = pygame.image.load("pr.gif").convert_alpha()
    img_q1_izq = pygame.transform.scale(img_q1_raw, (int(img_q1_raw.get_width() * escrf), int(img_q1_raw.get_height() * escrf)))
    img_q1_der = pygame.transform.flip(img_q1_izq, True, False)

    f1_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["c1r.gif", "c2r.gif"]]
    frames_caminar_1_izq = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in f1_izq_raw]
    frames_caminar_1_der = [pygame.transform.flip(img, True, False) for img in frames_caminar_1_izq]

    p1_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["p1r.gif", "p2r.gif"]]
    frames_puño_1_izq = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in p1_izq_raw]
    frames_puño_1_der = [pygame.transform.flip(img, True, False) for img in frames_puño_1_izq]

    s1_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["s1r.gif", "s2r.gif", "s3r.gif", "s2r.gif", "s1r.gif"]]
    frames_salto_1_izq = [pygame.transform.scale(img, (int(img.get_width() * escala), int(img.get_height() * escala))) for img in s1_izq_raw]
    frames_salto_1_der = [pygame.transform.flip(img, True, False) for img in frames_salto_1_izq]

    # ==========================================
    # PERSONAJE 2 (Roles intercambiados en Caminata, Salto y Puño)
    # ==========================================
    escalm = 0.2
    escrm = 0.1
    img_q2_raw = pygame.image.load("pr.gif").convert_alpha()  
    img_q2_izq = pygame.transform.scale(img_q2_raw, (int(img_q2_raw.get_width() * escrm), int(img_q2_raw.get_height() * escrm)))
    img_q2_der = pygame.transform.flip(img_q2_izq, True, False)

    # Caminata P2 (intercambiados)
    f2_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["c1m.gif", "c2m.gif"]]  
    frames_caminar_2_izq = [
        pygame.transform.flip(
            pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))), 
            True, False
        ) for img in f2_izq_raw
    ]
    frames_caminar_2_der = [
        pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))) 
        for img in f2_izq_raw
    ]

    # Puño P2 (intercambiados)
    p2_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["p1m.gif"]]  
    frames_puño_2_izq = [
        pygame.transform.flip(
            pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))), 
            True, False
        ) for img in p2_izq_raw
    ]
    frames_puño_2_der = [
        pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))) 
        for img in p2_izq_raw
    ]

    # Salto P2 (intercambiados)
    s2_izq_raw = [pygame.image.load(f).convert_alpha() for f in ["s1m.gif", "s2m.gif", "s1m.gif"]]  
    frames_salto_2_izq = [
        pygame.transform.flip(
            pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))), 
            True, False
        ) for img in s2_izq_raw
    ]
    frames_salto_2_der = [
        pygame.transform.scale(img, (int(img.get_width() * escalm), int(img.get_height() * escalm))) 
        for img in s2_izq_raw
    ]

except Exception as e:
    print(f"Error cargando imágenes: {e}")
    pygame.quit()
    sys.exit()

ancho_pj1 = frames_caminar_1_der[0].get_width()
alto_pj1 = frames_caminar_1_der[0].get_height()
suelo_y1 = ALTO - 120 - alto_pj1  

ancho_pj2 = frames_caminar_2_der[0].get_width()
alto_pj2 = frames_caminar_2_der[0].get_height()
suelo_y2 = ALTO - 120 - alto_pj2  

p1 = {
    "x": ANCHO // 3 - ancho_pj1 // 2,
    "y": suelo_y1,
    "vel_y": 0,
    "salto": False,
    "mirando_der": True,
    "ind_frame": 0,
    "ult_cambio": 0,
    "cooldown": 200,
    "ind_salto": 0,
    "ult_cambio_salto": 0,
    "cooldown_salto": 100,
    "golpeando": False,
    "ind_puño": 0,
    "ult_cambio_puño": 0,
    "cooldown_puño": 80,
    "offset_suelo": 25,
    "hb": pygame.Rect(0, 0, 0, 0)
}

p2 = {
    "x": (ANCHO // 3) * 2 - ancho_pj2 // 2,
    "y": suelo_y2,
    "vel_y": 0,
    "salto": False,
    "mirando_der": False,
    "ind_frame": 0,
    "ult_cambio": 0,
    "cooldown": 200,
    "ind_salto": 0,
    "ult_cambio_salto": 0,
    "cooldown_salto": 100,
    "golpeando": False,
    "ind_puño": 0,
    "ult_cambio_puño": 0,
    "cooldown_puño": 80,
    "offset_suelo": 25,
    "hb": pygame.Rect(0, 0, 0, 0)
}

velocidad_x = 7
gravedad = 0.6            
potencia_salto = -14    

ejecutando = True

while ejecutando:
    clock.tick(60)  
    tiempo_actual = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                ejecutando = False
            
            if (evento.key == pygame.K_w) and not p1["salto"]:
                p1["vel_y"] = potencia_salto
                p1["salto"] = True
                p1["ind_salto"] = 0  
                p1["ult_cambio_salto"] = tiempo_actual
            
            if evento.key == pygame.K_z and not p1["golpeando"]:
                p1["golpeando"] = True
                p1["ind_puño"] = 0
                p1["ult_cambio_puño"] = tiempo_actual

            if evento.key == pygame.K_UP and not p2["salto"]:
                p2["vel_y"] = potencia_salto
                p2["salto"] = True
                p2["ind_salto"] = 0  
                p2["ult_cambio_salto"] = tiempo_actual
            
            if evento.key == pygame.K_KP0 and not p2["golpeando"]:
                p2["golpeando"] = True
                p2["ind_puño"] = 0
                p2["ult_cambio_puño"] = tiempo_actual

    teclas = pygame.key.get_pressed()
    
    se_mueve_p1 = False
    if teclas[pygame.K_d]:
        if p1["x"] + velocidad_x < ANCHO - ancho_pj1:
            p1["x"] += velocidad_x
        p1["mirando_der"] = True
        se_mueve_p1 = True
    if teclas[pygame.K_a]:
        if p1["x"] - velocidad_x > 0:
            p1["x"] -= velocidad_x
        p1["mirando_der"] = False
        se_mueve_p1 = True

    se_mueve_p2 = False
    if teclas[pygame.K_RIGHT]:
        if p2["x"] + velocidad_x < ANCHO - ancho_pj2:
            p2["x"] += velocidad_x
        p2["mirando_der"] = True
        se_mueve_p2 = True
    if teclas[pygame.K_LEFT]:
        if p2["x"] - velocidad_x > 0:
            p2["x"] -= velocidad_x
        p2["mirando_der"] = False
        se_mueve_p2 = True

    if se_mueve_p1:
        if tiempo_actual - p1["ult_cambio"] > p1["cooldown"]:
            p1["ind_frame"] = (p1["ind_frame"] + 1) % len(frames_caminar_1_der)
            p1["ult_cambio"] = tiempo_actual
    else:
        p1["ind_frame"] = 0  

    if se_mueve_p2:
        if tiempo_actual - p2["ult_cambio"] > p2["cooldown"]:
            p2["ind_frame"] = (p2["ind_frame"] + 1) % len(frames_caminar_2_der)
            p2["ult_cambio"] = tiempo_actual
    else:
        p2["ind_frame"] = 0  

    p1["vel_y"] += gravedad
    p1["y"] += p1["vel_y"]
    if p1["y"] >= suelo_y1:
        p1["y"] = suelo_y1
        p1["vel_y"] = 0
        p1["salto"] = False

    p2["vel_y"] += gravedad
    p2["y"] += p2["vel_y"]
    if p2["y"] >= suelo_y2:
        p2["y"] = suelo_y2
        p2["vel_y"] = 0
        p2["salto"] = False

    pantalla.blit(img_fondo, (0, 0))

    dib_puño_1 = False
    if p1["salto"]:
        if tiempo_actual - p1["ult_cambio_salto"] > p1["cooldown_salto"]:
            if p1["ind_salto"] < len(frames_salto_1_der) - 1:
                p1["ind_salto"] += 1  
            p1["ult_cambio_salto"] = tiempo_actual
        frame_p1 = frames_salto_1_der[p1["ind_salto"]] if p1["mirando_der"] else frames_salto_1_izq[p1["ind_salto"]]
    elif p1["golpeando"]:
        if tiempo_actual - p1["ult_cambio_puño"] > p1["cooldown_puño"]:
            p1["ind_puño"] += 1
            if p1["ind_puño"] >= len(frames_puño_1_der):
                p1["golpeando"] = False  
                p1["ind_puño"] = 0
            p1["ult_cambio_puño"] = tiempo_actual
        if p1["golpeando"]:
            frame_p1 = frames_puño_1_der[p1["ind_puño"]] if p1["mirando_der"] else frames_puño_1_izq[p1["ind_puño"]]
            dib_puño_1 = True
        else:
            frame_p1 = img_q1_der if p1["mirando_der"] else img_q1_izq
    elif se_mueve_p1:
        frame_p1 = frames_caminar_1_der[p1["ind_frame"]] if p1["mirando_der"] else frames_caminar_1_izq[p1["ind_frame"]]
    else:
        frame_p1 = img_q1_der if p1["mirando_der"] else img_q1_izq

    dib_puño_2 = False
    if p2["salto"]:
        if tiempo_actual - p2["ult_cambio_salto"] > p2["cooldown_salto"]:
            if p2["ind_salto"] < len(frames_salto_2_der) - 1:
                p2["ind_salto"] += 1  
            p2["ult_cambio_salto"] = tiempo_actual
        frame_p2 = frames_salto_2_der[p2["ind_salto"]] if p2["mirando_der"] else frames_salto_2_izq[p2["ind_salto"]]
    elif p2["golpeando"]:
        if tiempo_actual - p2["ult_cambio_puño"] > p2["cooldown_puño"]:
            p2["ind_puño"] += 1
            if p2["ind_puño"] >= len(frames_puño_2_der):
                p2["golpeando"] = False  
                p2["ind_puño"] = 0
            p2["ult_cambio_puño"] = tiempo_actual
        if p2["golpeando"]:
            frame_p2 = frames_puño_2_der[p2["ind_puño"]] if p2["mirando_der"] else frames_puño_2_izq[p2["ind_puño"]]
            dib_puño_2 = True
        else:
            frame_p2 = img_q2_der if p2["mirando_der"] else img_q2_izq
    elif se_mueve_p2:
        frame_p2 = frames_caminar_2_der[p2["ind_frame"]] if p2["mirando_der"] else frames_caminar_2_izq[p2["ind_frame"]]
    else:
        frame_p2 = img_q2_der if p2["mirando_der"] else img_q2_izq

    pos_dibujo_y1 = p1["y"] - (frame_p1.get_height() - alto_pj1) + p1["offset_suelo"] if dib_puño_1 else p1["y"]
    pos_dibujo_y2 = p2["y"] - (frame_p2.get_height() - alto_pj2) + p2["offset_suelo"] if dib_puño_2 else p2["y"]

    ancho_ac1, alto_ac1 = frame_p1.get_width(), frame_p1.get_height()
    hb_w1, hb_h1 = int(ancho_ac1 * 0.6), int(alto_ac1 * 1)
    p1["hb"].x = p1["x"] + (ancho_ac1 - hb_w1) // 2
    p1["hb"].y = pos_dibujo_y1 + (alto_ac1 - hb_h1) // 2
    p1["hb"].width = hb_w1
    p1["hb"].height = hb_h1

    ancho_ac2, alto_ac2 = frame_p2.get_width(), frame_p2.get_height()
    hb_w2, hb_h2 = int(ancho_ac2 * 0.6), int(alto_ac2 * 1)
    p2["hb"].x = p2["x"] + (ancho_ac2 - hb_w2) // 2
    p2["hb"].y = pos_dibujo_y2 + (alto_ac2 - hb_h2) // 2
    p2["hb"].width = hb_w2
    p2["hb"].height = hb_h2

    pantalla.blit(frame_p1, (p1["x"], pos_dibujo_y1))
    pygame.draw.rect(pantalla, (255, 0, 0), p1["hb"], 2)

    pantalla.blit(frame_p2, (p2["x"], pos_dibujo_y2))
    pygame.draw.rect(pantalla, (0, 0, 255), p2["hb"], 2)
    
    pygame.display.flip()

pygame.quit()
sys.exit()