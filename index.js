const express = require('express');
const cors = require('cors');
const Movie = require('./models/movie')
const mongoose = require('mongoose')

const spawn = require("child_process").spawn;

const app = express();
const port = 8080;

//middleware
app.use(cors())

//connect to mongo
// const atlasDBUrl = process.env.DB_URL;
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

//user endpoints


//auth endpoints
//Login, register, logout

const get_movieIds_from_query = (query) => {
    //promise code inspired by:
    //https://www.geeksforgeeks.org/how-to-communicate-json-data-between-python-and-node-js/
    return new Promise((resolve, reject) => {
        try {

            const python = spawn("python", ["./recommendation-system/get-movieIds-from-query.py", query]);

            python.stdout.on("data", (data) => {
                resolve(data.toString());
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
    //given movieId
    console.log("movie received!: ", movieId)

    //return JSON movie object
    const movie = await Movie.findOne({ movieId })
    // console.log(JSON.stringify(movie))
    // return JSON.stringify(movie)
    return movie

}


app.get("/matches/:query", async (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)

    try {
        var data = await get_movieIds_from_query(query)
        var movieIds_matching_query = JSON.parse(data)
        console.log(movieIds_matching_query)

        if (Object.keys(movieIds_matching_query).length == 0) {
            console.log("no matches for query!")
            res.status(404)
            res.send({})
        }

        //Render all movie_ids into JSON movie objects by querying database
        var all_movieIds = [];
        all_movieIds.push(movieIds_matching_query.primaryId)
        all_movieIds.push(...movieIds_matching_query.others)
        // console.log(all_movieIds)

        var movies = [];
        for (movieId of all_movieIds) {
            let movie = await render_movie_from_id(movieId)
            console.log(movie)
            movies.push(movie)
        }
        console.log(movies)

        res.send(JSON.stringify(movies))

        //Send JSON movie objects to client side.
    } catch (err) { console.log('error!: ', err) };

});

app.get('/recommendations/:movieId', (req, res) => {
    //Get movie ids for recommended movies
    // const recommended_movieIds = await get_recommended_movies(movieIds_matching_query.primaryId)

})


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app