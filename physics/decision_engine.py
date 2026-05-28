"""
physics/decision_engine.py
==========================
SuspensionLab PRO — Decision Consistency Engine

Unifies numerical optimization (L-BFGS-B) with heuristic engineering diagnostics.
Acts as the single source of truth for UI setup recommendations.
"""

from typing import Dict, Any
from physics.quarter_car import QuarterCarResult

def generate_setup_verdict(result: QuarterCarResult, optimizer_output: Dict[str, Any]) -> Dict[str, str]:
    if not optimizer_output.get("success", False):
        return {
            "status": "FAILED",
            "headline": "OPTIMIZATION FAILED",
            "message": "The solver could not converge on a valid setup within the given constraints.",
            "action": "Relax maximum travel constraints or adjust objective weights."
        }

    # Defensive fallback for zeta_s
    new_zeta = getattr(result, "zeta_s", None)
    if new_zeta is None:
        new_zeta = getattr(result, "metrics", {}).get("zeta_s", 0.0)

    # 1. Damping Conflict: Optimizer brute-forces resonance control
    if new_zeta > 0.65:
        return {
            "status": "CONFLICT",
            "headline": "CONFLICT DETECTED: NUMERICAL VS. HEURISTIC",
            "message": "Optimization improved comfort numerically, but setup exceeds traditional damping guidelines.",
            "action": "Likely tradeoff between resonance suppression and sharp-input harshness. Accept for aero-platform stability; override and soften for road compliance."
        }
        
    # 2. Damping Conflict: Optimizer chases theoretical isolation at the cost of stability
    if new_zeta < 0.25:
        return {
            "status": "CONFLICT",
            "headline": "CONFLICT DETECTED: ISOLATION VS. STABILITY",
            "message": f"Optimizer minimized RMS acceleration by dropping damping dangerously low (ζ = {new_zeta:.2f}).",
            "action": "Override solver. Increase rebound damping manually to maintain safe chassis control over crests."
        }

    # 3. Packaging Conflict: Optimizer ignoring bump stops to chase comfort
    peak_travel_mm = result.peak_susp_travel * 1000.0
    if peak_travel_mm > 75.0:
        return {
            "status": "CONFLICT",
            "headline": "CONFLICT DETECTED: VIRTUAL VS. PHYSICAL LIMITS",
            "message": f"Optimizer achieved objective, but peak travel ({peak_travel_mm:.1f} mm) will likely strike physical bump stops.",
            "action": "Reject setup. Re-run optimizer with a stricter 'Max Allowed Travel' constraint."
        }

    # 4. Total Alignment
    return {
        "status": "ALIGNED",
        "headline": "SETUP VERIFIED: UNIFIED AGREEMENT",
        "message": "Mathematical optimization perfectly aligns with established engineering heuristics.",
        "action": "Apply setup confidently. No conflicting diagnostics detected."
    }