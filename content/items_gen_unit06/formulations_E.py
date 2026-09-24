"""Blind re-solve of the unit 6 generated items in stems_E.json, written from the stems alone.

Written by claude-opus-5-5 on the operator's delegation of 2026-09-24, reading only stems_E.json,
the verifier prompt, the unit 10 key_formulations.py for format and tools/key_recheck.py for its
helpers. No key, worked solution or template was seen. A statement item returns the text of the
choice whose content matches the mathematics computed here. The choice texts are copied into
this file so it runs without the stems file.
"""
import math
import re

import sympy
from sympy import E, Piecewise, Rational, exp, oo, sqrt
from sympy.parsing.sympy_parser import (
   convert_xor,
   implicit_multiplication,
   parse_expr,
   standard_transformations,
)

from tools.key_recheck import accumulation_derivative, definite_integral, t, x

k, n = sympy.symbols("k n")

CHOICES_BY_SUFFIX = {
   "06011-00": [
      "The integral converges to \\( -4 + 4 \\sqrt{2} \\).",
      "The integral converges to \\( -8 + 8 \\sqrt{2} \\).",
      "The integral converges to \\( 4 \\sqrt{3} \\).",
      "The integral converges to \\( 8 \\sqrt{3} \\).",
   ],
   "06011-01": [
      "The integral converges to \\( - 2 \\sqrt{3} + 2 \\sqrt{6} \\).",
      "The integral converges to \\( - 6 \\sqrt{3} + 6 \\sqrt{6} \\).",
      "The integral converges to \\( 18 \\sqrt{21} \\).",
      "The integral converges to \\( 6 \\sqrt{21} \\).",
   ],
   "06011-02": [
      "The integral converges to \\( - 18 \\sqrt{3} \\).",
      "The integral converges to \\( - 36 \\sqrt{3} \\).",
      "The integral converges to \\( \\infty - 18 \\sqrt{3} \\).",
      "The integral diverges.",
   ],
   "06011-03": [
      "The integral converges to \\( - 2 \\sqrt{65} \\).",
      "The integral converges to \\( - \\frac{2 \\sqrt{65}}{3} \\).",
      "The integral converges to \\( \\infty - \\frac{2 \\sqrt{65}}{3} \\).",
      "The integral diverges.",
   ],
   "06011-04": [
      "The integral converges to \\( \\frac{1}{16} \\).",
      "The integral converges to \\( \\frac{1}{48} \\).",
      "The integral converges to \\( \\frac{2}{3} \\).",
      "The integral converges to \\( \\frac{2}{9} \\).",
   ],
   "06011-05": [
      "The integral converges to \\( - \\frac{1}{24} \\).",
      "The integral converges to \\( - \\frac{1}{8} \\).",
      "The integral converges to \\( \\infty - \\frac{1}{24} \\).",
      "The integral diverges.",
   ],
   "06011-06": [
      "The integral converges to \\( - \\frac{2}{7} \\).",
      "The integral converges to \\( - \\frac{6}{7} \\).",
      "The integral converges to \\( \\infty - \\frac{2}{7} \\).",
      "The integral diverges.",
   ],
   "06011-07": [
      "The integral converges to \\( -14 + 14 \\sqrt{2} \\).",
      "The integral converges to \\( -7 + 7 \\sqrt{2} \\).",
      "The integral converges to \\( 14 \\sqrt{3} \\).",
      "The integral converges to \\( 7 \\sqrt{3} \\).",
   ],
   "06011-08": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( \\frac{1}{2} \\).",
      "The integral converges to \\( \\frac{9}{2} \\).",
      "The integral converges to \\( \\frac{9}{4} \\).",
   ],
   "06011-09": [
      "The integral converges to \\( -12 \\).",
      "The integral converges to \\( -6 \\).",
      "The integral converges to \\( \\infty - 6 \\).",
      "The integral diverges.",
   ],
   "06011-10": [
      "The integral converges to \\( \\frac{5}{14} \\).",
      "The integral converges to \\( \\frac{5}{28} \\).",
      "The integral converges to \\( \\frac{5}{3} \\).",
      "The integral converges to \\( \\frac{5}{6} \\).",
   ],
   "06011-11": [
      "The integral converges to \\( - 2 \\sqrt{10} \\).",
      "The integral converges to \\( - 6 \\sqrt{10} \\).",
      "The integral converges to \\( \\infty - 2 \\sqrt{10} \\).",
      "The integral diverges.",
   ],
   "06011-12": [
      "The integral converges to \\( - \\frac{1}{7} \\).",
      "The integral converges to \\( - \\frac{2}{7} \\).",
      "The integral converges to \\( \\infty - \\frac{1}{7} \\).",
      "The integral diverges.",
   ],
   "06011-13": [
      "The integral converges to \\( 2 \\).",
      "The integral converges to \\( 4 \\).",
      "The integral converges to \\( \\frac{4}{11} \\).",
      "The integral converges to \\( \\frac{8}{11} \\).",
   ],
   "06011-14": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( 3 \\).",
      "The integral converges to \\( \\frac{3}{32} \\).",
      "The integral converges to \\( \\frac{9}{32} \\).",
   ],
   "06011-15": [
      "The integral converges to \\( - \\frac{7}{19} \\).",
      "The integral converges to \\( - \\frac{7}{57} \\).",
      "The integral converges to \\( \\infty - \\frac{7}{57} \\).",
      "The integral diverges.",
   ],
   "06011-16": [
      "The integral converges to \\( 7 \\).",
      "The integral converges to \\( \\frac{7}{10} \\).",
      "The integral converges to \\( \\frac{7}{20} \\).",
      "The integral converges to \\( \\frac{7}{2} \\).",
   ],
   "06011-17": [
      "The integral converges to \\( -10 + 10 \\sqrt{2} \\).",
      "The integral converges to \\( -5 + 5 \\sqrt{2} \\).",
      "The integral converges to \\( 10 \\sqrt{3} \\).",
      "The integral converges to \\( 5 \\sqrt{3} \\).",
   ],
   "06011-18": [
      "The integral converges to \\( \\frac{7}{12} \\).",
      "The integral converges to \\( \\frac{7}{213} \\).",
      "The integral converges to \\( \\frac{7}{4} \\).",
      "The integral converges to \\( \\frac{7}{71} \\).",
   ],
   "06011-19": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( \\frac{1}{2} \\).",
      "The integral converges to \\( \\frac{3}{17} \\).",
      "The integral converges to \\( \\frac{3}{34} \\).",
   ],
   "06011-20": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( 2 \\).",
      "The integral converges to \\( 2 \\sqrt{15} \\).",
      "The integral converges to \\( \\sqrt{15} \\).",
   ],
   "06011-21": [
      "The integral converges to \\( 1 \\).",
      "The integral converges to \\( 5 \\).",
      "The integral converges to \\( \\frac{1}{3} \\).",
      "The integral converges to \\( \\frac{5}{3} \\).",
   ],
   "06014-00": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} e^{2 + \\frac{3k}{n}} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} e^{2 + \\frac{3k}{n}} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} e^{2 + \\frac{3k}{n}} \\cdot \\frac{3}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} e^{\\frac{3k}{n}} \\cdot \\frac{3}{n} \\)",
   ],
   "06014-01": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4\\left(4 + \\frac{6k}{n}\\right)^{2} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4\\left(4 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4\\left(4 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4\\left(\\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
   ],
   "06014-02": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(1 + \\frac{6k}{n}\\right)^{2} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(1 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(1 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(\\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
   ],
   "06014-03": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{1 + \\frac{5k}{n}} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{1 + \\frac{5k}{n}} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{1 + \\frac{5k}{n}} \\cdot \\frac{5}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{\\frac{5k}{n}} \\cdot \\frac{5}{n} \\)",
   ],
   "06014-04": [
      "\\( \\int_{0}^{1} 2\\left(4 + 4x\\right)^{2}\\,dx \\)",
      "\\( \\int_{0}^{4} 2x^{2}\\,dx \\)",
      "\\( \\int_{4}^{8} 2x^{2}\\,dx \\)",
      "\\( \\int_{4}^{8} 8x^{2}\\,dx \\)",
   ],
   "06014-05": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} \\left(5 + \\frac{2k}{n}\\right)^{2} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} \\left(5 + \\frac{2k}{n}\\right)^{2} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} \\left(5 + \\frac{2k}{n}\\right)^{2} \\cdot \\frac{2}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} \\left(\\frac{2k}{n}\\right)^{2} \\cdot \\frac{2}{n} \\)",
   ],
   "06014-06": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{3 + \\frac{3k}{n}} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{3 + \\frac{3k}{n}} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{3 + \\frac{3k}{n}} \\cdot \\frac{3}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\sqrt{\\frac{3k}{n}} \\cdot \\frac{3}{n} \\)",
   ],
   "06014-07": [
      "\\( \\int_{0}^{1} 3e^{4 + 5t}\\,dt \\)",
      "\\( \\int_{0}^{5} 3e^{t}\\,dt \\)",
      "\\( \\int_{4}^{9} 15e^{t}\\,dt \\)",
      "\\( \\int_{4}^{9} 3e^{t}\\,dt \\)",
   ],
   "06014-08": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 2e^{4 + \\frac{2k}{n}} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 2e^{4 + \\frac{2k}{n}} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 2e^{4 + \\frac{2k}{n}} \\cdot \\frac{2}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 2e^{\\frac{2k}{n}} \\cdot \\frac{2}{n} \\)",
   ],
   "06014-09": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(4 + \\frac{3k}{n}\\right)^{2} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(4 + \\frac{3k}{n}\\right)^{2} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(4 + \\frac{3k}{n}\\right)^{2} \\cdot \\frac{3}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 3\\left(\\frac{3k}{n}\\right)^{2} \\cdot \\frac{3}{n} \\)",
   ],
   "06014-10": [
      "\\( \\int_{0}^{1} 2\\left(2 + 4t\\right)^{2}\\,dt \\)",
      "\\( \\int_{0}^{4} 2t^{2}\\,dt \\)",
      "\\( \\int_{2}^{6} 2t^{2}\\,dt \\)",
      "\\( \\int_{2}^{6} 8t^{2}\\,dt \\)",
   ],
   "06014-11": [
      "\\( \\int_{0}^{1} 3\\left(1 + 2x\\right)^{3}\\,dx \\)",
      "\\( \\int_{0}^{2} 3x^{3}\\,dx \\)",
      "\\( \\int_{1}^{3} 3x^{3}\\,dx \\)",
      "\\( \\int_{1}^{3} 6x^{3}\\,dx \\)",
   ],
   "06014-12": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 5\\left(3 + \\frac{6k}{n}\\right)^{2} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 5\\left(3 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 5\\left(3 + \\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 5\\left(\\frac{6k}{n}\\right)^{2} \\cdot \\frac{6}{n} \\)",
   ],
   "06014-13": [
      "\\( \\int_{0}^{1} 5\\left(5 + 4t\\right)^{3}\\,dt \\)",
      "\\( \\int_{0}^{4} 5t^{3}\\,dt \\)",
      "\\( \\int_{5}^{9} 20t^{3}\\,dt \\)",
      "\\( \\int_{5}^{9} 5t^{3}\\,dt \\)",
   ],
   "06014-14": [
      "\\( \\int_{0}^{1} 4\\left(4 + 4x\\right)^{3}\\,dx \\)",
      "\\( \\int_{0}^{4} 4x^{3}\\,dx \\)",
      "\\( \\int_{4}^{8} 16x^{3}\\,dx \\)",
      "\\( \\int_{4}^{8} 4x^{3}\\,dx \\)",
   ],
   "06014-15": [
      "\\( \\int_{0}^{1} 2\\left(6 + 4x\\right)^{2}\\,dx \\)",
      "\\( \\int_{0}^{4} 2x^{2}\\,dx \\)",
      "\\( \\int_{6}^{10} 2x^{2}\\,dx \\)",
      "\\( \\int_{6}^{10} 8x^{2}\\,dx \\)",
   ],
   "06014-16": [
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4e^{6 + \\frac{2k}{n}} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4e^{6 + \\frac{2k}{n}} \\cdot \\frac{1}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4e^{6 + \\frac{2k}{n}} \\cdot \\frac{2}{n} \\)",
      "\\( \\lim_{n\\to\\infty} \\sum_{k=1}^{n} 4e^{\\frac{2k}{n}} \\cdot \\frac{2}{n} \\)",
   ],
   "06014-17": [
      "\\( \\int_{0}^{1} 5\\sqrt{4 + 3x}\\,dx \\)",
      "\\( \\int_{0}^{3} 5\\sqrt{x}\\,dx \\)",
      "\\( \\int_{4}^{7} 15\\sqrt{x}\\,dx \\)",
      "\\( \\int_{4}^{7} 5\\sqrt{x}\\,dx \\)",
   ],
   "06014-18": [
      "\\( \\int_{0}^{1} 5e^{5 + 5t}\\,dt \\)",
      "\\( \\int_{0}^{5} 5e^{t}\\,dt \\)",
      "\\( \\int_{5}^{10} 25e^{t}\\,dt \\)",
      "\\( \\int_{5}^{10} 5e^{t}\\,dt \\)",
   ],
   "06014-19": [
      "\\( \\int_{0}^{1} 2\\left(3 + 3t\\right)^{2}\\,dt \\)",
      "\\( \\int_{0}^{3} 2t^{2}\\,dt \\)",
      "\\( \\int_{3}^{6} 2t^{2}\\,dt \\)",
      "\\( \\int_{3}^{6} 6t^{2}\\,dt \\)",
   ],
   "06014-20": [
      "\\( \\int_{0}^{1} 2\\sqrt{6 + 4t}\\,dt \\)",
      "\\( \\int_{0}^{4} 2\\sqrt{t}\\,dt \\)",
      "\\( \\int_{6}^{10} 2\\sqrt{t}\\,dt \\)",
      "\\( \\int_{6}^{10} 8\\sqrt{t}\\,dt \\)",
   ],
   "06014-21": [
      "\\( \\int_{0}^{1} 4\\sqrt{3 + 4x}\\,dx \\)",
      "\\( \\int_{0}^{4} 4\\sqrt{x}\\,dx \\)",
      "\\( \\int_{3}^{7} 16\\sqrt{x}\\,dx \\)",
      "\\( \\int_{3}^{7} 4\\sqrt{x}\\,dx \\)",
   ],
   "06015-00": [
      "It is the total number of people who enter the stadium from \\( t = 7 \\) to \\( t = 13 \\) minutes, measured in people per minute.",
      "It is the total number of people who enter the stadium from \\( t = 7 \\) to \\( t = 13 \\) minutes, measured in people.",
      "It is the total number of people who enter the stadium from \\( t = 7 \\) to \\( t = 13 \\) minutes.",
      "It is the total number of people who enter the stadium over the whole time the model covers, measured in people.",
   ],
   "06015-01": [
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 6 \\) to \\( t = 10 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 6 \\) to \\( t = 10 \\) hours, measured in cars.",
      "It is the average rate at which cars leave the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that leave the garage from \\( t = 6 \\) to \\( t = 10 \\) hours, measured in cars.",
   ],
   "06015-02": [
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 5 \\) to \\( t = 9 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 5 \\) to \\( t = 9 \\) hours, measured in cars.",
      "It is the average rate at which cars leave the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that leave the garage from \\( t = 5 \\) to \\( t = 9 \\) hours, measured in cars.",
   ],
   "06015-03": [
      "It is the total number of cars that enter the garage from \\( t = 3 \\) to \\( t = 11 \\) hours, measured in cars per hour.",
      "It is the total number of cars that enter the garage from \\( t = 3 \\) to \\( t = 11 \\) hours, measured in cars.",
      "It is the total number of cars that enter the garage from \\( t = 3 \\) to \\( t = 11 \\) hours.",
      "It is the total number of cars that enter the garage over the whole time the model covers, measured in cars.",
   ],
   "06015-04": [
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 12 \\) to \\( t = 21 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 12 \\) to \\( t = 21 \\) hours, measured in cars.",
      "It is the average rate at which cars leave the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that leave the garage from \\( t = 12 \\) to \\( t = 21 \\) hours, measured in cars.",
   ],
   "06015-05": [
      "It is the average rate at which cars enter the garage over the time interval from \\( t = 3 \\) to \\( t = 10 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars enter the garage over the time interval from \\( t = 3 \\) to \\( t = 10 \\) hours, measured in cars.",
      "It is the average rate at which cars enter the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that enter the garage from \\( t = 3 \\) to \\( t = 10 \\) hours, measured in cars.",
   ],
   "06015-06": [
      "It is the total amount of water pumped into the tank from \\( t = 0 \\) to \\( t = 3 \\) minutes, measured in liters per minute.",
      "It is the total amount of water pumped into the tank from \\( t = 0 \\) to \\( t = 3 \\) minutes, measured in liters.",
      "It is the total amount of water pumped into the tank from \\( t = 0 \\) to \\( t = 3 \\) minutes.",
      "It is the total amount of water pumped into the tank over the whole time the model covers, measured in liters.",
   ],
   "06015-07": [
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 3 \\) to \\( t = 11 \\) hours, measured in cubic feet per hour.",
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 3 \\) to \\( t = 11 \\) hours, measured in cubic feet.",
      "It is the average rate at which sand is added to the pile over the whole time the model covers, measured in cubic feet per hour.",
      "It is the total volume of sand added to the pile from \\( t = 3 \\) to \\( t = 11 \\) hours, measured in cubic feet.",
   ],
   "06015-08": [
      "It is the total volume of sand added to the pile from \\( t = 6 \\) to \\( t = 11 \\) hours, measured in cubic feet per hour.",
      "It is the total volume of sand added to the pile from \\( t = 6 \\) to \\( t = 11 \\) hours, measured in cubic feet.",
      "It is the total volume of sand added to the pile from \\( t = 6 \\) to \\( t = 11 \\) hours.",
      "It is the total volume of sand added to the pile over the whole time the model covers, measured in cubic feet.",
   ],
   "06015-09": [
      "It is the total number of people who enter the stadium from \\( t = 5 \\) to \\( t = 15 \\) minutes, measured in people per minute.",
      "It is the total number of people who enter the stadium from \\( t = 5 \\) to \\( t = 15 \\) minutes, measured in people.",
      "It is the total number of people who enter the stadium from \\( t = 5 \\) to \\( t = 15 \\) minutes.",
      "It is the total number of people who enter the stadium over the whole time the model covers, measured in people.",
   ],
   "06015-10": [
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 1 \\) to \\( t = 9 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 1 \\) to \\( t = 9 \\) hours, measured in cars.",
      "It is the average rate at which cars leave the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that leave the garage from \\( t = 1 \\) to \\( t = 9 \\) hours, measured in cars.",
   ],
   "06015-11": [
      "It is the average rate at which people enter the stadium over the time interval from \\( t = 7 \\) to \\( t = 12 \\) minutes, measured in people per minute.",
      "It is the average rate at which people enter the stadium over the time interval from \\( t = 7 \\) to \\( t = 12 \\) minutes, measured in people.",
      "It is the average rate at which people enter the stadium over the whole time the model covers, measured in people per minute.",
      "It is the total number of people who enter the stadium from \\( t = 7 \\) to \\( t = 12 \\) minutes, measured in people.",
   ],
   "06015-12": [
      "It is the average rate at which snow melts off the roof over the time interval from \\( t = 7 \\) to \\( t = 14 \\) hours, measured in inches per hour.",
      "It is the average rate at which snow melts off the roof over the time interval from \\( t = 7 \\) to \\( t = 14 \\) hours, measured in inches.",
      "It is the average rate at which snow melts off the roof over the whole time the model covers, measured in inches per hour.",
      "It is the total depth of snow that melts off the roof from \\( t = 7 \\) to \\( t = 14 \\) hours, measured in inches.",
   ],
   "06015-13": [
      "It is the average rate at which water is pumped into the tank over the time interval from \\( t = 3 \\) to \\( t = 6 \\) minutes, measured in liters per minute.",
      "It is the average rate at which water is pumped into the tank over the time interval from \\( t = 3 \\) to \\( t = 6 \\) minutes, measured in liters.",
      "It is the average rate at which water is pumped into the tank over the whole time the model covers, measured in liters per minute.",
      "It is the total amount of water pumped into the tank from \\( t = 3 \\) to \\( t = 6 \\) minutes, measured in liters.",
   ],
   "06015-14": [
      "It is the total amount of oil pumped into the drum from \\( t = 1 \\) to \\( t = 10 \\) hours, measured in gallons per hour.",
      "It is the total amount of oil pumped into the drum from \\( t = 1 \\) to \\( t = 10 \\) hours, measured in gallons.",
      "It is the total amount of oil pumped into the drum from \\( t = 1 \\) to \\( t = 10 \\) hours.",
      "It is the total amount of oil pumped into the drum over the whole time the model covers, measured in gallons.",
   ],
   "06015-15": [
      "It is the average rate at which oil leaks out of the drum over the time interval from \\( t = 10 \\) to \\( t = 16 \\) hours, measured in gallons per hour.",
      "It is the average rate at which oil leaks out of the drum over the time interval from \\( t = 10 \\) to \\( t = 16 \\) hours, measured in gallons.",
      "It is the average rate at which oil leaks out of the drum over the whole time the model covers, measured in gallons per hour.",
      "It is the total amount of oil that leaks out of the drum from \\( t = 10 \\) to \\( t = 16 \\) hours, measured in gallons.",
   ],
   "06015-16": [
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 8 \\) to \\( t = 16 \\) hours, measured in cubic feet per hour.",
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 8 \\) to \\( t = 16 \\) hours, measured in cubic feet.",
      "It is the average rate at which sand is added to the pile over the whole time the model covers, measured in cubic feet per hour.",
      "It is the total volume of sand added to the pile from \\( t = 8 \\) to \\( t = 16 \\) hours, measured in cubic feet.",
   ],
   "06015-17": [
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 0 \\) to \\( t = 9 \\) hours, measured in cubic feet per hour.",
      "It is the average rate at which sand is added to the pile over the time interval from \\( t = 0 \\) to \\( t = 9 \\) hours, measured in cubic feet.",
      "It is the average rate at which sand is added to the pile over the whole time the model covers, measured in cubic feet per hour.",
      "It is the total volume of sand added to the pile from \\( t = 0 \\) to \\( t = 9 \\) hours, measured in cubic feet.",
   ],
   "06015-18": [
      "It is the total depth of snow that accumulates on the roof from \\( t = 5 \\) to \\( t = 14 \\) hours, measured in inches per hour.",
      "It is the total depth of snow that accumulates on the roof from \\( t = 5 \\) to \\( t = 14 \\) hours, measured in inches.",
      "It is the total depth of snow that accumulates on the roof from \\( t = 5 \\) to \\( t = 14 \\) hours.",
      "It is the total depth of snow that accumulates on the roof over the whole time the model covers, measured in inches.",
   ],
   "06015-19": [
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 5 \\) to \\( t = 12 \\) hours, measured in cars per hour.",
      "It is the average rate at which cars leave the garage over the time interval from \\( t = 5 \\) to \\( t = 12 \\) hours, measured in cars.",
      "It is the average rate at which cars leave the garage over the whole time the model covers, measured in cars per hour.",
      "It is the total number of cars that leave the garage from \\( t = 5 \\) to \\( t = 12 \\) hours, measured in cars.",
   ],
   "06015-20": [
      "It is the total amount of oil that leaks out of the drum from \\( t = 2 \\) to \\( t = 12 \\) hours, measured in gallons per hour.",
      "It is the total amount of oil that leaks out of the drum from \\( t = 2 \\) to \\( t = 12 \\) hours, measured in gallons.",
      "It is the total amount of oil that leaks out of the drum from \\( t = 2 \\) to \\( t = 12 \\) hours.",
      "It is the total amount of oil that leaks out of the drum over the whole time the model covers, measured in gallons.",
   ],
   "06015-21": [
      "It is the average rate at which people enter the stadium over the time interval from \\( t = 8 \\) to \\( t = 11 \\) minutes, measured in people per minute.",
      "It is the average rate at which people enter the stadium over the time interval from \\( t = 8 \\) to \\( t = 11 \\) minutes, measured in people.",
      "It is the average rate at which people enter the stadium over the whole time the model covers, measured in people per minute.",
      "It is the total number of people who enter the stadium from \\( t = 8 \\) to \\( t = 11 \\) minutes, measured in people.",
   ],
}

