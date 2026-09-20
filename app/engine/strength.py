"""The PFA strength formula, m_k = beta + gamma * log(1 + c) + rho * log(1 + f)."""
import math

from app.engine import constants


def phi(count):
   return math.log1p(count)


def sigmoid(logit):
   return 1.0 / (1.0 + math.exp(-logit))


def strength(state, retrievability=1.0):
   decay_penalty = constants.LAMBDA * (1.0 - retrievability)

   return state.beta + constants.GAMMA * phi(state.c) + constants.RHO * phi(state.f) - decay_penalty


def probability(state, retrievability=1.0):
   return sigmoid(strength(state, retrievability))
