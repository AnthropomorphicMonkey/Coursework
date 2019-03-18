import maths_scripts.mechanics as mechanics
import sympy

g = 9.8


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
            force += mechanics.x_component_calc(each_force[0], each_force[1])
        return force

    @property
    def force_y(self) -> float:
        force = 0
        for each_force in self.force_list:
            force += mechanics.y_component_calc(each_force[0], each_force[1])
        return force

    @property
    def force_magnitude(self) -> float:
        return mechanics.resultant_magnitude_calc(self.force_x, self.force_y)

    @property
    def force_direction(self) -> float:
        return mechanics.resultant_direction_calc(self.force_x, self.force_y)


class MovingObject(BasicObject):
    def __init__(self, mass: float = 0, initial_velocity_magnitude=0, initial_velocity_direction=0):
        super().__init__()
        # Initial velocity data:
        self.initial_velocity_x = 0
        self.initial_velocity_y = 0
        self.initial_velocity_magnitude = 0
        self.initial_velocity_direction = 0
        self.update_initial_velocity(initial_velocity_magnitude, initial_velocity_direction)
        # Set mass. If no mass is defined it is set to 0
        self.mass = mass

    def update_initial_velocity(self, magnitude: float, direction: float):
        self.initial_velocity_direction = direction
        self.initial_velocity_x = mechanics.x_component_calc(magnitude, direction)
        self.initial_velocity_y = mechanics.y_component_calc(magnitude, direction)
        self.initial_velocity_magnitude = magnitude

    def update_mass(self, new_mass: float):
        self.mass = new_mass

    # Acceleration calculations
    @property
    def acceleration_x(self) -> float:
        return mechanics.acceleration_calc(self.force_x, self.mass)

    @property
    def acceleration_y(self) -> float:
        return mechanics.acceleration_calc(self.force_y, self.mass)

    @property
    def acceleration_magnitude(self) -> float:
        return mechanics.acceleration_calc(self.force_magnitude, self.mass)

    @property
    def acceleration_direction(self) -> float:
        return self.force_direction

    # Velocity calculations
    def final_velocity_x(self, time: float):
        return mechanics.velocity_calc(self.initial_velocity_x, self.acceleration_x, time)

    def final_velocity_y(self, time: float):
        return mechanics.velocity_calc(self.initial_velocity_y, self.acceleration_y, time)

    def final_velocity_magnitude(self, time: float):
        return mechanics.resultant_magnitude_calc(self.final_velocity_x(time), self.final_velocity_y(time))

    def final_velocity_direction(self, time: float):
        return mechanics.resultant_direction_calc(self.final_velocity_x(time), self.final_velocity_y(time))

    # Displacement calculations
    def final_displacement_x(self, time: float):
        return mechanics.displacement_calc(self.initial_velocity_x, self.acceleration_x, time)

    def final_displacement_y(self, time: float):
        return mechanics.displacement_calc(self.initial_velocity_y, self.acceleration_y, time)

    def final_displacement_magnitude(self, time: float):
        return mechanics.resultant_magnitude_calc(self.final_displacement_x(time), self.final_displacement_y(time))

    def final_displacement_direction(self, time: float):
        return mechanics.resultant_direction_calc(self.final_displacement_x(time), self.final_displacement_y(time))

    def time_of_x_displacement(self, displacement: float):
        t = sympy.symbols('t')
        function = ((0.5 * self.acceleration_x) * (t ** 2)) + (self.initial_velocity_x * t) - displacement
        return sympy.solve(function, t)

    def time_of_y_displacement(self, displacement: float):
        t = sympy.symbols('t')
        function = ((0.5 * self.acceleration_y) * (t ** 2)) + (self.initial_velocity_y * t) - displacement
        return sympy.solve(function, t)


class Projectile(MovingObject):
    @property
    def force_y(self) -> float:
        force = (super().force_y - (self.mass * g))
        return force
