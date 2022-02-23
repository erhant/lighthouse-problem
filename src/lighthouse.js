const math = require("canvas-sketch-util/math");

class Lighthouses {
  constructor(n, r = 1, pc = { x: 0, y: 0 }) {
    // radius
    this.r = r;
    // angle (alpha)
    this.a = math.degToRad(360 / n);
    // placement center
    this.pc = pc;
    this.ls = new Array(n);

    // find illumination border points
    // TODO: ...
  }
}
