var MongoClient = require('mongodb').MongoClient;
var mongoUrl = "mongodb://localhost:27017/acl";
var query_list = require('./query_list');
var db;

var paperQueries = [1,101, 201,6,206,9,11,111,211,12,112,212,13,214,19,20,300];
var authorQueries = [4, 5, 105, 205, 204, 10,15,115,215,16,116,216];
var conferenceQueries = [7,8];

exports.connect = function(callback) {
  MongoClient.connect(mongoUrl, function(err, database) {
    if( err ) throw err;
    db = database.db('acl');
    callback();
  });
}

//Example query
quer = [{$match:{"conference":{$regex : "International Conference on Computational Linguistics", '$options': 'is'}}},{$sort:{"citations" : -1}},{$limit:10},{$project:{_id: "$paper_id", "Title": "$title", "Citations": "$citations"}}];

exports.getDocs = function(metaData, queryID, callback) {
  // this is using the same db connection

  var query_data = query_list.query(metaData, queryID);
  var exc_query = query_data.query;
  var meta = query_data.meta;


  if (paperQueries.indexOf(parseInt(queryID)) > -1) {
    console.log("IN PAPER");
    db.collection('papers').aggregate(exc_query).toArray(function(err, result) {
      callback(result, meta);
    });
  }
  else if (authorQueries.indexOf(parseInt(queryID)) > -1) {
    db.collection('authors').aggregate(exc_query).toArray(function(err, result) {
      callback(result, meta);
    });
  }
  else if (conferenceQueries.indexOf(parseInt(queryID)) > -1) {
    console.log("In conference with query ID", queryID);
    db.collection('conferences').aggregate(exc_query).toArray(function(err, result) {
      callback(result, meta);
    });
  }
  else {
    // TEST CASE FOR NOW
    console.log("Errror");
    callback({Error: "Sorry something unexpected happened"}, {type:99});

    // db.collection('papers').aggregate(id_to_query).toArray(function(err, result) {
    //   callback(result);
    // });
  }

}
