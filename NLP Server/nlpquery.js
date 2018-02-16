var MongoClient = require('mongodb').MongoClient;
var mongoUrl = "mongodb://localhost:27017/acl";
var query_list = require('./query_list');
var db;

var authorQueries = [50001, 5001, 5002, 5201, 5202, 5401, 5402, 5601, 5602, 5801, 5802,
                    6001, 6002, 6201, 6202, 6401, 6402, 6601, 6602, 6801, 6802,
                    7001, 7002, 7201, 7202, 7401, 7402, 7601, 7602, 7801, 7802,
                    8001, 8002, 8201, 8202, 8401, 8402, 8601, 8602, 8801, 8802,
                    9001, 9002, 9201, 9202, 9401, 9402, 9601, 9602, 9801, 9802,
                    10001, 10002, 10201, 10202, 10401, 10402, 10601, 10602, 10801, 10802 ]

var conferenceQueries = [50002, 5009, 5011, 5025, 5209, 5211, 5409, 5411, 5609, 5611, 5809, 5811,
                        6009, 6011, 6025, 6209, 6211, 6409, 6411, 6609, 6611, 6809, 6811,
                        7009, 7011, 7025, 7209, 7211, 7409, 7411, 7609, 7611, 7809, 7811,
                        8009, 8011, 8025, 8209, 8211, 8409, 8411, 8609, 8611, 8809, 8811,
                        9009, 9011, 9025, 9209, 9211, 9409, 9411, 9609, 9611, 9809,9811,
                        10009, 10011, 10025, 10209, 10211, 10409, 10411, 10609, 10611, 10809,10811]

exports.connect = function(callback) {
  MongoClient.connect(mongoUrl, function(err, database) {
    if( err ) throw err;
    db = database.db('acl');
    callback();
  });
}

exports.getDocs = function(metaData, queryID, callback) {
  // this is using the same db connection

  //meta collection 1=authors 2=papers 3=conferences
  var query_data = query_list.query(metaData, queryID);
  var exc_query = query_data.query;
  var meta = query_data.meta;


  if(queryID === 0) {
    console.log("Query Not in our Template");
    callback({Error: "Sorry something unexpected happened"}, {type:99});
  }
  else if (authorQueries.indexOf(queryID) > -1) {
    meta.collection = 1;
    if (queryID > 50000) {
      callback(exc_query, meta)
    }
    else {
      db.collection('authors').aggregate(exc_query).toArray(function(err, result) {
        callback(result, meta);
      });
    }
  }
  else if (conferenceQueries.indexOf(queryID) > -1) {
    meta.collection = 3;
    if (queryID > 50000) {
      callback(exc_query, meta)
    }
    else {
      db.collection('conferences').aggregate(exc_query).toArray(function(err, result) {
        callback(result, meta);
      });
    }
  }
  else {
    meta.collection = 4;
    db.collection('papers').aggregate(exc_query).toArray(function(err, result) {
      callback(result, meta);
    });
  }

}
