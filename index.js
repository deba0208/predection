const { spawn } = require("child_process");
const express = require("express");
const cors = require("cors");
const app = express();
const PORT = 3000;
app.use(express.json());
app.use(cors());

app.get("/prediction", async (req, res) => {
  let value = 0;
  const childProcess = spawn("python", [`indexChild.py`]);

  let pythonOutput = "";
  childProcess.stdout.on("data", (data) => {
    pythonOutput += data.toString();
  });

  childProcess.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script error" });
    }

    try {
      const result = JSON.parse(pythonOutput);
      res.status(200).json(result);
    } catch (error) {
      res
        .status(500)
        .json({ error: "Failed to parse JSON from python script" });
    }
  });
});

app.listen(PORT, () => {
  console.log(`server is running on: ${PORT}`);
});
