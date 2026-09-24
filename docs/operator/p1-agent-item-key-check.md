---
title: Mechanical key check of the 130 agent-drafted P1 items
research_date: 2026-09-23
status: pending_operator_review
purpose: Lists, per agent-drafted item, the answer SymPy computes from the stem alone beside the stored key, so the operator's sign-off and key audit start from a checked list.
---

# Mechanical key check of the 130 agent-drafted P1 items [verified]

Each stem in `content/items_p1_agent/` was written out as a SymPy computation from the stem text alone, without reading the stored key: the limit, derivative, continuity equation, domain interval, tangent line, implicit derivative or second derivative the stem asks for. The result was compared with the stored key through `app/items/mathjson.py` `to_sympy`, by symbolic simplification and, when that did not close, by numeric evaluation at 12 seeded points, at least 6 of which had to evaluate. Every MCQ option was compared the same way, so a distractor equal to the key would show.

Result: 130 of 130 keys match. On every item that carries options, exactly one option equals the computed answer, and it is the option marked as the key. The ten stated dy/dx formulas in BC-QA-03005 stems all equal the implicit derivative of the stated curve.

Positive control, same run: five planted wrong answers (01004-00, 02008-04, 02010-03, 03004-06, 03005-09) were all reported as differing from the key, and three of them were reported as equal to a distractor. A sign-flipped dy/dx on 03005-00 was reported wrong.

## What this does not settle [inferred]

This is a model's check, not the operator's. It says the stored key is the correct answer to the stem as written; it does not judge whether a stem reads ambiguously to a student, which gate 29 defines as the operator's judgement. The formulations were written by the same model family that drafted the items, so a stem both misread the same way would pass. None of these items has provenance `operator`, so none counts toward exit criterion 7 or gates 17, 29 and 30.

## Stem wording changed in this pass [verified]

R29 serves every item as a short answer at stages example and completion and on alternate attempts at stage unsupported (`app/engine/select.py` `format_for_attempt`), and nothing rewrites a stem for the served format. 27 stems asked "Which of the following is ...", which reads wrongly when no options are shown, so each became "Find ..." with the rest of the sentence unchanged. No key, option or worked solution changed. The items are marked in the table.

## Per item [verified]

