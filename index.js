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


app.get('/python', (req, res) => {


})


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

// async function get_movies_from_query(query) {
//     try {

//         const pythonProcess = spawn('python', ["recommendation-system/app.py", query]);

//         results = [];

//         pythonProcess.stdout.on('data', (data) => {
//             results.push(data);
//         });

//         await pythonProcess.stdout.on('end', () => {
//             let resultData = results.toString()
//             console.log("results: ", resultData)
//             return resultData
//         })

//     } catch (err) {
//         console.log("error in calling python script")
//     }
// }

// app.get('/search/:query', async (req, res) => {

//     const { query } = req.params;
//     console.log(`query is: ${query}`)

//     const results = await get_movies_from_query(query)
//     // get_movies_from_query(query)
//     //     .then(data => console.log("successful resolved promise! results are: ", data))
//     //     .catch(err => console.log('caught an error calling get_movies_from_query()!: ', err))
//     console.log("this should only run after we get results!", results)
// })

app.get('/recommendations', (req, res) => { })


app.get('*', (req, res) => res.status(404).send("Page not found!"))


app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})


module.exports = app