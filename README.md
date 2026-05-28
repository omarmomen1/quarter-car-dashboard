# 🏎️ SuspensionLab PRO — Quarter Car Simulation

A professional-grade 2-DOF quarter-car suspension dynamics dashboard. This tool simulates ride comfort, handling, and NVH (Noise, Vibration, and Harshness) metrics using both time-domain and frequency-domain numerical methods.

## Engineering Features

* **Physics Engine:** 2-DOF linear quarter-car model utilizing SciPy's `solve_ivp` (RK45) for time-domain integration.
* **Frequency Response:** Exact analytical impedance matrix inversion for Bode plots and transmissibility analysis.
* **ISO 2631-1 Comfort Metrics:** Automatic calculation of unweighted RMS sprung body acceleration.
* **Engineering Diagnostics:** Automated detection of critically underdamped states, wheel hop risks, and suspension travel limit violations.
* **Interactive Telemetry:** Formula 1 pit-wall inspired visualization layer built with Plotly.

## Repository Structure

* `ui/pages/` — Streamlit dashboard and user interface logic.
* `physics/` — Core mathematical models, state-space formulation, and ODE solver.
* `visualization/` — Plotly trace generation and aesthetic theme enforcement.

## Installation & Usage

Ensure you have Python installed, then install the required dependencies:

```bash
pip install streamlit scipy numpy pandas plotly