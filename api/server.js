let express = require('express')
let bodyParser = require('body-parser')
const PORT = 3000

let app = express()
// Parser the body
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.use(express.static('public'));

app.set('view engine', 'ejs')

app.get('/', (req, res) => {
  res.render('index')
})

app.get('/results', (req, res) => {
  res.render('results')
})

app.post('/results', (req, res) => {
  let advertisements = [ {url: "https://www.seiu1000.org/sites/main/files/main-images/camera_lense_0.jpeg", valid: false},
  {url: "https://img.freepik.com/premium-photo/image-colorful-galaxy-sky-generative-ai_791316-9864.jpg?w=2000", valid: true}]
  res.render('results', {advertisements})
})


app.listen(PORT, () => {
  console.log(`Server running at ${PORT}. Address: http://localhost:${PORT}`)
})