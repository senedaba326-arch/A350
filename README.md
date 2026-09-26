# Airbus A350-900 — FlightGear community aircraft

An early-stage, educational FlightGear/JSBSim aircraft package. The exterior and 3D flight deck are based on the GPL-licensed FlightGear A350XWB community model; this repository retains its independent, simplified JSBSim flight model and adds a small set of illustrative Nasal systems. This is **not** an Airbus product or an operationally accurate A350 simulation, and is not suitable for training or safety-critical use.

## Install and fly

1. Install this directory in a FlightGear aircraft search path as `Aircraft/A350`, or add its parent directory with `--fg-aircraft`.
2. Start FlightGear with `--aircraft=A350`.
3. Press **e** to show or hide the community systems-status page.
4. Press **E** to toggle the demonstrator's simulated external electrical power. It only enables display/system indications; it does not model a real external-power connection.
5. Use FlightGear's weight-and-balance dialog to load crew, passengers/baggage and forward/aft cargo. The stations are rough estimates; the dialog does not yet enforce fuel-plus-payload mass combinations.
6. Use FlightGear's normal controls for roll, pitch, yaw, throttle, flaps and landing gear. The flap lever uses A350-style detents. Press **s** to start both engines; the generic JSBSim cranking/light-off sequence takes roughly 30 seconds of simulation time. Press **Shift+s** to shut them down. **B** toggles the parking brake.
7. Use FlightGear's normal view controls to reach the copilot, full-cockpit, overhead-panel and pedestal views.

The aircraft set file selects `Models/A350XWB-900.xml` for the imported exterior/flight deck and `A350.xml` for the local JSBSim FDM. The earlier generated exterior (`Models/A350.xml` and `Models/A350.ac`) remains in the repository as a fallback/reference but is not selected by the set file. Airline liveries and the upstream dynamic livery selector were not imported; the included base texture is used instead.

## Package map

```text
A350-set.xml                         FlightGear entry point, operating limits, load stations and key bindings
A350-common.xml                      Cockpit/camera views, instruments, wing flex and sound references
A350.xml                             Generated JSBSim runtime configuration (local FDM)
fdm/*.xml                            Editable JSBSim sections; rebuild with tools/build_fdm.py
Systems/wingflexer-params.xml         Adapted visual wing-flex parameters and local tank aliases
Engines/TrentXWB84.xml               Generic 84-klbf-class turbofan approximation
Models/A350XWB-900.xml               GPL community exterior wrapper and animations
Models/A350XWB-900.ac                GPL community exterior geometry
Models/A350XWB-900-flightdeck.xml    GPL community 3D cockpit and instrument submodels
Models/                                Imported GPL geometry, textures, lights, effects and submodels
Sounds/                               Imported GPL sound assets/configuration
Systems/                              Imported generic FlightGear instrument/system configuration
Nasal/*.nas                            Local engine-start sequence plus simplified electrical,
                                      hydraulic, flight-control, pneumatic and display logic
Models/A350.xml, Models/A350.ac        Previous generated exterior fallback/reference
COPYING                                GPL version 2 license text from the upstream model
THIRD_PARTY_NOTICES.md                 Source revision, credits and adaptation notes
```

## Flight dynamics and systems scope

- The independent JSBSim FDM retains a conventional direct-control model. Its wing, tail, gear and engine station locations were brought closer to the imported model's coordinate frame; mass, inertia, aerodynamics, engine maps and gear response remain estimates.
- Airbus publishes a 66.80 m length, 64.75 m span, Mach 0.85 cruise, 283.0 t maximum take-off mass, 207.0 t maximum landing mass, 195.7 t maximum zero-fuel mass and 166,488 L maximum fuel capacity for the A350-900. These public figures now inform aircraft limits, flap detents, weight-and-balance stations and tank-capacity estimates. The three equal JSBSim tanks approximate total capacity using a nominal Jet-A density; they do not reproduce the real tank layout or fuel-transfer logic.
- Five approximate weight stations model crew, passengers/baggage and forward/aft/bulk cargo, and their maximum zero-fuel load is kept below the published MZFW for the selected baseline. FlightGear's mass limits are metadata/advisory: a coupled fuel-plus-payload take-off-mass interlock is not implemented, so users must keep the loaded aircraft below the published limits.
- The imported model's four wing-flex animations are now driven through FlightGear's generic spring/damper wing-flex system, using adapted external-wing fuel aliases. Its stiffness and damping are visual estimates, not structural analysis.
- The control system does **not** implement Airbus fly-by-wire laws, protections, envelope limiting, redundancy management or reconfiguration. Do not infer real A350 handling or procedures from it.
- The local electrical, hydraulic and pneumatic logic is illustrative. Nominal voltage/pressure indications and the display-availability bridge are simplified state flags, not component-level aircraft simulations. Engine keys **s** and **Shift+s** run JSBSim's generic two-engine starter/cutoff sequence (including the generic 15% N2 light-off threshold); this is not an authentic Trent XWB start procedure. The flight deck and legacy instrumentation are not validated together in FlightGear.
- The imported visual model is a community contribution. Its rendering, camera alignment, animations, sounds and interactive cockpit behavior have not been flight-tested in this checkout. FlightGear (`fgfs`) was unavailable in the development environment; the offline checks cannot establish in-simulator correctness.
- Airbus is not affiliated with or endorsing this project. No proprietary FCOM or restricted Airbus engineering data is included. Nothing here is certified, validated for real-world operation, or suitable for training or safety-critical use.

## License and third-party assets

The imported A350XWB community model is declared GPL version 2 or later by its upstream README. The upstream `COPYING` text is retained in this repository. See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for the exact source revision, credited contributors and the scope of our changes. The FDM and Nasal additions remain explicitly non-operational community work; consult the repository history for their authorship and licensing details.

## Development and validation

Run the checks with:

```sh
python3 -m unittest discover -s tests -v
```

The checks cover XML and asset references, external-model textures, published-mass/fuel data consistency, load-station wiring, FDM assembly/control response and (when enabled) a JSBSim smoke test that cranks, lights and shuts down both engines. The optional local runtime check runs when the `jsbsim` Python package and data are installed; GitHub Actions pins JSBSim 1.3.1 and runs it on each push. They do not test FlightGear rendering, Nasal execution, wing-flex runtime integration, sound, camera placement or cockpit behavior. `fgfs` is not installed in the current development environment.

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
- [JSBSim FGTurbine startup model](https://jsbsim-team.github.io/jsbsim/classJSBSim_1_1FGTurbine.html) and [FlightGear JSBSim engine-start notes](https://wiki.flightgear.org/JSBSim_Engines)
- [FlightGear Canvas snippets](https://wiki.flightgear.org/Canvas_Snippets)
- [Airbus A350-900 specifications](https://www.aircraft.airbus.com/en/aircraft/a350/a350-900) — dimensions, operating-weight limits, capacity, fuel volume and cruise Mach
- [EASA Type Certificate Data Sheet EASA.A.151](https://www.easa.europa.eu/en/downloads/17736/en) — A350-941 series, engine variants and certified technical limits
- [Rolls-Royce Trent XWB family](https://www.rolls-royce.com/media/our-stories/discover/2023/poweroftrent-the-only-new-generation-high-thrust-engine-in-service.aspx) — engine family and A350 application
- [FlightGear wing-flex system](https://wiki.flightgear.org/Wingflexer) — generic spring/damper animation implementation
