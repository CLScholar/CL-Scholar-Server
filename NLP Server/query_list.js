module.exports.query = function (metaData, queryID) {

  // AuthorsID in papers is String // AuthorsID in authors is int
  var queries = {
    // 000 is test query
    1 : [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}, "conference_id": parseInt(metaData.venue[0])}},{$group:{_id: "$year", num_papers:{$sum: 1}}},{$sort: {"_id": 1}}],
    101 : [{$match:{"topics":{$elemMatch:{$eq:metaData.field[0]}}, "conference_id": parseInt(metaData.venue[0])}},{$group:{_id: "$year", num_papers:{$sum: 1}}},{$sort: {"_id": 1}}],
    201: [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}, "conference_id": parseInt(metaData.venue[0])}},{$project:{"title": 1, _id: "$paper_id"}}],
    4: [{$match:{"author_id": parseInt(metaData.author[0])}},{$unwind: "$Yearwise_Publication"},{$project:{"year": "$Yearwise_Publication.year","Publications": "$Yearwise_Publication.number", "_id": 0}},{$sort:{"year": 1}}],
    204: [{$match:{"author_id": parseInt(metaData.author[0])}},{$unwind: "$papers"},{$project:{"Paper_ID": "$papers.paper_id", "Paper_Title": "$papers.paper_title", "_id": 0}}],
    5 : [{$match:{"author_id": parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paperid"}},{$match:{"paperid.topics":{$elemMatch:{$eq: metaData.field[0]}}},},{$unwind: '$paperid'},{$group:{_id: "$paperid.year", "count_paper":{$sum: 1}}},{$sort: {"_id": 1}}],
    105 : [{$match:{"author_id": parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paperid"}},{$match:{"paperid.topics":{$elemMatch:{$eq: metaData.field[0]}}},},{$unwind: '$paperid'},{$group:{_id: "$paperid.year", "count_paper":{$sum: 1}}},{$sort: {"_id": 1}}],
    205 : [{$match:{"author_id": parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paperid"}},{$match:{"paperid.topics":{$elemMatch:{$eq: metaData.field[0]}}},},{$unwind: '$paperid'},{$project:{_id: "$paperid.paper_id", "Title": "$paperid.title"}}],
    6: [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}}},{$group:{_id: "$year", num_papers:{$sum: 1}}},{$sort:{"_id": 1}}],
    206 : [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}}},{$project:{_id: "$paper_id", "Title": "$title"}}],
    7 : [{$unwind: "$Yearwise_Publication"},{$group:{_id: '$conference_id', "name":{"$first": "$name"}, "count":{$sum: "$Yearwise_Publication.number"}}},{$sort:{count: -1}},{$limit: 5}],
    8 : [{$match:{"conference_id": parseInt(metaData.venue[0])}},{$unwind: "$Yearwise_Publication"},{$project:{"Year": "$Yearwise_Publication.year", "Papers": "$Yearwise_Publication.number", _id: 0}},{$sort: {"Year": 1}}],
    9: [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}}},{$project:{"sumCit" :{$sum: "$citation_trend.citation"}, "CitTrend" : "$citation_trend", "Title" : "$title", "PaperID": "$paper_id"}},{$sort:{"sumCit": -1}},{$limit: 1},{$project:{_id: "$PaperID", Name: "$Title", total_cit: "$sumCit", cit_trend: "$CitTrend"}}],
    10: [{$match:{"author_id": parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paperid"}},{$match:{"paperid.topics":{$elemMatch:{$eq: metaData.field[0]}}},},{$unwind: '$paperid'},{$group:{_id: "$paperid.year", "count_paper":{$sum: 1}}},{$sort:{"_id": 1}}],
    11: [{$match:{$and: [{"authors.id": metaData.author[0]},{"authors.id": metaData.author[1]}]}},{$group:{_id: "$year", "paper_count":{$sum: 1}}},{$sort: {"_id": 1}}],
    111: [{$match:{$and: [{"authors.id": metaData.author[0]},{"authors.id": metaData.author[1]}]}},{$group:{_id: "$year", "paper_count":{$sum: 1}}},{$sort: {"_id": 1}}],
    211 : [{$match:{$and: [{"authors.id": metaData.author[0]},{"authors.id": metaData.author[1]}]}},{$project:{"Title": "$title", _id: "$paper_id"}}],
    12 : [{$match:{$and: [{"topics":{$elemMatch:{$eq: metaData.field[0]}}},{"authors.id":  metaData.author[0]},{"authors.id":  metaData.author[1]}]}},{$group:{_id: "$year", "paper_count":{$sum: 1}}},{$sort:{"_id": 1}}],
    112 : [{$match:{$and: [{"topics":{$elemMatch:{$eq: metaData.field[0]}}},{"authors.id":  metaData.author[0]},{"authors.id":  metaData.author[1]}]}},{$group:{_id: "$year", "paper_count":{$sum: 1}}},{$sort:{"_id": 1}}],
    212 : [{$match:{$and: [{"topics":{$elemMatch:{$eq: metaData.field[0]}}},{"authors.id": metaData.author[0]},{"authors.id": metaData.author[1]}]}},{$project:{"Title": "$title", _id: "$paper_id"}}],
    13 : [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}}},{$unwind: "$authors"},{$group:{_id: "$authors.id", "author_name":{$first: "$authors.name_list"}, "Cit_sum":{$sum: "$citations"}}},{$sort:{"Cit_sum": -1}},{$limit: 5}],
    15 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$lt: 0.3}}},{$group:{_id: null, count:{$sum: 1}}},{$project:{_id: 0, "Papers with negative sentiment": "$count"}}],
    115 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$lt: 0.3}}},{$project:{_id: "$paper.paper_id", "Title": "$paper.title", "Sentiment Score": "$paper.sentiment_score"}},{$sort:{"Sentiment Score": 1}}],
    215 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$lt: 0.3}}},{$project:{_id: "$paper.paper_id", "Title": "$paper.title", "Sentiment Score": "$paper.sentiment_score"}},{$sort:{"Sentiment Score": 1}}],
    16 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$gt: 0.6}}},{$group:{_id: null, count:{$sum: 1}}},{$project:{_id: 0, "Papers with positive sentiment": "$count"}}],
    116 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$gt: 0.6}}},{$project:{_id: "$paper.paper_id", "Title": "$paper.title", "Sentiment Score": "$paper.sentiment_score"}},{$sort:{"Sentiment Score": -1}}],
    216 : [{$match:{"author_id" : parseInt(metaData.author[0])}},{$lookup:{from: "papers", localField: "papers.paper_id", foreignField: "paper_id", as: "paper"}},{$unwind: "$paper"},{$match:{"paper.sentiment_score" :{$gt: 0.6}}},{$project:{_id: "$paper.paper_id", "Title": "$paper.title", "Sentiment Score": "$paper.sentiment_score"}},{$sort:{"Sentiment Score": -1}}],
    19: [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}, "year": metaData.year[0]}},{$group:{_id: "$conference_id", "Conference Name":{$first: "$conference"},"Total Papers":{$sum: 1}}}],
    20 : [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}}},{$group:{_id: "$conference_id", "Conference Name":{$first: "$conference"},"Total Papers":{$sum: 1}}}],
    300: [{$match:{"topics":{$elemMatch:{$eq: metaData.field[0]}}, $or: [{"conference_id": parseInt(metaData.venue[0])},{"conference_id": parseInt(metaData.venue[1])}]}},{$group:{_id:{"Year": "$year", "Conf": "$conference_id"}, Total_Papers:{$sum: 1}}},{$sort:{_id: 1}}]
  }


  // 0 Statistical 1 Binary 2 List
  // EXCEPTION TYPES
  // 11 Dynamic Keys 4 Name + Plot 5 DiffList + Plot
  // 12 Binary + show list
  var meta = {
    1: {type: 0, xlabel: "_id", ylabel: "num_papers"},
    101: {type: 1, xlabel: "_id", ylabel: "num_papers"},
    201: {type: 2},
    4: {type: 0, xlabel: "year", ylabel: "Publications"},
    204: {type: 2},
    5: {type: 0, xlabel: "_id", ylabel: "count_paper"},
    105: {type: 1, xlabel: "_id", ylabel: "count_paper"},
    205: {type: 2},
    6: {type: 0, xlabel: "_id", ylabel: "num_papers"},
    206: {type: 2},
    7: {type: 2}, //////////////////
    8: {type: 0, xlabel: "Year", ylabel: "Papers"},
    9: {type: 4, xlabel: "year", ylabel: "citation"},
    10: {type: 5, xlabel: "_id", ylabel: "count_paper"},
    11: {type: 0, xlabel:"_id", ylabel:"paper_count"},
    111: {type: 1, xlabel:"_id", ylabel:"paper_count"},
    211: {type: 2},
    12: {type: 0, xlabel:"_id", ylabel:"paper_count"},
    112: {type: 1, xlabel:"_id", ylabel:"paper_count"},
    212: {type: 2},
    13: {type: 2},
    15: {type: 2},
    115: {type: 12},
    215: {type: 2},
    16: {type: 2},
    116: {type: 12},
    216: {type: 2},
    19: {type: 0, xlabel: "Conference Name", ylabel: "Total Papers"},
    20: {type: 0, xlabel: "Conference Name", ylabel: "Total Papers"},
    300: {type: 3, var: "Year", sep_var: "Conf", count: "Total_Papers", sep_var1: metaData.venue[0], sep_var2: metaData.venue[1]}
  }

  console.log("In Query List:",queryID);
  console.log(queries[parseInt(queryID)])
  return {query: queries[parseInt(queryID)], meta: meta[parseInt(queryID)]}
}

// module.exports.query = {
//   "201": [{$match:{"topics":{$elemMatch:{$eq: "14"}}, "conference":{$regex: "International Conference on Computational Linguistics", '$options': 'is'}}},{$project:{"title": 1, _id: "$paper_id"}}],
//   "101": [{$match:{"topics":{$elemMatch:{$eq: "14"}}, "conference":{$regex: "International Conference on Computational Linguistics", '$options': 'is'}}},{$project:{"title": 1, _id: "$paper_id"}}]
// }
