# Availability/status demonstration only. JSBSim commands remain direct and
# conventional; these flags are not Airbus PRIM/SEC laws or protections.
var A350FlightControls = {
  update: func {
    var ac = getprop("/systems/a350/electrical/ac-available");
    var p0 = getprop("/systems/a350/hydraulics/circuit[0]/pressure-psi");
    var p1 = getprop("/systems/a350/hydraulics/circuit[1]/pressure-psi");
    var p2 = getprop("/systems/a350/hydraulics/circuit[2]/pressure-psi");
    if (ac == nil) ac = 0;
    if (p0 == nil) p0 = 0;
    if (p1 == nil) p1 = 0;
    if (p2 == nil) p2 = 0;
    var hydraulicAvailable = (p0 > 1000 or p1 > 1000 or p2 > 1000) ? 1 : 0;
    var lanePowered = ac and hydraulicAvailable;
    foreach (var lane; ["prim-1", "prim-2", "prim-3", "sec-1", "sec-2"]) {
      setprop("/systems/a350/fbw/" ~ lane ~ "/powered", lanePowered ? 1 : 0);
      setprop("/systems/a350/fbw/" ~ lane ~ "/valid", lanePowered ? 1 : 0);
    }
    var engines = getprop("/engines/engine[0]/running") or getprop("/engines/engine[1]/running");
    setprop("/systems/a350/fbw/control-law", "DIRECT - simplified FDM");
    setprop("/systems/a350/fbw/flight-controls-available", ac and engines);
  }
};
