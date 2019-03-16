from math import sin, cos, degrees, atan, radians


def x_component_calc(magnitude: float, direction: float) -> float:
    return magnitude * cos(radians(direction))


def y_component_calc(magnitude: float, direction: float) -> float:
    return magnitude * sin(radians(direction))


def resultant_magnitude_calc(x_component: float, y_component: float) -> float:
    return ((x_component ** 2) + (y_component ** 2)) ** 0.5


def resultant_direction_calc(x_component: float, y_component: float) -> float:
    if x_component == 0:
        if y_component > 0:
            return 90
        elif y_component < 0:
            return -90
        else:
            return 0
    direction = degrees(atan(y_component / x_component))
    if x_component < 0 < y_component:
        direction += 180
    if x_component < 0 and y_component < 0:
        direction -= 180
    return direction


def acceleration_calc(force: float, mass: float) -> float:
    if mass == 0:
        return 0
    else:
        return force / mass


def velocity_calc(initial_velocity: float, acceleration: float, time: float) -> float:
    return initial_velocity + (acceleration * time)


def displacement_calc(initial_velocity: float, acceleration: float, time: float) -> float:
    return (initial_velocity * time) + (0.5 * (acceleration * (time ** 2)))


if __name__ == '__main__':
    print(resultant_direction_calc(-1, -1))
