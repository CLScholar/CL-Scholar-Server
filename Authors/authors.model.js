const mongoose = require('mongoose'),
      mongoosePaginate = require('mongoose-paginate'),
      Schema = mongoose.Schema;

var PaperSchema = new Schema({
  collab_authors    : [String],
  paper_id        : String,
  paper_title     : String,
  paper_year      : Number,
  citations       : Number
});

// Schema for authors
var AuthorSchema = new Schema({
    _id: Number,
    author_id  : Number,
    name_list  : [String],
    papers     : [PaperSchema]
}, {collection: 'authors', _id: false });

AuthorSchema.plugin(mongoosePaginate);

const Authors = module.exports = mongoose.model("Authors", AuthorSchema)
