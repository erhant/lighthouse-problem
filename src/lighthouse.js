const math = require("canvas-sketch-util/math");
const {
  rotate2D,
  angle2D,
  circleLineCollision2D,
  shortestArcModulus,
  findTangentPoint2D,
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
    const left = rotate2D(mid, lc, this.a / 2);
    const right = rotate2D(mid, lc, -this.a / 2);
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
      // first variation
      const tang = findTangentPoint2D(source.lc, target.lc, target.r);
      if (
        math.radToDeg(angle2D(this.pc, source.lc, tang)) >
        math.radToDeg(this.a) / 2
      ) {
        // no, cant illuminate behind the target
        return [false, source.lc, tang];
      } else {
        // yes, can illuminate behind the target
        return [true, source.lc, tang];
      }
    } else if (v === Variation.ARC) {
      // second variation
      if (this.Ls.length != this.n) {
        throw new Error("Please create all lighthouses before trying this.");
      } else {
        const tang = findTangentPoint2D(source.left, target.lc, target.r);
        if (math.radToDeg(angle2D(tang, source.left, source.lc)) < 90) {
          // problem is at the source
          return [false, source.left, tang];
        } else {
          // source is okay, check for collusions in-between
          const checkIDs = shortestArcModulus(sourceID, targetID, this.n);
          for (let i of checkIDs) {
            if (
              circleLineCollision2D(this.Ls[i].lc, this.r, source.left, tang)
            ) {
              // collision happens
              return [false, source.left, tang];
            }
          }
          // all good
          return [true, source.left, tang];
        }
      }
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
}

module.exports = {
  LighthouseManager,
};
