# JSBSim turbine start sequence for the two-engine A350 demonstrator.
# The model follows JSBSim's generic starter/cutoff process, not a real
# Trent XWB procedure. JSBSim's cutoff command is shared by both engines.
var A350Engines = {
  timer: nil,
  starting: 0,
  stopping: 0,
  fuelEnabled: 0,
  statePath: "/systems/a350/engines/start-state",

  read: func(path, fallback = 0) {
    var value = getprop(path);
    if (value == nil) return fallback;
    return value;
  },

  setState: func(state) {
    setprop(me.statePath, state);
  },

  running: func(index) {
    return me.read("/fdm/jsbsim/propulsion/engine[" ~ index ~ "]/set-running") != 0;
  },

  speedN2: func(index) {
    return me.read("/fdm/jsbsim/propulsion/engine[" ~ index ~ "]/n2");
  },

  start: func {
    if (me.starting) return;
    if (me.running(0) and me.running(1)) {
      me.setState("RUNNING");
      return;
    }

    # Start with fuel cutoff closed. Once both cores exceed JSBSim's
    # published 15% N2 light-off threshold, open the shared cutoff.
    setprop("/fdm/jsbsim/propulsion/cutoff_cmd", 1);
    setprop("/fdm/jsbsim/propulsion/starter_cmd", 1);
    me.starting = 1;
    me.stopping = 0;
    me.fuelEnabled = 0;
    me.setState("CRANKING");
    if (me.timer == nil) {
      me.timer = maketimer(0.5, func { A350Engines.update(); });
    }
    me.timer.start();
  },

  shutdown: func {
    me.starting = 0;
    me.stopping = 1;
    me.fuelEnabled = 0;
    setprop("/fdm/jsbsim/propulsion/starter_cmd", 0);
    setprop("/fdm/jsbsim/propulsion/cutoff_cmd", 1);
    me.setState("STOPPING");
    if (me.timer == nil) {
      me.timer = maketimer(0.5, func { A350Engines.update(); });
    }
    me.timer.start();
    me.update();
  },

  update: func {
    var n2Left = me.speedN2(0);
    var n2Right = me.speedN2(1);
    var leftRunning = me.running(0);
    var rightRunning = me.running(1);

    if (me.starting) {
      if (!me.fuelEnabled and n2Left >= 15 and n2Right >= 15) {
        setprop("/fdm/jsbsim/propulsion/cutoff_cmd", 0);
        me.fuelEnabled = 1;
        me.setState("LIGHT-OFF");
      }
      if (leftRunning and rightRunning) {
        setprop("/fdm/jsbsim/propulsion/starter_cmd", 0);
        me.starting = 0;
        me.setState("RUNNING");
        if (me.timer != nil) me.timer.stop();
      }
      return;
    }

    if (me.stopping and !leftRunning and !rightRunning and n2Left < 5 and n2Right < 5) {
      me.stopping = 0;
      me.setState("OFF");
      if (me.timer != nil) me.timer.stop();
    }
  }
};

setprop("/systems/a350/engines/start-state", "OFF");
