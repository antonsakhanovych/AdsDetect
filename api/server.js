let express = require('express')
let bodyParser = require('body-parser')
const PORT = 3000

let app = express()
// Parser the body
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

app.set('view engine', 'ejs')

app.get('/', (req, res) => {
  res.render('index')
})

app.post('/backend', (req, res) => {
  console.log(req.body.url, " ", req.body.keywords)
  res.redirect('/')
})


app.listen(PORT, () => {
  console.log(`Server running at ${PORT}. Address: http://localhost:${PORT}`)
})