from __future__ import annotations
from typing import Tuple, List
from random import random
from math import sqrt
import pygame

class Entity:

    # Posicion de la entidad
    _position: List[float, float]
    _target_position: List[float, float]
    _target_done: bool
    
    # Variable de infeccion
    _infected: bool

    # Constantes de posicionamiento
    TARGET_DONE_RANGE = 0.1

    # Constante de la infeccion
    INFECT_PROB = 0.1
    INFECT_RADIO = 7

    def __init__(self, position: List[float, float], infected: bool = False):
        self._position = position
        self._target_position = position
        self._target_done = False
        self.__infected = infected

    def step(self):
        """
        Esta funcion debe hacer que la entidad se actualice
        """
        dx = (self._target_position[0] - self._position[0]) / 20
        dy = (self._target_position[1] - self._position[1]) / 20

        self._position[0] += dx
        self._position[1] += dy

        # Actualizando el estado del target
        self._target_done = abs(dx) < self.TARGET_DONE_RANGE and \
            abs(dy) < self.TARGET_DONE_RANGE

    def infect(self, entity: Entity):
        """
        Esta funcion debe infectar a la entidad si está dentro del rango
        que puede infectar.
        """
        if not self.__infected:
            return

        x1, y1 = self._position
        x2, y2 = entity.get_position()
        
        distance = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        if distance < self.INFECT_RADIO and random() <= self.INFECT_PROB:
            entity.set_infected(True)

    def get_position(self) -> List[float, float]:
        return self._position

    def set_infected(self, infected: bool):
        self.__infected = infected

    def is_infected(self):
        return self.__infected

    def set_target_position(self, target_position: Tuple[float, float]):
        self._target_position = target_position

    def is_target_done(self) -> bool:
        return self._target_done

    def draw(self, surface: pygame.surface.Surface):
        color = [200, 0, 0] if self.__infected else (0, 200, 0)
        
        casted_position = [self._position[0], self._position[1]]
        casted_position[0] = int(casted_position[0])
        casted_position[1] = int(casted_position[1])

        if self.__infected and random() < self.INFECT_PROB:
            pygame.draw.circle(surface, [150, 33, 33], casted_position,
                               self.INFECT_RADIO)

        pygame.draw.circle(surface, color, casted_position, 2)
        