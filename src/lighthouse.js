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
  }

  makeLighthouse() {
    // find the lighthouse center
    const lc = rotate2D(
      { x: this.pc.x + this.n, y: this.pc.y },
      this.pc,
      -this.a * this.Ls.length
    );
    // find the illumination points
    const mid = {
      x: ((this.n - 1) * lc.x + this.pc.x) / this.n,
      y: ((this.n - 1) * lc.y + this.pc.y) / this.n,
    };
    const right = rotate2D(mid, lc, this.a / 2);
    const left = rotate2D(mid, lc, -this.a / 2);
    // create lighthouse
    this.Ls.push(
      new Lighthouse(
        this.Ls.length,
        this.r,
        this.pc,
        lc,
        left,
        mid,
        right,
        this.a
      )
    );
    // return false if we have created them all
    return this.Ls.length < this.n;
  }

  // Tries to find the illumination line from source to target
  // Returns
  tryIlluminate(sourceID, targetID, v = Variation.POINT) {
    const source = this.Ls[sourceID];
    const target = this.Ls[targetID];
    if (v === Variation.POINT) {
      // find tangent points
      const [tang1, tang2] = findTangentPoints2D(
        source.lc,
        target.lc,
        target.r
      );
      // find the intersection of the ray and placement
      const [intersection1, intersection2] = [
        findLineIntersection2D(this.pc, target.lc, source.lc, tang1),
        findLineIntersection2D(this.pc, target.lc, source.lc, tang2),
      ];
      // check if they can reach behind the lighthouse
      let [isValid1, isValid2] = [
        this.isValidIntersection(intersection1, target),
        this.isValidIntersection(intersection2, target),
      ];
      // check if they do not collide with the source lighthouse itself
      isValid1 = isValid1 && angle2D(this.pc, source.lc, tang1) <= this.a / 2;
      isValid2 = isValid2 && angle2D(this.pc, source.lc, tang2) <= this.a / 2;

      return [
        {
          from: source.lc,
          to: tang1,
          isValid: true,
          intersection: intersection1,
        },
        {
          from: source.lc,
          to: tang2,
          isValid: isValid2,
          intersection: intersection2,
        },
      ];
    } else if (v === Variation.ARC) {
      // second variation
      if (this.Ls.length != this.n)
        throw new Error("Please create all lighthouses before trying this.");

      // lighthouse in between (needed for collision check later)
      const checkIDs = shortestArcModulus(sourceID, targetID, this.n);

      const ans = [];

      // we will do the calculations as in POINT, but from left and right side of the arcs.
      for (const sourcePoint of [source.left, source.right]) {
        // find tangent points from arc (left)
        const [tang1, tang2] = findTangentPoints2D(
          sourcePoint,
          target.lc,
          target.r
        );
        // find the intersection of the ray and placement
        const [intersection1, intersection2] = [
          findLineIntersection2D(this.pc, target.lc, sourcePoint, tang1),
          findLineIntersection2D(this.pc, target.lc, sourcePoint, tang2),
        ];
        // check if they can reach behind the lighthouse
        let [isValid1, isValid2] = [
          this.isValidIntersection(intersection1, target),
          this.isValidIntersection(intersection2, target),
        ];
        // check if they are at a correct angle with the source arc (must be more than 90 for left)
        isValid1 =
          isValid1 && angle2D(source.lc, sourcePoint, tang1) > Math.PI / 2;
        isValid2 =
          isValid2 && angle2D(source.lc, sourcePoint, tang2) > Math.PI / 2;

        // check if any of them collide with another lighthouse on the way
        isValid1 =
          isValid1 &&
          checkIDs.some((i) =>
            circleLineCollision2D(this.Ls[i].lc, this.r, sourcePoint, tang1)
          );
        isValid2 =
          isValid2 &&
          checkIDs.some((i) =>
            circleLineCollision2D(this.Ls[i].lc, this.r, sourcePoint, tang2)
          );

        // all good
        ans.push({
          from: sourcePoint,
          to: tang1,
          isValid: isValid1,
          intersection: intersection1,
        });
        ans.push({
          from: sourcePoint,
          to: tang2,
          isValid: isValid2,
          intersection: intersection2,
        });
      }

      return ans;
    } else {
      throw new Error("Unknown variation.");
    }
  }

  findFirstIlluminatingID(targetID, v = Variation.POINT) {
    let candidateID;
    for (let i = 0; i < this.n / 2; i++) {
      candidateID = (targetID + 1 + i) % this.n;
      let [success, sP, tP] = this.tryIlluminate(candidateID, targetID, v);
      if (success) {
        return candidateID;
      }
    }
    // no candidates!
    return -1;
  }

  // Check if a ray from sourceP that crosses over tangP, can illuminate the target lighthouse at targetC
  isValidIntersection(intersection, target) {
    const d1 = this.n + target.r; // placement center <--> target edge
    const d2 = dist2D(target.lc, intersection) - target.r; // target edge <--> intersection
    const d3 = dist2D(this.pc, intersection); // placement center <--> intersection
    return d3 === d2 + d1;
  }
}

module.exports = {
  LighthouseManager,
};
