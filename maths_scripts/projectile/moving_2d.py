import maths_scripts.projectile.base_2d as base2d
from maths_scripts.projectile.force_functions import *


class MovingObject(base2d.BasicObject):
    def __init__(self, **kwargs: float):
        super().__init__()
        # Initial velocity data:
        self.initial_velocity_x = 0
        self.initial_velocity_y = 0
        self.initial_velocity = 0
        self.initial_velocity_direction = 0
        # Set mass. If no mass is defined it is set to 0
        self.mass = 0
        if kwargs:
            if 'mass' in kwargs:
                self.update_mass(kwargs.get('mass'))
            if ('initial_velocity' and 'initial_velocity_angle') in kwargs:
                self.update_initial_velocity(kwargs.get('initial_velocity'), kwargs.get('initial_velocity_angle'))

    def update_initial_velocity(self, magnitude: float, direction: float):
        self.initial_velocity_direction = direction
        self.initial_velocity_x = horizontal_component_calc(magnitude, direction)
        self.initial_velocity_y = vertical_component_calc(magnitude, direction)
        self.initial_velocity = magnitude

    def update_mass(self, new_mass: float):
        self.mass = new_mass

    # Velocity calculations
    def final_velocity_x(self, time: float):
        return velocity_calc(self.initial_velocity_x, self.acceleration_x, time)

    def final_velocity_y(self, time: float):
        return velocity_calc(self.initial_velocity_y, self.acceleration_y, time)

    def final_velocity(self, time: float):
        return resultant_magnitude_calc(self.final_velocity_x(time), self.final_velocity_y(time))

    def final_velocity_direction(self, time: float):
        return resultant_direction_calc(self.final_velocity_x(time), self.final_velocity_y(time))

    # Acceleration calculations
    @property
    def acceleration_x(self) -> float:
        return acceleration_calc(self.force_x, self.mass)

    @property
    def acceleration_y(self) -> float:
        return acceleration_calc(self.force_y, self.mass)

    @property
    def acceleration(self) -> float:
        return resultant_magnitude_calc(self.acceleration_x, self.acceleration_y)

    @property
    def acceleration_direction(self) -> float:
        return resultant_direction_calc(self.acceleration_x, self.acceleration_y)
