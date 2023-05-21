let express = require('express')
let bodyParser = require('body-parser')
const { exec, spawn } = require('child_process');
const PORT = 3000


function runPythonScript(scriptPath, args) {
  return new Promise((resolve, reject) => {
    const pythonProcess = spawn('python', [scriptPath, ...args]);

    let scriptOutput = '';
    let scriptError = '';

    pythonProcess.stdout.on('data', (data) => {
      scriptOutput += data.toString();
    });

    pythonProcess.stderr.on('data', (data) => {
      scriptError += data.toString();
    });

    pythonProcess.on('close', (code) => {
      if (code !== 0) {
        reject(new Error(`Python script execution failed with code ${code}: ${scriptError}`));
      } else {
        resolve(scriptOutput);
      }
    });
  });
}


let app = express()
// Parser the body
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static('public'));

app.set('view engine', 'ejs')

app.get('/', (req, res) => {
  res.render('index')
})


app.post('/results', async (req, res) => {
  let url = req.body.url
  var isPhish = await runPythonScript("../model/classifyDomain.py", [url])
  let dest_urls = []
  if(url.includes("google") && url.includes("search")){
    const result = await runPythonScript("../model/ads_parser/googleads.py", [url])
    var json = JSON.parse(result)
    dest_urls.push(json)
    for(let i = 0; i < json.length; i++){
      let title = json[i]["title"]
      let currUrl = json[i]["website_link"]
      json[i]["isScam"] = parseInt(await runPythonScript("../model/classifyScam.py", [title]))
      json[i]["isPhishing"] = parseInt(await runPythonScript("../model/classifyDomain.py", [currUrl]))
    }
    
  }
  
  let advertisements = {"url": url,
     "user-agent": req.headers['user-agent'],
     "context": "Kontekst przeglądarki",
     "isPhishing": parseInt(isPhish, 10),
     "ads": {"name": "Unique name",
      "destination_url": dest_urls,
      "words": ["Firma Inwestcyjna", "Produkt"],
      "screenshot_ads": []
     }}

  res.render('results', {advertisements})
})


app.listen(PORT, () => {
  console.log(`Server running at ${PORT}. Address: http://localhost:${PORT}`)
})