PARSE_TRANSFORMATIONS = standard_transformations + (implicit_multiplication, convert_xor)
PARSE_NAMES = {"x": x, "t": t, "k": k, "n": n, "e": E, "sqrt": sqrt, "exp": exp, "oo": oo}
RIEMANN_SUM_TERMS = 200000
VALUE_TOLERANCE = 1e-9
RIEMANN_TOLERANCE = 1e-3


def braced_argument(text, open_index):
   depth = 0

   for index in range(open_index, len(text)):
      if text[index] == "{":
         depth += 1
      elif text[index] == "}":
         depth -= 1

         if depth == 0:
            return text[open_index + 1:index], index + 1

   raise ValueError(f"unbalanced braces in {text}")


def rewrite_command(text, command, arity, template):
   while command in text:
      start = text.index(command)
      cursor = start + len(command)
      arguments = []

      for _ in range(arity):
         argument, cursor = braced_argument(text, cursor)
         arguments.append(argument)

      text = text[:start] + template.format(*arguments) + text[cursor:]

   return text


def latex_to_sympy(latex):
   text = latex.replace("\\left", "").replace("\\right", "").replace("\\,", " ")
   text = text.replace("\\cdot", "*").replace("\\infty", "oo")
   text = rewrite_command(text, "\\frac", 2, "(({0})/({1}))")
   text = rewrite_command(text, "\\sqrt", 1, "sqrt({0})")
   text = rewrite_command(text, "^", 1, "**({0})")

   return parse_expr(text, local_dict=PARSE_NAMES, transformations=PARSE_TRANSFORMATIONS)


