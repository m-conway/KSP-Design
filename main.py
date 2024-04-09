import constants as c

from utilities import load_data, print_result
from planets import kerbin


import math


def compute_delta_veocity(isp, mass_i, mass_f):
    # dV = ve * ln(mi / mf)
    # dV = Isp * g0 * ln(mi / mf)

    delta_V = isp * c.G0 * math.log(mass_i / mass_f)
    return delta_V


def compute_hoffman_transfer():
    # Example transfer to GEO orbit
    mu = 3.986e5 * 1000**3  # m**3/s**2
    r_e = 6378e3  # m
    r_leo = 250e3 + r_e  # km
    v_leo = math.sqrt(mu / r_leo)
    print_result(v_leo, "m/s")

    sidereal_day = 86164.0905  # s
    r_cubed = mu * sidereal_day**2 / (4 * math.pi**2)
    r_geo = r_cubed ** (1 / 3)
    v_geo = math.sqrt(mu / r_geo)
    print_result(r_geo, "m")
    print_result(v_geo, "m/s")

    r_p = r_leo
    r_a = r_geo
    h_t = math.sqrt(2 * mu * r_a * r_p / (r_a + r_p))
    v_tp = h_t / r_p
    v_ta = h_t / r_a
    print_result(v_tp, "m/s")
    print_result(v_ta, "m/s")

    delat_v = abs(v_geo - v_ta) + abs(v_tp - v_leo)
    I_sp = 450.5  # s
    geos_mass = 5_192e3  # g
    delta_m = geos_mass * (1 - math.exp(-delat_v / (I_sp * c.G0)))
    print_result(delat_v, "m/s")
    print_result(delta_m, "g")


if __name__ == "__main__":
    # dV = compute_delta_veocity(340, 24.81, 8.81)
    # print_result(dV, "m/s")
    # print(dV)

    compute_hoffman_transfer()
