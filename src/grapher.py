import pygame
from random import random
from src.entity import Entity
from typing import List

class Grapher:

    _entitys: List[Entity]

    _done: bool
    _screen: pygame.surface.Surface

    # Constantes
    SCREEN_WIDTH = 900
    SCREEN_HEIGHT = 600

    WORLD_WIDTH = 600
    WORLD_HEIGHT = 600

    def __init__(self):
        # Creando lista de entidades
        self._entitys = []

        # Inicializando graficador
        self._done = False
        pygame.init()

        # TODO: hacer una configuración global de esto si es necesario
        self._screen = pygame.display.set_mode((self.SCREEN_WIDTH, 
                                                self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pandemic Simulator")

    def add_entity(self, entity: Entity = None, infected: bool = False):
        if entity is None:
            w, h = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
            position = [random()*w, random()*h]
            entity = Entity(position, infected=infected)

        # Agregando entidad a la lista de entidades
        self._entitys.append(entity)

    def run(self):
        while not self._done:
            # Actualizando eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._done = True
                    break
            
            # Actualizando pantalla
            self._draw_and_update()
            
    def _draw_and_update(self):
        self._screen.fill((33, 33, 33))

        # Dibujando 
        for entity in self._entitys:
            entity.step()

            if entity.is_target_done():
                w, h = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
                position = [random()*w, random()*h]
                entity.set_target_position(position)

            #* OPTIMIZE: Colocar aquí el mágico quadtree
            for other_entity in self._entitys:
                entity.infect(other_entity)

            entity.draw(self._screen)


        # Dibujando linea limite del mundo
        pygame.draw.rect(self._screen, (255, 255, 255), 
                        (0, 0, self.WORLD_WIDTH, self.WORLD_HEIGHT), width=1)
        pygame.display.update()