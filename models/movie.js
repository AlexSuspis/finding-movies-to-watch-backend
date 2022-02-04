//What does a movie object look like?
// {title, countries, provider}

const mongoose = require('mongoose')
const Schema = mongoose.Schema;

const MovieSchema = new Schema({
    title: String,
    movieId: Number,
    countries: [String],
    providers: [String]
})


module.exports = mongoose.model('Movie', MovieSchema)