def math_segments(text):
   return re.findall(r"\\\((.+?)\\\)", text)


def only_choice(matching):
   if len(matching) == 1:
      return matching[0]

   return matching


def rational_antiderivative(integrand):
   """Polynomial part integrated term by term, each linear partial fraction c/(a x + b) as
   (c / a) ln|a x + b| with integer a and b."""
   antiderivative = sympy.Integer(0)

   for term in sympy.Add.make_args(sympy.apart(sympy.together(integrand), x)):
      numerator, denominator = sympy.fraction(sympy.factor(term))
      is_polynomial_term = not denominator.has(x)

      if is_polynomial_term:
         antiderivative += sympy.integrate(term, x)
         continue

      linear_factor = sympy.Poly(denominator, x)
      is_simple_linear = linear_factor.degree() == 1 and not numerator.has(x)

      if not is_simple_linear:
         raise ValueError(f"unexpected partial fraction {term}")

      leading, constant = linear_factor.all_coeffs()
      content = sympy.gcd(leading, constant)
      primitive_leading = leading / content
      primitive_constant = constant / content
      coefficient = numerator / content
      antiderivative += coefficient / primitive_leading * sympy.log(sympy.Abs(primitive_leading * x + primitive_constant))

   return sympy.expand(antiderivative)


def rational_integral(numerator, denominator):
   return rational_antiderivative(numerator / denominator)


