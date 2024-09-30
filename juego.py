import pygame
import random

# Inicializar Pygame
pygame.init()

# Definir los colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Dimensiones de la ventana
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Juego para niños - Evita los bloques")

# Función para mostrar el menú principal
def menu_principal():
    while True:
        pantalla.fill(BLANCO)
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("Juego - Evita los bloques", True, NEGRO)
        pantalla.blit(texto, (50, 250))
        
        fuente = pygame.font.Font(None, 36)
        instrucciones = fuente.render("Presiona ENTER para jugar", True, NEGRO)
        pantalla.blit(instrucciones, (200, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return

# Clase para el jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(AZUL)
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO_PANTALLA // 2, ALTO_PANTALLA - 50)

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO_PANTALLA:
            self.rect.right = ANCHO_PANTALLA

# Clase para los bloques que caen
class Bloque(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
        self.rect.y = random.randint(-100, -50)
        self.velocidad_y = random.randint(3, 6)

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.top > ALTO_PANTALLA:
            self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
            self.rect.y = random.randint(-100, -50)
            self.velocidad_y = random.randint(3, 6)

# Clase para los enemigos
class Enemigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([50, 50])
        self.image.fill((255, 165, 0))  # Naranja
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO_PANTALLA - 50)
        self.rect.y = random.randint(0, ALTO_PANTALLA // 2)
        self.velocidad_x = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.velocidad_x
        if self.rect.left < 0 or self.rect.right > ANCHO_PANTALLA:
            self.velocidad_x *= -1  # Cambiar dirección

# Crear grupos de sprites
jugador = Jugador()
bloques = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
todos_los_sprites = pygame.sprite.Group()

todos_los_sprites.add(jugador)

for i in range(10):
    bloque = Bloque()
    bloques.add(bloque)
    todos_los_sprites.add(bloque)

for i in range(5):  # Crear 5 enemigos
    enemigo = Enemigo()
    enemigos.add(enemigo)
    todos_los_sprites.add(enemigo)

# Reloj para controlar la velocidad de actualización
reloj = pygame.time.Clock()

# Mostrar el menú principal
menu_principal()

# Ciclo principal del juego
jugando = True
while jugando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jugando = False

    todos_los_sprites.update()

    # Detectar colisiones
    if pygame.sprite.spritecollide(jugador, bloques, False) or pygame.sprite.spritecollide(jugador, enemigos, False):
        jugando = False

    pantalla.fill(BLANCO)
    todos_los_sprites.draw(pantalla)
    pygame.display.flip()

    reloj.tick(60)

pygame.quit()
