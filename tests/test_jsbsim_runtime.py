"""Optional JSBSim runtime smoke test; set JSBSIM_ROOT to its data directory."""
import importlib.util
import os
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
JSBSIM_ROOT = os.environ.get("JSBSIM_ROOT")


@unittest.skipUnless(
    importlib.util.find_spec("jsbsim") and JSBSIM_ROOT,
    "optional: install the jsbsim Python module and set JSBSIM_ROOT",
)
class JSBSimRuntimeTests(unittest.TestCase):
    def test_aircraft_loads_and_integrates(self):
        source_data = Path(JSBSIM_ROOT).resolve()
        self.assertTrue((source_data / "engine/direct.xml").is_file(), "JSBSIM_ROOT must contain engine/direct.xml")

        with tempfile.TemporaryDirectory(prefix="a350-jsbsim-") as temporary:
            runtime_root = Path(temporary)
            aircraft_dir = runtime_root / "aircraft/A350"
            engine_dir = runtime_root / "engine"
            aircraft_dir.mkdir(parents=True)
            engine_dir.mkdir(parents=True)
            (runtime_root / "systems").mkdir()
            shutil.copy2(ROOT / "A350.xml", aircraft_dir / "A350.xml")
            shutil.copy2(ROOT / "Engines/TrentXWB84.xml", engine_dir / "TrentXWB84.xml")
            shutil.copy2(source_data / "engine/direct.xml", engine_dir / "direct.xml")

            import jsbsim

            fdm = jsbsim.FGFDMExec(str(runtime_root))
            fdm.set_aircraft_path("aircraft")
            fdm.set_engine_path("engine")
            fdm.set_systems_path("systems")
            self.assertTrue(fdm.load_model("A350"))
            initial_conditions = {
                # With a ~13 ft gear station and tyre radius, 15.5 ft places
                # the aircraft near the runway instead of burying its CG in it.
                "ic/h-sl-ft": 15.5,
                "ic/vt-kts": 0,
                "ic/alpha-deg": 0,
                "ic/beta-deg": 0,
                "ic/phi-deg": 0,
                "ic/theta-deg": 0,
                "ic/psi-true-deg": 0,
                "ic/lat-geod-deg": 0,
                "ic/long-gc-deg": 0,
            }
            for property_path, value in initial_conditions.items():
                fdm[property_path] = value
            self.assertTrue(fdm.run_ic())
            default_payload = (600, 55000, 5000, 10000, 1000)
            for index, expected_lbs in enumerate(default_payload):
                self.assertAlmostEqual(fdm[f"inertia/pointmass-weight-lbs[{index}]"], expected_lbs)
            # Confirm that the payload station is adjustable in the live JSBSim model.
            fdm["inertia/pointmass-weight-lbs[1]"] = 65000
            fdm["fcs/aileron-cmd-norm"] = 0.5
            fdm["fcs/flap-cmd-norm"] = 1.0
            for _ in range(120):
                self.assertTrue(fdm.run())
            self.assertGreater(fdm["simulation/sim-time-sec"], 0.9)
            self.assertAlmostEqual(fdm["inertia/pointmass-weight-lbs[1]"], 65000)
            self.assertAlmostEqual(fdm["fcs/left-aileron-pos-norm"], 0.5, places=3)
            self.assertAlmostEqual(fdm["fcs/right-aileron-pos-norm"], -0.5, places=3)
            self.assertGreater(fdm["fcs/flap-pos-norm"], 0.0)
            self.assertLessEqual(fdm["fcs/flap-pos-norm"], 1.0)


if __name__ == "__main__":
    unittest.main()
