import questions.question_scripts as question_scripts
import maths_scripts.mechanics.two_dimensions as two_dimensions
import random
import sympy


def find_resultant_of_two_forces(difficulty: int) -> question_scripts.Question:
    type_id = 2
    obj = two_dimensions.BasicObject()
    force_magnitude_1 = random.randint(1, 100)
    force_direction_1 = random.randint(-180, 180)
    obj.add_force(force_magnitude_1, force_direction_1)
    force_magnitude_2 = random.randint(1, 100)
    force_direction_2 = random.randint(-180, 180)
    obj.add_force(force_magnitude_2, force_direction_2)
    question_to_ask = random.randint(1, 2)
    if question_to_ask == 1 or difficulty < 3:
        question_text = 'A force P acts on an object on a frictionless plane with magnitude {}N in the direction {}° ' \
                        'to the x axis and another force, Q acts with magnitude {}N in the direction {}° to the x ' \
                        'axis. ' \
                        'Find the magnitude of the resultant force.'.format(force_magnitude_1,
                                                                            force_direction_1,
                                                                            force_magnitude_2,
                                                                            force_direction_2)
        correct_answer = round(obj.force_magnitude, 2)
        question = question_scripts.Question('Find resultant of two forces', type_id, difficulty, question_text,
                                             correct_answer)
        return question
    elif question_to_ask == 2 and difficulty >= 3:
        question_text = 'A force P acts on an object on a frictionless plane with magnitude {}N in the direction {}° ' \
                        'to the x axis and another force, Q acts with magnitude {}N in the direction {}° to the x ' \
                        'axis. ' \
                        'Find the direction relative to the x axis of the resultant force.'.format(force_magnitude_1,
                                                                                                   force_direction_1,
                                                                                                   force_magnitude_2,
                                                                                                   force_direction_2)
        correct_answer = round(obj.force_direction, 2)
        question = question_scripts.Question('Find resultant of two forces', type_id, difficulty, question_text,
                                             correct_answer)
        return question


def projectile(difficulty: int) -> [question_scripts.Question, str, float, float]:
    type_id = 6
    mass: int = random.randint(1, 10)
    initial_velocity_magnitude: int = random.randint(1, 100)
    initial_velocity_direction: int = random.randint(0, 90)
    projectile_instance = two_dimensions.Projectile(mass=mass, initial_velocity_magnitude=initial_velocity_magnitude,
                                                    initial_velocity_direction=initial_velocity_direction)
    limit_positions = projectile_instance.time_of_y_displacement(0)
    time: int = round(random.uniform(min(limit_positions), max(limit_positions)), 2)
    upper_limit = projectile_instance.final_displacement_x(time)
    lower_limit = projectile_instance.final_displacement_x(min(limit_positions))
    x = sympy.symbols('x')
    a: float = 0.5 * projectile_instance.acceleration_x
    b: float = projectile_instance.initial_velocity_x
    if a == 0:
        t = x / b
    else:
        c: float = -x
        t = ((-b + (((b ** 2) - (4 * a * c)) ** 0.5)) / (2 * a))
    function = (0.5 * projectile_instance.acceleration_y * (t ** 2)) + (projectile_instance.initial_velocity_y * t)
    ##
    question_to_ask = random.randint(1, 2)
    if question_to_ask == 1:
        question_text: str = 'A projectile is launched with velocity {} at an angle of {} to the horizontal. ' \
                             'Find horizontal displacement after {} seconds'.format(initial_velocity_magnitude,
                                                                                    initial_velocity_direction, time)
        correct_answer: float = projectile_instance.final_displacement_x(time)
    else:
        question_text: str = 'A projectile is launched with velocity {} at an angle of {} to the horizontal. ' \
                             'Find vertical displacement after {} seconds'.format(initial_velocity_magnitude,
                                                                                  initial_velocity_direction, time)
        correct_answer: float = projectile_instance.final_displacement_y(time)
    correct_answer = round(correct_answer, 2)
    question = question_scripts.Question("Projectile", type_id, difficulty, question_text, correct_answer)
    upper_limit: float = upper_limit * (random.uniform(1.1, 1.5))
    return question, function, lower_limit, upper_limit

