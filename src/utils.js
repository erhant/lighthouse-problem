const math = require("canvas-sketch-util/math");

// Find distance between 2 points in 2D.
function dist2D(p1, p2) {
  const dx = p2.x - p1.x;
  const dy = p2.y - p1.y;
  return Math.sqrt(dx * dx + dy * dy);
}

// Find angle between <aob> in radians
function angle2D(a, o, b) {
  // const ang = math.radToDeg(
  //   Math.atan2(b.y - o.y, b.x - o.x) - Math.atan2(a.y - o.y, a.x - o.x)
  // );
  // if (ang < 0) {
  //   return math.degToRad(ang + 360);
  // } else {
  //   return math.degToRad(ang);
  // }
  return Math.atan2(b.y - o.y, b.x - o.x) - Math.atan2(a.y - o.y, a.x - o.x);
}

// Rotate p around o for ang radians. (counterclockwise)
function rotate2D(p, o, ang) {
  return {
    x: o.x + Math.cos(ang) * (p.x - o.x) - Math.sin(ang) * (p.y - o.y),
    y: o.y + Math.sin(ang) * (p.x - o.x) + Math.cos(ang) * (p.y - o.y),
  };
}

// Check if a line from ls to le collides with a circle at c with radius r
// source: https://math.stackexchange.com/a/275533
function circleLineCollision2D(c, r, ls, le) {
  const i = ls.y - le.y;
  const j = le.x - ls.x;
  const k = -(j * ls.y + i * ls.x);
  const dist = Math.abs(i * c.x + j * c.y + k) / Math.sqrt(i * i + j * j);

  if (r < dist) {
    // line is outside
    return false;
  } else if (r === dist) {
    // line is tangent
    return false;
  } else {
    // line is inside (collides)
    return true;
  }
}

// s is a source point, and t is the center of a circle with radius r.
// finds the tangent from source to that circle
function findTangentPoints2D(s, t, r) {
  const ang = Math.asin(r / dist2D(s, t));
  return [rotate2D(t, s, ang), rotate2D(t, s, -ang)];
}

// Find the meeting point of lines [p1, p2] and [p3, p4]
// https://observablehq.com/@bumbeishvili/two-unlimited-lines-intersection-in-javascript
function findLineIntersection2D(p1, p2, p3, p4) {
  // Check if none of the lines are of length 0
  if ((p1.x === p2.x && p1.y === p2.y) || (p3.x === p4.x && p3.y === p4.y)) {
    return false;
  }

  const denominator =
    (p4.y - p3.y) * (p2.x - p1.x) - (p4.x - p3.x) * (p2.y - p1.y);

  // Lines are parallel
  if (denominator === 0) {
    return false;
  }

  const ua =
    ((p4.x - p3.x) * (p1.y - p3.y) - (p4.y - p3.y) * (p1.x - p3.x)) /
    denominator;
  const ub =
    ((p2.x - p1.x) * (p1.y - p3.y) - (p2.y - p1.y) * (p1.x - p3.x)) /
    denominator;

  // Return a object with the x and y coordinates of the intersection
  return { x: p1.x + ua * (p2.x - p1.x), y: p1.y + ua * (p2.y - p1.y) };
}

// In a clock with n values, find the values at the shortest path between s and t.
function shortestArcModulus(s, t, n) {
  let l, r, ls, rs;
  l = r = s; // start from the source, and go in two direction to the target
  ls = rs = []; // keep record of the values seen
  // find left direction
  while (l != t) {
    l = (l - 1) % n;
    ls.push(l);
  }
  // find right direction
  while (r != t) {
    r = (r + 1) % n;
    rs.push(r);
  }
  // exclude t
  ls.pop();
  rs.pop();
  // return the smaller one
  return ls.length < rs.length ? ls : rs;
}

module.exports = {
  dist2D,
  rotate2D,
  angle2D,
  circleLineCollision2D,
  findTangentPoints2D,
  findLineIntersection2D,
  shortestArcModulus,
};