def integral_by_parts(integrand):
   return sympy.expand(sympy.integrate(integrand, x))


def improper_integral_choice(suffix, integrand, lower, upper):
   value = definite_integral(integrand, lower, upper)
   diverges = value.has(oo, -oo, sympy.zoo, sympy.nan)
   choices = CHOICES_BY_SUFFIX[suffix]

   if diverges:
      return only_choice([choice for choice in choices if choice == "The integral diverges."])

   matching = []

   for choice in choices:
      segments = math_segments(choice)

      if not segments:
         continue

      stated = latex_to_sympy(segments[0])
      is_finite = not stated.has(oo, -oo)
      is_equal = is_finite and abs(complex(sympy.N(stated - value, 30))) < VALUE_TOLERANCE

      if is_equal:
         matching.append(choice)

   return only_choice(matching)


def chain_rule_accumulation(integrand, lower, upper, at):
   return accumulation_derivative(integrand, lower, upper, at)


def piecewise_step(left_value, right_value, jump):
   return Piecewise((left_value, x < jump), (right_value, True))


def combined_integral(known_integrals, scale, step, lower, upper):
   """known_integrals: ((p, q), value) pairs of the integral of f from p to q, all sharing p."""
   anchor = known_integrals[0][0][0]
   accumulated = {anchor: sympy.Integer(0)}

   for (start, end), value in known_integrals:
      if start != anchor:
         raise ValueError("known integrals must share their lower limit")

      accumulated[end] = sympy.nsimplify(value)

   integral_of_f = accumulated[upper] - accumulated[lower]
   integral_of_step = definite_integral(step, lower, upper)

   return scale * integral_of_f + integral_of_step


