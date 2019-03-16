from maths_scripts.mechanics.two_dimensions import *


def tests(projectile):
    print("List of forces:", projectile.force_list)
    print("Mass:", projectile.mass)
    print("x force:", projectile.force_x)
    print("y force:", projectile.force_y)
    print("Force magnitude:", projectile.force_magnitude)
    print("Force direction:", projectile.force_direction)
    print("x acceleration:", projectile.acceleration_x)
    print("y acceleration:", projectile.acceleration_y)
    print("Acceleration magnitude:", projectile.acceleration_magnitude)
    print("Acceleration direction:", projectile.acceleration_direction)
    print("x velocity at t=0:", projectile.initial_velocity_x)
    print("y velocity at t=0:", projectile.initial_velocity_y)
    print("Velocity magnitude at t=0:", projectile.initial_velocity_magnitude)
    print("Velocity direction at t=0:", projectile.initial_velocity_direction)
    print("x velocity at t=10:", projectile.final_velocity_x(10))
    print("y velocity at t=10:", projectile.final_velocity_y(10))
    print("Velocity magnitude at t=10:", projectile.final_velocity_magnitude(10))
    print("Velocity direction at t=10:", projectile.final_velocity_direction(10))
    print("x displacement at t=10:", projectile.final_displacement_x(10))
    print("y displacement at t=10:", projectile.final_displacement_y(10))
    print("Displacement magnitude at t=10:", projectile.final_displacement_magnitude(10))
    print("Displacement direction at t=10:", projectile.final_displacement_direction(10))
    print(projectile.time_of_x_displacement(0))
    print(projectile.time_of_y_displacement(0))


if __name__ == '__main__':
    object_1 = Projectile(mass=10, initial_velocity_magnitude=100, initial_velocity_direction=45)
    print("\nInitial values")
    object_1.add_force(100, 0)
    tests(object_1)
