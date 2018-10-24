from math import pi, asin, acos, atan


# Values should be in radians, max and min are inclusive. Function returns sorted array of all solutions within range
def solutions_in_range(trig_function: str, value: float, minimum: float, maximum: float):
    # Initialise unsorted solution array
    unsorted_values = []

    # Find initial tan values
    if trig_function == 'tan':
        # Find simplest solution and next solution (to work with same code as sin and cos for finding further solutions)
        unsorted_values = [atan(value), atan(value) + pi]

    # Find initial sin values
    elif trig_function == 'sin':
        # Find simplest solution
        first_value = asin(value)
        # Correct for negative solution by finding equivalent positive solution
        if first_value < 0:
            first_value += 2 * pi
        # Add first solution to list of solutions
        unsorted_values.append(first_value)
        # Find second solution within first 2π radians (if it exists, 2π not included) and add to list of solutions
        if first_value == pi / 2 or first_value == pi * 1.5:
            pass
        elif 0 <= first_value < pi / 2:
            unsorted_values.append(pi - first_value)
        elif pi / 2 < first_value < pi:
            unsorted_values.append(pi - first_value)
        elif pi <= first_value < pi * 1.5:
            unsorted_values.append(2 * pi - (first_value - pi))
        elif pi * 1.5 < first_value < 2 * pi:
            unsorted_values.append((2 * pi - first_value) + pi)
    # Find initial cos values
    elif trig_function == 'cos':
        # Find simplest solution
        first_value = acos(value)
        # Correct for negative solution by finding equivalent positive solution
        if first_value < 0:
            first_value += 2 * pi
        # Add first solution to list of solutions
        unsorted_values.append(first_value)
        # Find second solution within first 2π radians (if it exists, 2π not included) and add to list of solutions
        if first_value == 0 or first_value == pi:
            pass
        elif 0 < first_value < pi / 2:
            unsorted_values.append(2 * pi - first_value)
        elif pi / 2 <= first_value < pi:
            unsorted_values.append(1.5 * pi - (first_value - pi / 2))
        elif pi < first_value < pi * 1.5:
            unsorted_values.append(pi / 2 + (1.5 * pi - first_value))
        elif pi * 1.5 <= first_value < 2 * pi:
            unsorted_values.append(first_value - 2 * pi)
    # Initialise sorted solution array with all values within first 2π radians
    solution = [] + unsorted_values
    # Use solutions within first 2π radians to find remaining solutions at 2π intervals from these values
    for each_solution in unsorted_values:
        # Find values above 2π radians less than specified maximum
        next_value = each_solution + 2 * pi
        while next_value <= maximum:
            solution.append(next_value)
            next_value += 2 * pi
        # Find values below 0 radians greater than specified minimum
        previous_value = each_solution - 2 * pi
        while previous_value >= minimum:
            solution.append(previous_value)
            previous_value -= 2 * pi
    # Sort full list of solutions
    solution.sort()
    # Return sorted list of all solutions
    return solution


if __name__ == '__main__':
    # If run as main can be used to test values
    f = input("Enter function: ")
    x = float(input("{}(x) = ".format(f)))
    lower = float(input("Enter lower boundary: "))
    upper = float(input("Enter upper boundary: "))
    print(solutions_in_range(f, x, lower, upper))