def riemann_limit_value(sum_latex):
   match = re.fullmatch(r"\\lim_\{n\\to\\infty\} \\sum_\{k=(\d+)\}\^\{(n|n-1)\} (.+)", sum_latex.strip())

   if match is None:
      raise ValueError(f"not a Riemann sum limit: {sum_latex}")

   first_index = int(match.group(1))
   last_offset = -1 if match.group(2) == "n-1" else 0
   term = latex_to_sympy(match.group(3))
   term_function = sympy.lambdify((k, n), term, "math")
   count = RIEMANN_SUM_TERMS

   return math.fsum(term_function(index, count) for index in range(first_index, count + last_offset + 1))


def definite_integral_value(integral_latex):
   match = re.fullmatch(r"\\int_\{(.+?)\}\^\{(.+?)\} (.+)\\,d([a-z])", integral_latex.strip())

   if match is None:
      raise ValueError(f"not a definite integral: {integral_latex}")

   variable = sympy.Symbol(match.group(4))
   integrand = latex_to_sympy(match.group(3)).subs({x: variable, t: variable})
   lower = latex_to_sympy(match.group(1))
   upper = latex_to_sympy(match.group(2))

   return sympy.N(sympy.integrate(integrand, (variable, lower, upper)), 30)


def relatively_close(left, right):
   scale = max(abs(float(right)), 1.0)

   return abs(float(left) - float(right)) / scale < RIEMANN_TOLERANCE


