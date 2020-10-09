import random
from math import sqrt
import pygame


# Factores que reducen contagio
MASK_FACTOR_SICK = 0.2
MASK_FACTOR_HEALTHY = 0.6
RECOVERED_FACTOR = 0.999

# Probabilidad de muerte despues de 0.7 el avance total de la enfermedad
DEATH_RATE_AFTER_07 = 0.01

# Tiempos de enfermedad e inmunidad
SICKNESS_DURATION = 1000
IMMUNITY_DURATION = 3000

# Probabilidad de extension del tiempo del inmunidad
IMMUNITY_PROB_AFTER_TIME = 0.001

# Radio de infeccion
INFECT_RADIUS = 7
MASK_RADIUS_INFECTION = 0.8

# Probabilidades de contagio
INFECT_PROB = 0.3
IMMUNITY_FAIL = 0.000001

# Probabilidades de recuperacion
RECOVERY_AFTER_TIME = 0.9
RECOVERY_BEFORE_TIME = 0.0001


class Entity:
    # Constantes de posicionamiento
    TARGET_DONE_RANGE = 0.1
    PERSON_ID = 0

    def __init__(self, x, y, is_infected=False, has_mask=False):
        Entity.PERSON_ID += 1
        self.x = x
        self.y = y
        self.z = None
        self.person_id = Entity.PERSON_ID

        self._x_target = x
        self._y_target = y
        self._z_target = None
        self._target_done = True

        self.is_infected = is_infected
        self.is_recovered = False
        self.is_immune = False
        self.is_alive = True
        self.has_mask = has_mask

        self.sick_time = 0
        self.immunity_time = 0

    def step(self):
        """
                Esta funcion debe hacer que la entidad se actualice
                """
        if self.is_alive:
            dx = (self._x_target - self.x) / 20
            dy = (self._y_target - self.y) / 20

            self.x += dx
            self.y += dy

            # Actualizando el estado del target
            self._target_done = abs(dx) < self.TARGET_DONE_RANGE and \
                                abs(dy) < self.TARGET_DONE_RANGE

            self.update_status()

    def set_target_position(self, x, y):
        self._x_target = x
        self._y_target = y

    def in_target(self):
        return self._target_done

    def radius(self):
        if self.has_mask:
            return INFECT_RADIUS * MASK_RADIUS_INFECTION
        return INFECT_RADIUS

    def update_status(self):
        if self.is_infected:
            self.sick_time += 1
            probability = random.random()
            if probability <= DEATH_RATE_AFTER_07 and \
                    self.sick_time / SICKNESS_DURATION >= 0.7:
                self.is_alive = False
                self.is_infected = False

            elif probability <= RECOVERY_BEFORE_TIME:
                self.is_infected = False
            elif self.sick_time >= SICKNESS_DURATION and \
                    probability <= RECOVERY_AFTER_TIME:
                self.is_infected = False

            if not self.is_infected and self.is_alive:
                self.sick_time = 0
                self.is_immune = True
                self.is_recovered = True

        if self.is_immune:
            self.immunity_time += 1

            if self.immunity_time >= IMMUNITY_DURATION:
                if random.random() <= IMMUNITY_PROB_AFTER_TIME:
                    self.immunity_time = 0
                    self.is_immune = False

    def infect(self, entity):
        """
        Esta funcion debe infectar a la entidad si está dentro del rango
        que puede infectar.
        """
        if not self.is_infected or not self.is_alive:
            return
        if entity.is_infected or not entity.is_alive:
            return

        x2, y2 = entity.x, entity.y

        distance = sqrt((self.x - x2) ** 2 + (self.y - y2) ** 2)

        infection_value = INFECT_PROB
        if entity.is_immune:
            infection_value *= IMMUNITY_FAIL
        if entity.has_mask:
            infection_value *= MASK_FACTOR_HEALTHY
        if self.has_mask:
            infection_value *= MASK_FACTOR_SICK
        if entity.is_recovered:
            infection_value *= RECOVERED_FACTOR

        # La probabilidad de infectarse depende del radio de infeccion de la
        # entidad infecciosa. Este radio cambia si la entidad tiene mascarilla
        # a medida que la distancia sea mayor, menos probabilidades la otra
        # entidad tendra de contagiarse
        if distance < self.radius() and random.random() <= infection_value:
            if random.random() >= distance/self.radius():
                entity.is_infected = True

    def draw(self, surface: pygame.surface.Surface):
        radius = INFECT_RADIUS
        if self.is_alive:
            if self.is_infected:
                color = [200, 0, 0]
                if self.has_mask:
                    color = [200, 147, 0]
                    radius = INFECT_RADIUS * MASK_RADIUS_INFECTION
            elif self.is_immune:
                color = [0, 200, 200]
                if self.has_mask:
                    color = [255, 255, 255]
            else:
                color = [0, 200, 0]
                if self.has_mask:
                    color = [200, 0, 200]
        else:
            color = [102, 102, 102]

        casted_position = [int(self.x), int(self.y)]

        if self.is_infected and random.random() < INFECT_PROB:
            pygame.draw.circle(surface, color, casted_position,
                               int(radius))

        pygame.draw.circle(surface, color, casted_position, 2)


if __name__ == '__main__':
    person1 = Entity(0, 0)
    person2 = Entity(1, 0, is_infected=True)
    person3 = Entity(1, 1, has_mask=True)

    print(f'ID de las personas\n{person1.person_id}\n{person2.person_id}'
          f'\n{person3.person_id}')
    while not person1.is_infected:
        print('contagiando a personas')
        person2.infect(person1)
        person2.infect(person3)
