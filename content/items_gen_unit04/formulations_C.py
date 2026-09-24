"""Answers to the unit 4 generated items in stems_C.json, worked from the stems alone.

Written by a blind solver, claude-opus-5-5, on the operator's delegation of 2026-09-24. Only the
stems file and the shared recheck helpers were read, never a key, a worked solution, a template or
a candidate record. Each statement item's four choices are copied into CHOICES below, and its
formulation returns the one choice the mathematics makes true, or a list of every such choice when
there is not exactly one.
"""
import sympy
from sympy import Rational, exp, pi, sqrt

from tools.key_recheck import derivative, related_rate, t, x, y


def choice_where(suffix, is_correct):
   matching = [choice for choice in CHOICES[suffix] if is_correct(choice)]
   has_single_match = len(matching) == 1

   if has_single_match:
      return matching[0]

   return matching


def decimal_text(value):
   is_whole = value == int(value)

   if is_whole:
      return str(int(value))

   return str(float(value))


def interpretation(suffix, order, value, time_unit):
   """The meaning of the order-th derivative of an amount, equal to value at one instant."""
   direction = "increasing" if value > 0 else "decreasing"
   rate_phrase = f" is {direction} at a rate of {decimal_text(abs(value))} "
   units_ending = f" per {time_unit}" * order + "."
   units_too_long = f" per {time_unit}" * (order + 1) + "."

   def is_correct(choice):
      at_one_instant = choice.startswith("At time t = ")
      states_rate = rate_phrase in choice
      speaks_of_rate_of_change = "the rate at which" in choice
      names_right_quantity = speaks_of_rate_of_change == (order == 2)
      has_right_units = choice.endswith(units_ending) and not choice.endswith(units_too_long)

      return at_one_instant and states_rate and names_right_quantity and has_right_units

   return choice_where(suffix, is_correct)


def average_rate(values, left, right):
   return Rational(values[right] - values[left], right - left)


def speed_statement(suffix, given, expression, at):
   velocity = derivative(expression, t) if given == "position" else expression
   velocity_value = velocity.subs(t, at)
   acceleration_value = derivative(velocity, t).subs(t, at)
   is_speeding_up = velocity_value * acceleration_value > 0
   change = "increasing" if is_speeding_up else "decreasing"
   agreement = "have the same sign" if is_speeding_up else "have opposite signs"
   expected = (
      f"The speed is {abs(velocity_value)} meters per second, and it is {change} at that time, because "
      f"\\( v({at}) = {velocity_value} \\) and \\( a({at}) = {acceleration_value} \\) {agreement}."
   )

   return choice_where(suffix, lambda choice: choice == expected)


def interval_text(left, right):
   return f"\\( \\left({sympy.latex(left)}, {sympy.latex(right)}\\right) \\)"


def joined(parts):
   if len(parts) == 1:
      return parts[0]

   return ", ".join(parts[:-1]) + " and " + parts[-1]


def direction_intervals(suffix, position, end, direction):
   velocity = derivative(position, t)
   roots = sorted(root for root in sympy.solve(velocity, t) if root.is_real and 0 < root < end)
   boundaries = [sympy.Integer(0)] + roots + [sympy.Integer(end)]
   wanted_sign = 1 if direction == "right" else -1
   moving = []

   for left, right in zip(boundaries, boundaries[1:]):
      sign_there = sympy.sign(velocity.subs(t, (left + right) / 2))

      if sign_there == wanted_sign:
         moving.append(interval_text(left, right))

   comparison = ">" if direction == "right" else "<"

   if moving:
      expected = (
         f"The particle is moving to the {direction} on {joined(moving)}, "
         f"because \\( v(t) {comparison} 0 \\) there."
      )
   else:
      expected = (
         f"The particle is never moving to the {direction} for \\( 0 < t < {end} \\), "
         f"because \\( v(t) {comparison} 0 \\) at no time in that interval."
      )

   return choice_where(suffix, lambda choice: choice == expected)


def rate_statement(suffix, given, expression, at, time_unit):
   rate = derivative(expression, t) if given == "amount" else expression
   value = sympy.N(rate.subs(t, at), 30)
   shown = f"{float(value):.3f}"
   magnitude = f"{abs(float(value)):.3f}"
   direction = "increasing" if value > 0 else "decreasing"

   def is_correct(choice):
      states_value = f"= {shown} \\)" in choice
      at_the_time = f"at time t = {at} " in choice
      states_rate = f"is {direction} at a rate of {magnitude} " in choice
      rate_per_time = choice.endswith(f" per {time_unit}.")
      speaks_of_velocity = "velocity" in choice

      return states_value and at_the_time and states_rate and rate_per_time and not speaks_of_velocity

   return choice_where(suffix, is_correct)


def cone_depth_rate(inflow, height_per_radius, depth):
   """V = pi h^3 / (3 k^2) when the height is k times the radius, so dh/dt = k^2 V' / (pi h^2)."""
   return sympy.nsimplify(inflow * height_per_radius ** 2) / (pi * depth ** 2)


def cube_volume_rate(edge_rate, edge):
   return 3 * edge ** 2 * edge_rate


def ladder_top_rate(length, base_rate, base):
   height = sqrt(length ** 2 - base ** 2)

   return sympy.nsimplify(-base * base_rate / height)


def sphere_volume_rate(radius_rate, radius):
   return 4 * pi * radius ** 2 * radius_rate


def circle_area_rate(radius_rate, radius):
   return 2 * pi * radius * radius_rate


def curve_rate(curve, point, horizontal_rate):
   return related_rate(curve, point, horizontal_rate, known="x")


def tangent_estimate(center, value, slope, target):
   return value + slope.subs(x, center) * (target - center)


def tangent_estimate_statement(suffix, center, value, slope, target):
   estimate = tangent_estimate(center, value, slope, target)
   bending = derivative(slope, x)
   left, right = sorted([sympy.nsimplify(center), target])
   bending_values = [bending.subs(x, left), bending.subs(x, right)]
   bending_values += [bending.subs(x, point) for point in sympy.solve(bending, x) if left < point < right]
   is_concave_up = all(value_there > 0 for value_there in bending_values)
   is_concave_down = all(value_there < 0 for value_there in bending_values)

   if not (is_concave_up or is_concave_down):
      raise ValueError("concavity changes between the center and the target")

   verdict = "an underestimate" if is_concave_up else "an overestimate"
   concavity = "concave up" if is_concave_up else "concave down"

   def is_correct(choice):
      shown = choice.split("\\( ", 1)[1].split(" \\)", 1)[0]
      states_estimate = sympy.nsimplify(shown) == estimate
      states_verdict = f"it is {verdict}," in choice
      reasons_by_concavity = concavity in choice

      return states_estimate and states_verdict and reasons_by_concavity

   return choice_where(suffix, is_correct)


def hermite_limit(conditions, build, point):
   """A cubic with the stated values and slopes stands in for f, which is enough because the limit
   depends only on those values and slopes."""
   coefficients = sympy.symbols("c0:4")
   cubic = sum(coefficient * x ** power for power, coefficient in enumerate(coefficients))
   equations = []

   for at, value, slope in conditions:
      equations.append(sympy.Eq(cubic.subs(x, at), value))
      equations.append(sympy.Eq(derivative(cubic, x).subs(x, at), slope))

   stand_in = cubic.subs(sympy.solve(equations, coefficients))

   def f(argument):
      return stand_in.subs(x, argument)

   return sympy.limit(build(f), x, point)


def position_from_velocity(velocity, start, start_position, finish):
   return start_position + sympy.integrate(velocity, (t, start, finish))


