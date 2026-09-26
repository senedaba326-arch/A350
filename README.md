# Airbus A350-900 — FlightGear community model

A self-contained **early-stage, educational FlightGear/JSBSim aircraft package**. It provides a simplified A350-900-shaped FDM, a generated low-polygon exterior, conventional JSBSim control surfaces, and a Nasal/Canvas systems status page. It is not an Airbus product, not an operationally accurate aircraft simulation, and not suitable for training or safety-critical use.

## Install and run

1. Copy this repository directory into a FlightGear aircraft search path as `Aircraft/A350` (or add its parent directory with `--fg-aircraft`).
2. Start FlightGear with `--aircraft=A350`.
3. Press **E** to show or hide the community systems status page.
4. Use the normal FlightGear controls for aileron, elevator, rudder, throttle, flaps, and landing gear. Start engines using FlightGear's normal engine controls.

The root `A350-set.xml` references `A350.xml` as the JSBSim FDM and `Models/A350.xml` as the exterior model wrapper. The editable JSBSim source is split into `fdm/*.xml`; after changing those sections, regenerate the single runtime file with `python3 tools/build_fdm.py`. `Models/A350.ac` can be regenerated using `python3 tools/generate_model.py`. Both builders use Python's standard library and create compact outputs.

## Package layout

```text
A350-set.xml                 FlightGear aircraft entry point and key binding
A350.xml                     Generated JSBSim runtime configuration
fdm/fileheader.xml           Model metadata and safety notes
fdm/metrics.xml              Reference dimensions
fdm/mass_balance.xml         Estimated mass, payload and inertia
fdm/ground_reactions.xml     Nose and main landing-gear contacts
fdm/propulsion.xml           Two engines and three fuel tanks
fdm/flight_control.xml       Conventional pilot-to-surface FCS
fdm/aerodynamics.xml         Estimated force and moment coefficients
fdm/output.xml               Optional JSBSim CSV telemetry
Engines/TrentXWB84.xml       Generic 84-klbf-class turbofan approximation
Models/A350.xml              AC3D model wrapper and control/gear animations
Models/A350.ac               Generated low-poly exterior geometry
Nasal/electrical.nas         Simplified electrical bus availability
Nasal/hydraulics.nas         Three illustrative hydraulic pressure states
Nasal/flight-controls.nas    PRIM/SEC availability flags (not control laws)
Nasal/pneumatics.nas         Simplified bleed and pack availability
Nasal/systems.nas            Scheduler and property initialization
Nasal/display.nas            On-demand Canvas systems-status display (E key)
tools/build_fdm.py           Assemble FDM sections into A350.xml
tools/generate_model.py      Generate AC3D geometry from source
tests/test_package.py        Offline package structure/XML smoke tests
```

## Scope and modeling notes

- Airbus publishes headline A350-900 dimensions and performance figures; the dimensions used here are 66.80 m length and 64.75 m span. The FDM uses a nominal 280–283 t maximum take-off mass class and two generic 84,000 lbf-class engines as broad reference points. These are **not a complete set of authoritative configuration-specific limits**.
- The aerodynamic coefficients, inertia tensor, fuel split, load distribution, landing-gear characteristics, engine maps, and all systems logic are independent rough estimates. They have not been flight-tested or validated against Airbus data.
- The JSBSim flight controls are intentionally conventional and direct. The Nasal PRIM/SEC indicators are availability/status demonstrations only; they do **not** implement Airbus fly-by-wire laws, protections, reconfiguration, envelope limiting, or redundancy management.
- Hydraulic pressures are simple first-order state estimates around 5,000 psi. Electrical buses show nominal 115/200 V, 400 Hz service values but do not simulate three-phase circuits, generators, contactors, or load shedding. Pneumatics are indicative source/pack flags, not thermodynamic bleed-air or cabin-pressure models.
- The Canvas panel is a small systems-status window, not an ECAM, PFD/ND, or finished 3D cockpit. Exterior geometry is generated from simple polygons and has no production textures or airline livery.

Never use this package to operate a real aircraft or infer real aircraft procedures.

## Development checks

Run the repository's offline smoke tests with:

```sh
python3 -m unittest discover -s tests -v
```

The tests check XML well-formedness, FDM rebuild reproducibility, package references, generated model object names, and core public-dimension consistency. The FDM has also been loaded and integrated in a JSBSim 1.3.1 smoke test. FlightGear rendering, Nasal execution, and cockpit presentation still require an in-simulator check.

## References consulted

- FlightGear aircraft set-file format and package guidance: <https://wiki.flightgear.org/Aircraft-set.xml> and <https://wiki.flightgear.org/Howto:Make_an_aircraft>
- JSBSim XML model/reference material: <https://jsbsim.sourceforge.net/JSBSim.xsd.html> and the JSBSim reference manual.
- JSBSim generic turbine examples: <https://github.com/JSBSim-Team/jsbsim/blob/master/engine/CFM56.xml>
- FlightGear Canvas snippets: <https://wiki.flightgear.org/Canvas_Snippets>
- Airbus public A350-900 specifications: <https://www.aircraft.airbus.com/en/aircraft/a350/a350-900>

The proprietary Airbus FCOM and restricted engineering data are not included or reproduced. This community project makes no claim of absolute technical accuracy or Airbus endorsement.
