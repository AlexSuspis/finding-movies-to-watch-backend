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

const render_movie_from_id = (movieId) => {
    //given movieId
    //return JSON movie object
}


app.get("/search/:query", async (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)

    //Get movie ids matching the query
    await get_movieIds_from_query(query)
        .then(res => {
            const movieIds_matching_query = JSON.parse(res);
            console.log(movieIds_matching_query)

            //Render all movie_ids into JSON movie objects by querying database

            //Send JSON movie objects to client side.
        })
        .catch(err => console.log("Error from get_movieIds_from_query(): ", err));


    // const response = await get_movieIds_from_query(query);
    // console.log(movieIds_matching_query);
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