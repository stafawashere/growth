"""The reader from a confirmed LaTeX line to SymPy (app/grading/latex.py). Each case is a habit of
handwritten calculus that the lark grammar did not read, or read two ways, before normalisation;
an unreadable line must stay Unreadable so the check reports unsettled and the model decides."""
import pytest
import sympy

from app.grading import latex

x, y, b, C, n, theta = sympy.symbols("x y b C n theta")

READINGS = [
   (r"e^{2x}\cos x", sympy.exp(2 * x) * sympy.cos(x)),
   (r"x^2 e^{x} - \sin(3x)+C", x**2 * sympy.exp(x) - sympy.sin(3 * x) + C),
   (r"\ln|x|+C", sympy.log(sympy.Abs(x)) + C),
   (r"\ln(x+1) + 2", sympy.log(x + 1) + 2),
   (r"\sin^{2}(x)+\cos^{2}(x)", sympy.sin(x) ** 2 + sympy.cos(x) ** 2),
   (r"\frac{x^2}{2}\ln x - \frac{x^2}{4}+C", x**2 * sympy.log(x) / 2 - x**2 / 4 + C),
   (r"\sin(\pi x)", sympy.sin(sympy.pi * x)),
   (r"\mathrm{e}^{x}", sympy.exp(x)),
   (r"(x^{2} + 2x)e^{x}", (x**2 + 2 * x) * sympy.exp(x)),
   (r"2(1 + 2x)e^{2x}", 2 * (1 + 2 * x) * sympy.exp(2 * x)),
   (r"\int_{0}^{3} x^{2}\,dx", sympy.Integral(x**2, (x, 0, 3))),
   (r"\int_{1}^{b} x^{-2} dx", sympy.Integral(x**-2, (x, 1, b))),
   (r"\sum_{n=1}^{\infty} x^{n}", sympy.Sum(x**n, (n, 1, sympy.oo))),
   (r"\frac{1}{2}\int_{0}^{\pi} (1+2\sin\theta)^2 \, d\theta", sympy.Integral((1 + 2 * sympy.sin(theta)) ** 2, (theta, 0, sympy.pi)) / 2),
]


@pytest.mark.parametrize("written, meant", READINGS, ids=[written for written, _meant in READINGS])
def test_a_handwritten_habit_reads_as_the_expression_meant(written, meant):
   read = latex.to_sympy(written)
   difference = read.doit() - meant.doit()

   assert sympy.simplify(difference) == 0


def test_a_claim_is_read_by_its_right_hand_side():
   assert latex.rhs_to_sympy(r"f'(x) = 3x^2 - 7") == 3 * x**2 - 7
   assert latex.rhs_to_sympy(r"\frac{dy}{dx} = \frac{-x}{y}") == -x / y
   assert latex.rhs_to_sympy(r"\approx 1.386") == sympy.Float("1.386")


def test_decimal_places_are_counted_from_what_was_written():
   assert latex.decimal_places(r"A \approx 1.39") == 2
   assert latex.decimal_places(r"\boxed{2.7183}") == 4
   assert latex.decimal_places(r"x = \frac{1}{2}") is None


@pytest.mark.parametrize("written", [r"\frac{dy}{y^{2}}", r"\begin{matrix} 3 \end{matrix}", ""])
def test_what_cannot_be_read_is_unreadable_rather_than_guessed(written):
   with pytest.raises(latex.Unreadable):
      latex.to_sympy(written)


def test_an_inequality_that_reads_two_ways_is_unreadable_and_its_check_is_unsettled():
   from app.grading import checks

   line = r"|f(1.4) - P_{3}(1.4)| \le \frac{0.4^{4}}{4!} \cdot 5"

   with pytest.raises(latex.Unreadable):
      latex.to_sympy(line)

   result = checks.run_check(
      {"kind": "sympy_equivalence", "target": "any_line", "expected": "1", "variable": "x"},
      {"part_id": "a", "lines": [{"kind": "math", "content": line}], "answer": ""},
   )

   assert result.outcome == checks.UNSETTLED
