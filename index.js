const express = require('express');
const cors = require('cors');
const Movie = require('./models/movie')
const mongoose = require('mongoose')
const axios = require('axios')

const spawn = require("child_process").spawn;

const app = express();
const port = process.env.PORT || 8080;

//middleware
app.use(cors())

//connect to mongo
// const atlasDBUrl = process.env.DB_URL;
// const dbUrl = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority";
const dbUrl = "mongodb+srv://root_user:root123@cluster0.i7dzt.mongodb.net/finding-movies-to-watch?retryWrites=true&w=majority";
mongoose.connect(dbUrl,
    {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .then(() => console.log('Connected to database!'))
    .catch(err => console.log(err));


app.get('/', (req, res) => {
    res.send('Welcome to the home page!');
})

const render_movieIds_into_movies = async (movieIds) => {
    let movies = []
    for (let movieId of movieIds) {
        let movie = await render_movie_from_id(movieId)
        console.log(movie)
        movies.push(movie)
    }
    console.log(movies)
    return movies
}

const render_movie_from_id = async (movieId) => {
    console.log("movie received!: ", movieId)
    //fetch movie in database by movieId
    const movie = await Movie.findOne({ movieId })
    return movie
}



app.get("/matches/:query", async (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)


    const getMatchedMovies = async function () {
        try {
            // const response = await axios.get(`http://finding-movies-to-watch_recommendation-system_1:3000/matches/${query}/3`)            // console.log(response)
            const response = await axios.get(`http://recommendation-system:3000/matches/${query}/3`)            // console.log(response)
            var matched_movieIds = response.data

            console.log(matched_movieIds)

            //If no matched movies
            if (Object.keys(matched_movieIds).length == 0) {
                console.log("no matches for query!")
                res.status(404)
                res.send({ "errorMessage": "No matches found for query!" })
                return
            }

            //render movieIds into movie objects
            let movies = await render_movieIds_into_movies(matched_movieIds)
            res.send(JSON.stringify(movies))
            return
        }
        catch (err) {
            console.log(err)
            res.send({ "error!": err })
        }
    }
    await getMatchedMovies()

    return
});
const get_recommended_movieIds = (movieIds) => {
    //promise code inspired by:
    //https://www.geeksforgeeks.org/how-to-communicate-json-data-between-python-and-node-js/
    return new Promise((resolve, reject) => {
        try {
            const python = spawn(
                "python",
                ["recommendation-system/find_recommendations_for_movies.py", movieIds]
            );
            python.stdout.on("data", (data) => {
                var recommended_movieIds = JSON.parse(data.toString())
                resolve(recommended_movieIds);
            });
            python.stderr.on("data", (data) => {
                reject(data.toString());
            });
        }
        catch (err) {
            console.log("error!: ", err)
        }
    });


};

//Input: movieIds
//Output: movieIds most similar to input movieId, not including any of the input movieIds
app.get('/recommendations/:movieIds', async (req, res) => {

    const { movieIds } = req.params;
    console.log(`movieIDs: ${movieIds}`)

    const getRecommendedMovies = async function () {
        try {
            const response = await axios.get(`http://localhost:3000/recommendations/${movieIds}`)
            // console.log(response)
            var recommended_movieIds = response.data

            console.log(recommended_movieIds)

            //render movieIds into movie objects
            let movies = await render_movieIds_into_movies(recommended_movieIds)
            res.send(JSON.stringify(movies))
            return
        }
        catch (err) {
            console.log(err)
            res.send({ "errorMessage": "Something went wrong!" })
            return
        }
    }
    await getRecommendedMovies()

    return
})


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})

module.exports = {
    app,
    get_recommended_movieIds,
}