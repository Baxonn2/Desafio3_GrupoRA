import random
import math
from src.entity import Entity

class Node:
    
    def __init__(self,x,y,w,h,capacity):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.capacity = capacity
        self.entities = []
        self.divided = False

    def contains(self,x,y):
        return (x < self.x+self.w and x >= self.x-self.w and y < self.y+self.h and y >= self.y-self.h) 

    def subdivide(self):
        self.upper_right_child = Node(self.x + self.w/2, self.y - self.h/2,self.w/2,self.h/2,self.capacity)
        self.upper_left_child = Node(self.x - self.w/2, self.y - self.h/2,self.w/2,self.h/2,self.capacity)
        self.down_right_child = Node(self.x + self.w/2, self.y + self.h/2,self.w/2,self.h/2,self.capacity)
        self.down_left_child = Node(self.x - self.w/2, self.y + self.h/2,self.w/2,self.h/2,self.capacity)
        self.divided = True

        for entity in self.entities:
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)
        
        self.entities = []	


    def insert(self,entity):
        if not self.contains(entity.get_position()[0],entity.get_position()[1]):
            #print ("nc")
            return False
        if len(self.entities) <= self.capacity and not self.divided:
            #print("inserted {}".format(entity.aid))
            self.entities.append(entity)
        else:
            if not self.divided:
                self.subdivide()
            self.upper_left_child.insert(entity)
            self.upper_right_child.insert(entity)
            self.down_left_child.insert(entity)
            self.down_right_child.insert(entity)

    def points_within_radius(self,x,y,radius,presition):
        if presition > 1:
            print("presition entre 0 y 1 pls")
            return None
        if presition <0.1:
            presition=0.1
        #presition de 0 a 1 
        rad_step = math.floor(presition*10)
        deg_step = math.floor(360/(90*presition))
        
        test_points = []

        current_radius = 0
        current_degree = 0
        for i in range(1,rad_step+1):
            current_radius = i/rad_step*radius
            # print(current_radius)

            while current_degree < 360:
                p_x = x + math.cos(current_degree*math.pi/180)*current_radius
                p_y = y + math.sin(current_degree*math.pi/180)*current_radius
                test_points.append((p_x, p_y))
                current_degree+=deg_step

            current_degree = 0

        ret = []
        for i in test_points:
            for j in (self.get_leaf(i[0],i[1])):
                if j not in ret:
                    ret.append(j)

        fixed_ret = []
        for i in ret:
            if i not in fixed_ret:
                fixed_ret.append(i)


        return(fixed_ret)



    def get_leaf(self,x,y):
        if not self.divided:
            if self.contains(x,y):
                return self.entities
            else:
                return []
        else:
            ret = []

            for i in self.upper_right_child.get_leaf(x,y):
                ret.append(i)
            for i in self.upper_left_child.get_leaf(x,y):
                ret.append(i)
            for i in self.down_right_child.get_leaf(x,y):
                ret.append(i)
            for i in self.down_left_child.get_leaf(x,y):
                ret.append(i)

            fixed_ret = [x for x in ret if x]
            return fixed_ret
            