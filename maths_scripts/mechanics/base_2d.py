from maths_scripts.mechanics.force_functions import *


class BasicObject:
    def __init__(self):
        # Force data:
        self.force_list = []

    # Force data manipulation:
    def add_force(self, magnitude: float, direction: float):
        self.force_list.append([magnitude, direction])

    def remove_force(self, force_number: int):
        del self.force_list[force_number]

    # Force calculations:
    @property
    def force_x(self) -> float:
        force = 0
        for each_force in self.force_list:
            force += horizontal_component_calc(each_force[0], each_force[1])
        return force

    @property
    def force_y(self) -> float:
        force = 0
        for each_force in self.force_list:
            force += vertical_component_calc(each_force[0], each_force[1])
        return force

    @property
    def force(self) -> float:
        return resultant_magnitude_calc(self.force_x, self.force_y)

    @property
    def force_direction(self) -> float:
        return resultant_direction_calc(self.force_x, self.force_y)
