import pygame, sys
from pygame.locals import *

#numero de frames por segundo
FPS = 200

#variables globales que usaremos durante el juego

anchoVentana = 400
alturaVentana = 300
grosorLinea = 10
tamRaqueta = 50
compensarRaqueta = 20
#colores rgb
azul = (0,0,255)
negro = (0,0,0)
blanco = (255,255,255)
verde = (127,255,0)

def dibujarPantalla():
    """ metodo para dibujar nuestra pantalla de juego """
    pantalla.fill((154,50,205))
    #dibujamos el contorno
    pygame.draw.rect(pantalla,azul,((0,0),(anchoVentana,alturaVentana)),grosorLinea*2)
    #dibujamos la linea central
    pygame.draw.line(pantalla,azul,((anchoVentana//2),0),((anchoVentana//2),alturaVentana),(grosorLinea//2))



def dibujarRaqueta(raqueta):
    """ metodo para dibujar la raqueta """
    # no dejamos pasar la pala por fuera del eje de abajo, ni de arriba
    if raqueta.bottom > alturaVentana - grosorLinea:
        raqueta.bottom = alturaVentana - grosorLinea
    elif raqueta.top < grosorLinea:
        raqueta.top = grosorLinea
    #dibujamos la linea
    pygame.draw.rect(pantalla,verde,raqueta)


def dibujarPelota(pelota):
    """metodo para dibujar la pelota"""
    pygame.draw.rect(pantalla,blanco,pelota)

def moverPelota(pelota,dirPelotaX,dirPelotaY):
    """mueve la pelota y devuelve nueva posicion"""
    pelota.x += dirPelotaX
    pelota.y += dirPelotaY
    return pelota

def colisionBorde(pelota,dirPelotaX,dirPelotaY):
    """ metodo para cambiar la direccion cuando la plota choca con el borde"""
    if pelota.top == (grosorLinea) or pelota.bottom == (alturaVentana -grosorLinea):
        dirPelotaY = dirPelotaY * -1
    if pelota.left == (grosorLinea) or pelota.right == (anchoVentana - grosorLinea):
        dirPelotaX = dirPelotaX * -1
    return dirPelotaX,dirPelotaY

def golpearPelota (pelota, raqueta1,raqueta2,dirPelotaX):
    """ devuelve menos 1 cando choca con las raquetas """
    if dirPelotaX == -1 and raqueta1.right == pelota.left and raqueta1.top <= pelota.top and raqueta1.bottom >= pelota.bottom:
        return -1
    elif dirPelotaX == 1 and raqueta2.left == pelota.right and raqueta2.top < pelota.top and raqueta2.bottom > pelota.bottom:
        return -1
    else :
        return 1

def puntuacion(raqueta1,pelota,score,dirPelotaX):
    """metodo que nos calcula la puntuacion"""
    if pelota.left == grosorLinea:
        return 0
    elif dirPelotaX == -1 and raqueta1.right == pelota.left and raqueta1.top < pelota.top and raqueta1.bottom > pelota.bottom:
        score+=1
        return score
    elif pelota.right == anchoVentana - grosorLinea:
        score+=5
        return score
    else :
        return score

def mostrarScore (score):
    """metodo para mostrar la puntuacion en pantalla """
    rS = fuente.render ('Score = %s' %(score),True,blanco)
    rR = rS.get_rect()
    rR.topleft = (anchoVentana-150,25)
    pantalla.blit(rS,rR)

def movimientoPc(pelota,dirPelotaX,raqueta2):
    """metodo para mover la pala del pc"""
    # si la bola se mueve fuera de la raqueta
    if dirPelotaX == -1 :
        if raqueta2.centery < (alturaVentana//2):
            raqueta2.y += 1
        elif raqueta2.centery > (alturaVentana//2):
            raqueta2.y -= 1
    # si la pelota va direccion a la raqueta
    elif dirPelotaX == 1 :
        if raqueta2.centery < pelota.centery:
            raqueta2.y += 1
        else :
            raqueta2.y -= 1
    return raqueta2



def main():
    pygame.init()
    global pantalla

    #fuente
    global fuente, tamFuente
    tamFuente = 20
    fuente = pygame.font.Font('freesansbold.ttf',tamFuente)

    reloj = pygame.time.Clock()

    pantalla = pygame.display.set_mode((anchoVentana,alturaVentana))
    pygame.display.set_caption('Pong')
    pygame.mouse.set_visible(False)
    #creamos  las variables para las posiciones
    pelotaX = anchoVentana//2 -grosorLinea//2
    pelotaY = alturaVentana//2 - grosorLinea//2
    posicionJug1 = (alturaVentana - tamRaqueta)//2
    posicionJug2 = (alturaVentana - tamRaqueta)//2
    score = 0
    #direccion pelota
    dirPelotaX = -1
    dirPelotaY = -1
    # creamos raquetas y pelota
    raqueta1 = pygame.Rect(compensarRaqueta,posicionJug1,grosorLinea,tamRaqueta)
    raqueta2 = pygame.Rect(anchoVentana - compensarRaqueta - grosorLinea,posicionJug2,grosorLinea,tamRaqueta)
    pelota = pygame.Rect(pelotaX,pelotaY,grosorLinea,grosorLinea)
    #dibujamos posicion inicial
    dibujarPantalla()
    dibujarRaqueta(raqueta1)
    dibujarRaqueta(raqueta2)
    dibujarPelota(pelota)

    while True:
        #control de eventos y movimiento
        for event in pygame.event.get ():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN :   #movimiento teclas
                if event.key == pygame.K_UP:
                    raqueta1.y += -40
                if event.key == pygame.K_DOWN:
                    raqueta1.y +=  40
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    raqueta1.y += 0
                if event.key == pygame.K_UP:
                    raqueta1.y += 0

        #dibujar
        dibujarPantalla()
        dibujarRaqueta(raqueta1)
        dibujarRaqueta(raqueta2)
        dibujarPelota(pelota)

        #ejecutar movimientos
        pelota=moverPelota(pelota,dirPelotaX,dirPelotaY)
        dirPelotaX,dirPelotaY = colisionBorde(pelota,dirPelotaX,dirPelotaY)
        score = puntuacion (raqueta1,pelota,score,dirPelotaX)
        dirPelotaX = dirPelotaX * golpearPelota (pelota,raqueta1,raqueta2,dirPelotaX)
        raqueta2 = movimientoPc (pelota,dirPelotaX,raqueta2)


        mostrarScore(score)

        pygame.display.update()
        reloj.tick(FPS)
