// Import Conferences Model
Conferences = require('./conferences.model');

// Get Conferences By name
module.exports.getConferencesByName = (name, pageNum, callback) => {
  // Authors.find({ 'name_list': { $regex : name, '$options': 'is' } }, 'author_id name_list', callback);
  var reg = addFullTextSearch(name);
  Conferences.paginate(
    {name: { $regex : reg, '$options': 'is' }},
    {select: 'conference_id name', page: pageNum, limit: 15 },
    callback
  );
}

// Get Conferences
module.exports.getConferences = (callback, limit) => {
  Conferences.find(({}), 'conference_id name', callback).limit(limit).sort({'name' : 1});
}


// Get Conferences By ID
module.exports.getConferenceByID = (_id, callback) => {
  Conferences.findOne({"conference_id" : _id}, callback);
}

function addFullTextSearch(searchString ) {
    if (searchString) {
        var r = "";
        var sss = searchString.split(" ");
        if (sss.length<=1) {            // only one word
            r = sss[0];
        } else {
            for (var s in sss) {
                r += "(?=.*" + sss[s] + ")";
            }
            r += ".*";
        }
        return r;
    }
}  // addFullTextSearch
