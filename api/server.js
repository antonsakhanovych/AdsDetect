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

// app.get('/results', (req, res) => {
//   res.render('results')
// })

app.post('/results', (req, res) => {
  let advertisements = {"url": "https://www.seiu1000.org/sites/main/files/main-images/camera_lense_0.jpeg",
     "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
     "context": "Kontekst przeglądarki",
     "ads": {"name": "Unique name",
      "destination_url":
       ["https://tracking_url_1.pl",
        "https://tracking_url_2.pl",
        "https://firmaxyz.pl/produkt"],
      "words": ["Firma Inwestcyjna", "Produkt"],
      "screenshot_ads": ["https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",
       "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg", "https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg",]
    }}
  res.render('results', {advertisements})
})


app.listen(PORT, () => {
  console.log(`Server running at ${PORT}. Address: http://localhost:${PORT}`)
})