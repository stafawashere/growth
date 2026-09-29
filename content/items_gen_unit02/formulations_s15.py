"""Each unit 2 item in stems batch s15, written as the SymPy computation of the answer its stem asks for."""
import sympy

from tools.key_recheck import derivative

t = sympy.Symbol("t")


def instantaneous_rate(quantity, at):
   return derivative(quantity, t).subs(t, at)


BY_SUFFIX = {
   "02014-00": lambda: instantaneous_rate(t**3 - 7 * t + 15, 2),
   "02014-01": lambda: instantaneous_rate(5 * t**2 - 6 * t + 20, 2),
   "02014-02": lambda: instantaneous_rate(4 * t**2 + 8 * t + 10, 3),
   "02014-03": lambda: instantaneous_rate(-2 * t**2 + t + 11, 2),
   "02014-04": lambda: instantaneous_rate(-5 * t**2 + 8 * t + 15, 4),
   "02014-05": lambda: instantaneous_rate(t**2 - 9 * t + 16, 2),
   "02014-06": lambda: instantaneous_rate(-4 * t**2 - 3 * t + 9, 3),
   "02014-07": lambda: instantaneous_rate(-4 * t**2 - 4 * t + 1, 3),
   "02014-08": lambda: instantaneous_rate(4 * t**3 + 8 * t + 8, 5),
   "02014-09": lambda: instantaneous_rate(-4 * t**3 + 9 * t + 5, 4),
   "02014-10": lambda: instantaneous_rate(-3 * t**2 - 5 * t + 15, 3),
   "02014-11": lambda: instantaneous_rate(6 - t**3, 5),
   "02014-12": lambda: instantaneous_rate(5 * t**3 + 4 * t + 20, 3),
   "02014-13": lambda: instantaneous_rate(3 * t**2 + 5 * t + 19, 5),
   "02014-14": lambda: instantaneous_rate(-2 * t**2 + 4 * t + 16, 4),
   "02014-15": lambda: instantaneous_rate(-5 * t**3 - 9 * t + 12, 3),
   "02014-16": lambda: instantaneous_rate(3 * t**2 + 5 * t + 14, 4),
   "02014-17": lambda: instantaneous_rate(-4 * t**2 + 8 * t + 1, 5),
   "02014-18": lambda: instantaneous_rate(3 * t**3 - 3 * t + 16, 5),
   "02014-19": lambda: instantaneous_rate(-t**3 - 5 * t + 18, 3),
   "02014-20": lambda: instantaneous_rate(2 * t**3 - 9 * t + 15, 2),
   "02014-21": lambda: instantaneous_rate(3 * t**3 + 6 * t + 1, 5),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
