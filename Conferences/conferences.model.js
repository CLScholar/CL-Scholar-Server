const mongoose = require('mongoose'),
      mongoosePaginate = require('mongoose-paginate'),
      Schema = mongoose.Schema;

var PaperSchema = new Schema({
  paper_id        : String,
  paper_title     : String,
  paper_year      : Number,
  citations       : Number
});

// Schema for Conferences
var ConferenceSchema = new Schema({
    _id          : Number,
    name         : [String],
    last_held    : Number,
    papers       : [PaperSchema],
    conference_id: Number

}, {collection: 'conferences', _id: false });

ConferenceSchema.plugin(mongoosePaginate);

const Conferences = module.exports = mongoose.model("Conferences", ConferenceSchema)
