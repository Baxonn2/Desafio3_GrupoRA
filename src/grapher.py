import pygame
from src.entity import Entity
from src.population import Population
from src.chart import Chart, Data
from .parameters.status import STATUS_COLORS


class Grapher:
    __done: bool
    __screen: pygame.surface.Surface

    __entity_manager: Population

    # Constantes
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600

    def __init__(self, algorithm='quadtree', quarantine_enabled=True):
        # Creando manager de entidades
        self.__entity_manager = Population(algorithm=algorithm,
                                           quarantine_enabled=quarantine_enabled)
        self.algorithm = algorithm

        # Inicializando graficador
        self.__done = False
        pygame.init()

        # Configurando ventana
        self.__screen = pygame.display.set_mode((self.SCREEN_WIDTH,
                                                 self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pandemic Simulator")

        self.__clock = pygame.time.Clock()

        # Agregando graficos
        self.chart1 = Chart([600, 10], [300, 100])
        self.chart2 = Chart([600, 150], [300, 100])

    def add_entities(self, population, infected, masks=0, quarantine=None):
        """
        Agrega la cantidad de entidades solicitadas
        :param quarantine: Habilita o deshabilita la cuarentena en la poblacion
        :param population: Cantidad de entidades totales sanos + infectados
        :param infected: Cantidad de entidades infectadas
        :param masks: Probabilidad de que una entidad use mascarilla
        """
        self.__entity_manager.add_entities(population, infected, masks,
                                           quarantine)

    def run(self):
        """
        Bucle del graficador. Es necesario correr esta funcion para que el
        graficador funcione.
        """
        while not self.__done:
            # Actualizando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__done = True
                    break

            # Actualizando pantalla
            self._draw_and_update()

    #  Metodo de dibujo protegido
    def _draw_and_update(self):
        """
        Dibuja y actualiza todos los elementos dentro del graficador
        """
        self.__screen.fill((33, 33, 33))
        self.__clock.tick(60)

        # Dibujando y actualizando entidades
        self.__draw_population()
        # Dibujando y actualizando graficoS
        cantidad_update = self.__entity_manager.get_update_count()
        if cantidad_update % 10 == 0:
            self.chart1.add(Data(cantidad_update, self.__entity_manager.get_infected()))
            fps = int(self.__clock.get_fps())
            self.chart2.add(Data(cantidad_update, fps))
        self.chart1.draw(self.__screen)
        self.chart2.draw(self.__screen)

        # cuarentena
        pygame.draw.rect(self.__screen, (255, 0, 0),
                         pygame.Rect(self.SCREEN_WIDTH * 0.7,
                                     self.SCREEN_HEIGHT * 0.5,
                                     self.SCREEN_WIDTH * 0.26,
                                     self.SCREEN_HEIGHT * 0.4), 2)
        # Texto de cuarentena. (Este texto causa el loading del principio)
        self.__screen.blit(pygame.font.SysFont(None, 32).render('Quarentine Zone', True, (255,0,0)), (self.SCREEN_WIDTH*0.73,self.SCREEN_HEIGHT*0.91))

        pygame.display.update()

    # Metodos de dibujo privados

    def __draw_population(self):
        """
        Dibuja la poblacion y la actualiza
        """
        for entity in self.__entity_manager.entities:
            self.__entity_manager.update_entity(entity)
            # Dibujando entidad
            self.__draw_entity(entity)
        self.__entity_manager.update()

    def __draw_entity(self, entity: Entity):
        """
        Dibuja la entidad seleccionada.

        :param entity: Entidad seleccionada
        """
        status, infecting, position, radius = entity.get_status()

        if infecting:
            pygame.draw.circle(self.__screen, STATUS_COLORS[status],
                               position, int(radius))
        pygame.draw.circle(self.__screen, STATUS_COLORS[status], position, 2)
