const express = require('express');
const cors = require('cors');

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


//movie endpoints
// input: receive a query string which is a string 
// output: a list of 20 movie titles in JSON. 
//The first 5 are the closest matches by name in the database, 
//and the other 15 are recommendations based on what other users have liked in the past

//both of these problems can be solved by python and pandas. I could delegate to a script. This script could also have access to a mongo database!

app.get('/movie/:query', (req, res) => {

    const { query } = req.params;
    console.log(query)

    //search database records for movies which are a match for this movie title query
    //connect to mongoose
    //find by id? 

    //find movies similar to 

})

app.get('/movie/similar', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))




app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})