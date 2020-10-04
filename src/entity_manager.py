from random import random
from src.entity import Entity
from typing import List
import pygame

class EntityManager:

    __entitys: List[Entity]

    # Constantes
    WORLD_WIDTH = 600
    WORLD_HEIGHT = 600

    def __init__(self):
        self.__entitys = []

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
        if entity is None:
            w, h = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
            position = [random()*w, random()*h]
            entity = Entity(position, infected=infected)

        # Agregando entidad a la lista de entidades
        self.__entitys.append(entity)

    def draw_and_update(self, screen: pygame.surface.Surface):
        """
        Actualiza y dibuja las entidades en pantalla

        Args:
            screen (pygame.surface.Surface): Superficie donde se va a dibujar.
        """
        for entity in self.__entitys:
            self.__update_entity(entity)

            # Dibujando entidad
            entity.draw(screen)

        # Dibujando linea limite del mundo
        pygame.draw.rect(screen, (132, 132, 132), 
                        (0, 0, self.WORLD_WIDTH, self.WORLD_HEIGHT), width=1)

    def update(self):
        """
        Actualiza todas las entidades
        """
        for entity in self.__entitys:
            self.__update_entity(entity)
    
    def __update_entity(self, entity: Entity):
        """
        Actualiza la entidad ingresada como parametro. También infecta a todas
        las que esta entidad puede infectar.

        Args:
            entity (Entity): Entidad a actualizar.
        """
        # Actualizando entidad
        entity.step()

        # Definiendo nueva posicion objetivo de la entidad
        if entity.is_target_done():
            w, h = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
            position = [random()*w, random()*h]
            entity.set_target_position(position)

        # Infectando otras entidades
        #* OPTIMIZE: Colocar aquí el mágico quadtree
        for other_entity in self.__entitys:
            entity.infect(other_entity)
    
    

