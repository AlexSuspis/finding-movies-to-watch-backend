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
    const movie_ids_matching_query = await get_movieIds_from_query(query);
    console.log(movie_ids_matching_query);

    //Get movie ids for recommended movies


    //Render all movie_ids into JSON movie objects by querying database

    //Send JSON movie objects to client side.

    //Option 1) Choose the movie which matches the query the most?
    //Option 2) Don't choose any movie, send all movies received to user

    //We will need also to get a list of recommendations. 
    //but will this be for a single movie, or for a whole list of movies?
    //it is easier to do with just a single movie. But if the python algorithm only performs recommendations
    //for one movie, how do we choose this movie? The one who looks the most like the user query.
    //Is this done in the python script, and then sent as a JSON object, {primary_movie: 123, others: [1,2,..,n]}
    //or in this Express server?
    //It would make more sense to do it in the python script, as that's where all the data processing is taking place.
    //thus, the Express server would only render the actual objects to send to the client side, given movie ids.


});

app.get('/recommendations', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app