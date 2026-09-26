# Three independent, first-order 5,000 psi pressure indications.
# This does not reproduce the A350 hydraulic architecture or control logic.
var A350Hydraulics = {
  pressure: [0, 0, 0],

  value: func(path, fallback = 0) {
    var result = getprop(path);
    if (result == nil) return fallback;
    return result;
  },

  clamp: func(value, low, high) {
    if (value < low) return low;
    if (value > high) return high;
    return value;
  },

  update: func(dt) {
    var engine0 = me.value("/engines/engine[0]/running", 0);
    var engine1 = me.value("/engines/engine[1]/running", 0);
    var engineDrivenPump = (engine0 or engine1) ? 1 : 0;
    foreach (var circuit; [0, 1, 2]) {
      var commanded = me.value("/systems/a350/hydraulics/pump-command[" ~ circuit ~ "]", 1);
      var electricPump = me.value("/systems/a350/hydraulics/electric-pump[" ~ circuit ~ "]", 0);
      var sourceAvailable = (engineDrivenPump or electricPump) and commanded;
      var target = sourceAvailable ? 5000 : 0;
      var tau = sourceAvailable ? 3.0 : 8.0;
      me.pressure[circuit] = me.pressure[circuit] + (target - me.pressure[circuit]) * dt / tau;
      me.pressure[circuit] = me.clamp(me.pressure[circuit], 0, 5000);
      setprop("/systems/a350/hydraulics/circuit[" ~ circuit ~ "]/pressure-psi", me.pressure[circuit]);
      setprop("/systems/a350/hydraulics/circuit[" ~ circuit ~ "]/pump-available", sourceAvailable ? 1 : 0);
      setprop("/systems/a350/hydraulics/circuit[" ~ circuit ~ "]/low-pressure", me.pressure[circuit] < 1450 ? 1 : 0);
    }
  }
};