def riemann_sum_for_integral(suffix, integrand, lower, upper):
   """The choice whose limit of sums equals the integral. A choice with no width factor grows
   without bound and one with the wrong width or sample points has a different limit."""
   target = sympy.N(definite_integral(integrand, lower, upper), 30)
   matching = [
      choice for choice in CHOICES_BY_SUFFIX[suffix]
      if relatively_close(riemann_limit_value(math_segments(choice)[0]), target)
   ]

   return only_choice(matching)


def integral_for_riemann_sum(suffix, sum_latex):
   target = riemann_limit_value(sum_latex)
   matching = [
      choice for choice in CHOICES_BY_SUFFIX[suffix]
      if relatively_close(definite_integral_value(math_segments(choice)[0]), target)
   ]

   return only_choice(matching)


def rate_units(stem):
   match = re.search(r"at a rate of R\(t\) (.+?) per (\w+), where", stem)

   return match.group(1), match.group(2)


def accumulation_interpretation(suffix, stem):
   """A plain integral of a rate is the amount over the interval, in the amount's units; one over
   the interval length times that integral is the average rate, in the rate's units."""
   amount_unit, time_unit = rate_units(stem)
   integral = re.search(r"\\\( (\\frac\{1\}\{(\d+)\})?\\int_\{(\d+)\}\^\{(\d+)\} R\(t\)\\,dt \\\)", stem)
   lower = int(integral.group(3))
   upper = int(integral.group(4))
   is_average = integral.group(1) is not None
   interval_text = f"from \\( t = {lower} \\) to \\( t = {upper} \\)"

   if is_average:
      divisor = int(integral.group(2))

      if divisor != upper - lower:
         raise ValueError("the factor is not one over the interval length")

      wanted = [
         choice for choice in CHOICES_BY_SUFFIX[suffix]
         if "average rate" in choice and interval_text in choice and choice.endswith(f"measured in {amount_unit} per {time_unit}.")
      ]
   else:
      wanted = [
         choice for choice in CHOICES_BY_SUFFIX[suffix]
         if choice.startswith("It is the total") and interval_text in choice and choice.endswith(f"measured in {amount_unit}.")
      ]

   return only_choice(wanted)


def interpretation(suffix):
   stem = INTERPRETATION_STEMS[suffix]

   return lambda: accumulation_interpretation(suffix, stem)


INTERPRETATION_STEMS = {
   "06015-00": "People enter a stadium at a rate of R(t) people per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\int_{7}^{13} R(t)\\,dt \\) in the context of the problem.",
   "06015-01": "Cars leave a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{4}\\int_{6}^{10} R(t)\\,dt \\) in the context of the problem.",
   "06015-02": "Cars leave a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{4}\\int_{5}^{9} R(t)\\,dt \\) in the context of the problem.",
   "06015-03": "Cars enter a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\int_{3}^{11} R(t)\\,dt \\) in the context of the problem.",
   "06015-04": "Cars leave a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{9}\\int_{12}^{21} R(t)\\,dt \\) in the context of the problem.",
   "06015-05": "Cars enter a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{7}\\int_{3}^{10} R(t)\\,dt \\) in the context of the problem.",
   "06015-06": "Water is pumped into a tank at a rate of R(t) liters per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\int_{0}^{3} R(t)\\,dt \\) in the context of the problem.",
   "06015-07": "Sand is added to a pile at a rate of R(t) cubic feet per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{8}\\int_{3}^{11} R(t)\\,dt \\) in the context of the problem.",
   "06015-08": "Sand is added to a pile at a rate of R(t) cubic feet per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\int_{6}^{11} R(t)\\,dt \\) in the context of the problem.",
   "06015-09": "People enter a stadium at a rate of R(t) people per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\int_{5}^{15} R(t)\\,dt \\) in the context of the problem.",
   "06015-10": "Cars leave a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{8}\\int_{1}^{9} R(t)\\,dt \\) in the context of the problem.",
   "06015-11": "People enter a stadium at a rate of R(t) people per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\frac{1}{5}\\int_{7}^{12} R(t)\\,dt \\) in the context of the problem.",
   "06015-12": "Snow melts off a flat roof at a rate of R(t) inches per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{7}\\int_{7}^{14} R(t)\\,dt \\) in the context of the problem.",
   "06015-13": "Water is pumped into a tank at a rate of R(t) liters per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\frac{1}{3}\\int_{3}^{6} R(t)\\,dt \\) in the context of the problem.",
   "06015-14": "Oil is pumped into a storage drum at a rate of R(t) gallons per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\int_{1}^{10} R(t)\\,dt \\) in the context of the problem.",
   "06015-15": "Oil leaks out of a storage drum at a rate of R(t) gallons per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{6}\\int_{10}^{16} R(t)\\,dt \\) in the context of the problem.",
   "06015-16": "Sand is added to a pile at a rate of R(t) cubic feet per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{8}\\int_{8}^{16} R(t)\\,dt \\) in the context of the problem.",
   "06015-17": "Sand is added to a pile at a rate of R(t) cubic feet per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{9}\\int_{0}^{9} R(t)\\,dt \\) in the context of the problem.",
   "06015-18": "Snow accumulates on a flat roof at a rate of R(t) inches per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\int_{5}^{14} R(t)\\,dt \\) in the context of the problem.",
   "06015-19": "Cars leave a parking garage at a rate of R(t) cars per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\frac{1}{7}\\int_{5}^{12} R(t)\\,dt \\) in the context of the problem.",
   "06015-20": "Oil leaks out of a storage drum at a rate of R(t) gallons per hour, where R is a positive function and t is measured in hours. Using correct units, interpret the meaning of \\( \\int_{2}^{12} R(t)\\,dt \\) in the context of the problem.",
   "06015-21": "People enter a stadium at a rate of R(t) people per minute, where R is a positive function and t is measured in minutes. Using correct units, interpret the meaning of \\( \\frac{1}{3}\\int_{8}^{11} R(t)\\,dt \\) in the context of the problem.",
}

