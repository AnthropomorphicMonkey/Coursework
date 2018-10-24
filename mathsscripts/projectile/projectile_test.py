import mathsscripts.projectile.projectile_2d as projectile2d


def tests(object_1):
    print("List of forces:", object_1.force_list)
    print("Mass:", object_1.mass)
    print("x force:", object_1.force_x)
    print("y force:", object_1.force_y)
    print("Force magnitude:", object_1.force)
    print("Force direction:", object_1.force_direction)
    print("x acceleration:", object_1.acceleration_x)
    print("y acceleration:", object_1.acceleration_y)
    print("Acceleration magnitude:", object_1.acceleration)
    print("Acceleration direction:", object_1.acceleration_direction)
    print("x velocity at t=0:", object_1.initial_velocity_x)
    print("y velocity at t=0:", object_1.initial_velocity_y)
    print("Velocity magnitude at t=0:", object_1.initial_velocity)
    print("Velocity direction at t=0:", object_1.initial_velocity_direction)
    print("x velocity at t=10:", object_1.final_velocity_x(10))
    print("y velocity at t=10:", object_1.final_velocity_y(10))
    print("Velocity magnitude at t=10:", object_1.final_velocity(10))
    print("Velocity direction at t=10:", object_1.final_velocity_direction(10))


def projectile_test():
    object_1 = projectile2d.Projectile(mass=10, initial_velocity=100, initial_velocity_angle=60)
    print("\nInitial values")
    object_1.add_force(100, 0)
    object_1.add_force(100, 90)
    object_1.add_force(100, 45)
    tests(object_1)
    print("\nRemoving second force")
    object_1.remove_force(1)
    tests(object_1)
    print("\nChanging mass to 20")
    object_1.update_mass(20)
    tests(object_1)
    print("\nNo force in x direction")
    object_1.remove_force(0)
    object_1.remove_force(0)
    object_1.add_force(100, 90)
    tests(object_1)
    print("\nNo force")
    object_1.update_mass(0)
    object_1.remove_force(0)
    tests(object_1)


if __name__ == '__main__':
    projectile_test()
