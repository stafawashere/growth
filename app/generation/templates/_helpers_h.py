"""Shared pieces for the unit 10 series templates."""
import sympy

from app.generation.kit import tex

n = sympy.Symbol("n", positive=True, integer=True)
x = sympy.Symbol("x")

INFINITY_LIMIT = r"\lim_{n\to\infty}"


def series_tex(term_tex, start):
   return rf"\sum_{{n={start}}}^{{\infty}} {term_tex}"


def power_tex(base_tex, exponent):
   """The power of a displacement written the way a polynomial term is written."""
   if exponent == 0:
      return ""

   if exponent == 1:
      return base_tex

   return rf"{base_tex}^{{{exponent}}}"


def displacement_tex(centre):
   if centre == 0:
      return "x"

   if centre > 0:
      return rf"\left(x - {centre}\right)"

   return rf"\left(x + {-centre}\right)"


def taylor_polynomial(coefficients, centre):
   """The polynomial sum of coefficients[k] (x - centre)^k, kept exact."""
   return sum((coefficient * (x - centre) ** power for power, coefficient in enumerate(coefficients)), sympy.Integer(0))


def polynomial_tex(coefficients, centre):
   """A Taylor polynomial in powers of the displacement, lowest degree first, zero terms left out."""
   pieces = []
   base = displacement_tex(centre)

   for power, coefficient in enumerate(coefficients):
      if coefficient == 0:
         continue

      magnitude = abs(coefficient)
      is_negative = coefficient < 0
      power_part = power_tex(base, power)

      if power == 0:
         body = tex(magnitude)
      elif magnitude == 1:
         body = power_part
      else:
         body = f"{tex(magnitude)} {power_part}"

      if not pieces:
         pieces.append(f"-{body}" if is_negative else body)
      else:
         pieces.append(f"- {body}" if is_negative else f"+ {body}")

   return " ".join(pieces) if pieces else "0"
