const express = require('express');
      app = express();
      bodyParser = require('body-parser');
      mongoose = require('mongoose');

const port = process.env.PORT || 4000
const limitPerPage = 10;

//Import Python shell
var PythonShell = require('python-shell');
// var pyshell = new PythonShell('master.py', {mode:'text', pythonOptions: ['-u']} );

/////////////////////////////////////
///////NLP QUERY HANDLING////////////
/////////////////////////////////////
database = require('./NLP Server/nlpquery');

// Initialize connection
database.connect(function() {
  // Start the application after the database connection is ready


  //Get Query string from Client
  app.post('/api/nlpquery', function (req, res) {

    var options = {
      mode: 'text',
      // pythonOptions: ['-u'], // get print results in real-time
      args: [req.body.query]
    };

    PythonShell.run('master.py', options, function (err, results) {
      if (err) throw err;
      // results is an array consisting of messages collected during execution

        let queryID = results[0];
        queryID = queryID.replace(/'/g, '"');
        queryID = JSON.parse(queryID)

        let meta = queryID[1];
        var metaData = {
          author: meta['$a'].map(Number),
          venue: meta['$v'].map(Number),
          field: meta['$f'],
          university: meta['$u'],
          year: meta['$y'].map(Number),
          number: meta['$n'].map(Number)
        }
        result = queryID[0];
        result = parseInt(result);
        database.getDocs(metaData, result, function(documents, meta) {
          res.send({docs:documents, meta: meta});
        });
    });
  });
});


// Import Author Controller
author_controller = require('./Authors/authors.controller');
paper_controller = require('./Papers/papers.controller');
conference_controller = require('./Conferences/conferences.controller');

// Middleware
app.use(bodyParser.json());

// Connect to Mongoose
mongoose.Promise = global.Promise;

mongoose.connect('mongodb://localhost/acl', { useMongoClient: true });
// mongodb://acl_user:acl_pass@ds127864.mlab.com:27864/acl
var db = mongoose.connection;

//Bind connection to error event (to get notification of connection errors)
db.on('error', console.error.bind(console, 'MongoDB connection error:'));

app.get('/', (req, res) => {
  res.send('Please use the route /api/author')
});

// Allow CORS
app.all('/*', function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Methods", "GET")
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  next();
});


// Route for Authors
app.get('/api/authors', (req, res) => {
  if (req.query.name) {
    author_controller.getAuthorsByName(req.query.name, req.query.page, (err, authors) => {
      if (err) {
        console.error(err);
      } else {
        res.json(authors.docs);
      }
    });
  }
  else {
    author_controller.getAuthors((err, authors) => {
      if(err) {throw err}
      res.json(authors);
    }, limitPerPage);
  }
});

// Route for a single Author
app.get('/api/authors/:_id', (req, res) => {
  author_controller.getAuthorById(req.params._id, (err, author) => {
    if(err) {throw err}
    res.json(author);
  });
});

// Route for a Single Papers
app.get('/api/paper/:_id', (req, res) => {
  paper_controller.getPaperById(req.params._id, (err, paper) => {
    if(err) {throw err}
    res.json(paper);
  });
});

// Route for a Meta data of  Papers
app.get('/api/papermeta/:_id', (req, res) => {
  paper_controller.getPaperMetaById(req.params._id, (err, paper) => {
    if(err) {throw err}
    res.json(paper);
  });
});


// Route for Collaborators
app.get('/api/authors/collabs/:_id', (req, res) => {
  paper_controller.getCollabsByPaperId(req.params._id, (err, author) => {
    if(err) {throw err}
    res.json(author)
  });
});

//Route for Papers
app.get('/api/papers', (req, res) => {
  if (req.query.title) {
    paper_controller.getPapersByName(req.query.title, req.query.page, (err, papers) => {
      if (err) {
        console.error(err);
      } else {
        res.json(papers.docs);
      }
    });
  }
});

// Route for Conferences
app.get('/api/papers/conferences', (req, res) => {
  if (req.query.name) {
    paper_controller.getPapersByConference(req.query.name, req.query.page, (err, papers) => {
      if (err) {
        console.error(err);
      } else {
        res.json(papers.docs);
      }
    });
  }
});

// Route for Conference search
app.get('/api/conferences', (req, res) => {
  if (req.query.name) {
    conference_controller.getConferencesByName(req.query.name, req.query.page, (err, authors) => {
      if (err) {
        console.error(err);
      } else {
        res.json(authors.docs);
      }
    });
  }
  else {
    conference_controller.getConferences((err, authors) => {
      if(err) {throw err}
      res.json(authors);
    }, limitPerPage);
  }
});

// Route for a Single Conference
app.get('/api/conference/:_id', (req, res) => {
  conference_controller.getConferenceByID(req.params._id, (err, paper) => {
    if(err) {throw err}
    res.json(paper);
  });
});

// 404 Handling
app.get('*', function(req, res){
  res.status(404).send("404 Not Found");
});

// START THE SERVER
// ==============================================
app.listen(port);
console.log("Voodoo Magic happening at port " + port);
