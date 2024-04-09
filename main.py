import constants as c

from utilities import load_data, print_result


import math


def compute_delta_veocity(isp, mass_i, mass_f):
    # dV = ve * ln(mi / mf)
    # dV = Isp * g0 * ln(mi / mf)

    delta_V = isp * c.G0 * math.log(mass_i / mass_f)
    return delta_V

dV = compute_delta_veocity(340, 24.81, 8.81)
print_result(dV, "m/s")