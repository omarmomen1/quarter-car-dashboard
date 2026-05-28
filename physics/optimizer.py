"""
physics/optimizer.py
====================
Setup Solver Optimization Engine
"""
import numpy as np
from scipy.optimize import minimize

from physics.quarter_car import (
    QuarterCarParams,
    RoadProfile,
    run_quarter_car_analysis
)

def objective(x, base_params: QuarterCarParams, profile: RoadProfile, objective_type: str, max_travel: float):
    ks = x[0]
    c = x[1]

    p = QuarterCarParams(
        m_s=base_params.m_s,
        m_u=base_params.m_u,
        k_s=ks,
        c=c,
        k_t=base_params.k_t,
        c_t=base_params.c_t,
        MR=base_params.MR  # Fixed to match your dataclass
    )

    # Run lower-res simulation for speed during optimization loops
    result = run_quarter_car_analysis(p, profile, f_min=1.0, f_max=20.0, n_freq=100)

    # Fixed to match your QuarterCarResult attributes
    rms_accel = result.rms_body_accel
    peak_travel = result.peak_susp_travel

    penalty = 0
    if peak_travel > max_travel:
        penalty += 100000 * (peak_travel - max_travel) ** 2

    if objective_type == "Ride Comfort":
        cost = rms_accel
    elif objective_type == "Min Travel":
        cost = peak_travel * 100
    else: # Balanced
        cost = rms_accel + (peak_travel * 10)

    return cost + penalty


def optimize_setup(base_params: QuarterCarParams, profile: RoadProfile, objective_type: str, max_travel: float):
    x0 = [base_params.k_s, base_params.c]

    bounds = [
        (10000.0, 150000.0), # Spring Rate bounds
        (500.0, 15000.0)     # Damping bounds
    ]

    sol = minimize(
        objective,
        x0=x0,
        args=(base_params, profile, objective_type, max_travel),
        bounds=bounds,
        method="L-BFGS-B"
    )

    return {
        "optimal_ks": float(sol.x[0]),
        "optimal_c": float(sol.x[1]),
        "success": sol.success
    }