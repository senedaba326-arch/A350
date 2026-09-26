"""Offline integrity checks for the early-stage FlightGear A350 package."""
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


class PackageIntegrityTests(unittest.TestCase):
    def parse(self, relative):
        return ET.parse(ROOT / relative).getroot()

    def test_all_xml_files_are_well_formed(self):
        for path in sorted(ROOT.rglob("*.xml")):
            with self.subTest(path=path.relative_to(ROOT)):
                ET.parse(path)

    def test_set_file_points_to_existing_assets(self):
        root = self.parse("A350-set.xml")
        sim = root.find("sim")
        self.assertIsNotNone(sim)
        self.assertEqual(sim.findtext("flight-model"), "jsb")
        self.assertEqual(sim.findtext("aero"), "A350")
        self.assertTrue((ROOT / "A350.xml").is_file())
        model = sim.find("model")
        self.assertEqual(model.get("path"), "Aircraft/A350/Models/A350XWB-900.xml")
        self.assertTrue((ROOT / "Models/A350XWB-900.xml").is_file())
        self.assertEqual(root.get("include"), "A350-common.xml")
        common = self.parse("A350-common.xml")
        self.assertIsNotNone(common.find("./sim/systems/path"))
        self.assertIsNotNone(common.find("./sim/instrumentation/path"))
        for node in common.findall(".//path"):
            fg_path = (node.text or "").strip().removeprefix("Aircraft/A350/")
            self.assertTrue((ROOT / fg_path).is_file(), node.text)
        self.assertTrue((ROOT / "Models/A350XWB-900.ac").is_file())
        self.assertTrue((ROOT / "Models/A350XWB-900-flightdeck.xml").is_file())
        for filename in root.findall("./nasal/load/file"):
            fg_path = filename.text or ""
            self.assertTrue(fg_path.startswith("Aircraft/A350/"), fg_path)
            local = ROOT / fg_path.removeprefix("Aircraft/A350/")
            self.assertTrue(local.is_file(), fg_path)

    def test_imported_model_and_sound_references_resolve(self):
        for path in sorted((ROOT / "Models").rglob("*.xml")):
            root = ET.parse(path).getroot()
            for node in root.iter("path"):
                value = (node.text or "").strip()
                if value.startswith(("Aircraft/A350/", "/Aircraft/A350/")):
                    local = value.removeprefix("/").removeprefix("Aircraft/A350/")
                    self.assertTrue((ROOT / local).is_file(), f"{path.relative_to(ROOT)}: {value}")
        sounds = ET.parse(ROOT / "Sounds/A350XWB-sounds.xml").getroot()
        for node in sounds.iter("path"):
            value = (node.text or "").strip().removeprefix("/")
            if value.startswith("Aircraft/A350/"):
                value = value.removeprefix("Aircraft/A350/")
            elif not value.startswith("Sounds/"):
                continue
            self.assertTrue((ROOT / value).is_file(), value)

    def test_imported_ac3d_texture_references_exist(self):
        available = {path.name for path in (ROOT / "Models").rglob("*") if path.is_file()}
        references = []
        for path in (ROOT / "Models").rglob("*.ac"):
            text = path.read_text(encoding="utf-8", errors="replace")
            references.extend(re.findall(r'^texture "([^"]+)"', text, re.MULTILINE))
        missing = sorted({Path(value).name for value in references} - available)
        self.assertEqual(missing, [])

    def test_imported_assets_keep_license_and_credits(self):
        notices = (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8")
        self.assertIn("d7e32927548d2da84ea40cc734f82d43f6ca6bc2", notices)
        self.assertIn("GPL2+", notices)
        self.assertIn("Sbyx", notices)
        self.assertTrue((ROOT / "COPYING").is_file())

    def test_public_dimension_reference_values(self):
        root = self.parse("A350.xml")
        metrics = root.find("metrics")
        self.assertAlmostEqual(float(metrics.findtext("wingspan")) * 0.3048, 64.75, delta=0.02)
        self.assertAlmostEqual(float(metrics.findtext("chord")) * 0.3048, 6.84, delta=0.03)
        self.assertAlmostEqual(float(metrics.findtext("wingarea")) * 0.092903, 442.96, delta=1.0)

    def test_fdm_sections_rebuild_the_runtime_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "A350.xml"
            subprocess.run(
                [sys.executable, str(ROOT / "tools/build_fdm.py"), "--output", str(output)],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(output.read_bytes(), (ROOT / "A350.xml").read_bytes())

    def test_fdm_has_two_engines_three_tanks_and_control_surfaces(self):
        root = self.parse("A350.xml")
        propulsion = root.find("propulsion")
        self.assertEqual(len(propulsion.findall("engine")), 2)
        self.assertEqual(len(propulsion.findall("tank")), 3)
        self.assertTrue((ROOT / "Engines/TrentXWB84.xml").is_file())
        controls = root.find("flight_control")
        names = {node.get("name") for node in controls.iter()}
        for expected in ("Pitch", "Roll", "Yaw", "Flaps", "Landing gear"):
            self.assertIn(expected, names)

    def test_animation_object_names_exist_in_ac3d_model(self):
        wrapper = self.parse("Models/A350.xml")
        self.assertEqual(wrapper.findtext("path"), "A350.ac")
        ac_text = (ROOT / "Models/A350.ac").read_text(encoding="utf-8")
        model_names = set(re.findall(r'^name "([^"]+)"$', ac_text, re.MULTILINE))
        animation_names = {
            node.text for node in wrapper.findall("./animation/object-name") if node.text
        }
        self.assertTrue(animation_names)
        self.assertEqual(animation_names - model_names, set())
        self.assertIn("Fuselage", model_names)
        self.assertGreaterEqual(len(model_names), 20)

        lines = ac_text.splitlines()
        vertices = []
        for index, line in enumerate(lines):
            if line.startswith("name \"Fuselage\""):
                count = int(lines[index + 2].split()[1])
                vertices = [tuple(map(float, row.split())) for row in lines[index + 3:index + 3 + count]]
                break
        self.assertTrue(vertices)
        xs = [vertex[0] for vertex in vertices]
        self.assertAlmostEqual(max(xs) - min(xs), 66.8, delta=0.02)

    def test_systems_page_and_safety_scope_are_documented(self):
        nasal = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "Nasal").glob("*.nas"))
        display = (ROOT / "Nasal/display.nas").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for phrase in ("5000", "prim-1", "sec-2", "ac-bus-1", "pneumatic"):
            self.assertIn(phrase, nasal)
        self.assertIn("canvas.Window.new", display)
        self.assertIn("not suitable for training", readme)
        self.assertNotRegex(nasal + display, r"TODO|PLACEHOLDER|à compléter")


if __name__ == "__main__":
    unittest.main()
