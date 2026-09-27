"""Formulations for the setup points stage 13 (content2) gave checks on the six calculator
questions of stage 6: limits written as the stem's named roots and setup equations whose unknown
is a root. Each value reuses a blind formulation from key_formulations_p5.py, written from the stem
by a separate agent on 2026-09-24, because a setup equation's unknown is the part's own answer and
a named root's value is what that file already solves for. Merged by key_formulations.py.
"""
import importlib.util
from pathlib import Path

import sympy


def stage_six_module():
   path = Path(__file__).with_name("key_formulations_p5.py")
   spec = importlib.util.spec_from_file_location("frq_formulations_p5_reused", path)
   module = importlib.util.module_from_spec(spec)
   spec.loader.exec_module(module)

   return module


blind = stage_six_module()


def turning_time_09005():
   return blind.root(blind.velocity_y_09005, blind.t, 2)


FORMULATIONS = {
   "FRQ-AGT-08001-01:b1": blind.average_crossing_08001,
   "FRQ-AGT-08001-01:c2": blind.running_average_crossing_08001,
   "FRQ-AGT-08012-01:a2": blind.crossings_08012,
   "FRQ-AGT-08012-01:c1": blind.half_volume_radius_08012,
   "FRQ-AGT-09005-01:b1": lambda: (2, turning_time_09005()),
   "FRQ-AGT-09005-01:c1": blind.time_at_x_seven_09005,
   "FRQ-AGT-09013-01:a2": blind.intersections_09013,
   "FRQ-AGT-09013-01:b2": lambda: (blind.intersections_09013()[1], sympy.pi),
   "FRQ-AGT-09013-01:c2": blind.splitting_ray_09013,
   "FRQ-AGT-99008-01:c1": blind.garage_fill_time_99008,
}
