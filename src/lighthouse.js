const math = require("canvas-sketch-util/math");
const {
  rotate2D,
  angle2D,
  circleLineCollision2D,
  shortestArcModulus,
  findTangentPoints2D,
  findLineIntersection2D,
  dist2D,
} = require("./utils");

const Variation = {
  POINT: 1,
  ARC: 2,
};

class Lighthouse {
  constructor(id, r, pc, lc, left, mid, right, a) {
    this.id = id;
    this.r = r;
    this.pc = pc;
    this.lc = lc;
    this.left = left;
    this.mid = mid;
    this.right = right;
    this.a = a;
  }
}

class LighthouseManager {
  constructor(n, r = 1, pc = { x: 0, y: 0 }) {
    this.r = r; // radius
    this.a = math.degToRad(360 / n); // angle (alpha)
    this.n = n; // number of lighthouses
    this.pc = pc; // placement center
    this.Ls = []; // lighthouses
    for (let i = 0; i < n; ++i) {
      // find lighthouse center
      const lc = rotate2D(
        { x: this.pc.x + this.n, y: this.pc.y },
        this.pc,
        -this.a * i
      );
      // find the illumination points
      const mid = {
        x: ((this.n - this.r) * lc.x + this.pc.x) / this.n,
        y: ((this.n - this.r) * lc.y + this.pc.y) / this.n,
      };
      const right = rotate2D(mid, lc, this.a / 2);
      const left = rotate2D(mid, lc, -this.a / 2);
      // create lighthouse
      this.Ls[i] = new Lighthouse(
        i,
        this.r,
        this.pc,
        lc,
        left,
        mid,
        right,
        this.a
      );
    }
  }

  // Tries to find the illumination line from source to target
  // Returns
  tryIlluminate(sourceID, targetID, v = Variation.POINT) {
    const source = this.Ls[sourceID];
    const target = this.Ls[targetID];
    const ans = [];
    if (v === Variation.POINT) {
      // find tangent points
      const tangents = findTangentPoints2D(source.lc, target.lc, target.r);
      for (const tang of tangents) {
        // find the intersection of the ray and placement
        const intersection = findLineIntersection2D(
          this.pc,
          target.lc,
          source.lc,
          tang
        );
        // check if they can reach behind the lighthouse
        let isValid = this.isValidIntersection(intersection, target);
        // check if they do not collide with the source lighthouse itself
        isValid =
          isValid && Math.abs(angle2D(this.pc, source.lc, tang)) < this.a / 2;
        // record this line
        ans.push({
          from: source.lc,
          to: tang,
          isValid: isValid,
          intersection: intersection,
        });
      }
    } else if (v === Variation.ARC) {
      // lighthouses in between source and target (needed for collision check later)
      const checkIDs = shortestArcModulus(sourceID, targetID, this.n);
      // we will do the calculations as in POINT, but from left and right side of the arcs.
      for (const sourcePoint of [source.left, source.right]) {
        // find tangent points from arc (left)
        const tangents = findTangentPoints2D(sourcePoint, target.lc, target.r);
        for (const tang of tangents) {
          // find the intersection of the ray and placement
          const intersection = findLineIntersection2D(
            this.pc,
            target.lc,
            sourcePoint,
            tang
          );
          // check if they can reach behind the lighthouse
          let isValid = this.isValidIntersection(intersection, target);

          // check if they are at a correct angle with the source arc
          isValid =
            isValid &&
            Math.abs(angle2D(tang, sourcePoint, source.lc)) >=
              math.degToRad(90);
          // check if any of them collide with another lighthouse on the way
          isValid =
            isValid &&
            !checkIDs.some((i) =>
              circleLineCollision2D(this.Ls[i].lc, this.r, sourcePoint, tang)
            );

          // all good
          ans.push({
            from: sourcePoint,
            to: tang,
            isValid: isValid,
            intersection: intersection,
          });
        }
      }
    }

    return ans;
  }

  findFirstIlluminatingID(targetID, v = Variation.POINT) {
    // no candidates!
    return -1;
  }

  // Check if intersection is behind the target lighthouse, away from the placement center
  isValidIntersection(intersection, target) {
    return (
      dist2D(this.pc, intersection) > this.n + target.r &&
      dist2D(this.pc, intersection) > dist2D(target.lc, intersection)
    );
  }
}

module.exports = {
  LighthouseManager,
  Variation,
};
