# Airbus A350-900 — FlightGear community aircraft

An early-stage, educational FlightGear/JSBSim aircraft package. The exterior and 3D flight deck are based on the GPL-licensed FlightGear A350XWB community model; this repository retains its independent, simplified JSBSim flight model and adds a small set of illustrative Nasal systems. This is **not** an Airbus product or an operationally accurate A350 simulation, and is not suitable for training or safety-critical use.

## Install and fly

1. Install this directory in a FlightGear aircraft search path as `Aircraft/A350`, or add its parent directory with `--fg-aircraft`.
2. Start FlightGear with `--aircraft=A350`.
3. Press **e** to show or hide the community systems-status page.
4. Press **E** to toggle the demonstrator's simulated external electrical power. It only enables display/system indications; it does not model a real external-power connection.
5. Use FlightGear's normal controls for roll, pitch, yaw, throttle, flaps and landing gear. Start the engines using FlightGear's normal engine controls. **B** toggles the parking brake.
6. Use FlightGear's normal view controls to reach the copilot, full-cockpit, overhead-panel and pedestal views.

The aircraft set file selects `Models/A350XWB-900.xml` for the imported exterior/flight deck and `A350.xml` for the local JSBSim FDM. The earlier generated exterior (`Models/A350.xml` and `Models/A350.ac`) remains in the repository as a fallback/reference but is not selected by the set file. Airline liveries and the upstream dynamic livery selector were not imported; the included base texture is used instead.

## Package map

```text
A350-set.xml                         FlightGear entry point, local Nasal loading and key bindings
A350-common.xml                      Cockpit/camera views, instrumentation, systems and sound references
A350.xml                             Generated JSBSim runtime configuration (local FDM)
fdm/*.xml                            Editable JSBSim sections; rebuild with tools/build_fdm.py
Engines/TrentXWB84.xml               Generic 84-klbf-class turbofan approximation
Models/A350XWB-900.xml               GPL community exterior wrapper and animations
Models/A350XWB-900.ac                GPL community exterior geometry
Models/A350XWB-900-flightdeck.xml    GPL community 3D cockpit and instrument submodels
Models/                                Imported GPL geometry, textures, lights, effects and submodels
Sounds/                               Imported GPL sound assets/configuration
Systems/                              Imported generic FlightGear instrument/system configuration
Nasal/*.nas                            Local simplified electrical, hydraulic, flight-control,
                                      pneumatic and status-display demonstrations
Models/A350.xml, Models/A350.ac        Previous generated exterior fallback/reference
COPYING                                GPL version 2 license text from the upstream model
THIRD_PARTY_NOTICES.md                 Source revision, credits and adaptation notes
```

## Flight dynamics and systems scope

- The independent JSBSim FDM retains a conventional direct-control model. Its wing, tail, gear and engine station locations were brought closer to the imported model's coordinate frame; mass, inertia, aerodynamics, engine maps and gear response remain estimates.
- Public A350-900 headline dimensions (66.80 m length and 64.75 m span) and a nominal 280–283 t maximum-takeoff-mass class inform the model. The current wing reference area is an approximate input, not an authoritative aircraft limit or configuration-specific data.
- The control system does **not** implement Airbus fly-by-wire laws, protections, envelope limiting, redundancy management or reconfiguration. Do not infer real A350 handling or procedures from it.
- The local electrical, hydraulic and pneumatic logic is illustrative. Nominal voltage/pressure indications and the display-availability bridge are simplified state flags, not component-level aircraft simulations. The flight deck and legacy instrumentation are not validated together in FlightGear.
- The imported visual model is a community contribution. Its rendering, camera alignment, animations, sounds and interactive cockpit behavior have not been flight-tested in this checkout. FlightGear (`fgfs`) was unavailable in the development environment; the offline checks cannot establish in-simulator correctness.
- Airbus is not affiliated with or endorsing this project. No proprietary FCOM or restricted Airbus engineering data is included. Nothing here is certified, validated for real-world operation, or suitable for training or safety-critical use.

## License and third-party assets

The imported A350XWB community model is declared GPL version 2 or later by its upstream README. The upstream `COPYING` text is retained in this repository. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the exact source revision, credited contributors and the scope of our changes. The FDM and Nasal additions remain explicitly non-operational community work; consult the repository history for their authorship and licensing details.

## Development and validation

Run the offline checks with:

```sh
python3 -m unittest discover -s tests -v
```

The checks cover XML parsing, the set-file's selected assets, reproducible FDM assembly, model geometry and a JSBSim smoke test when its Python module and data directory are installed. They do not test FlightGear rendering, Nasal execution, sound, camera placement or cockpit behavior. `fgfs` is not installed in the current development environment.

Rebuild the local FDM after changing `fdm/*.xml`:

```sh
python3 tools/build_fdm.py
```

The earlier generated low-polygon fallback can be regenerated with `python3 tools/generate_model.py`. Both scripts use Python's standard library. No total repository-size cap is imposed; keep individual GitHub-hosted files within the platform's per-file limits and use Git LFS if future single assets exceed them.

## References consulted

- [FlightGear aircraft set file](https://wiki.flightgear.org/Aircraft-set.xml) and [aircraft creation guidance](https://wiki.flightgear.org/Howto:Make_an_aircraft)
- [FlightGear systems properties](https://wiki.flightgear.org/FGproperties/Systems)
- [JSBSim XML reference material](https://jsbsim.sourceforge.net/JSBSim.xsd.html) and the JSBSim reference manual
- [JSBSim generic CFM56 engine example](https://github.com/JSBSim-Team/jsbsim/blob/master/engine/CFM56.xml)
- [FlightGear Canvas snippets](https://wiki.flightgear.org/Canvas_Snippets)
- [Airbus public A350-900 specifications](https://www.aircraft.airbus.com/en/aircraft/a350/a350-900)
