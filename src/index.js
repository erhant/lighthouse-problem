const canvasSketch = require("canvas-sketch");
const random = require("canvas-sketch-util/random");
const math = require("canvas-sketch-util/math");
const Tweakpane = require("tweakpane");
const { LighthouseManager, Variation } = require("./lighthouse");

const settings = {
  dimensions: [1080, 1080],
};

const DrawTypes = {
  NONE: 0, // show nothing
  FIND: 1, // find the first correct source to chosen target
  CHOOSE: 2, // draw from chosen source to chosen target
  ALL: 3, // draw from all sources to chosen target
};

const params = {
  N: 3,
  radius: 1,
  variation: Variation.ARC,
  scaleFactor: 4,
  source: 3,
  target: 0,
  drawType: DrawTypes.ALL,
};

let scale;

const sketch = () => {
  return ({ context, width, height }) => {
    params.source = Math.floor(params.source) % params.N;
    params.target = Math.floor(params.target) % params.N;
    // background
    context.fillStyle = "white";
    context.fillRect(0, 0, width, height);

    context.translate(width / 2, height / 2); // move to center
    scale = Math.max(
      width / (params.scaleFactor * params.N),
      height / (params.scaleFactor * params.N)
    );
    context.scale(scale, scale); // scale up
    context.lineWidth = 2 / scale;

    const L = new LighthouseManager(params.N, params.radius); // create manager
    L.Ls.forEach((l) => drawLighthouse(context, l)); // draw lighthouses

    // placement center
    context.save();
    context.fillStyle = "#f7f4f4";
    context.beginPath();
    context.arc(0, 0, (width * 1e-2) / scale, 0, Math.PI * 2);
    context.fill();
    context.restore();

    if (params.drawType === DrawTypes.FIND) {
      // find the first illuminating ID
      const s = L.findFirstIlluminatingID(params.target, params.variation);
      if (s !== -1) {
        drawIllumination(
          context,
          L.tryIlluminate(s, params.target, params.variation)
        );
      } else {
        console.log("No lighthouse can illuminate this target.");
      }
    } else if (params.drawType === DrawTypes.CHOOSE) {
      // draw from source to target chosen by user
      drawIllumination(
        context,
        L.tryIlluminate(params.source, params.target, params.variation)
      );
    } else if (params.drawType === DrawTypes.ALL) {
      // draw all
      for (let i = 1; i < params.N; i++) {
        drawIllumination(
          context,
          L.tryIlluminate(
            (params.target + i) % params.N,
            params.target,
            params.variation
          )
        );
      }
    }
  };
};

const createPaneAndStart = async () => {
  const pane = new Tweakpane.Pane();
  let folder;

  folder = pane.addFolder({ title: "lighthouses" });
  folder.addInput(params, "N", { min: 2, max: 40, step: 1 });
  folder.addInput(params, "source");
  folder.addInput(params, "target");
  folder.addInput(params, "radius", { min: 0.06, max: 3.14, step: 0.04 });
  folder.addInput(params, "scaleFactor", { min: 3, max: 10, step: 1 });
  folder.addInput(params, "drawType", {
    options: {
      find: DrawTypes.FIND,
      choose: DrawTypes.CHOOSE,
      all: DrawTypes.ALL,
      none: DrawTypes.NONE,
    },
  });
  folder.addInput(params, "variation", {
    options: { point: Variation.POINT, arc: Variation.ARC },
  });

  const sketchmgr = await canvasSketch(sketch, settings);

  pane.on("change", () => sketchmgr.render());
};

createPaneAndStart();

// Draw a lighthouse
function drawLighthouse(context, l) {
  context.save();

  // halo
  context.strokeStyle = "black";
  context.beginPath();
  context.arc(l.lc.x, l.lc.y, l.r, 0, Math.PI * 2);
  context.stroke();

  // center
  context.beginPath();
  context.fillStyle = "orange";
  context.arc(l.lc.x, l.lc.y, l.r / 10, 0, Math.PI * 2);
  context.fill();

  // left illum point
  context.beginPath();
  context.fillStyle = "red";
  context.arc(l.left.x, l.left.y, l.r / 10, 0, Math.PI * 2);
  context.fill();

  // right illum point
  context.beginPath();
  context.fillStyle = "blue";
  context.arc(l.right.x, l.right.y, l.r / 10, 0, Math.PI * 2);
  context.fill();

  // line to both illum points
  context.strokeStyle = "gray";
  context.beginPath();
  context.moveTo(l.lc.x, l.lc.y);
  context.lineTo(l.right.x, l.right.y);
  context.moveTo(l.lc.x, l.lc.y);
  context.lineTo(l.left.x, l.left.y);
  context.stroke();

  context.restore();
}

// Draw an illumination line
function drawIllumination(context, illumLines) {
  //console.log(illumLines);
  context.save();

  illumLines.forEach((line) => {
    context.beginPath();
    context.strokeStyle = line.isValid ? "green" : "red";
    context.moveTo(line.from.x, line.from.y);
    context.lineTo(line.to.x, line.to.y);
    context.stroke();
    //context.fillStyle = line.isValid ? "green" : "gray";
    if (line.isValid) {
      context.save();
      context.beginPath();
      context.moveTo(line.to.x, line.to.y);
      context.lineTo(line.intersection.x, line.intersection.y);
      context.stroke();
      context.beginPath();
      context.fillStyle = "green";
      context.arc(
        line.intersection.x,
        line.intersection.y,
        params.radius / 10,
        0,
        Math.PI * 2
      );
      context.fill();
      context.restore();
    }
  });

  context.restore();
}
