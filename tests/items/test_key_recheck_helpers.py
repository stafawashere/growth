"""The stem helpers tools/key_recheck.py offers for integrals, accumulation, series, differential
equations, polar curves and related rates. Each expected value is worked by hand here, never taken
from the helper, so a helper that computes the wrong quantity turns its test red.
"""
from sympy import Rational, cos, exp, oo, pi, sin, sqrt, symbols

from tools import key_recheck
from tools.key_recheck import t, theta, x, y

k, n = symbols("k n", positive=True, integer=True)


def test_definite_integral_over_a_finite_and_an_infinite_interval():
   assert key_recheck.definite_integral(x * exp(x), 0, 1) == 1
   assert key_recheck.definite_integral(1 / x**2, 1, oo) == 1


def test_pinned_antiderivative_adds_the_accumulated_change_to_the_anchor():
   assert key_recheck.pinned_antiderivative_value(2 * x, 1, 5, 3) == 13


def test_accumulation_derivative_uses_both_limits_and_the_chain_rule():
   assert key_recheck.accumulation_derivative(t**2, 1, x**2, 2) == 64
   assert key_recheck.accumulation_derivative(t, x, 3 * x, 1) == 8


def test_trapezoidal_sum_uses_each_subinterval_width():
   assert key_recheck.trapezoidal_sum([(0, 1), (1, 3), (3, 7)]) == 12


def test_riemann_sum_limit_is_the_integral_the_sum_describes():
   assert key_recheck.riemann_sum_limit((1 + k / n) ** 2 / n, k, n) == Rational(7, 3)


def test_series_value_starts_at_the_stated_index():
   assert key_recheck.series_value(Rational(1, 3) ** k, k, 1) == Rational(1, 2)


def test_first_omitted_term_is_the_next_term_in_magnitude():
   assert key_recheck.first_omitted_term((-1) ** k / k, k, 4) == Rational(1, 5)


def test_least_terms_for_tolerance_is_strictly_within_it():
   assert key_recheck.least_terms_for_tolerance((-1) ** k / k**2, k, 1, Rational(1, 100)) == 10


def test_limit_comparison_value_is_the_limit_of_the_ratio():
   assert key_recheck.limit_comparison_value((2 * n + 1) / (n**3 + 1), 1 / n**2, n) == 2


def test_lagrange_error_bound_uses_the_next_factorial_and_power():
   assert key_recheck.lagrange_error_bound(3, Rational(1, 2), 0, 2) == Rational(1, 16)


def test_radius_of_convergence_from_the_ratio_test():
   assert key_recheck.radius_of_convergence(x**k / 3**k, k) == [3]
   assert key_recheck.radius_of_convergence(k * (x - 2) ** k / 5**k, k, center=2) == [5]
   assert key_recheck.radius_of_convergence(x ** (2 * k) / 4**k, k) == [2]


def test_taylor_polynomial_stops_at_the_stated_degree():
   assert key_recheck.taylor_polynomial(exp(x), 0, 3) == 1 + x + x**2 / 2 + x**3 / 6


def test_taylor_from_derivatives_divides_by_the_factorial():
   expected = 2 - (x - 1) + 2 * (x - 1) ** 2

   assert (key_recheck.taylor_from_derivatives([2, -1, 4], 1) - expected).expand() == 0


def test_taylor_from_relation_differentiates_along_the_solution():
   assert key_recheck.taylor_from_relation(x + y**2, 0, 2, 2) == 2 + 4 * x + Rational(17, 2) * x**2


def test_euler_approximation_takes_the_stated_steps():
   assert key_recheck.euler_approximation(x + y, 0, 1, Rational(1, 2), 2) == Rational(5, 2)


def test_particular_solutions_keep_only_the_branch_through_the_point():
   assert key_recheck.particular_solutions(x * y, 0, 2) == [2 * exp(x**2 / 2)]
   assert key_recheck.particular_solutions(x / y, 0, -2) == [-sqrt(x**2 + 4)]


def test_is_solution_tells_a_solution_from_a_non_solution():
   assert key_recheck.is_solution(exp(3 * x), 3 * y) is True
   assert key_recheck.is_solution(exp(2 * x), 3 * y) is False


def test_polar_slope_divides_dy_by_dx_in_the_angle():
   assert key_recheck.polar_slope(theta, pi / 2) == -2 / pi
   assert key_recheck.polar_slope(1 + cos(theta), pi / 2) == 1


def test_related_rate_solves_for_the_other_coordinate():
   assert key_recheck.related_rate(x**2 + y**2 - 25, (3, 4), 2) == Rational(-3, 2)
   assert key_recheck.related_rate(x**2 + y**2 - 25, (3, 4), 2, known="y") == Rational(-8, 3)


def test_function_with_values_matches_the_stated_derivatives():
   stand_in = key_recheck.function_with_values(2, [0, 3, 5])

   assert key_recheck.limit_at(stand_in / (x - 2), 2) == 3
   assert key_recheck.limit_at((stand_in - 3 * (x - 2)) / (x - 2) ** 2, 2) == Rational(5, 2)


def test_polar_slope_on_a_circle_is_perpendicular_to_the_radius():
   assert key_recheck.polar_slope(2 * sin(theta), pi / 6) == sqrt(3)


def test_vertical_asymptotes_leave_out_a_removable_zero_of_the_denominator():
   expression = (x**2 - 3 * x + 2) / ((x - 1) * (x + 3) * (x - 5))

   assert key_recheck.vertical_asymptotes(expression) == [-3, 5]


def test_crossings_are_the_sorted_real_intersections():
   assert key_recheck.crossings(x**2, 2 * x + 3) == [-1, 3]
   assert key_recheck.crossings(x**2 + 1, 0 * x) == []


def test_area_between_curves_counts_each_piece_as_positive():
   assert key_recheck.area_between_curves(x**2, 2 * x + 3, -1, 3) == Rational(32, 3)
   assert key_recheck.area_between_curves(3 * x, 0 * x, -1, 2) == Rational(15, 2)


def test_polar_area_takes_half_the_integral_of_the_squared_radius():
   assert key_recheck.polar_area(3 + 0 * theta, 0, 2 * pi) == 9 * pi
   assert key_recheck.polar_area(1 + cos(theta), 0, 2 * pi) == 3 * pi / 2


def test_polar_coordinate_rates_differentiate_x_and_y_in_the_angle():
   horizontal_rate, vertical_rate = key_recheck.polar_coordinate_rates(theta, pi / 4)

   assert (horizontal_rate - (sqrt(2) / 2 - pi * sqrt(2) / 8)).simplify() == 0
   assert (vertical_rate - (sqrt(2) / 2 + pi * sqrt(2) / 8)).simplify() == 0


def test_mean_value_points_match_the_average_of_the_rate_inside_the_interval():
   assert key_recheck.mean_value_points(3 * t**2, 0, 2) == [2 * sqrt(3) / 3]
   assert key_recheck.mean_value_points(3 * t**2, -2, 2) == [-2 * sqrt(3) / 3, 2 * sqrt(3) / 3]


def test_mean_value_points_fall_back_to_a_numeric_root():
   points = key_recheck.mean_value_points(t + sin(t), 0, 3)

   assert len(points) == 1
   assert abs(float(points[0]) - 1.2231527244835694) < 1e-12


def test_numeric_definite_integral_evaluates_an_integral_with_no_elementary_antiderivative():
   value = key_recheck.numeric_definite_integral(exp(-(t**2)), 0, 2, t)

   assert abs(float(value) - 0.8820813907624215) < 1e-12
