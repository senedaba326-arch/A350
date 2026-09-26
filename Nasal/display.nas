# Lightweight Canvas systems/status page. Press E to open or close it.
# It is an educational status page, not an ECAM or cockpit implementation.
var A350Display = {
  dialog: nil,
  canvas: nil,
  labels: [],
  engineLabel: nil,
  timer: nil,

  textLine: func(root, label, y, size = 20, color = [0.55, 0.95, 0.75]) {
    var item = root.createChild("text")
      .setText(label)
      .setTranslation(24, y)
      .setAlignment("left-top")
      .setFontSize(size)
      .setFont("LiberationFonts/LiberationSans-Regular.ttf")
      .setColor(color[0], color[1], color[2]);
    append(me.labels, item);
    return item;
  },

  open: func {
    if (me.dialog != nil) return;
    me.labels = [];
    me.dialog = canvas.Window.new([640, 430], "dialog").set("title", "A350 SYSTEMS — COMMUNITY SIM");
    me.canvas = me.dialog.createCanvas().set("background", "#101820");
    var root = me.canvas.createGroup();
    me.textLine(root, "A350-900  |  SYSTEMS DEMONSTRATOR", 18, 24, [0.3, 0.85, 1.0]);
    me.textLine(root, "NOT AN AIRBUS ECAM • NON-CERTIFIED MODEL", 56, 15, [1.0, 0.72, 0.2]);
    me.textLine(root, "ELECTRICAL", 102, 19, [0.4, 0.8, 1.0]);
    me.textLine(root, "HYDRAULICS", 170, 19, [0.4, 0.8, 1.0]);
    me.textLine(root, "FLIGHT CONTROLS / PNEUMATICS", 280, 19, [0.4, 0.8, 1.0]);
    me.textLine(root, "Press E to close. All indications are simplified simulation values.", 390, 14, [0.7, 0.75, 0.8]);
    for (var i = 0; i < 5; i += 1) me.textLine(root, "", 132 + i * 26, 17);
    for (var j = 0; j < 4; j += 1) me.textLine(root, "", 200 + j * 24, 17);
    for (var k = 0; k < 4; k += 1) me.textLine(root, "", 310 + k * 24, 17);
    me.engineLabel = me.textLine(root, "", 80, 14, [0.7, 0.9, 0.8]);
    me.update();
    me.timer = maketimer(1.0, func { A350Display.update(); });
    me.timer.start();
  },

  close: func {
    if (me.timer != nil) me.timer.stop();
    if (me.dialog != nil) me.dialog.del();
    me.dialog = nil;
    me.canvas = nil;
    me.engineLabel = nil;
    me.timer = nil;
    me.labels = [];
  },

  toggle: func {
    if (me.dialog == nil) me.open(); else me.close();
  },

  read: func(path, fallback = 0) {
    var v = getprop(path);
    if (v == nil) return fallback;
    return v;
  },

  update: func {
    if (me.dialog == nil) return;
    var ac1 = me.read("/systems/a350/electrical/ac-bus-1/voltage");
    var ac2 = me.read("/systems/a350/electrical/ac-bus-2/voltage");
    var dc = me.read("/systems/a350/electrical/dc-essential/voltage");
    me.labels[6].setText("AC BUS 1  " ~ sprintf("%3.0f", ac1) ~ " V    AC BUS 2  " ~ sprintf("%3.0f", ac2) ~ " V");
    me.labels[7].setText("DC ESS     " ~ sprintf("%2.0f", dc) ~ " V    FREQUENCY  " ~ sprintf("%3.0f", me.read("/systems/a350/electrical/ac-bus-1/frequency-hz")) ~ " Hz");
    me.labels[8].setText("SOURCE  ENG 1 " ~ (me.read("/systems/a350/electrical/source-engine-1") ? "ON" : "OFF") ~ "   ENG 2 " ~ (me.read("/systems/a350/electrical/source-engine-2") ? "ON" : "OFF"));
    me.labels[9].setText("EXTERNAL POWER " ~ (me.read("/systems/a350/electrical/source-external") ? "ON" : "OFF") ~ "   APU " ~ (me.read("/systems/a350/electrical/source-apu") ? "ON" : "OFF"));
    me.labels[10].setText("NOMINAL SERVICE  115/200 VAC, 400 Hz  •  SIMPLIFIED BUS MODEL");
    me.labels[11].setText("CIRCUIT 1  " ~ sprintf("%4.0f", me.read("/systems/a350/hydraulics/circuit[0]/pressure-psi")) ~ " psi");
    me.labels[12].setText("CIRCUIT 2  " ~ sprintf("%4.0f", me.read("/systems/a350/hydraulics/circuit[1]/pressure-psi")) ~ " psi");
    me.labels[13].setText("CIRCUIT 3  " ~ sprintf("%4.0f", me.read("/systems/a350/hydraulics/circuit[2]/pressure-psi")) ~ " psi");
    me.labels[14].setText("THREE INDEPENDENT PRESSURE STATES • ELECTRIC/PUMP INPUTS ARE SIMPLIFIED");
    me.labels[15].setText("FBW MODEL  " ~ me.read("/systems/a350/fbw/control-law", "DIRECT"));
    me.labels[16].setText("PRIM 1/2/3  " ~ me.read("/systems/a350/fbw/prim-1/valid") ~ " / " ~ me.read("/systems/a350/fbw/prim-2/valid") ~ " / " ~ me.read("/systems/a350/fbw/prim-3/valid"));
    me.labels[17].setText("SEC 1/2     " ~ me.read("/systems/a350/fbw/sec-1/valid") ~ " / " ~ me.read("/systems/a350/fbw/sec-2/valid") ~ "    BLEED " ~ sprintf("%2.0f", me.read("/systems/a350/pneumatic/bleed-sources")) ~ " sources");
    me.labels[18].setText("PACK 1 " ~ (me.read("/systems/a350/pneumatic/pack-1-available") ? "AVAIL" : "OFF") ~ "    PACK 2 " ~ (me.read("/systems/a350/pneumatic/pack-2-available") ? "AVAIL" : "OFF"));
    me.engineLabel.setText("ENGINES  " ~ me.read("/systems/a350/engines/start-state", "OFF") ~ "   s START / Shift+s SHUT DOWN");
  }
};
