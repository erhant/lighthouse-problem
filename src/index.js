const canvasSketch = require("canvas-sketch");
const random = require("canvas-sketch-util/random");
const math = require("canvas-sketch-util/math");
const Tweakpane = require("tweakpane");
const { LighthouseManager } = require("./lighthouse");

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
  N: 5,
  variation: 1, // 1:point, 2:arc
  source: 3,
  target: 0,
  drawType: DrawTypes.FIND,
};

const sketch = () => {
  return ({ context, width, height }) => {
    params.source = params.source % params.N;
    params.target = params.target % params.N;
    // background
    context.fillStyle = "#f7f4f4";
    context.fillRect(0, 0, width, height);

    context.translate(width / 2, height / 2); // move to center
    const scale = Math.max(width / (3 * params.N), height / (3 * params.N));
    context.scale(scale, scale); // scale up
    context.lineWidth = 2 / scale;

    const L = new LighthouseManager(params.N); // create manager
    while (L.makeLighthouse()) {} // creates lighthouses
    L.Ls.forEach((l) => drawLighthouse(context, l)); // draw lighthouses

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

    // placement center
    context.save();
    context.fillStyle = "grey";
    context.beginPath();
    context.arc(0, 0, (width * 1e-2) / scale, 0, Math.PI * 2);
    context.fill();
    context.restore();
  };
};

const createPaneAndStart = async () => {
  const pane = new Tweakpane.Pane();
  let folder;

  folder = pane.addFolder({ title: "lighthouses" });
  folder.addInput(params, "N", { min: 2, max: 40, step: 1 });
  folder.addInput(params, "source");
  folder.addInput(params, "target");
  folder.addInput(params, "drawType", {
    options: {
      find: DrawTypes.FIND,
      choose: DrawTypes.CHOOSE,
      all: DrawTypes.ALL,
      none: DrawTypes.NONE,
    },
  });
  folder.addInput(params, "variation", {
    options: { point: 1, arc: 2 },
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
function drawIllumination(context, illumObject) {
  let [success, sP, tP] = illumObject; // success, source point, target point
  //console.log(success, sP, tP);
  context.save();
  context.strokeStyle = success ? "green" : "red";
  context.beginPath();
  context.moveTo(sP.x, sP.y);
  context.lineTo(tP.x, tP.y);
  context.stroke();
  context.restore();
}
