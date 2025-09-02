import unittest
import numpy as np
from pyfiberamp.fibers.passive_fiber import PassiveFiber
from pyfiberamp.fibers.active_fiber import ActiveFiber
from pyfiberamp.channels import Channels
from pyfiberamp.spectroscopies.spectroscopy import Spectroscopy
from pyfiberamp.helper_funcs import wl_to_freq

class ModeAreaOverlapTestCase(unittest.TestCase):
    def test_core_area_override(self):
        mode_area = 50e-12
        fiber = PassiveFiber(length=1, mode_area=mode_area)
        self.assertAlmostEqual(fiber.core_area(), mode_area)

    def test_channel_from_overlaps(self):
        mode_area = 30e-12
        core_radius = np.sqrt(mode_area/np.pi)
        absorption = np.array([[1e-6, 1e-24], [1.1e-6, 1e-24]])
        emission = np.array([[1e-6, 2e-24], [1.1e-6, 2e-24]])
        spec = Spectroscopy(absorption, emission, 1e-3, 'linear')
        ion_density = 1e25
        fiber = ActiveFiber(length=1, core_radius=core_radius, spectroscopy=spec,
                            ion_number_density=ion_density, mode_area=mode_area)
        channels = Channels(fiber)
        overlap = 0.5
        wl = 1.05e-6
        channels.create_channel('signal', 1, fiber, input_power=1.0, wl=wl,
                                 overlaps=np.array([overlap]))
        ch = channels.forward_signals[0]
        freq = wl_to_freq(wl)
        gcs = spec.gain_cs_interp(freq)
        acs = spec.absorption_cs_interp(freq)
        expected_gain = overlap * gcs * ion_density
        expected_abs = overlap * acs * ion_density
        self.assertAlmostEqual(ch.gain[0], expected_gain)
        self.assertAlmostEqual(ch.absorption[0], expected_abs)

if __name__ == '__main__':
    unittest.main()
