const mongoose = require('mongoose'),
      mongoosePaginate = require('mongoose-paginate'),
      Schema = mongoose.Schema;

var AuthorSchema = new Schema({
  name_list       : [String],
  id              : Number
});

// Schema for Papers
var PaperSchema = new Schema({
    _id: Number,
    paper_id  : String,
    cited: [String],
    cocited: [String],
    citing: [String],
    title  : String,
    conference: String,
    urls: [String],
    year: Number,
    authors: [AuthorSchema],
    summary: String,
    affiliations: [String],
    sentiment_score: Number,
    abstract: String
}, {collection: 'papers', _id: false });

PaperSchema.plugin(mongoosePaginate);

const Papers = module.exports = mongoose.model("Papers", PaperSchema)
