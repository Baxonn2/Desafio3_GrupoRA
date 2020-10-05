import pygame
from random import random
from src.entity import Entity
from src.entity_manager import EntityManager
from typing import List


class Grapher:

    __done: bool
    __screen: pygame.surface.Surface

    __entity_manager: EntityManager

    # Constantes
    SCREEN_WIDTH = 600
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

        # Dibujando y actualizando entidades
        self.__entity_manager.draw_and_update(self.__screen)

        
        pygame.display.update()