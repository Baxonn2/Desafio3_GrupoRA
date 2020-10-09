from .entity import Entity
import random
from src.search.quadtree import Node
import pygame

WORLD_WIDTH = 600
WORLD_HEIGHT = 600


class Population:

    def __init__(self, population=0, sick_entities=0, masks=0):
        self.entities = []
        self.sick_entities = {}
        self.healthy_entities = {}
        self.current_iteration = 0
        self.__update_count = 0
        if population > 0 or sick_entities > 0:
            self.add_entities(population, sick_entities, masks)

    def add_entities(self, total_population, initial_sick, mask=0):
        """
        Agrega una nueva entidad al manager de entidades

        Args:
            entity (Entity, optional): Nueva entidad a agregar. Si no se define
                                       esta entidad se creara una con parametros
                                       aleatorios.
            infected (bool, optional): Establece si la entidad esta o no
                                       infectada. Por defecto es False.
        """

        # Creating healthy entities
        total_sick = 1
        for i in range(total_population):
            x, y = random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT
            has_mask = mask > 0 and random.random() <= mask
            entity = Entity(x, y, total_sick <= initial_sick, has_mask)
            total_sick += 1

            self.entities.append(entity)
            if entity.is_infected:
                self.sick_entities[entity.person_id] = entity
            else:
                self.healthy_entities[entity.person_id] = entity
        print(len(self.entities))
        print(len(self.healthy_entities))
        print(len(self.sick_entities))

    def draw_and_update(self, screen: pygame.surface.Surface):
        """
        Actualiza y dibuja las entidades en pantalla

        Args:
            screen (pygame.surface.Surface): Superficie donde se va a dibujar.
        """
        self.current_iteration += 1
        for entity in self.entities:
            self.__update_entity(entity)
            # Dibujando entidad
            entity.draw(screen)

        # Buscando infectados
        quadtree = Node(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, WORLD_WIDTH / 2,
                        WORLD_HEIGHT / 2, 10)

        for entity in self.healthy_entities.values():
            quadtree.insert(entity)
        new_infected = set()

        for infected_entity in self.sick_entities.values():
            x, y = infected_entity.x, infected_entity.y
            # entities = quadtree.points_within_radius(x, y,
            #                                          infected_entity.radius(),
            #                                          PRECISION)
            entities = quadtree.find_neighbors(x, y, infected_entity.radius())

            ids = []
            for i in entities:
                infected_entity.infect(i)
                if i.is_infected:
                    ids.append(i.person_id)

            new_infected.update(ids)

        for entity_id in new_infected:
            self.sick_entities[entity_id] = self.healthy_entities.pop(entity_id)

    def __update_entity(self, entity: Entity):
        """
        Actualiza la entidad ingresada como parametro. También infecta a todas
        las que esta entidad puede infectar.

        Args:
            entity (Entity): Entidad a actualizar.
        """
        # Actualizando entidad
        if entity.is_alive:
            infected = entity.is_infected
            entity.step()

            if entity.in_target():
                x, y = random.random()*WORLD_WIDTH, random.random()*WORLD_HEIGHT
                entity.set_target_position(x, y)
            if infected and not entity.is_infected:
                self.sick_entities.pop(entity.person_id)
                self.healthy_entities[entity.person_id] = entity

    def get_update_count(self) -> int:
        """
        Obtiene la cantidad de iteraciones que se han hecho.

        Returns:
            int: Cantidad de iteraciones realizadas.
        """
        return self.__update_count

    def get_infected(self) -> int:
        return len(self.sick_entities)
