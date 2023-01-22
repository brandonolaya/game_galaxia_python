import pygame
import random
import math
from pygame import mixer
import io


def fuente_bytes(fuente):
    with open(fuente, 'rb') as f:
        otf_bytes = f.read()
    return io.BytesIO(otf_bytes)



pygame.init()#inicializo pygame para traer todas sus herramientas

#Disply es para mostrar
pantalla = pygame.display.set_mode((900, 600))#crea la pantalla y le da tamaño que quiero que muestre

#titulo icono fondo
pygame.display.set_caption('Espaciales') # nombre que tendra el juego
icono = pygame.image.load("iconos/ovni-volando.png")#cargo la imagen a una variable
pygame.display.set_icon(icono) # cambio el icono al que deseo
fondo = pygame.image.load("imagenes/127957.jpeg")


#muscia
mixer.music.load('song/Musica-Kevin-MacLeod-Broken-Reality.mp3')
mixer.music.set_volume(0.6)
mixer.music.play(-1)


img_jugador = pygame.image.load("iconos/nave-espacial.png") #cargo la imagen del personaje principal au una variable
#seran la posicion donde ubico a mi jugador
jugador_x= 418
jugador_y=520
jugador_x_movimiento = 0
jugador_y_movimiento = 0


#enemigo
img_enemigo = []
enemigo_x= []
enemigo_y= []
enemigo_x_movimiento = []
enemigo_y_movimiento = []
cantidad_enemigo = 7



#bala
img_bala = pygame.image.load('iconos/bala.png')
bala_x= 0
bala_y= 500
bala_x_movimiento = 0
bala_y_movimiento = 5
bala_visible = False #oculta la imagen


#puntaje
puntaje = 0
# freesansboldes el unico tipo de fuente gratuita incorporada en pygame
#pero se la cambio por otra
fuente_como_bytes = fuente_bytes('funts/SKY BRIDGE.otf')
fuente = pygame.font.Font(fuente_como_bytes, 30)
texto_x = 10
texto_y = 10


#texto final de juego
fuente_final = pygame.font.Font(fuente_como_bytes, 45)





def texto_final():
    my_final = fuente_final.render("SOOS UN PERDEDOR", True, (255, 255, 255))
    pantalla.blit(my_final, (200,250))



#motrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255,255,255))#render es imprimir en pantalla no consola
    pantalla.blit(texto, (x,y))



def disparar_bala(x, y):
    global bala_visible
    bala_visible = True #permite la visibilidad de la imagen
    pantalla.blit(img_bala, (x + 16, y + 16))


def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y)) # la bala es de 32 px y la nave de 64 px esto para que quede centrado


def jugador(x, y):
    #blit es como arrojar, le pasa la info de la imagen y la pisicion
    pantalla.blit(img_jugador,(x, y))


#colicion
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False



for e in range(cantidad_enemigo):
    img_enemigo.append(pygame.image.load("iconos/ovni .png"))  #cargo la imagen del personaje principal au una variable
    #seran la posicion donde ubico a mi jugador
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,150))
    enemigo_x_movimiento.append(2)
    enemigo_y_movimiento.append(35)


ejecutar = True
#Todo lo que se actualice dentro del juego debe de quedar en el loop
while ejecutar:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get(): # revista todos lo eventos que suceden dentro de la pantalla
        if evento.type == pygame.QUIT: # cuando uno le ta a la X de cerrara entra para que este pueda cerrar la pantalla
            ejecutar = False

        #mira se se preciono una tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                jugador_x_movimiento = -3
            if evento.key == pygame.K_d:
                jugador_x_movimiento = 3
            if evento.key == pygame.K_s:
                jugador_y_movimiento = 3
            if evento.key == pygame.K_w:
                jugador_y_movimiento = -3
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    sonido_bala = mixer.Sound('song/disparo_1.mp3')
                    sonido_bala.set_volume(0.2)
                    sonido_bala.play()
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        #mira la tecla sea soltado
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_a or evento.key == pygame.K_d:
                jugador_x_movimiento = 0
            if evento.key == pygame.K_s or evento.key == pygame.K_w:
                jugador_y_movimiento = 0

    #bordes del jugador
    if jugador_x<=0:
        jugador_x = 1
    elif jugador_x >= 830:
        jugador_x = 830

    if jugador_y <= 200:
        jugador_y = 200
    elif jugador_y >= 530:
        jugador_y = 530

    #movimiento jugador
    jugador_x += jugador_x_movimiento
    jugador_y += jugador_y_movimiento





    #movimiento enemigo
    for e in range(cantidad_enemigo):

        if enemigo_y[e] > 530:## para que cuando toque casi donde inicio la nave se acabe el juego
            for k in range(cantidad_enemigo):
                enemigo_y[k] = 700
            texto_final()
            break

        enemigo_x[e] += enemigo_x_movimiento[e]
        #movimiento enemigo
        if enemigo_x[e]<=0:
            enemigo_x_movimiento[e] = 1.5
            enemigo_y[e] += enemigo_y_movimiento[e]
        elif enemigo_x[e] >= 830:
            enemigo_x_movimiento[e] = -1.5
            enemigo_y[e] += enemigo_y_movimiento[e]

        #colicion
        colicion = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colicion:
            sonido_colicion = mixer.Sound('song/massive-thump-116359.mp3')
            sonido_colicion.play()
            bala_y = jugador_y
            bala_visible = False
            puntaje += 1
            enemigo_x[e]= random.randint(0,736)
            enemigo_y[e]= random.randint(50,150)
        enemigo(enemigo_x[e],enemigo_y[e], e)

    #movimiento bala
    if bala_y <= -32:
        bala_y = jugador_y
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_movimiento



    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()#actualiza la pantalla o los eventos anteriores para cargarlos