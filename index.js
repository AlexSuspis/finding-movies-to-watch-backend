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


//movie endpoints


app.get('*', (req, res) => res.status(404).send("Page not found!"))




app.listen(port, () => {
    console.log(`Example app listening on port ${port}`)
})