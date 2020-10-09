import math


class Node:

    NODE_ID = 1

    def __init__(self, x, y, w, h, capacity, parent=None):
        if parent is None:
            Node.NODE_ID = 1
        else:
            Node.NODE_ID += 1
        self.n_id = Node.NODE_ID
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.capacity = capacity
        self.entities = []
        self.divided = False
        self.parent = parent

    def contains(self, x, y):
        return self.x + self.w > x >= self.x - self.w and \
               self.y + self.h > y >= self.y - self.h

    def subdivide(self):
        self.upper_right_child = Node(self.x + self.w / 2, self.y - self.h / 2, self.w / 2, self.h / 2, self.capacity, self)
        self.upper_left_child = Node(self.x - self.w / 2, self.y - self.h / 2, self.w / 2, self.h / 2, self.capacity, self)
        self.down_right_child = Node(self.x + self.w / 2, self.y + self.h / 2, self.w / 2, self.h / 2, self.capacity, self)
        self.down_left_child = Node(self.x - self.w / 2, self.y + self.h / 2, self.w / 2, self.h / 2, self.capacity, self)
        self.divided = True

        for entity in self.entities:
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)

        self.entities = []

    def insert(self, entity):
        if not self.contains(entity.x, entity.y):
            return False
        if len(self.entities) <= self.capacity and not self.divided:
            self.entities.append(entity)
        else:
            if not self.divided:
                self.subdivide()
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)

    def find_neighbors(self, x, y, radius):
        points = [(x+radius, y),
                  (x-radius, y),
                  (x, y+radius),
                  (x, y-radius)]

        base_node = self.find_node(x, y)
        contains_all = False

        while not contains_all:
            if base_node.parent is not None:
                break
            contains_all = True
            for x_, y_ in points:
                if not base_node.contains(x_, y_):
                    contains_all = False
                    base_node = base_node.parent
        entities = base_node.get_leaves()
        return entities

    def find_node(self, x, y):
        if self.contains(x, y):
            if self.divided:
                if self.upper_left_child.contains(x, y):
                    return self.upper_left_child.find_node(x, y)
                elif self.upper_right_child.contains(x,y):
                    return self.upper_right_child.find_node(x, y)
                elif self.down_left_child.contains(x,y):
                    return self.down_left_child.find_node(x, y)
                elif self.down_right_child.contains(x,y):
                    return self.down_right_child.find_node(x, y)
            else:
                return self
        else:
            return None

    def get_leaf(self, x, y):
        if not self.divided:
            if self.contains(x, y):
                return self.entities
            else:
                return []
        else:
            ret = []

            for i in self.upper_right_child.get_leaf(x, y):
                ret.append(i)
            for i in self.upper_left_child.get_leaf(x, y):
                ret.append(i)
            for i in self.down_right_child.get_leaf(x, y):
                ret.append(i)
            for i in self.down_left_child.get_leaf(x, y):
                ret.append(i)

            fixed_ret = [x for x in ret if x]
            return fixed_ret

    def get_leaves(self):
        entities = []
        if self.divided:
            entities += self.upper_right_child.get_leaves()
            entities += self.upper_left_child.get_leaves()
            entities += self.down_right_child.get_leaves()
            entities += self.down_left_child.get_leaves()
        else:
            return self.entities
        return entities

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, pygame.Rect(self.x - self.w, self.y - self.h, self.w * 2, self.h * 2), 1)
        if self.divided:
            self.upper_left_child.draw(screen, color)
            self.upper_right_child.draw(screen, color)
            self.down_left_child.draw(screen, color)
            self.down_right_child.draw(screen, color)


class Entity:
    def __init__(self, w, h, aid):
        self.x, self.y = (random.random() * w, random.random() * h)
        self.aid = aid

    def move(self):
        x = self.x + random.random() * 2 - 1
        y = self.y + random.random() * 2 - 1
        self.x, self.y = (x, y)


if __name__ == '__main__':
    import random
    import pygame
    import math

    w = 500
    h = 500

    pygame.init()
    random.seed(42)

    colors = {
        'magenta': (1, 199, 200),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'red': (255, 0, 0)
    }
    screen = pygame.display.set_mode((w, h))
    pygame.display.set_caption("Pandemic Simulator")

    exit = False
    quadTree = Node(w / 2, h / 2, w / 2, h / 2, 4)

    enti = []
    for i in range(100):
        enti.append(Entity(w, h, i))

    for i in enti:
        quadTree.insert(i)

    for i in quadTree.points_within_radius(250, 250, 100, 0.1):
        print(i.x, i.y)

    while not exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

        screen.fill(colors['black'])
        for i in enti:
            pygame.draw.circle(screen, colors['white'], (int(i.x), int(i.y)), 1)

        quadTree.draw(screen, colors['red'])

        pygame.display.update()

        # for i in enti:
        # i.move()

        quadTree = Node(w / 2, h / 2, w / 2, h / 2, 4)
        for i in enti:
            quadTree.insert(i)
