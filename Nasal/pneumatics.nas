# Simplified engine/APU bleed-source and pack availability indications.
var A350Pneumatics = {
  update: func {
    var engine0 = getprop("/engines/engine[0]/running") or 0;
    var engine1 = getprop("/engines/engine[1]/running") or 0;
    var apu = getprop("/systems/a350/electrical/apu-generator") or 0;
    var sources = (engine0 and engine1) ? 2 : ((engine0 or engine1) ? 1 : 0);
    var nominalPsi = sources ? 42 : 0;
    setprop("/systems/a350/pneumatic/bleed-sources", sources);
    setprop("/systems/a350/pneumatic/left-manifold-psi", engine0 ? nominalPsi : 0);
    setprop("/systems/a350/pneumatic/right-manifold-psi", engine1 ? nominalPsi : 0);
    setprop("/systems/a350/pneumatic/pack-1-available", engine0 or apu);
    setprop("/systems/a350/pneumatic/pack-2-available", engine1 or apu);
    setprop("/systems/a350/pneumatic/cabin-pressurization-available", sources or apu);
  }
};
