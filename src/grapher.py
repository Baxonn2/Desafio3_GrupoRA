import pygame
from random import random
from src.entity import Entity
from src.entity_manager import EntityManager
from src.chart import Chart, Data
from typing import List


class Grapher:

    __done: bool
    __screen: pygame.surface.Surface

    __entity_manager: EntityManager

    # Constantes
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600

    def __init__(self):
        # Creando manager de entidades
        self.__entity_manager = EntityManager()

        # Inicializando graficador
        self.__done = False
        pygame.init()

        # Configurando ventana
        self.__screen = pygame.display.set_mode((self.SCREEN_WIDTH, 
                                                self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pandemic Simulator")

        self.__clock = pygame.time.Clock()

        # Agregando graficos
        self.chart1 = Chart((600, 10), (300, 100))
        self.chart2 = Chart((600, 150), (300, 100))

    def add_entity(self, entity: Entity = None, infected: bool = False):
        """
        Agrega una nueva entidad al manager de entidades

        Args:
            entity (Entity, optional): Nueva entidad a agregar. Si no se define
                                       esta entidad se creara una con parametros
                                       aleatorios.
            infected (bool, optional): Establece si la entidad esta o no
                                       infectada. Por defecto es False.
        """
        self.__entity_manager.add_entity(entity, infected=infected)

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
            
    def _draw_and_update(self):
        """
        Dibuja y actualiza todo lo que está dentro de graficador
        """
        self.__screen.fill((33, 33, 33))
        self.__clock.tick(60)

        # Dibujando y actualizando entidades
        self.__entity_manager.draw_and_update(self.__screen)

        # Dibujando y actualizando graficoS
        cantidad_update = self.__entity_manager.get_update_count()
        if cantidad_update % 10 == 0:
            self.chart1.add(Data(cantidad_update, self.__entity_manager.get_infected()))
            fps = int(self.__clock.get_fps())
            self.chart2.add(Data(cantidad_update, fps))
        self.chart1.draw(self.__screen)
        self.chart2.draw(self.__screen)

        pygame.display.update()