| Item | Format | Stored key | Computed from the stem | Result | Stem reworded |
| --- | --- | --- | --- | --- | --- |
| ITM-AGT-01004-00 | mcq | `5/6` | `5/6` | match |  |
| ITM-AGT-01004-01 | short_answer | `2` | `2` | match |  |
| ITM-AGT-01004-02 | short_answer | `7/8` | `7/8` | match |  |
| ITM-AGT-01004-03 | mcq | `3/2` | `3/2` | match |  |
| ITM-AGT-01004-04 | short_answer | `4/3` | `4/3` | match |  |
| ITM-AGT-01004-05 | mcq | `5/4` | `5/4` | match |  |
| ITM-AGT-01004-06 | mcq | `-1` | `-1` | match |  |
| ITM-AGT-01004-07 | short_answer | `5/3` | `5/3` | match |  |
| ITM-AGT-01004-08 | mcq | `1/2` | `1/2` | match |  |
| ITM-AGT-01004-09 | short_answer | `-1/4` | `-1/4` | match |  |
| ITM-AGT-01008-00 | mcq | `3` | `3` | match |  |
| ITM-AGT-01008-01 | short_answer | `3` | `3` | match |  |
| ITM-AGT-01008-02 | mcq | `2` | `2` | match |  |
| ITM-AGT-01008-03 | mcq | `1` | `1` | match |  |
| ITM-AGT-01008-04 | short_answer | `5/2` | `5/2` | match |  |
| ITM-AGT-01008-05 | mcq | `5` | `5` | match |  |
| ITM-AGT-01008-06 | short_answer | `2` | `2` | match |  |
| ITM-AGT-01008-07 | mcq | `-1` | `-1` | match |  |
| ITM-AGT-01008-08 | short_answer | `2` | `2` | match |  |
| ITM-AGT-01008-09 | mcq | `-2` | `-2` | match |  |
| ITM-AGT-01015-00 | mcq | `5` | `5` | match |  |
| ITM-AGT-01015-01 | short_answer | `1` | `1` | match |  |
| ITM-AGT-01015-02 | mcq | `-2` | `-2` | match |  |
| ITM-AGT-01015-03 | mcq | `15` | `15` (left limit at 3 = 1, f(3) = 1, joint continuous True) | match |  |
| ITM-AGT-01015-04 | short_answer | `5` | `5` | match |  |
| ITM-AGT-01015-05 | mcq | `3` | `3` | match |  |
| ITM-AGT-01015-06 | short_answer | `-10` | `-10` | match |  |
| ITM-AGT-01015-07 | mcq | `9` | `9` | match |  |
| ITM-AGT-01015-08 | short_answer | `4` | `4` (left limit at 1 = 3/5, f(1) = 3/5, joint continuous True) | match |  |
| ITM-AGT-01015-09 | mcq | `-5` | `-5` | match |  |
| ITM-AGT-02002-00 | mcq | `6*x - 5` | `6*x - 5` | match |  |
| ITM-AGT-02002-01 | short_answer | `10` | `10` | match |  |
| ITM-AGT-02002-02 | short_answer | `-4*x` | `-4*x` | match |  |
| ITM-AGT-02002-03 | short_answer | `1/6` | `1/6` | match |  |
| ITM-AGT-02002-04 | mcq | `-3/(3*x + 1)^2` | `-3/(9*x^2 + 6*x + 1)` | match |  |
| ITM-AGT-02002-05 | short_answer | `1` | `1` | match |  |
| ITM-AGT-02002-06 | mcq | `1/sqrt(2*x + 5)` | `1/sqrt(2*x + 5)` | match |  |
| ITM-AGT-02002-07 | short_answer | `-1` | `-1` | match |  |
| ITM-AGT-02002-08 | short_answer | `(x + 1)^(-2)` | `1/(x^2 + 2*x + 1)` | match |  |
| ITM-AGT-02002-09 | short_answer | `12` | `12` | match |  |
| ITM-AGT-02006-00 | short_answer | `20*x^3 - 6*x + 8` | `20*x^3 - 6*x + 8` | match |  |
| ITM-AGT-02006-01 | mcq | `6*x + 3/sqrt(x)` | `6*x + 3/sqrt(x)` | match | yes |
| ITM-AGT-02006-02 | mcq | `6*x^2 - 8/x^3` | `2*(3*x^5 - 4)/x^3` | match | yes |
| ITM-AGT-02006-03 | mcq | `15` | `15` | match |  |
| ITM-AGT-02006-04 | short_answer | `40*x^3 - 6/x^3` | `2*(20*x^6 - 3)/x^3` | match |  |
| ITM-AGT-02006-05 | mcq | `4*x^3 + 4/x^(1/3)` | `4*(x^4 + (x^2)^(1/3))/x` | match | yes |
| ITM-AGT-02006-06 | mcq | `10*x + x^(-3/2)` | `10*x + x^(-3/2)` | match | yes |
| ITM-AGT-02006-07 | short_answer | `41/8` | `41/8` | match |  |
| ITM-AGT-02006-08 | mcq | `4` | `4` | match |  |
| ITM-AGT-02006-09 | short_answer | `-12/s^5 - 4/s^(3/5)` | `-4*(s^2)^(1/5)/s - 12/s^5` | match |  |
| ITM-AGT-02007-00 | mcq | `3*exp(x) - 5*sin(x)` | `3*exp(x) - 5*sin(x)` | match | yes |
| ITM-AGT-02007-01 | mcq | `3*x^2 + exp(x) + 4*sin(x)` | `3*x^2 + exp(x) + 4*sin(x)` | match | yes |
| ITM-AGT-02007-02 | short_answer | `-exp(x) - 2*sin(x) + 7/x` | `-exp(x) - 2*sin(x) + 7/x` | match |  |
| ITM-AGT-02007-03 | mcq | `-2*exp(pi/2) - 3` | `-2*exp(pi/2) - 3` | match |  |
| ITM-AGT-02007-04 | short_answer | `-3/2 + exp(pi/6) + 12/pi` | `-3/2 + exp(pi/6) + 12/pi` | match |  |
| ITM-AGT-02007-05 | mcq | `exp(x) + 2*sin(x) + 3/x` | `exp(x) + 2*sin(x) + 3/x` | match | yes |
| ITM-AGT-02007-06 | short_answer | `4*t^3 + 5*exp(t) + 3*sin(t)` | `4*t^3 + 5*exp(t) + 3*sin(t)` | match |  |
| ITM-AGT-02007-07 | mcq | `-3 - exp(pi/6)` | `-3 - exp(pi/6)` | match |  |
| ITM-AGT-02007-08 | short_answer | `exp(x) - 2*sin(x) - 4*cos(x) + 3/x` | `exp(x) - 2*sin(x) - 4*cos(x) + 3/x` | match |  |
| ITM-AGT-02007-09 | mcq | `7*exp(x) - sin(x) - 2/x` | `7*exp(x) - sin(x) - 2/x` | match | yes |
| ITM-AGT-02008-00 | mcq | `(x^2 + 1)*exp(x)/(x + 1)^2` | `(x*(x + 1) - x + 1)*exp(x)/(x + 1)^2` | match | yes |
| ITM-AGT-02008-01 | short_answer | `-pi*(2 + pi)/(1 + pi)^2` | `pi*(-pi - 2)/(1 + pi)^2` | match |  |
| ITM-AGT-02008-02 | mcq | `-(x^2 + x + 1)*exp(-x)/x^2` | `(-x^2 - x - 1)*exp(-x)/x^2` | match | yes |
| ITM-AGT-02008-03 | mcq | `(x^2 + 2*x)*exp(x)/4` | `x*(x + 2)*exp(x)/4` | match | yes |
| ITM-AGT-02008-04 | short_answer | `(x^4 + x^2 + 2*x)*exp(x)/(x^2 + 1)^2` | `x*(x^3 + x + 2)*exp(x)/(x^4 + 2*x^2 + 1)` | match |  |
| ITM-AGT-02008-05 | mcq | `(sin(x) + 1)*exp(x)/(cos(x) + 1)` | `(sqrt(2)*(cos(x) + 1)*sin(x + pi/4) + sin(x)^2)*exp(x)/(cos(x) + 1)^2` | match | yes |
| ITM-AGT-02008-06 | mcq | `3*E/4` | `3*E/4` | match |  |
| ITM-AGT-02008-07 | short_answer | `t*(t^2 + 2*t + 2)*exp(t)/(t + 1)^2` | `t*(t^2 + 2*t + 2)*exp(t)/(t^2 + 2*t + 1)` | match |  |
| ITM-AGT-02008-08 | mcq | `4/9` | `4/9` | match |  |
| ITM-AGT-02008-09 | short_answer | `(x + 2*log(x) + 2)/(x + 2)^2` | `(x + 2*log(x) + 2)/(x^2 + 4*x + 4)` | match |  |
| ITM-AGT-02010-00 | mcq | `-cot(x)*csc(x) - csc(x)^2` | `-(cos(x) + 1)/sin(x)^2` | match |  |
| ITM-AGT-02010-01 | mcq | `-3*cot(x)*csc(x) + 2*csc(x)^2` | `(2 - 3*cos(x))/sin(x)^2` | match |  |
| ITM-AGT-02010-02 | mcq | `-2*pi/3 + sqrt(3)` | `-2*pi/3 + sqrt(3)` | match |  |
| ITM-AGT-02010-03 | mcq | `-csc(x)^2 + sec(x)^2` | `tan(x)^2 - cot(x)^2` | match |  |
| ITM-AGT-02010-04 | mcq | `-cot(t)^2*csc(t) - csc(t)^3` | `(1 - 2/sin(t)^2)*csc(t)` | match |  |
| ITM-AGT-02010-05 | mcq | `8 - 2*sqrt(3)` | `8 - 2*sqrt(3)` | match |  |
| ITM-AGT-02010-06 | mcq | `-x^2*csc(x)^2 + 2*x*cot(x)` | `x*(-x/sin(x)^2 + 2/tan(x))` | match |  |
| ITM-AGT-02010-07 | short_answer | `-tan(x)*sec(x) + 6*sec(x)^2` | `(6 - sin(x))/cos(x)^2` | match |  |
| ITM-AGT-02010-08 | short_answer | `tan(theta)^2*sec(theta) + sec(theta)^3` | `(2*tan(theta)^2 + 1)*sec(theta)` | match |  |
| ITM-AGT-02010-09 | short_answer | `-44/3` | `-44/3` | match |  |
| ITM-AGT-02011-00 | mcq | `5*x + 7` | `5*x + 7` | match | yes |
| ITM-AGT-02011-01 | mcq | `-x - 4` | `-x - 4` | match | yes |
| ITM-AGT-02011-02 | mcq | `-8*x - 12` | `-8*x - 12` | match | yes |
| ITM-AGT-02011-03 | mcq | `21/10` | `21/10` | match |  |
| ITM-AGT-02011-04 | mcq | `-9*x - 1` | `-9*x - 1` | match | yes |
| ITM-AGT-02011-05 | mcq | `(1 - pi/2)*(x + pi/2)` | `-pi*x/2 + x - pi^2/4 + pi/2` | match | yes |
| ITM-AGT-02011-06 | short_answer | `6*x - 4` | `6*x - 4` | match |  |
| ITM-AGT-02011-07 | short_answer | `2*x - E` | `2*x - E` | match |  |
| ITM-AGT-02011-08 | short_answer | `48/25 - 9*x/25` | `48/25 - 9*x/25` | match |  |
| ITM-AGT-02011-09 | short_answer | `-9/2` | `-9/2` | match |  |
| ITM-AGT-03001-00 | mcq | `15*x*sin(5*x)^2*cos(5*x) + sin(5*x)^3` | `(15*x*cos(5*x) + sin(5*x))*sin(5*x)^2` | match | yes |
| ITM-AGT-03001-01 | mcq | `x*(3*x + 2)*exp(3*x)` | `x*(3*x + 2)*exp(3*x)` | match | yes |
| ITM-AGT-03001-02 | short_answer | `7` | `7` | match |  |
| ITM-AGT-03001-03 | mcq | `(-2*x*sin(2*x) - cos(2*x))/x^2` | `-(2*x*sin(2*x) + cos(2*x))/x^2` | match | yes |
| ITM-AGT-03001-04 | short_answer | `-2*x^2*tan(x^2) + log(cos(x^2))` | `-2*x^2*tan(x^2) + log(cos(x^2))` | match | yes |
| ITM-AGT-03001-05 | mcq | `1 - pi` | `1 - pi` | match |  |
| ITM-AGT-03001-06 | mcq | `(x^2 + 1)^4*(11*x^2 + 1)` | `(x^2 + 1)^4*(11*x^2 + 1)` | match | yes |
| ITM-AGT-03001-07 | short_answer | `5/27` | `5/27` | match |  |
| ITM-AGT-03001-08 | mcq | `x^2/((x^2 + 1)*sqrt(log(x^2 + 1))) + sqrt(log(x^2 + 1))` | `(x^2 + (x^2 + 1)*log(x^2 + 1))/((x^2 + 1)*sqrt(log(x^2 + 1)))` | match | yes |
| ITM-AGT-03001-09 | short_answer | `(1 + sqrt(3))*exp(pi/3)/2` | `(1 + sqrt(3))*exp(pi/3)/2` | match |  |
| ITM-AGT-03004-00 | mcq | `-(2*x + 4*y)/(4*x + 3*y^2)` | `2*(-x - 2*y)/(4*x + 3*y^2)` | match |  |
| ITM-AGT-03004-01 | short_answer | `(-y*cos(x) + 4)/(2*y + sin(x))` | `(-y*cos(x) + 4)/(2*y + sin(x))` | match |  |
| ITM-AGT-03004-02 | mcq | `1/5` | `1/5` | match |  |
| ITM-AGT-03004-03 | short_answer | `2` | `2` (y roots with y>1 at x=1: [2]) | match |  |
| ITM-AGT-03004-04 | short_answer | `7` | `7` | match |  |
| ITM-AGT-03004-05 | short_answer | `5` | `5` | match |  |
| ITM-AGT-03004-06 | mcq | `(12*x^2 + 5*y)/(-5*x + 2*y)` | `(-12*x^2 - 5*y)/(5*x - 2*y)` | match | yes |
| ITM-AGT-03004-07 | short_answer | `(6*x^2 + y^2)/(-2*x*y + 7)` | `(-6*x^2 - y^2)/(2*x*y - 7)` | match |  |
| ITM-AGT-03004-08 | mcq | `-4/13` | `-4/13` | match |  |
| ITM-AGT-03004-09 | mcq | `(4*x - y^2)/(2*x*y + 3)` | `(4*x - y^2)/(2*x*y + 3)` | match | yes |
| ITM-AGT-03005-00 | mcq | `3` | `3` | match |  |
| ITM-AGT-03005-01 | short_answer | `8` | `8` | match |  |
| ITM-AGT-03005-02 | mcq | `-2` | `-2` | match |  |
| ITM-AGT-03005-03 | mcq | `-4` | `-4` | match |  |
| ITM-AGT-03005-04 | short_answer | `-2` | `-2` (horizontal k values [-4, -2]) | match |  |
| ITM-AGT-03005-05 | short_answer | `2 + 2*sqrt(3)` | `2 + 2*sqrt(3)` | match |  |
| ITM-AGT-03005-06 | mcq | `6` | `6` (vertical k values [2, 6]) | match |  |
| ITM-AGT-03005-07 | short_answer | `4` | `4` (vertical k values [4, 6]) | match |  |
| ITM-AGT-03005-08 | mcq | `-7` | `-7` | match |  |
| ITM-AGT-03005-09 | mcq | `-4` | `-4` (horizontal k values [-4, -2]) | match |  |
| ITM-AGT-03008-00 | mcq | `6*x*log(x) + 5*x` | `x*(6*log(x) + 5)` | match | yes |
| ITM-AGT-03008-01 | mcq | `20*exp(2)` | `20*exp(2)` | match |  |
| ITM-AGT-03008-02 | short_answer | `22` | `22` | match |  |
| ITM-AGT-03008-03 | mcq | `5` | `5` | match |  |
| ITM-AGT-03008-04 | mcq | `-42/125` | `-42/125` | match |  |
| ITM-AGT-03008-05 | short_answer | `(8*x^2 + 24*x + 12)*exp(2*x)` | `(8*x^2 + 24*x + 12)*exp(2*x)` | match |  |
| ITM-AGT-03008-06 | mcq | `(x - 2)*exp(-x)` | `(x - 2)*exp(-x)` | match | yes |
| ITM-AGT-03008-07 | short_answer | `x^3 + x^2*y + 2*x + y` | `x^2*(x + y) + 2*x + y` | match |  |
| ITM-AGT-03008-08 | mcq | `12` | `12` | match |  |
| ITM-AGT-03008-09 | mcq | `9` | `9` | match |  |
