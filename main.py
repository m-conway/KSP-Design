from Data.constants import constants as c

from utilities import load_data, print_result
from Data.planets import planets


import math
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


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


def vertical_launch():

    def rocket_propulsion_equation(t, y, I_sp, burn_rate, body):
        v, h, m = y

        radius = body["radius"]
        C_D = 1.2  # Made up placeholder.

        gravity = c["G0"] * (radius / (radius + h)) ** 2  # From: g  = G m/r^2
        drag = C_D * v

        dmdt = -burn_rate
        dvdt = (-I_sp * c["G0"] / m) * dmdt - gravity - drag / m
        dhdt = v

        return dvdt, dhdt, dmdt

    I_sp = 250
    m_0 = 12700
    m_p = 8610
    t_burn = 60
    burn_rate = m_p / t_burn

    sol = solve_ivp(
        rocket_propulsion_equation,
        [0, t_burn],
        [0, 0, m_0],
        args=(I_sp, burn_rate, planets["Earth"]),
        dense_output=True,
    )

    time = np.linspace(0, t_burn, 100)
    z = sol.sol(time)

    _, axes = plt.subplots(3, 1)

    axes[0].plot(time, z[0, :])
    axes[0].set_ylabel("Velocity (m/s)")
    axes[0].grid(True)

    axes[1].plot(time, z[1, :] / 1000)
    axes[1].set_ylabel("Altitude (km)")
    axes[1].grid(True)

    axes[2].plot(time, z[2, :])
    axes[2].set_ylabel("Prop (kg)")
    axes[2].set_xlabel("Time (s)")
    axes[2].grid(True)

    plt.show()

    print(f"Burnout velocity: {z[0,-1]: 5.2f} m/s")
    print(f"Burnout altitude: {z[1,-1]/1000: 5.2f} km")


if __name__ == "__main__":
    # dV = compute_delta_veocity(340, 24.81, 8.81)
    # print_result(dV, "m/s")
    # print(dV)

    # delta_v = compute_hoffman_transfer(250e3, 42164.154e3, planets["Earth"])
    # print_result(delta_v, "m/s")

    # delta_v = compute_hoffman_transfer(70e3, 1000e3, planets["Kerbin"])
    # print_result(delta_v, "m/s")

    vertical_launch()
