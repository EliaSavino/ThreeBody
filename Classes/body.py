'''
Author: Elia Savino
github: github.com/EliaSavino

Happy Hacking!

Descr: Body Class for a three body problem simulation

'''

import numpy as np


class Body:
    '''Body class for a 2 dimensional three body problem simulation'''
    g = 6.67430e-11
    trace_len = 1000


    def __init__(self, init_position: np.array, init_velocity:np.array, mass: float, color: str = 'k', size = 1.0):
        self.position = np.array(init_position)
        self.velocity = np.array(init_velocity)
        self.mass = mass
        self.position_history = [self.position.copy()]
        self.force = np.array([0.0, 0.0])
        self.acceleration = np.array([0.0, 0.0])
        self.color = color
        self.size = size

    def update_position(self, dt):
        if len(self.position_history) > self.trace_len:
            self.position_history.pop(0)
        self.position_history.append(self.position.copy())
        self.position += self.velocity * dt


    def update_velocity(self, dt):
        self.velocity += self.acceleration * dt

    def update_acceleration(self):
        self.acceleration = self.force / self.mass

    def calculate_force(self, other_bodies: list):
        '''calculates the force applied on the object given the other objects in the system
        :param other_bodies: list of Body objects
        '''
        self.force = np.array([0.0, 0.0])
        for body in other_bodies:
            if body == self:
                continue
            r = body.position - self.position
            r_norm = np.linalg.norm(r)
            self.force += self.g * self.mass * body.mass / r_norm**2 * r / r_norm