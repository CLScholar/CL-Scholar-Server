// Import Author Model
Authors = require('./authors.model');

// Get Authors
module.exports.getAuthors = (callback, limit) => {
  Authors.find(({}), 'author_id name_list', callback).limit(limit).sort({'author_id' : 1});
}

// Get Authors By name
module.exports.getAuthorsByName = (name, pageNum, callback) => {
  // Authors.find({ 'name_list': { $regex : name, '$options': 'is' } }, 'author_id name_list', callback);
  var reg = addFullTextSearch(name);
  Authors.paginate(
    {name_list: { $regex : reg, '$options': 'is' }},
    {select: 'author_id name_list', page: pageNum, limit: 15 },
    callback
  );
}

// Get Author by ID
module.exports.getAuthorById = (_id, callback) => {
  Authors.findOne({"author_id" : _id}, callback);
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
