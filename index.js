const { spawn } = require("child_process");
setInterval(() => {
  const childProcess = spawn("python", [`indexChild.py`]);
  childProcess.stdout.on("data", (data) => {
    // pythonOutput += data.toString();
    console.log(data.toString());
  });
}, 10000);
