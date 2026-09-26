#!/usr/bin/env python3
"""Assemble the runtime JSBSim aircraft XML from independently editable sections."""
from argparse import ArgumentParser
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = (
    "fileheader",
    "metrics",
    "mass_balance",
    "ground_reactions",
    "propulsion",
    "flight_control",
    "aerodynamics",
    "output",
)
XSI = "http://www.w3.org/2001/XMLSchema-instance"
ET.register_namespace("xsi", XSI)


def build_tree():
    aircraft = ET.Element("fdm_config", {
        "name": "A350",
        "version": "2.0",
        "release": "ALPHA",
        f"{{{XSI}}}noNamespaceSchemaLocation": "http://jsbsim.sourceforge.net/JSBSim.xsd",
    })
    for section in SECTIONS:
        path = ROOT / "fdm" / f"{section}.xml"
        node = ET.parse(path).getroot()
        if node.tag != section:
            raise ValueError(f"{path.relative_to(ROOT)} must have <{section}> as its root element")
        aircraft.append(node)
    return aircraft


def render() -> bytes:
    tree = build_tree()
    ET.indent(tree, space="  ")
    return ET.tostring(tree, encoding="UTF-8", xml_declaration=True) + b"\n"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "A350.xml", help="compiled JSBSim file path")
    args = parser.parse_args()
    payload = render()
    ET.fromstring(payload)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(payload)
    print(f"Built {args.output} ({len(payload):,} bytes; {len(SECTIONS)} sections)")


if __name__ == "__main__":
    main()
