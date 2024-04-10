from Data.constants import constants as c

from utilities import load_data, print_result
from Data.planets import planets


import math


def compute_delta_veocity(isp, mass_i, mass_f):
    # dV = ve * ln(mi / mf)
    # dV = Isp * g0 * ln(mi / mf)

    delta_V = isp * c["G0"] * math.log(mass_i / mass_f)
    return delta_V


def compute_hoffman_transfer(h_i: float, r_f: float, body: dict) -> float:
    mu = body["gravitation_parameter"]

    r_e = body["radius"]
    r_i = h_i + r_e  # km

    v_i = math.sqrt(mu / r_i)
    v_f = math.sqrt(mu / r_f)

    r_p = r_i
    r_a = r_f

    h_t = math.sqrt(2 * mu * r_a * r_p / (r_a + r_p))

    v_tp = h_t / r_p
    v_ta = h_t / r_a

    delta_v = abs(v_f - v_ta) + abs(v_tp - v_i)

    return delta_v


if __name__ == "__main__":
    # dV = compute_delta_veocity(340, 24.81, 8.81)
    # print_result(dV, "m/s")
    # print(dV)

    delta_v = compute_hoffman_transfer(250e3, 42164.154e3, planets["Earth"])
    print_result(delta_v, "m/s")

    delta_v = compute_hoffman_transfer(70e3, 1000e3, planets["Kerbin"])
    print_result(delta_v, "m/s")
