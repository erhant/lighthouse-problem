const math = require("canvas-sketch-util/math");

// Find distance between 2 points in 2D.
function dist2D(p1, p2) {
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  return Math.sqrt(dx * dx + dy * dy);
}

// Find angle between <aob> in radians
function angle2D(a, o, b) {
  const ang = math.radToDeg(
    Math.atan2(b.y - o.y, b.x - o.x) - Math.atan2(a.y - o.y, a.x - o.x)
  );
  if (ang < 0) {
    return math.degToRad(ang + 360);
  } else {
    return math.degToRad(ang);
  }
}

// Rotate p around o for ang radians.
function rotate(p, o, ang) {
  return {
    x: o.x + Math.cos(ang) * (p.x - o.x) - Math.sin(ang) * (p.y - o.y),
    y: o.y + Math.sin(ang) * (p.x - o.x) + Math.cos(ang) * (p.y - o.y),
  };
}
