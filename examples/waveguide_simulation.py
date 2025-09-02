"""Waveguide simulation example using custom mode area and overlaps.

This script demonstrates how to simulate amplification in an integrated
waveguide without relying on a mode solver.  The effective mode area and
modal overlaps are supplied directly by the user.
"""

from pathlib import Path
import sys
import numpy as np

# Allow running the example without installing the package
sys.path.append(str(Path(__file__).resolve().parents[1]))

from pyfiberamp.fibers.yb_doped_fiber import YbDopedFiber
from pyfiberamp.steady_state import SteadyStateSimulation


# Effective mode area of the waveguide (m^2). For a rectangular
# 4.5 µm x 4.5 µm waveguide this is roughly 20e-12 m^2.
MODE_AREA = 20e-12
ION_DENSITY = 1e25  # 1/m^3

# Create a Yb-doped waveguide using the supplied mode area.
fiber = YbDopedFiber(length=0.02, ion_number_density=ION_DENSITY,
                     mode_area=MODE_AREA)

# Set up a simple forward‑pumped amplifier: a pump at 980 nm and a
# small signal at 1030 nm.  The modal overlaps with the doped region are
# specified directly and no mode solver is needed.
sim = SteadyStateSimulation(fiber)
sim.add_forward_pump(wl=980e-9, input_power=5.0, overlap=0.9)
sim.add_forward_signal(wl=1030e-9, input_power=1e-3, overlap=0.85)

# Run the simulation and print the output powers.
result = sim.run()
for cid, ch in result.make_result_dict().items():
    print(f"{cid}: output {ch['output_power']:.3f} W, gain {ch['gain']:.2f} dB")
