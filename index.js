const express = require('express');
const cors = require('cors');

const spawn = require("child_process").spawn;

const app = express();
const port = 8080;

//middleware
app.use(cors())


app.get('/', (req, res) => {
    res.send('Welcome to the home page!');
})

//user endpoints


//auth endpoints
//Login, register, logout

const get_movieIds_from_query = (query) => {
    return new Promise((resolve, reject) => {
        try {

            const python = spawn("python", ["./recommendation-system/app.py", query]);

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

app.get("/search/:query", async (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)

    //Get movie ids matching the query

    const response = await get_movieIds_from_query(query);
    const movieIds_matching_query = JSON.parse(response);
    console.log(movieIds_matching_query);

    //Get movie ids for recommended movies
    const recommended_movieIds = await get_recommended_movies(movieIds_matching_query.primaryId)

    //Render all movie_ids into JSON movie objects by querying database

    //Send JSON movie objects to client side.

    //Option 1) Choose the movie which matches the query the most?



});

app.get('/recommendations', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app