BY_SUFFIX = {
   "06010-00": lambda: rational_integral(2*x**2 - x + 2, 2*x**2 - x - 1),
   "06010-01": lambda: rational_integral(18, 5*x**2 - 2*x - 16),
   "06010-02": lambda: rational_integral(-22, 5*x**2 - x - 6),
   "06010-03": lambda: rational_integral(3*x**2 - 2*x + 59, 3*x**2 - 2*x - 21),
   "06010-04": lambda: rational_integral(5*x**2 - 3*x + 5, 5*x**2 - 3*x - 2),

   "06011-00": lambda: improper_integral_choice("06011-00", 4*x / sqrt(x**2 - 1), 1, 2),
   "06011-01": lambda: improper_integral_choice("06011-01", 3*x**2 / sqrt(x**3 - 27), 3, 6),
   "06011-02": lambda: improper_integral_choice("06011-02", 9*x / sqrt(x**2 + 3), 3, oo),
   "06011-03": lambda: improper_integral_choice("06011-03", x**2 / sqrt(x**3 + 1), 4, oo),
   "06011-04": lambda: improper_integral_choice("06011-04", 2*x**2 / (x**3 + 5)**2, 3, oo),
   "06011-05": lambda: improper_integral_choice("06011-05", 7*x**2 / (x**3 - 8)**2, 2, 4),
   "06011-06": lambda: improper_integral_choice("06011-06", 6*x**2 / (x**3 - 1)**2, 1, 2),
   "06011-07": lambda: improper_integral_choice("06011-07", 7*x / sqrt(x**2 - 1), 1, 2),
   "06011-08": lambda: improper_integral_choice("06011-08", 9*x / (x**2 + 5)**2, 2, oo),
   "06011-09": lambda: improper_integral_choice("06011-09", 2*x / sqrt(x**2 + 5), 2, oo),
   "06011-10": lambda: improper_integral_choice("06011-10", 5*x / (x**2 + 5)**2, 3, oo),
   "06011-11": lambda: improper_integral_choice("06011-11", 3*x**2 / sqrt(x**3 + 9), 1, oo),
   "06011-12": lambda: improper_integral_choice("06011-12", 6*x / (x**2 - 4)**2, 2, 5),
   "06011-13": lambda: improper_integral_choice("06011-13", 8*x / (x**2 + 7)**2, 2, oo),
   "06011-14": lambda: improper_integral_choice("06011-14", 9*x**2 / (x**3 + 5)**2, 3, oo),
   "06011-15": lambda: improper_integral_choice("06011-15", 7*x**2 / (x**3 - 8)**2, 2, 3),
   "06011-16": lambda: improper_integral_choice("06011-16", 7*x / (x**2 + 9)**2, 1, oo),
   "06011-17": lambda: improper_integral_choice("06011-17", 5*x / sqrt(x**2 - 1), 1, 2),
   "06011-18": lambda: improper_integral_choice("06011-18", 7*x**2 / (x**3 + 7)**2, 4, oo),
   "06011-19": lambda: improper_integral_choice("06011-19", 3*x / (x**2 + 8)**2, 3, oo),
   "06011-20": lambda: improper_integral_choice("06011-20", x / sqrt(x**2 - 1), 1, 4),
   "06011-21": lambda: improper_integral_choice("06011-21", 5*x**2 / (x**3 + 4)**2, 1, oo),

   "06012-00": lambda: chain_rule_accumulation(2*t**2 + 2, 1, 2*x**3, 2),
   "06012-01": lambda: chain_rule_accumulation(6 - 2*t**2, 0, x**3, 2),
   "06012-02": lambda: chain_rule_accumulation(t**2 + 2, -2, x**3, -2),
   "06012-03": lambda: chain_rule_accumulation(2*t**2 + 3, -2, 2*x**2, -2),
   "06012-04": lambda: chain_rule_accumulation(-t**2, 3, 2*x**3, -1),

   "06013-00": lambda: combined_integral((((1, 4), 3), ((1, 10), 11)), 3, piecewise_step(-4, 3, 7), 4, 10),
   "06013-01": lambda: combined_integral((((0, 1), 3), ((0, 4), 3)), 2, piecewise_step(-2, 0, 2), 1, 4),
   "06013-02": lambda: combined_integral((((1, 3), 5), ((1, 7), -11)), 3, piecewise_step(4, -4, 4), 3, 7),
   "06013-03": lambda: combined_integral((((-2, -1), -3), ((-2, 1), -3)), 2, piecewise_step(-1, 2, 0), -1, 1),
   "06013-04": lambda: combined_integral((((1, 4), 8), ((1, 8), -5)), 2, piecewise_step(-2, -4, 7), 8, 4),

   "06014-00": lambda: riemann_sum_for_integral("06014-00", exp(x), 2, 5),
   "06014-01": lambda: riemann_sum_for_integral("06014-01", 4*x**2, 4, 10),
   "06014-02": lambda: riemann_sum_for_integral("06014-02", 3*x**2, 1, 7),
   "06014-03": lambda: riemann_sum_for_integral("06014-03", 3*sqrt(x), 1, 6),
   "06014-04": lambda: integral_for_riemann_sum("06014-04", r"\lim_{n\to\infty} \sum_{k=1}^{n} 2\left(4 + \frac{4k}{n}\right)^{2} \cdot \frac{4}{n}"),
   "06014-05": lambda: riemann_sum_for_integral("06014-05", x**2, 5, 7),
   "06014-06": lambda: riemann_sum_for_integral("06014-06", 3*sqrt(x), 3, 6),
   "06014-07": lambda: integral_for_riemann_sum("06014-07", r"\lim_{n\to\infty} \sum_{k=1}^{n} 3e^{4 + \frac{5k}{n}} \cdot \frac{5}{n}"),
   "06014-08": lambda: riemann_sum_for_integral("06014-08", 2*exp(x), 4, 6),
   "06014-09": lambda: riemann_sum_for_integral("06014-09", 3*x**2, 4, 7),
   "06014-10": lambda: integral_for_riemann_sum("06014-10", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 2\left(2 + \frac{4k}{n}\right)^{2} \cdot \frac{4}{n}"),
   "06014-11": lambda: integral_for_riemann_sum("06014-11", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 3\left(1 + \frac{2k}{n}\right)^{3} \cdot \frac{2}{n}"),
   "06014-12": lambda: riemann_sum_for_integral("06014-12", 5*x**2, 3, 9),
   "06014-13": lambda: integral_for_riemann_sum("06014-13", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 5\left(5 + \frac{4k}{n}\right)^{3} \cdot \frac{4}{n}"),
   "06014-14": lambda: integral_for_riemann_sum("06014-14", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 4\left(4 + \frac{4k}{n}\right)^{3} \cdot \frac{4}{n}"),
   "06014-15": lambda: integral_for_riemann_sum("06014-15", r"\lim_{n\to\infty} \sum_{k=1}^{n} 2\left(6 + \frac{4k}{n}\right)^{2} \cdot \frac{4}{n}"),
   "06014-16": lambda: riemann_sum_for_integral("06014-16", 4*exp(x), 6, 8),
   "06014-17": lambda: integral_for_riemann_sum("06014-17", r"\lim_{n\to\infty} \sum_{k=1}^{n} 5\sqrt{4 + \frac{3k}{n}} \cdot \frac{3}{n}"),
   "06014-18": lambda: integral_for_riemann_sum("06014-18", r"\lim_{n\to\infty} \sum_{k=1}^{n} 5e^{5 + \frac{5k}{n}} \cdot \frac{5}{n}"),
   "06014-19": lambda: integral_for_riemann_sum("06014-19", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 2\left(3 + \frac{3k}{n}\right)^{2} \cdot \frac{3}{n}"),
   "06014-20": lambda: integral_for_riemann_sum("06014-20", r"\lim_{n\to\infty} \sum_{k=1}^{n} 2\sqrt{6 + \frac{4k}{n}} \cdot \frac{4}{n}"),
   "06014-21": lambda: integral_for_riemann_sum("06014-21", r"\lim_{n\to\infty} \sum_{k=0}^{n-1} 4\sqrt{3 + \frac{4k}{n}} \cdot \frac{4}{n}"),

   **{f"06015-{index:02d}": interpretation(f"06015-{index:02d}") for index in range(22)},

   "06016-00": lambda: integral_by_parts(6*x*exp(-4*x)),
   "06016-01": lambda: rational_integral(3*x**2 + 3, x + 4),
   "06016-02": lambda: integral_by_parts(x*exp(-2*x)),
   "06016-03": lambda: rational_integral(6*x**2 + 42, x + 5),
   "06016-04": lambda: integral_by_parts(4*x*exp(-3*x)),
   "06016-05": lambda: rational_integral(6*x**2 + 12, x - 3),
   "06016-06": lambda: rational_integral(4*x**2 + 20, x - 1),
   "06016-07": lambda: integral_by_parts(x*exp(2*x)),
   "06016-08": lambda: integral_by_parts(5*x*exp(-3*x)),
   "06016-09": lambda: integral_by_parts(x*exp(-3*x)),
   "06016-10": lambda: integral_by_parts(5*x*exp(x)),
   "06016-11": lambda: rational_integral(3*x**2 + 9, x + 3),
   "06016-12": lambda: integral_by_parts(2*x*exp(x)),
   "06016-13": lambda: integral_by_parts(6*x*exp(3*x)),
   "06016-14": lambda: rational_integral(4*x**2 + 36, x - 1),
   "06016-15": lambda: integral_by_parts(6*x*exp(-2*x)),
   "06016-16": lambda: rational_integral(5*x**2 + 45, x + 4),
   "06016-17": lambda: integral_by_parts(x*exp(-x)),
   "06016-18": lambda: rational_integral(4*x**2 + 16, x + 3),
   "06016-19": lambda: rational_integral(3*x**2 + 18, x + 1),
   "06016-20": lambda: integral_by_parts(2*x*exp(-4*x)),
   "06016-21": lambda: rational_integral(4*x**2 + 16, x - 4),
}

FORMULATIONS = {f"ITM-GEN-{suffix}": formulation for suffix, formulation in BY_SUFFIX.items()}
