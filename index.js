const express = require('express');
const cors = require('cors');
const Movie = require('./models/movie')
const mongoose = require('mongoose')

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

const get_movieIds_from_query = (query, n) => {
    //promise code inspired by:
    //https://www.geeksforgeeks.org/how-to-communicate-json-data-between-python-and-node-js/
    return new Promise((resolve, reject) => {
        try {
            const python = spawn(
                "python",
                ["/app/recommendation-system/find_matches_for_query.py", query, n]
            );
            python.stdout.on("data", (data) => {
                movieIds = JSON.parse(data.toString())
                resolve(movieIds)
                // resolve(data.toString());
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

const render_movie_from_id = async (movieId) => {
    console.log("movie received!: ", movieId)
    //fetch movie in database by movieId
    const movie = await Movie.findOne({ movieId })
    return movie
}



app.get("/matches/:query", async (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)
    try {
        var movieIds_matching_query = await get_movieIds_from_query(query, 3)
        console.log(movieIds_matching_query)

        if (Object.keys(movieIds_matching_query).length == 0) {
            console.log("no matches for query!")
            res.status(404)
            res.send({ "errorMessage": "No matches found for query!" })
            return
        }
        var movies = [];
        for (let movieId of movieIds_matching_query) {
            let movie = await render_movie_from_id(movieId)
            console.log(movie)
            movies.push(movie)
        }
        console.log(movies)
        res.send(JSON.stringify(movies))

    } catch (err) {
        console.log('error!: ', err)
        res.status(404)
        res.send({ "errorMessage": "Something went wrong!" })
    };
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
    let { movieIds } = req.params
    try {
        var recommended_movieIds = [];
        recommended_movieIds = await get_recommended_movieIds(movieIds)
        // console.log(recommended_movieIds)
        // console.log(typeof (recommended_movieIds))

        var movies = [];
        for (let movieId of recommended_movieIds) {
            let movie = await render_movie_from_id(movieId)
            // console.log(movie)
            movies.push(movie)
        }
        console.log(movies)
        res.send(JSON.stringify(movies))

    } catch (err) {
        console.log('error in GET /recommendations/:movieIds endpoint: ', err)
        res.status(404)
        res.send({ "errorMessage": "Something went wrong!" })
    }
})


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})

module.exports = {
    app,
    get_recommended_movieIds,
    get_movieIds_from_query
}