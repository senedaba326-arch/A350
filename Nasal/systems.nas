# Scheduler and property initialization for the independently defined systems.
# All underlying models are deliberately simplified and non-operational.
var A350Systems = {
  timer: nil,
  initialized: 0,

  init: func {
    if (me.initialized) return;
    me.initialized = 1;
    setprop("/systems/a350/description", "A350 systems demonstrator - not for operational use");
    setprop("/systems/a350/hydraulics/nominal-psi", 5000);
    setprop("/systems/a350/electrical/ac-frequency-hz", 400);
    setprop("/systems/a350/electrical/ac-nominal-voltage", 115);
    setprop("/systems/a350/electrical/ac-line-voltage", 200);
    setprop("/systems/a350/pneumatic/nominal-psi", 45);
    setprop("/systems/a350/electrical/external-power", 0);
    setprop("/systems/a350/hydraulics/pump-command[0]", 1);
    setprop("/systems/a350/hydraulics/pump-command[1]", 1);
    setprop("/systems/a350/hydraulics/pump-command[2]", 1);
    me.timer = maketimer(0.25, func { A350Systems.update(); });
    me.timer.start();
  },

  update: func {
    A350Electrical.update();
    A350Hydraulics.update(0.25);
    A350FlightControls.update();
    A350Pneumatics.update();
    var wow = getprop("/gear/gear[1]/wow");
    if (wow == nil) wow = 1;
    setprop("/systems/a350/weight-on-wheels", wow ? 1 : 0);
  }
};

A350Systems.init();
