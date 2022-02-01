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

    const dataFromPython = await get_movieIds_from_query(query);
    res.send(dataFromPython);
});

app.get('/recommendations', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app