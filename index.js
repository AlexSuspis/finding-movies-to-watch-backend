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


app.get('/python', (req, res) => {


})

const get_movies_from_query = (query => {
    const spawn = require("child_process").spawn;
    const pythonProcess = spawn('python', ["recommendation-system/app.py", query]);

    results = [];

    pythonProcess.stdout.on('data', (data) => {
        //console.log(Buffer.from(data).values())
        results.push(data);
    });

    pythonProcess.stdout.on('end', () => {
        console.log("python script ended")
        //let resultData = Buffer.from(results).values()
        //let resultData = JSON.parse(results)
        let resultData = results.toString()
        console.log(resultData)
    })
})

app.get('/search/:query', (req, res) => {
    const { query } = req.params;
    console.log(`query is: ${query}`)

    movie_ids = get_movies_from_query(query)
    //console.log(movie_ids)

})

app.get('/recommendations', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app