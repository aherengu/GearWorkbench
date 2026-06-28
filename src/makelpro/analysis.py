"""Pure analysis helpers used for smoke tests and scripted checks."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class GearboxInputs:
    inputTorqueNm: float = 300.0
    inputSpeedRpm: float = 40.0
    normalPressureAngleDeg: float = 20.0
    helixAngleDeg: float = 30.0
    stage1Ratio: float = 5.0
    stage2Ratio: float = 6.0
    gear2DiameterMm: float = 300.0
    gear4DiameterMm: float = 300.0


def deg_to_rad(deg: float) -> float:
    return deg * math.pi / 180.0


def transverse_pressure_angle_deg(phi_n_deg: float, helix_deg: float) -> float:
    phi_n_rad = deg_to_rad(phi_n_deg)
    psi_rad = deg_to_rad(helix_deg)
    tan_phi_t = math.tan(phi_n_rad) / math.cos(psi_rad)
    return math.degrees(math.atan(tan_phi_t))


def mesh_forces(
    torque_nm: float,
    driver_diameter_mm: float,
    phi_n_deg: float,
    helix_deg: float,
) -> tuple[float, float, float, float]:
    phi_t_deg = transverse_pressure_angle_deg(phi_n_deg, helix_deg)
    tan_phi_t = math.tan(deg_to_rad(phi_t_deg))
    tan_psi = math.tan(deg_to_rad(helix_deg))
    tangential_force_n = 2000.0 * torque_nm / max(1e-9, driver_diameter_mm)
    radial_force_n = tangential_force_n * tan_phi_t
    axial_force_n = tangential_force_n * tan_psi
    return tangential_force_n, radial_force_n, axial_force_n, phi_t_deg


def default_mesh_summary(inputs: GearboxInputs | None = None) -> dict[str, float]:
    values = inputs or GearboxInputs()
    ft23, fr23, fa23, phi_t = mesh_forces(
        values.inputTorqueNm,
        values.gear2DiameterMm,
        values.normalPressureAngleDeg,
        values.helixAngleDeg,
    )
    intermediate_torque_nm = values.inputTorqueNm / values.stage1Ratio
    ft45, fr45, fa45, _ = mesh_forces(
        intermediate_torque_nm,
        values.gear4DiameterMm,
        values.normalPressureAngleDeg,
        values.helixAngleDeg,
    )
    return {
        "phi_t_deg": phi_t,
        "ft23_n": ft23,
        "fr23_n": fr23,
        "fa23_n": fa23,
        "resultant23_n": math.hypot(ft23, fr23),
        "ft45_n": ft45,
        "fr45_n": fr45,
        "fa45_n": fa45,
        "resultant45_n": math.hypot(ft45, fr45),
    }