CHOICES = {
   "04001-00": [
      "At time t = 12 hours, the depth of snow on the field has changed by a total of -6 inches.",
      "At time t = 12 hours, the depth of snow on the field is decreasing at a rate of 6 hours per inch.",
      "At time t = 12 hours, the depth of snow on the field is decreasing at a rate of 6 inches per hour.",
      "At time t = 12 hours, the depth of snow on the field is increasing at a rate of 6 inches per hour.",
   ],
   "04001-01": [
      "At time t = 6 hours, the number of bacteria in the dish is decreasing at a rate of 7 bacteria per hour per hour.",
      "At time t = 6 hours, the rate at which the number of bacteria in the dish is changing is decreasing at a rate of 7 bacteria per hour per hour.",
      "At time t = 6 hours, the rate at which the number of bacteria in the dish is changing is decreasing at a rate of 7 bacteria per hour.",
      "At time t = 6 hours, the rate at which the number of bacteria in the dish is changing is increasing at a rate of 7 bacteria per hour per hour.",
   ],
   "04001-02": [
      "At time t = 3 minutes, the number of people in the line has changed by a total of 8 people.",
      "At time t = 3 minutes, the number of people in the line is increasing at a rate of 8 minutes per person.",
      "At time t = 3 minutes, the number of people in the line is increasing at a rate of 8 people per minute.",
      "Over the first 3 minutes, the number of people in the line is increasing at a rate of 8 people per minute.",
   ],
   "04001-03": [
      "At time t = 8 seconds, the height of the balloon has changed by a total of -6.5 meters.",
      "At time t = 8 seconds, the height of the balloon is decreasing at a rate of 6.5 meters per second.",
      "At time t = 8 seconds, the height of the balloon is decreasing at a rate of 6.5 seconds per meter.",
      "At time t = 8 seconds, the height of the balloon is increasing at a rate of 6.5 meters per second.",
   ],
   "04001-04": [
      "At time t = 4 seconds, the height of the balloon is decreasing at a rate of 0.5 meters per second per second.",
      "At time t = 4 seconds, the rate at which the height of the balloon is changing is decreasing at a rate of 0.5 meters per second per second.",
      "At time t = 4 seconds, the rate at which the height of the balloon is changing is decreasing at a rate of 0.5 meters per second.",
      "At time t = 4 seconds, the rate at which the height of the balloon is changing is increasing at a rate of 0.5 meters per second per second.",
   ],
   "04001-05": [
      "At time t = 9 minutes, the mass of the block of ice has changed by a total of 6.5 kilograms.",
      "At time t = 9 minutes, the mass of the block of ice is increasing at a rate of 6.5 kilograms per minute.",
      "At time t = 9 minutes, the mass of the block of ice is increasing at a rate of 6.5 minutes per kilogram.",
      "Over the first 9 minutes, the mass of the block of ice is increasing at a rate of 6.5 kilograms per minute.",
   ],
   "04001-06": [
      "At time t = 6 hours, the rate at which the volume of water in the tank is changing is increasing at a rate of 5 liters per hour per hour.",
      "At time t = 6 hours, the rate at which the volume of water in the tank is changing is increasing at a rate of 5 liters per hour.",
      "At time t = 6 hours, the volume of water in the tank is changing at a rate of 5 liters per hour.",
      "At time t = 6 hours, the volume of water in the tank is increasing at a rate of 5 liters per hour per hour.",
   ],
   "04001-07": [
      "At time t = 2 minutes, the temperature of the tea has changed by a total of 8 degrees Celsius.",
      "At time t = 2 minutes, the temperature of the tea is increasing at a rate of 8 degrees Celsius per minute.",
      "At time t = 2 minutes, the temperature of the tea is increasing at a rate of 8 minutes per degree Celsius.",
      "Over the first 2 minutes, the temperature of the tea is increasing at a rate of 8 degrees Celsius per minute.",
   ],
   "04001-08": [
      "At time t = 4 hours, the depth of snow on the field is decreasing at a rate of 2.5 inches per hour per hour.",
      "At time t = 4 hours, the rate at which the depth of snow on the field is changing is decreasing at a rate of 2.5 inches per hour per hour.",
      "At time t = 4 hours, the rate at which the depth of snow on the field is changing is decreasing at a rate of 2.5 inches per hour.",
      "At time t = 4 hours, the rate at which the depth of snow on the field is changing is increasing at a rate of 2.5 inches per hour per hour.",
   ],
   "04001-09": [
      "At time t = 6 hours, the amount of sand in the pile is decreasing at a rate of 2 cubic feet per hour per hour.",
      "At time t = 6 hours, the rate at which the amount of sand in the pile is changing is decreasing at a rate of 2 cubic feet per hour per hour.",
      "At time t = 6 hours, the rate at which the amount of sand in the pile is changing is decreasing at a rate of 2 cubic feet per hour.",
      "At time t = 6 hours, the rate at which the amount of sand in the pile is changing is increasing at a rate of 2 cubic feet per hour per hour.",
   ],
   "04001-10": [
      "At time t = 6 hours, the rate at which the volume of water in the tank is changing is decreasing at a rate of 4.5 liters per hour per hour.",
      "At time t = 6 hours, the rate at which the volume of water in the tank is changing is decreasing at a rate of 4.5 liters per hour.",
      "At time t = 6 hours, the rate at which the volume of water in the tank is changing is increasing at a rate of 4.5 liters per hour per hour.",
      "At time t = 6 hours, the volume of water in the tank is decreasing at a rate of 4.5 liters per hour per hour.",
   ],
   "04001-11": [
      "At time t = 5 hours, the depth of snow on the field has changed by a total of 3.5 inches.",
      "At time t = 5 hours, the depth of snow on the field is increasing at a rate of 3.5 hours per inch.",
      "At time t = 5 hours, the depth of snow on the field is increasing at a rate of 3.5 inches per hour.",
      "Over the first 5 hours, the depth of snow on the field is increasing at a rate of 3.5 inches per hour.",
   ],
   "04001-12": [
      "At time t = 3 minutes, the number of people in the line is decreasing at a rate of 3.5 people per minute per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is decreasing at a rate of 3.5 people per minute per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is decreasing at a rate of 3.5 people per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is increasing at a rate of 3.5 people per minute per minute.",
   ],
   "04001-13": [
      "At time t = 5 minutes, the mass of the block of ice has changed by a total of 6 kilograms.",
      "At time t = 5 minutes, the mass of the block of ice is increasing at a rate of 6 kilograms per minute.",
      "At time t = 5 minutes, the mass of the block of ice is increasing at a rate of 6 minutes per kilogram.",
      "Over the first 5 minutes, the mass of the block of ice is increasing at a rate of 6 kilograms per minute.",
   ],
   "04001-14": [
      "At time t = 7 minutes, the number of people in the line has changed by a total of -6.5 people.",
      "At time t = 7 minutes, the number of people in the line is decreasing at a rate of 6.5 minutes per person.",
      "At time t = 7 minutes, the number of people in the line is decreasing at a rate of 6.5 people per minute.",
      "At time t = 7 minutes, the number of people in the line is increasing at a rate of 6.5 people per minute.",
   ],
   "04001-15": [
      "At time t = 5 minutes, the number of people in the line has changed by a total of -2.5 people.",
      "At time t = 5 minutes, the number of people in the line is decreasing at a rate of 2.5 minutes per person.",
      "At time t = 5 minutes, the number of people in the line is decreasing at a rate of 2.5 people per minute.",
      "At time t = 5 minutes, the number of people in the line is increasing at a rate of 2.5 people per minute.",
   ],
   "04001-16": [
      "At time t = 7 hours, the depth of snow on the field has changed by a total of -0.5 inches.",
      "At time t = 7 hours, the depth of snow on the field is decreasing at a rate of 0.5 hours per inch.",
      "At time t = 7 hours, the depth of snow on the field is decreasing at a rate of 0.5 inches per hour.",
      "At time t = 7 hours, the depth of snow on the field is increasing at a rate of 0.5 inches per hour.",
   ],
   "04001-17": [
      "At time t = 4 minutes, the number of people in the line is changing at a rate of 4.5 people per minute.",
      "At time t = 4 minutes, the number of people in the line is increasing at a rate of 4.5 people per minute per minute.",
      "At time t = 4 minutes, the rate at which the number of people in the line is changing is increasing at a rate of 4.5 people per minute per minute.",
      "At time t = 4 minutes, the rate at which the number of people in the line is changing is increasing at a rate of 4.5 people per minute.",
   ],
   "04001-18": [
      "At time t = 8 minutes, the mass of the block of ice is changing at a rate of 5 kilograms per minute.",
      "At time t = 8 minutes, the mass of the block of ice is increasing at a rate of 5 kilograms per minute per minute.",
      "At time t = 8 minutes, the rate at which the mass of the block of ice is changing is increasing at a rate of 5 kilograms per minute per minute.",
      "At time t = 8 minutes, the rate at which the mass of the block of ice is changing is increasing at a rate of 5 kilograms per minute.",
   ],
   "04001-19": [
      "At time t = 12 seconds, the height of the balloon is decreasing at a rate of 8.5 meters per second per second.",
      "At time t = 12 seconds, the rate at which the height of the balloon is changing is decreasing at a rate of 8.5 meters per second per second.",
      "At time t = 12 seconds, the rate at which the height of the balloon is changing is decreasing at a rate of 8.5 meters per second.",
      "At time t = 12 seconds, the rate at which the height of the balloon is changing is increasing at a rate of 8.5 meters per second per second.",
   ],
   "04001-20": [
      "At time t = 3 minutes, the number of people in the line is decreasing at a rate of 7 people per minute per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is decreasing at a rate of 7 people per minute per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is decreasing at a rate of 7 people per minute.",
      "At time t = 3 minutes, the rate at which the number of people in the line is changing is increasing at a rate of 7 people per minute per minute.",
   ],
   "04001-21": [
      "At time t = 4 hours, the number of bacteria in the dish has changed by a total of -9 bacteria.",
      "At time t = 4 hours, the number of bacteria in the dish is decreasing at a rate of 9 bacteria per hour.",
      "At time t = 4 hours, the number of bacteria in the dish is decreasing at a rate of 9 hours per bacterium.",
      "At time t = 4 hours, the number of bacteria in the dish is increasing at a rate of 9 bacteria per hour.",
   ],
   "04003-00": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 18 \\) have opposite signs.",
      "The speed is 11 meters per second, and it is increasing at that time, because \\( v(1) = -11 \\) and \\( a(1) = -5 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 18 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(1) = 18 \\) is positive, so the particle is speeding up.",
   ],
   "04003-01": [
      "The speed is -1 meters per second, and it is increasing at that time, because \\( v(1) = -1 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 1 meters per second, and it is decreasing at that time, because \\( a(1) = -8 \\) is negative, so the particle is slowing down.",
      "The speed is 1 meters per second, and it is increasing at that time, because \\( v(1) = -1 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -12 \\) have the same sign.",
   ],
   "04003-02": [
      "The speed is -9 meters per second, and it is decreasing at that time, because \\( v(1) = -9 \\) and \\( a(1) = 2 \\) have opposite signs.",
      "The speed is 15 meters per second, and it is increasing at that time, because \\( v(1) = -15 \\) and \\( a(1) = -9 \\) have the same sign.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( v(1) = -9 \\) and \\( a(1) = 2 \\) have opposite signs.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( a(1) = 2 \\) is positive, so the particle is speeding up.",
   ],
   "04003-03": [
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(3) = -14 \\) and \\( a(3) = -6 \\) have the same sign.",
      "The speed is 53 meters per second, and it is increasing at that time, because \\( v(3) = 53 \\) and \\( a(3) = 6 \\) have the same sign.",
      "The speed is 6 meters per second, and it is decreasing at that time, because \\( a(3) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 6 meters per second, and it is decreasing at that time, because \\( v(3) = 6 \\) and \\( a(3) = -14 \\) have opposite signs.",
   ],
   "04003-04": [
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = -6 \\) have the same sign.",
      "The speed is 35 meters per second, and it is increasing at that time, because \\( v(2) = 35 \\) and \\( a(2) = 9 \\) have the same sign.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( a(2) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = -14 \\) have opposite signs.",
   ],
   "04003-05": [
      "The speed is 14 meters per second, and it is decreasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = 6 \\) have opposite signs.",
      "The speed is 20 meters per second, and it is increasing at that time, because \\( v(2) = 20 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 6 meters per second, and it is increasing at that time, because \\( a(2) = 20 \\) is positive, so the particle is speeding up.",
      "The speed is 6 meters per second, and it is increasing at that time, because \\( v(2) = 6 \\) and \\( a(2) = 20 \\) have the same sign.",
   ],
   "04003-06": [
      "The speed is -9 meters per second, and it is increasing at that time, because \\( v(3) = -9 \\) and \\( a(3) = -24 \\) have the same sign.",
      "The speed is 51 meters per second, and it is decreasing at that time, because \\( v(3) = 51 \\) and \\( a(3) = -9 \\) have opposite signs.",
      "The speed is 9 meters per second, and it is decreasing at that time, because \\( a(3) = -24 \\) is negative, so the particle is slowing down.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( v(3) = -9 \\) and \\( a(3) = -24 \\) have the same sign.",
   ],
   "04003-07": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(1) = -7 \\) and \\( a(1) = 4 \\) have opposite signs.",
      "The speed is 3 meters per second, and it is increasing at that time, because \\( v(1) = -3 \\) and \\( a(1) = -7 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(1) = -7 \\) and \\( a(1) = 4 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(1) = 4 \\) is positive, so the particle is speeding up.",
   ],
   "04003-08": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(3) = -5 \\) and \\( a(3) = 22 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(3) = -5 \\) and \\( a(3) = 22 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(3) = 22 \\) is positive, so the particle is speeding up.",
      "The speed is 89 meters per second, and it is increasing at that time, because \\( v(3) = -89 \\) and \\( a(3) = -5 \\) have the same sign.",
   ],
   "04003-09": [
      "The speed is -2 meters per second, and it is increasing at that time, because \\( v(3) = -2 \\) and \\( a(3) = -40 \\) have the same sign.",
      "The speed is 2 meters per second, and it is decreasing at that time, because \\( a(3) = -40 \\) is negative, so the particle is slowing down.",
      "The speed is 2 meters per second, and it is increasing at that time, because \\( v(3) = -2 \\) and \\( a(3) = -40 \\) have the same sign.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(3) = -40 \\) and \\( a(3) = -32 \\) have the same sign.",
   ],
   "04003-10": [
      "The speed is -8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -2 \\) have the same sign.",
      "The speed is 2 meters per second, and it is increasing at that time, because \\( v(1) = -2 \\) and \\( a(1) = -8 \\) have the same sign.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( a(1) = -2 \\) is negative, so the particle is slowing down.",
      "The speed is 8 meters per second, and it is increasing at that time, because \\( v(1) = -8 \\) and \\( a(1) = -2 \\) have the same sign.",
   ],
   "04003-11": [
      "The speed is 30 meters per second, and it is increasing at that time, because \\( v(3) = -30 \\) and \\( a(3) = -12 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( a(3) = -30 \\) is negative, so the particle is slowing down.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(3) = 5 \\) and \\( a(3) = -30 \\) have opposite signs.",
      "The speed is 91 meters per second, and it is increasing at that time, because \\( v(3) = 91 \\) and \\( a(3) = 5 \\) have the same sign.",
   ],
   "04003-12": [
      "The speed is -3 meters per second, and it is increasing at that time, because \\( v(3) = -3 \\) and \\( a(3) = -30 \\) have the same sign.",
      "The speed is 3 meters per second, and it is decreasing at that time, because \\( a(3) = -30 \\) is negative, so the particle is slowing down.",
      "The speed is 3 meters per second, and it is increasing at that time, because \\( v(3) = -3 \\) and \\( a(3) = -30 \\) have the same sign.",
      "The speed is 72 meters per second, and it is decreasing at that time, because \\( v(3) = 72 \\) and \\( a(3) = -3 \\) have opposite signs.",
   ],
   "04003-13": [
      "The speed is -5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 10 \\) have opposite signs.",
      "The speed is 15 meters per second, and it is increasing at that time, because \\( v(1) = -15 \\) and \\( a(1) = -5 \\) have the same sign.",
      "The speed is 5 meters per second, and it is decreasing at that time, because \\( v(1) = -5 \\) and \\( a(1) = 10 \\) have opposite signs.",
      "The speed is 5 meters per second, and it is increasing at that time, because \\( a(1) = 10 \\) is positive, so the particle is speeding up.",
   ],
   "04003-14": [
      "The speed is -7 meters per second, and it is increasing at that time, because \\( v(2) = -7 \\) and \\( a(2) = -14 \\) have the same sign.",
      "The speed is 14 meters per second, and it is increasing at that time, because \\( v(2) = -14 \\) and \\( a(2) = -18 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( a(2) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( v(2) = -7 \\) and \\( a(2) = -14 \\) have the same sign.",
   ],
   "04003-15": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 10 \\) have opposite signs.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(3) = -40 \\) and \\( a(3) = -7 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 10 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(3) = 10 \\) is positive, so the particle is speeding up.",
   ],
   "04003-16": [
      "The speed is -7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 47 \\) have opposite signs.",
      "The speed is 47 meters per second, and it is increasing at that time, because \\( v(3) = 47 \\) and \\( a(3) = 26 \\) have the same sign.",
      "The speed is 7 meters per second, and it is decreasing at that time, because \\( v(3) = -7 \\) and \\( a(3) = 47 \\) have opposite signs.",
      "The speed is 7 meters per second, and it is increasing at that time, because \\( a(3) = 47 \\) is positive, so the particle is speeding up.",
   ],
   "04003-17": [
      "The speed is -1 meters per second, and it is increasing at that time, because \\( v(3) = -1 \\) and \\( a(3) = -28 \\) have the same sign.",
      "The speed is 1 meters per second, and it is decreasing at that time, because \\( a(3) = -28 \\) is negative, so the particle is slowing down.",
      "The speed is 1 meters per second, and it is increasing at that time, because \\( v(3) = -1 \\) and \\( a(3) = -28 \\) have the same sign.",
      "The speed is 69 meters per second, and it is decreasing at that time, because \\( v(3) = 69 \\) and \\( a(3) = -1 \\) have opposite signs.",
   ],
   "04003-18": [
      "The speed is -4 meters per second, and it is decreasing at that time, because \\( v(2) = -4 \\) and \\( a(2) = 40 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is decreasing at that time, because \\( v(2) = -4 \\) and \\( a(2) = 40 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( a(2) = 40 \\) is positive, so the particle is speeding up.",
      "The speed is 40 meters per second, and it is increasing at that time, because \\( v(2) = 40 \\) and \\( a(2) = 30 \\) have the same sign.",
   ],
   "04003-19": [
      "The speed is -4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -14 \\) have the same sign.",
      "The speed is 2 meters per second, and it is decreasing at that time, because \\( v(1) = 2 \\) and \\( a(1) = -4 \\) have opposite signs.",
      "The speed is 4 meters per second, and it is decreasing at that time, because \\( a(1) = -14 \\) is negative, so the particle is slowing down.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -14 \\) have the same sign.",
   ],
   "04003-20": [
      "The speed is 10 meters per second, and it is decreasing at that time, because \\( v(2) = -10 \\) and \\( a(2) = 9 \\) have opposite signs.",
      "The speed is 24 meters per second, and it is increasing at that time, because \\( v(2) = 24 \\) and \\( a(2) = 12 \\) have the same sign.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( a(2) = 24 \\) is positive, so the particle is speeding up.",
      "The speed is 9 meters per second, and it is increasing at that time, because \\( v(2) = 9 \\) and \\( a(2) = 24 \\) have the same sign.",
   ],
   "04003-21": [
      "The speed is 10 meters per second, and it is increasing at that time, because \\( v(1) = 10 \\) and \\( a(1) = 8 \\) have the same sign.",
      "The speed is 4 meters per second, and it is increasing at that time, because \\( v(1) = -4 \\) and \\( a(1) = -12 \\) have the same sign.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( a(1) = -4 \\) is negative, so the particle is slowing down.",
      "The speed is 8 meters per second, and it is decreasing at that time, because \\( v(1) = 8 \\) and \\( a(1) = -4 \\) have opposite signs.",
   ],
   "04004-00": [
      "The particle is moving to the left on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 5\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{11}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left on \\( \\left(3, 8\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(3, \\frac{13}{3}\\right) \\), because \\( v(t) < 0 \\) there.",
   ],
   "04004-01": [
      "The particle is moving to the right on \\( \\left(0, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{2}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right on \\( \\left(\\frac{1}{3}, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 7 \\), because \\( x(t) > 0 \\) at no time in that interval.",
   ],
   "04004-02": [
      "The particle is moving to the right on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{11}{3}\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(3, 5\\right) \\) and \\( \\left(5, 9\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{13}{3}, 9\\right) \\), because v(t) is increasing there.",
   ],
   "04004-03": [
      "The particle is moving to the right on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(4, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{10}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04004-04": [
      "The particle is moving to the left on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(4, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(\\frac{10}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-05": [
      "The particle is moving to the right on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{7}{3}\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(1, 5\\right) \\) and \\( \\left(5, 6\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{11}{3}, 6\\right) \\), because v(t) is increasing there.",
   ],
   "04004-06": [
      "The particle is moving to the right on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{10}{3}, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 2\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(4, 8\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{8}{3}, 8\\right) \\), because v(t) is increasing there.",
   ],
   "04004-07": [
      "The particle is moving to the left on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{7}{3}\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(1, 5\\right) \\) and \\( \\left(5, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(\\frac{11}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-08": [
      "The particle is moving to the left on \\( \\left(0, 1\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{5}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left on \\( \\left(\\frac{4}{3}, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 10 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-09": [
      "The particle is moving to the left on \\( \\left(0, 4\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, 4\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{4}{3}\\right) \\) and \\( \\left(4, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(\\frac{8}{3}, 9\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-10": [
      "The particle is moving to the left on \\( \\left(0, 1\\right) \\) and \\( \\left(1, 2\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{4}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left on \\( \\left(1, \\frac{5}{3}\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 9 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-11": [
      "The particle is moving to the right on \\( \\left(0, \\frac{10}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right on \\( \\left(\\frac{5}{3}, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 10 \\), because \\( v(t) > 0 \\) at no time in that interval.",
      "The particle is never moving to the right for \\( 0 < t < 10 \\), because \\( x(t) > 0 \\) at no time in that interval.",
   ],
   "04004-12": [
      "The particle is moving to the right on \\( \\left(0, 5\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{11}{3}\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(3, 5\\right) \\) and \\( \\left(5, 8\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{13}{3}, 8\\right) \\), because v(t) is increasing there.",
   ],
   "04004-13": [
      "The particle is moving to the right on \\( \\left(0, 1\\right) \\) and \\( \\left(\\frac{7}{3}, 7\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 1\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(3, 7\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{5}{3}, 7\\right) \\), because v(t) is increasing there.",
   ],
   "04004-14": [
      "The particle is moving to the right on \\( \\left(0, 4\\right) \\) and \\( \\left(\\frac{16}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 4\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(6, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{14}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04004-15": [
      "The particle is moving to the right on \\( \\left(0, 1\\right) \\) and \\( \\left(1, 5\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{1}{3}\\right) \\) and \\( \\left(1, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(1, 5\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{2}{3}, 5\\right) \\), because v(t) is increasing there.",
   ],
   "04004-16": [
      "The particle is moving to the right on \\( \\left(0, 4\\right) \\) and \\( \\left(\\frac{16}{3}, 7\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 4\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(6, 7\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{14}{3}, 7\\right) \\), because v(t) is increasing there.",
   ],
   "04004-17": [
      "The particle is moving to the left on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, 3\\right) \\) and \\( \\left(\\frac{11}{3}, 7\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(4, 7\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(\\frac{10}{3}, 7\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-18": [
      "The particle is moving to the left on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{14}{3}, 9\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(6, 9\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(\\frac{10}{3}, 9\\right) \\), because v(t) is decreasing there.",
   ],
   "04004-19": [
      "The particle is moving to the left on \\( \\left(0, 1\\right) \\), because \\( x(t) < 0 \\) there.",
      "The particle is moving to the left on \\( \\left(0, \\frac{5}{3}\\right) \\), because v(t) is decreasing there.",
      "The particle is moving to the left on \\( \\left(\\frac{4}{3}, 2\\right) \\), because \\( v(t) < 0 \\) there.",
      "The particle is never moving to the left for \\( 0 < t < 6 \\), because \\( v(t) < 0 \\) at no time in that interval.",
   ],
   "04004-20": [
      "The particle is moving to the right on \\( \\left(0, 3\\right) \\) and \\( \\left(3, 4\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, \\frac{10}{3}\\right) \\), because v(t) is increasing there.",
      "The particle is moving to the right on \\( \\left(3, \\frac{11}{3}\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is never moving to the right for \\( 0 < t < 9 \\), because \\( v(t) > 0 \\) at no time in that interval.",
   ],
   "04004-21": [
      "The particle is moving to the right on \\( \\left(0, 2\\right) \\) and \\( \\left(\\frac{10}{3}, 10\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(0, 2\\right) \\), because \\( v(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(4, 10\\right) \\), because \\( x(t) > 0 \\) there.",
      "The particle is moving to the right on \\( \\left(\\frac{8}{3}, 10\\right) \\), because v(t) is increasing there.",
   ],
   "04005-00": [
      "\\( H'(3) = -3.543 \\), so at 3 the function H is decreasing at a rate of 3.543 degrees Celsius per minute.",
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 3.543 degrees Celsius per minute.",
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 3.543 minutes per degree Celsius.",
      "\\( H'(3) = -3.543 \\), so at time t = 3 minutes the temperature of the liquid is moving with a velocity of -3.543 degrees Celsius per minute.",
   ],
   "04005-01": [
      "\\( N'(4) = -2.274 \\), so at 4 the function N is decreasing at a rate of 2.274 people per minute.",
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is decreasing at a rate of 2.274 minutes per person.",
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is decreasing at a rate of 2.274 people per minute.",
      "\\( N'(4) = -2.274 \\), so at time t = 4 minutes the number of people inside the museum is moving with a velocity of -2.274 people per minute.",
   ],
   "04005-02": [
      "\\( H'(5) = 3.639 \\), so at 5 the function H is increasing at a rate of 3.639 degrees Celsius per minute.",
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is increasing at a rate of 3.639 degrees Celsius per minute.",
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is increasing at a rate of 3.639 minutes per degree Celsius.",
      "\\( H'(5) = 3.639 \\), so at time t = 5 minutes the temperature of the liquid is moving with a velocity of 3.639 degrees Celsius per minute.",
   ],
   "04005-03": [
      "\\( B'(9) = 3.253 \\), so at 9 the function B is increasing at a rate of 3.253 watt-hours per minute.",
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is increasing at a rate of 3.253 minutes per watt-hour.",
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is increasing at a rate of 3.253 watt-hours per minute.",
      "\\( B'(9) = 3.253 \\), so at time t = 9 minutes the charge stored in the battery is moving with a velocity of 3.253 watt-hours per minute.",
   ],
   "04005-04": [
      "\\( B'(5) = 3.639 \\), so at 5 the function B is increasing at a rate of 3.639 watt-hours per minute.",
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is increasing at a rate of 3.639 minutes per watt-hour.",
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is increasing at a rate of 3.639 watt-hours per minute.",
      "\\( B'(5) = 3.639 \\), so at time t = 5 minutes the charge stored in the battery is moving with a velocity of 3.639 watt-hours per minute.",
   ],
   "04005-05": [
      "\\( C'(8) = 2.529 \\), so at 8 the function C is increasing at a rate of 2.529 milligrams per liter per hour.",
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is increasing at a rate of 2.529 hours per milligram per liter.",
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is increasing at a rate of 2.529 milligrams per liter per hour.",
      "\\( C'(8) = 2.529 \\), so at time t = 8 hours the concentration of the medicine is moving with a velocity of 2.529 milligrams per liter per hour.",
   ],
   "04005-06": [
      "\\( L'(7) = 2.558 \\), so at 7 the function L is increasing at a rate of 2.558 parts per billion per day.",
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is increasing at a rate of 2.558 days per part per billion.",
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is increasing at a rate of 2.558 parts per billion per day.",
      "\\( L'(7) = 2.558 \\), so at time t = 7 days the level of the pollutant is moving with a velocity of 2.558 parts per billion per day.",
   ],
   "04005-07": [
      "\\( W'(6) = -4.044 \\), so at 6 the function W is decreasing at a rate of 4.044 hundreds of gallons per hour.",
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is decreasing at a rate of 4.044 hours per hundred gallons.",
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is decreasing at a rate of 4.044 hundreds of gallons per hour.",
      "\\( W'(6) = -4.044 \\), so at time t = 6 hours the amount of water in the tank is moving with a velocity of -4.044 hundreds of gallons per hour.",
   ],
   "04005-08": [
      "\\( C'(2) = 9.384 \\), so at 2 the function C is increasing at a rate of 9.384 milligrams per liter per hour.",
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is increasing at a rate of 9.384 hours per milligram per liter.",
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is increasing at a rate of 9.384 milligrams per liter per hour.",
      "\\( C'(2) = 9.384 \\), so at time t = 2 hours the concentration of the medicine is moving with a velocity of 9.384 milligrams per liter per hour.",
   ],
   "04005-09": [
      "\\( C'(6) = 3.372 \\), so at 6 the function C is increasing at a rate of 3.372 milligrams per liter per hour.",
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is increasing at a rate of 3.372 hours per milligram per liter.",
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is increasing at a rate of 3.372 milligrams per liter per hour.",
      "\\( C'(6) = 3.372 \\), so at time t = 6 hours the concentration of the medicine is moving with a velocity of 3.372 milligrams per liter per hour.",
   ],
   "04005-10": [
      "\\( H'(3) = -4.868 \\), so at 3 the function H is decreasing at a rate of 4.868 degrees Celsius per minute.",
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 4.868 degrees Celsius per minute.",
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is decreasing at a rate of 4.868 minutes per degree Celsius.",
      "\\( H'(3) = -4.868 \\), so at time t = 3 minutes the temperature of the liquid is moving with a velocity of -4.868 degrees Celsius per minute.",
   ],
   "04005-11": [
      "\\( B'(5) = -4.708 \\), so at 5 the function B is decreasing at a rate of 4.708 watt-hours per minute.",
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is decreasing at a rate of 4.708 minutes per watt-hour.",
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is decreasing at a rate of 4.708 watt-hours per minute.",
      "\\( B'(5) = -4.708 \\), so at time t = 5 minutes the charge stored in the battery is moving with a velocity of -4.708 watt-hours per minute.",
   ],
   "04005-12": [
      "\\( W'(9) = -0.787 \\), so at 9 the function W is decreasing at a rate of 0.787 hundreds of gallons per hour.",
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is decreasing at a rate of 0.787 hours per hundred gallons.",
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is decreasing at a rate of 0.787 hundreds of gallons per hour.",
      "\\( W'(9) = -0.787 \\), so at time t = 9 hours the amount of water in the tank is moving with a velocity of -0.787 hundreds of gallons per hour.",
   ],
   "04005-13": [
      "\\( H'(7) = 3.476 \\), so at 7 the function H is increasing at a rate of 3.476 degrees Celsius per minute.",
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is increasing at a rate of 3.476 degrees Celsius per minute.",
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is increasing at a rate of 3.476 minutes per degree Celsius.",
      "\\( H'(7) = 3.476 \\), so at time t = 7 minutes the temperature of the liquid is moving with a velocity of 3.476 degrees Celsius per minute.",
   ],
   "04005-14": [
      "\\( N'(3) = 3.842 \\), so at 3 the function N is increasing at a rate of 3.842 people per minute.",
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is increasing at a rate of 3.842 minutes per person.",
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is increasing at a rate of 3.842 people per minute.",
      "\\( N'(3) = 3.842 \\), so at time t = 3 minutes the number of people inside the museum is moving with a velocity of 3.842 people per minute.",
   ],
   "04005-15": [
      "\\( W'(7) = 2.325 \\), so at 7 the function W is increasing at a rate of 2.325 hundreds of gallons per hour.",
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is increasing at a rate of 2.325 hours per hundred gallons.",
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is increasing at a rate of 2.325 hundreds of gallons per hour.",
      "\\( W'(7) = 2.325 \\), so at time t = 7 hours the amount of water in the tank is moving with a velocity of 2.325 hundreds of gallons per hour.",
   ],
   "04005-16": [
      "\\( L'(5) = 4.782 \\), so at 5 the function L is increasing at a rate of 4.782 parts per billion per day.",
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is increasing at a rate of 4.782 days per part per billion.",
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is increasing at a rate of 4.782 parts per billion per day.",
      "\\( L'(5) = 4.782 \\), so at time t = 5 days the level of the pollutant is moving with a velocity of 4.782 parts per billion per day.",
   ],
   "04005-17": [
      "\\( B'(4) = -5.841 \\), so at 4 the function B is decreasing at a rate of 5.841 watt-hours per minute.",
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is decreasing at a rate of 5.841 minutes per watt-hour.",
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is decreasing at a rate of 5.841 watt-hours per minute.",
      "\\( B'(4) = -5.841 \\), so at time t = 4 minutes the charge stored in the battery is moving with a velocity of -5.841 watt-hours per minute.",
   ],
   "04005-18": [
      "\\( B'(6) = -1.769 \\), so at 6 the function B is decreasing at a rate of 1.769 watt-hours per minute.",
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is decreasing at a rate of 1.769 minutes per watt-hour.",
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is decreasing at a rate of 1.769 watt-hours per minute.",
      "\\( B'(6) = -1.769 \\), so at time t = 6 minutes the charge stored in the battery is moving with a velocity of -1.769 watt-hours per minute.",
   ],
   "04005-19": [
      "\\( H'(4) = 4.180 \\), so at 4 the function H is increasing at a rate of 4.180 degrees Celsius per minute.",
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is increasing at a rate of 4.180 degrees Celsius per minute.",
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is increasing at a rate of 4.180 minutes per degree Celsius.",
      "\\( H'(4) = 4.180 \\), so at time t = 4 minutes the temperature of the liquid is moving with a velocity of 4.180 degrees Celsius per minute.",
   ],
   "04005-20": [
      "\\( H'(8) = 2.471 \\), so at 8 the function H is increasing at a rate of 2.471 degrees Celsius per minute.",
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is increasing at a rate of 2.471 degrees Celsius per minute.",
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is increasing at a rate of 2.471 minutes per degree Celsius.",
      "\\( H'(8) = 2.471 \\), so at time t = 8 minutes the temperature of the liquid is moving with a velocity of 2.471 degrees Celsius per minute.",
   ],
   "04005-21": [
      "\\( C'(3) = 6.571 \\), so at 3 the function C is increasing at a rate of 6.571 milligrams per liter per hour.",
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is increasing at a rate of 6.571 hours per milligram per liter.",
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is increasing at a rate of 6.571 milligrams per liter per hour.",
      "\\( C'(3) = 6.571 \\), so at time t = 3 hours the concentration of the medicine is moving with a velocity of 6.571 milligrams per liter per hour.",
   ],
   "04008-06": [
      "The approximation is \\( -1 \\), and it is an underestimate, because \\( f''(x) = 2 x \\) is positive for x > 0, so the graph of f is concave up and lies above its tangent line there.",
      "The approximation is \\( -2.312 \\), and it is an underestimate, because \\( f''(x) = 2 x \\) is positive for x > 0, so the graph of f is concave up and lies above its tangent line there.",
      "The approximation is \\( -2.4 \\), and it is an overestimate, because \\( f'(1) = -7 \\) is negative, so f is decreasing and its values fall below the starting value f(1).",
      "The approximation is \\( -2.4 \\), and it is an underestimate, because \\( f''(x) = 2 x \\) is positive for x > 0, so the graph of f is concave up and lies above its tangent line there.",
   ],
   "04008-14": [
      "The approximation is \\( -5.7 \\), and it is an overestimate, because \\( f''(x) = - 6 x \\) is negative for x > 0, so the graph of f is concave down and lies below its tangent line there.",
      "The approximation is \\( -5.7 \\), and it is an underestimate, because \\( f'(1) = 3 \\) is positive, so f is increasing and its values rise above the starting value f(1).",
      "The approximation is \\( -5.763 \\), and it is an overestimate, because \\( f''(x) = - 6 x \\) is negative for x > 0, so the graph of f is concave down and lies below its tangent line there.",
      "The approximation is \\( -6 \\), and it is an overestimate, because \\( f''(x) = - 6 x \\) is negative for x > 0, so the graph of f is concave down and lies below its tangent line there.",
   ],
}


BY_SUFFIX = {
   "04001-00": lambda: interpretation("04001-00", order=1, value=Rational("-6"), time_unit="hour"),
   "04001-01": lambda: interpretation("04001-01", order=2, value=Rational("-7"), time_unit="hour"),
   "04001-02": lambda: interpretation("04001-02", order=1, value=Rational("8"), time_unit="minute"),
   "04001-03": lambda: interpretation("04001-03", order=1, value=Rational("-6.5"), time_unit="second"),
   "04001-04": lambda: interpretation("04001-04", order=2, value=Rational("-0.5"), time_unit="second"),
   "04001-05": lambda: interpretation("04001-05", order=1, value=Rational("6.5"), time_unit="minute"),
   "04001-06": lambda: interpretation("04001-06", order=2, value=Rational("5"), time_unit="hour"),
   "04001-07": lambda: interpretation("04001-07", order=1, value=Rational("8"), time_unit="minute"),
   "04001-08": lambda: interpretation("04001-08", order=2, value=Rational("-2.5"), time_unit="hour"),
   "04001-09": lambda: interpretation("04001-09", order=2, value=Rational("-2"), time_unit="hour"),
   "04001-10": lambda: interpretation("04001-10", order=2, value=Rational("-4.5"), time_unit="hour"),
   "04001-11": lambda: interpretation("04001-11", order=1, value=Rational("3.5"), time_unit="hour"),
   "04001-12": lambda: interpretation("04001-12", order=2, value=Rational("-3.5"), time_unit="minute"),
   "04001-13": lambda: interpretation("04001-13", order=1, value=Rational("6"), time_unit="minute"),
   "04001-14": lambda: interpretation("04001-14", order=1, value=Rational("-6.5"), time_unit="minute"),
   "04001-15": lambda: interpretation("04001-15", order=1, value=Rational("-2.5"), time_unit="minute"),
   "04001-16": lambda: interpretation("04001-16", order=1, value=Rational("-0.5"), time_unit="hour"),
   "04001-17": lambda: interpretation("04001-17", order=2, value=Rational("4.5"), time_unit="minute"),
   "04001-18": lambda: interpretation("04001-18", order=2, value=Rational("5"), time_unit="minute"),
   "04001-19": lambda: interpretation("04001-19", order=2, value=Rational("-8.5"), time_unit="second"),
   "04001-20": lambda: interpretation("04001-20", order=2, value=Rational("-7"), time_unit="minute"),
   "04001-21": lambda: interpretation("04001-21", order=1, value=Rational("-9"), time_unit="hour"),
   "04002-00": lambda: average_rate({1: 66, 5: 54, 9: 48, 10: 35, 11: 34}, 5, 10),
   "04002-01": lambda: average_rate({1: 20, 2: 29, 4: 56, 10: 60, 12: 66}, 2, 10),
   "04002-02": lambda: average_rate({3: 27, 5: 46, 7: 54, 9: 65, 10: 85}, 5, 9),
   "04002-03": lambda: average_rate({2: 88, 5: 82, 7: 79, 8: 44, 12: 36}, 5, 8),
   "04002-04": lambda: average_rate({0: 81, 2: 65, 5: 64, 11: 49, 12: 43}, 2, 11),
   "04002-05": lambda: average_rate({0: 82, 2: 67, 5: 50, 9: 27, 11: 18}, 2, 9),
   "04002-06": lambda: average_rate({5: 77, 9: 61, 10: 49, 11: 16, 12: 10}, 9, 11),
   "04002-07": lambda: average_rate({1: 73, 2: 71, 5: 64, 6: 59, 9: 13}, 2, 6),
   "04002-08": lambda: average_rate({2: 14, 5: 15, 7: 47, 8: 56, 12: 57}, 5, 8),
   "04002-09": lambda: average_rate({0: 41, 2: 32, 7: 30, 9: 28, 11: 26}, 2, 9),
   "04002-10": lambda: average_rate({0: 18, 2: 25, 3: 36, 6: 73, 8: 89}, 2, 6),
   "04002-11": lambda: average_rate({3: 12, 7: 28, 8: 49, 10: 65, 12: 89}, 7, 10),
   "04002-12": lambda: average_rate({0: 63, 1: 49, 7: 46, 9: 28, 11: 18}, 1, 9),
   "04002-13": lambda: average_rate({0: 10, 2: 53, 8: 54, 11: 61, 12: 83}, 2, 11),
   "04002-14": lambda: average_rate({1: 10, 5: 45, 7: 57, 9: 73, 11: 74}, 5, 9),
   "04002-15": lambda: average_rate({0: 55, 3: 51, 4: 27, 10: 20, 11: 10}, 3, 10),
   "04002-16": lambda: average_rate({2: 17, 3: 26, 4: 27, 9: 78, 12: 79}, 3, 9),
   "04002-17": lambda: average_rate({0: 26, 3: 30, 7: 41, 9: 50, 12: 51}, 3, 9),
   "04002-18": lambda: average_rate({5: 88, 6: 54, 8: 46, 11: 40, 12: 24}, 6, 11),
   "04002-19": lambda: average_rate({1: 28, 2: 45, 3: 60, 4: 82, 5: 90}, 2, 4),
   "04002-20": lambda: average_rate({1: 26, 3: 38, 8: 41, 9: 60, 10: 66}, 3, 9),
   "04002-21": lambda: average_rate({1: 81, 7: 78, 10: 29, 11: 25, 12: 22}, 7, 11),
   "04003-00": lambda: speed_statement("04003-00", "position", 2*t**3 + 3*t**2 - 17*t + 1, 1),
   "04003-01": lambda: speed_statement("04003-01", "velocity", -t**3 - 3*t**2 + t + 2, 1),
   "04003-02": lambda: speed_statement("04003-02", "position", t**3 - 2*t**2 - 8*t - 6, 1),
   "04003-03": lambda: speed_statement("04003-03", "position", -t**3 + 2*t**2 + 21*t - 1, 3),
   "04003-04": lambda: speed_statement("04003-04", "position", -t**3 - t**2 + 25*t - 3, 2),
   "04003-05": lambda: speed_statement("04003-05", "position", 2*t**3 - 2*t**2 - 10*t - 2, 2),
   "04003-06": lambda: speed_statement("04003-06", "position", -t**3 - 3*t**2 + 36*t - 3, 3),
   "04003-07": lambda: speed_statement("04003-07", "position", t**3 - t**2 - 8*t + 5, 1),
   "04003-08": lambda: speed_statement("04003-08", "position", t**3 + 2*t**2 - 44*t - 2, 3),
   "04003-09": lambda: speed_statement("04003-09", "velocity", -2*t**3 + 2*t**2 + 2*t + 28, 3),
   "04003-10": lambda: speed_statement("04003-10", "velocity", -t**3 - t**2 + 3*t - 9, 1),
   "04003-11": lambda: speed_statement("04003-11", "position", -2*t**3 + 3*t**2 + 41*t - 5, 3),
   "04003-12": lambda: speed_statement("04003-12", "position", -2*t**3 + 3*t**2 + 33*t, 3),
   "04003-13": lambda: speed_statement("04003-13", "position", t**3 + 2*t**2 - 12*t - 6, 1),
   "04003-14": lambda: speed_statement("04003-14", "velocity", -2*t**3 + 3*t**2 - 2*t + 1, 2),
   "04003-15": lambda: speed_statement("04003-15", "position", t**3 - 4*t**2 - 10*t - 1, 3),
   "04003-16": lambda: speed_statement("04003-16", "velocity", t**3 + 4*t**2 - 4*t - 58, 3),
   "04003-17": lambda: speed_statement("04003-17", "position", -2*t**3 + 4*t**2 + 29*t, 3),
   "04003-18": lambda: speed_statement("04003-18", "velocity", 2*t**3 + 3*t**2 + 4*t - 40, 2),
   "04003-19": lambda: speed_statement("04003-19", "position", -2*t**3 - t**2 + 4*t + 1, 1),
   "04003-20": lambda: speed_statement("04003-20", "position", 2*t**3 - 15*t + 4, 2),
   "04003-21": lambda: speed_statement("04003-21", "position", -2*t**3 + 4*t**2 + 6*t + 2, 1),
   "04004-00": lambda: direction_intervals("04004-00", (t - 3)**2*(3*t - 15), 8, "left"),
   "04004-01": lambda: direction_intervals("04004-01", -t*(t - 1)**2, 7, "right"),
   "04004-02": lambda: direction_intervals("04004-02", (t - 5)**2*(t - 3), 9, "right"),
   "04004-03": lambda: direction_intervals("04004-03", (t - 4)*(t - 3)**2, 10, "right"),
   "04004-04": lambda: direction_intervals("04004-04", (8 - 2*t)*(t - 3)**2, 7, "left"),
   "04004-05": lambda: direction_intervals("04004-05", (t - 5)**2*(t - 1), 6, "right"),
   "04004-06": lambda: direction_intervals("04004-06", (t - 4)*(t - 2)**2, 8, "right"),
   "04004-07": lambda: direction_intervals("04004-07", -3*(t - 5)**2*(t - 1), 7, "left"),
   "04004-08": lambda: direction_intervals("04004-08", 2*(t - 2)**2*(t - 1), 10, "left"),
   "04004-09": lambda: direction_intervals("04004-09", -t*(t - 4)**2, 9, "left"),
   "04004-10": lambda: direction_intervals("04004-10", (t - 1)**2*(2*t - 4), 9, "left"),
   "04004-11": lambda: direction_intervals("04004-11", -t*(t - 5)**2, 10, "right"),
   "04004-12": lambda: direction_intervals("04004-12", 2*(t - 5)**2*(t - 3), 8, "right"),
   "04004-13": lambda: direction_intervals("04004-13", (t - 1)**2*(2*t - 6), 7, "right"),
   "04004-14": lambda: direction_intervals("04004-14", (t - 4)**2*(3*t - 18), 10, "right"),
   "04004-15": lambda: direction_intervals("04004-15", t*(t - 1)**2, 5, "right"),
   "04004-16": lambda: direction_intervals("04004-16", (t - 6)*(t - 4)**2, 7, "right"),
   "04004-17": lambda: direction_intervals("04004-17", (8 - 2*t)*(t - 3)**2, 7, "left"),
   "04004-18": lambda: direction_intervals("04004-18", (12 - 2*t)*(t - 2)**2, 9, "left"),
   "04004-19": lambda: direction_intervals("04004-19", 3*(t - 2)**2*(t - 1), 6, "left"),
   "04004-20": lambda: direction_intervals("04004-20", (4 - t)*(t - 3)**2, 9, "right"),
   "04004-21": lambda: direction_intervals("04004-21", (t - 4)*(t - 2)**2, 10, "right"),
   "04005-00": lambda: rate_statement("04005-00", "amount", 40 + 30*exp(-t/4), 3, "minute"),
   "04005-01": lambda: rate_statement("04005-01", "rate", -15*exp(-t/8)/4, 4, "minute"),
   "04005-02": lambda: rate_statement("04005-02", "amount", 110 - 60*exp(-t/10), 5, "minute"),
   "04005-03": lambda: rate_statement("04005-03", "rate", 8*exp(-t/10), 9, "minute"),
   "04005-04": lambda: rate_statement("04005-04", "amount", 105 - 60*exp(-t/10), 5, "minute"),
   "04005-05": lambda: rate_statement("04005-05", "amount", 100 - 55*exp(-t/8), 8, "hour"),
   "04005-06": lambda: rate_statement("04005-06", "amount", 85 - 55*exp(-t/12), 7, "day"),
   "04005-07": lambda: rate_statement("04005-07", "rate", -20*exp(-t/12)/3, 6, "hour"),
   "04005-08": lambda: rate_statement("04005-08", "amount", 120 - 70*exp(-t/5), 2, "hour"),
   "04005-09": lambda: rate_statement("04005-09", "amount", 95 - 55*exp(-t/6), 6, "hour"),
   "04005-10": lambda: rate_statement("04005-10", "amount", 60 + 75*exp(-t/12), 3, "minute"),
   "04005-11": lambda: rate_statement("04005-11", "rate", -65*exp(-t/6)/6, 5, "minute"),
   "04005-12": lambda: rate_statement("04005-12", "amount", 10 + 20*exp(-t/12), 9, "hour"),
   "04005-13": lambda: rate_statement("04005-13", "rate", 7*exp(-t/10), 7, "minute"),
   "04005-14": lambda: rate_statement("04005-14", "amount", 80 - 35*exp(-t/5), 3, "minute"),
   "04005-15": lambda: rate_statement("04005-15", "rate", 25*exp(-t/12)/6, 7, "hour"),
   "04005-16": lambda: rate_statement("04005-16", "rate", 13*exp(-t/5), 5, "day"),
   "04005-17": lambda: rate_statement("04005-17", "rate", -13*exp(-t/5), 4, "minute"),
   "04005-18": lambda: rate_statement("04005-18", "rate", -35*exp(-t/12)/12, 6, "minute"),
   "04005-19": lambda: rate_statement("04005-19", "amount", 100 - 70*exp(-t/12), 4, "minute"),
   "04005-20": lambda: rate_statement("04005-20", "amount", 115 - 55*exp(-t/10), 8, "minute"),
   "04005-21": lambda: rate_statement("04005-21", "rate", 65*exp(-t/6)/6, 3, "hour"),
   "04006-00": lambda: cone_depth_rate(3, 4, 7),
   "04006-01": lambda: cube_volume_rate(8, 8),
   "04006-02": lambda: ladder_top_rate(10, 5, 8),
   "04006-03": lambda: cone_depth_rate(4, 3, 5),
   "04006-04": lambda: cube_volume_rate(7, 6),
   "04006-05": lambda: sphere_volume_rate(6, 10),
   "04006-06": lambda: sphere_volume_rate(3, 3),
   "04006-07": lambda: sphere_volume_rate(6, 3),
   "04006-08": lambda: ladder_top_rate(10, 4, 6),
   "04006-09": lambda: cone_depth_rate(8, 3, 5),
   "04006-10": lambda: cube_volume_rate(8, 2),
   "04006-11": lambda: ladder_top_rate(5, 6, 4),
   "04006-12": lambda: ladder_top_rate(10, 5, 6),
   "04006-13": lambda: ladder_top_rate(15, 6, 12),
   "04006-14": lambda: circle_area_rate(9, 4),
   "04006-15": lambda: cone_depth_rate(8, 2, 2),
   "04006-16": lambda: cone_depth_rate(2, 3, 5),
   "04006-17": lambda: cube_volume_rate(8, 3),
   "04006-18": lambda: ladder_top_rate(5, 3, 3),
   "04006-19": lambda: sphere_volume_rate(9, 5),
   "04006-20": lambda: ladder_top_rate(15, 3, 9),
   "04006-21": lambda: cone_depth_rate(8, 2, 7),
   "04007-00": lambda: curve_rate(2*x**2 - 2*x*y + 3*y**2 - (42), (-3, 2), 2),
   "04007-01": lambda: curve_rate(x**2 - x*y + 2*y**2 - (23), (3, -2), -4),
   "04007-02": lambda: curve_rate(x**2 - x*y + 3*y**2 - (9), (-3, -1), -3),
   "04007-03": lambda: curve_rate(2*x**2 - 3*x*y + 2*y**2 - (9), (-3, -3), 2),
   "04007-04": lambda: curve_rate(x**2 - x*y + 2*y**2 - (16), (2, -2), -2),
   "04008-00": lambda: tangent_estimate(2, 1, 3*x**2 - 6, Rational("2.2")),
   "04008-01": lambda: tangent_estimate(2, -1, 4 - 3*x**2, Rational("2.1")),
   "04008-02": lambda: tangent_estimate(1, -2, -2*x**2 - 9, Rational("0.5")),
   "04008-03": lambda: tangent_estimate(3, 4, 3*x**2 + 1, Rational("2.8")),
   "04008-04": lambda: tangent_estimate(1, -2, -3*x**2 - 9, Rational("1.5")),
   "04008-05": lambda: tangent_estimate(2, -2, 3*x**2, Rational("1.5")),
   "04008-06": lambda: tangent_estimate_statement("04008-06", 1, -1, x**2 - 8, Rational("1.2")),
   "04008-07": lambda: tangent_estimate(2, 6, x**2 - 6, Rational("1.5")),
   "04008-08": lambda: tangent_estimate(1, -1, -x**2 - 6, Rational("0.5")),
   "04008-09": lambda: tangent_estimate(2, 5, -x**2 - 1, Rational("1.8")),
   "04008-10": lambda: tangent_estimate(3, 1, 4 - 2*x**2, Rational("2.9")),
   "04008-11": lambda: tangent_estimate(2, -2, -2*x**2 - 2, Rational("2.2")),
   "04008-12": lambda: tangent_estimate(1, 5, 2*x**2 - 4, Rational("0.8")),
   "04008-13": lambda: tangent_estimate(1, 6, -2*x**2 - 1, Rational("1.1")),
   "04008-14": lambda: tangent_estimate_statement("04008-14", 1, -6, 6 - 3*x**2, Rational("1.1")),
   "04008-15": lambda: tangent_estimate(1, 0, x**2 - 2, Rational("0.8")),
   "04008-16": lambda: tangent_estimate(2, -3, 3*x**2 - 5, Rational("1.8")),
   "04008-17": lambda: tangent_estimate(1, -1, -3*x**2, Rational("1.2")),
   "04008-18": lambda: tangent_estimate(3, -2, 4 - x**2, Rational("3.2")),
   "04008-19": lambda: tangent_estimate(3, 2, 2*x**2 + 2, Rational("3.1")),
   "04008-20": lambda: tangent_estimate(3, -1, -2*x**2 - 2, Rational("2.8")),
   "04008-21": lambda: tangent_estimate(3, -6, x**2 - 2, Rational("3.5")),
   "04009-00": lambda: hermite_limit([(1, 1, 6), (2, -5, 4)], lambda f: (f(2 * x) + 5) / (exp(x - 1) - 1), 1),
   "04009-01": lambda: hermite_limit([(2, -1, 1), (6, -6, 6)], lambda f: (f(3 * x) + 6) / (x**2 - 4), 2),
   "04009-02": lambda: hermite_limit([(2, -1, 4), (4, -2, 6)], lambda f: (f(2 * x) + 2) / (x**3 - 8), 2),
   "04009-03": lambda: hermite_limit([(2, -3, 2), (4, 4, -5)], lambda f: (f(2 * x) - 4) / (exp(x - 2) - 1), 2),
   "04009-04": lambda: hermite_limit([(1, -3, -2), (2, 3, 4)], lambda f: (f(2 * x) - 3) / (x**2 - 1), 1),
   "04010-00": lambda: position_from_velocity(-3*t**2 - 6*t, 2, 3, 5),
   "04010-01": lambda: position_from_velocity(-3*t**2 - 4*t + 4, 3, -6, 2),
   "04010-02": lambda: position_from_velocity(-3*t**2 - 6, 3, 4, 6),
   "04010-03": lambda: position_from_velocity(3*t**2 + 2*t - 3, 1, 9, 0),
   "04010-04": lambda: position_from_velocity(6*t**2 + 4*t - 6, 1, -7, 0),
   "04010-05": lambda: position_from_velocity(-3*t**2 - 4, 2, -7, 0),
   "04010-06": lambda: position_from_velocity(-6*t**2 - 2*t, 1, 5, 4),
   "04010-07": lambda: position_from_velocity(6*t**2 + 6*t - 1, 2, -6, 3),
   "04010-08": lambda: position_from_velocity(-6*t**2 - 6*t + 6, 1, -4, 3),
   "04010-09": lambda: position_from_velocity(6*t**2 + 6*t + 4, 1, 3, 3),
   "04010-10": lambda: position_from_velocity(3*t**2 + 1, 1, 7, 2),
   "04010-11": lambda: position_from_velocity(6*t**2 + 2*t - 3, 3, -5, 2),
   "04010-12": lambda: position_from_velocity(6*t**2 - 4, 2, -9, 3),
   "04010-13": lambda: position_from_velocity(3*t**2 - 2*t - 1, 3, -5, 0),
   "04010-14": lambda: position_from_velocity(-3*t**2 - 4*t + 1, 3, 4, 5),
   "04010-15": lambda: position_from_velocity(3*t**2 + 4*t - 1, 1, -5, 0),
   "04010-16": lambda: position_from_velocity(-3*t**2 + 2*t - 1, 2, -8, 0),
   "04010-17": lambda: position_from_velocity(6*t**2 + 4*t + 5, 3, 3, 1),
   "04010-18": lambda: position_from_velocity(-6*t**2 + 4*t - 3, 2, 5, 5),
   "04010-19": lambda: position_from_velocity(3*t**2 + 4*t + 5, 3, -5, 1),
   "04010-20": lambda: position_from_velocity(-6*t**2 - 5, 2, 3, 1),
   "04010-21": lambda: position_from_velocity(6*t**2 + 6*t + 4, 1, -6, 3),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
