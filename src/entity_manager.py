from random import random
from src.entity import Entity
from src.quadtree import Node
from typing import List
import pygame

class EntityManager:

    __entitys: List[Entity]
    __infected_entitys: List[Entity]
    __healthy_entitys: List[Entity]

    __update_count: int

    # Constantes
    WORLD_WIDTH = 600
    WORLD_HEIGHT = 600

    def __init__(self):
        self.__entitys = []
        self.__infected_entitys = []
        self.__healthy_entitys = []

        self.__update_count = 0

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

        if entity.is_infected():
            self.__infected_entitys.append(entity)
        else:
            self.__healthy_entitys.append(entity)

    def draw_and_update(self, screen: pygame.surface.Surface):
        """
        Actualiza y dibuja las entidades en pantalla

        Args:
            screen (pygame.surface.Surface): Superficie donde se va a dibujar.
        """
        self.__update_count += 1
        for entity in self.__entitys:
            self.__update_entity(entity)

            # Dibujando entidad
            entity.draw(screen)

        # Buscando infectados
        quadtree = Node(self.WORLD_WIDTH/2, self.WORLD_HEIGHT/2,
                        self.WORLD_WIDTH/2, self.WORLD_HEIGHT/2, 4)
        for entity in self.__healthy_entitys:
            quadtree.insert(entity)

        now_infected = []
        for infected_entity in self.__infected_entitys:
            x, y = infected_entity.get_position()
            radius = Entity.INFECT_RADIO
            presition = 0.1
            entitys = quadtree.points_within_radius(x, y, radius, presition)
            for healthy_entity in entitys:
                infected_entity.infect(healthy_entity)

                if healthy_entity.is_infected():
                    try:
                        self.__healthy_entitys.remove(healthy_entity)
                        now_infected.append(healthy_entity)
                    except:
                        print("Exception")
                        pass
                    
        for infected in now_infected:
            self.__infected_entitys.append(infected)

    def update(self):
        """
        Actualiza todas las entidades
        """
        self.__update_count += 1
        for entity in self.__entitys:
            self.__update_entity(entity)

        # TODO: agregar la funcionalidad del quadtree aqui
    
    def __update_entity(self, entity: Entity):
        """
        Actualiza la entidad ingresada como parametro. También infecta a todas
        las que esta entidad puede infectar.

        Args:
            entity (Entity): Entidad a actualizar.
        """
        # Actualizando entidad
        was_infected = entity.is_infected()
        entity.step()

        # Definiendo nueva posicion objetivo de la entidad
        if entity.is_target_done():
            w, h = (self.WORLD_WIDTH, self.WORLD_HEIGHT)
            position = [random()*w, random()*h]
            entity.set_target_position(position)

        # Cuando la entidad se cura
        elif was_infected and not entity.is_infected():
            self.__infected_entitys.remove(entity)
            self.__healthy_entitys.append(entity)

        # Infectando otras entidades
        #* OPTIMIZE: Colocar aquí el mágico quadtree
        # if entity.is_infected():
        #     infected = []
        #     for other_entity in self.__healthy_entitys:
        #         entity.infect(other_entity)
        #         if other_entity.is_infected():
        #             infected.append(other_entity)
        #     for to_medicate in infected:
        #         self.__healthy_entitys.remove(to_medicate)
        #         self.__infected_entitys.append(to_medicate)
        # elif was_infected:
        #     self.__infected_entitys.remove(entity)
        #     self.__healthy_entitys.append(entity)

    def get_update_count(self) -> int:
        """
        Obtiene la cantidad de iteraciones que se han hecho.

        Returns:
            int: Cantidad de iteraciones realizadas.
        """
        return self.__update_count
    
    def get_infected(self) -> int:
        return len(self.__infected_entitys)
