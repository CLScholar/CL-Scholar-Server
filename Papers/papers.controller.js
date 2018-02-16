// Import Author Model
Papers = require('./papers.model');


// Get Papers By name
module.exports.getPapersByName = (title, pageNum, callback) => {
  Papers.paginate(
    {title: { $regex : title, '$options': 'is' }},
    {select: 'title year paper_id citations', page: pageNum, limit: 15 },
    callback
  );
}

// Get Collaborators
module.exports.getCollabsByPaperId = (_id, callback) => {
  Papers.findOne({"paper_id" : _id}, 'authors', callback);
}

//Get Papers by Conference Venue
module.exports.getPapersByConference = (conference, pageNum, callback) => {
  Papers.paginate(
    {conference: { $regex : conference, '$options': 'is' }},
    {select: 'conference title paper_id year citations', page: pageNum, limit: 15 },
    callback
  );
}

//Get Papers Meta by ID
module.exports.getPaperMetaById = (_id, callback) => {
  var callItems = _id.split(',');
  Papers.find({"paper_id" : { $in: callItems }}, 'title  year paper_id citations', callback);

}

// Get Papers By ID
module.exports.getPaperById = (_id, callback) => {
  Papers.findOne({"paper_id" : _id}, callback);
}
