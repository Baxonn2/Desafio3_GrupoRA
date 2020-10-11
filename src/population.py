from .entity import Entity
import random
from src.search.quadtree import Node as Node

WORLD_WIDTH = 600
WORLD_HEIGHT = 600


class Population:

    def __init__(self, population=0, sick_entities=0, masks=0, algorithm='quadtree'):
        self.entities = []
        self.sick_entities = {}
        self.healthy_entities = {}
        self.current_iteration = 0
        self.__update_count = 0
        self.algorithm = algorithm
        if population > 0 or sick_entities > 0:
            self.add_entities(population, sick_entities, masks)

    def add_entities(self, total_population: int, initial_sick: int,
                     mask: float = 0):
        """
        Crea una poblacion de entidades.

        :param total_population: cantidad total de entidades en la poblacion
        :param initial_sick: cantidad de entidades enfermas al inicio de la
                             propagacion de la enfermedad
        :param mask: probabilidad entre 0 y 1 de que una entidad use mascara
        """

        total_sick = 1
        if initial_sick > total_population:
            raise ValueError("La cantidad de infectados es mayor al tamaño de la población")

        for i in range(total_population):
            # Posicion inicial de la entidad
            x, y = random.random() * WORLD_WIDTH, random.random() * WORLD_HEIGHT
            # Uso de mascara
            has_mask = mask > 0 and random.random() <= mask
            # Primero crea a los infectados y luego a los sanos
            entity = Entity(x, y, total_sick <= initial_sick, has_mask)
            total_sick += 1

            self.entities.append(entity)
            if entity.is_infected:
                self.sick_entities[entity.person_id] = entity
            else:
                self.healthy_entities[entity.person_id] = entity

    def update(self):
        """
        Actualiza y dibuja las entidades en pantalla
        """
        self.current_iteration += 1
        if self.algorithm == "quadtree":
            self.__update_quadtree()

    def __update_quadtree(self):
        # Buscando infectados
        quadtree = Node(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, WORLD_WIDTH / 2,
                        WORLD_HEIGHT / 2, 10)

        for entity in self.healthy_entities.values():
            quadtree.insert(entity)
        new_infected = set()

        for infected_entity in self.sick_entities.values():
            x, y = infected_entity.x, infected_entity.y
            entities = quadtree.find_neighbors(x, y, infected_entity.radius())

            ids = []
            for i in entities:
                infected_entity.infect(i)
                if i.is_infected:
                    ids.append(i.person_id)

            new_infected.update(ids)

        for entity_id in new_infected:
            self.sick_entities[entity_id] = self.healthy_entities.pop(entity_id)

    def update_entity(self, entity: Entity):
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
