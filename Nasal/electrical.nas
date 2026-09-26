# Simplified electrical bus state model; not a component-level network simulation.
var A350Electrical = {
  value: func(path, fallback = 0) {
    var result = getprop(path);
    if (result == nil) return fallback;
    return result;
  },

  update: func {
    var engine0 = me.value("/engines/engine[0]/running", 0);
    var engine1 = me.value("/engines/engine[1]/running", 0);
    var apu = me.value("/systems/a350/electrical/apu-generator", 0);
    var external = me.value("/systems/a350/electrical/external-power", 0);
    var available = (engine0 or engine1 or apu or external) ? 1 : 0;

    # Nominal 115/200 VAC, 400 Hz and 28 VDC indications only. The phase
    # voltages, generator dynamics, tie contactors and load shedding are absent.
    foreach (var bus; ["ac-bus-1", "ac-bus-2", "ac-essential"]) {
      setprop("/systems/a350/electrical/" ~ bus ~ "/voltage", available ? 115 : 0);
      setprop("/systems/a350/electrical/" ~ bus ~ "/frequency-hz", available ? 400 : 0);
      setprop("/systems/a350/electrical/" ~ bus ~ "/powered", available);
    }
    foreach (var bus; ["dc-bus-1", "dc-bus-2", "dc-essential"]) {
      setprop("/systems/a350/electrical/" ~ bus ~ "/voltage", available ? 28 : 0);
      setprop("/systems/a350/electrical/" ~ bus ~ "/powered", available);
    }
    setprop("/systems/a350/electrical/ac-available", available);
    setprop("/systems/a350/electrical/dc-available", available);
    setprop("/systems/a350/electrical/source-engine-1", engine0);
    setprop("/systems/a350/electrical/source-engine-2", engine1);
    setprop("/systems/a350/electrical/source-apu", apu);
    setprop("/systems/a350/electrical/source-external", external);
  }
};
