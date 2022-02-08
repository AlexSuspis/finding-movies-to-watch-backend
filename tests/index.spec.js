const request = require('supertest')
const app = require('../index')


// GET /search/:query
//searches for and retrieves a movie name in the dataset.
//Input: query string
//Output: JSON object with multiple movies inside, or error if movie not found
// describe('GET /search/:query endpoint', () => {
//     it('should unpack a query string from the request object parameter', () => { })
//     it('should return error code if movie title not found from query string', () => { })
//     it('should return an array of JSON movie objects if query string matches', () => { })
//     it('should return a 200 OK status code if movie title match is found', () => { })
// })

describe('get_recommended_movies(movieId) function', () => {
    const { get_recommended_movieIds } = require('../index')
    it('if promise is resolved successfully, should always return an array', () => {

    })
    it('should return an array of length 0 if movieId does not exist in dataset', () => {

    })
    it('should return an array of length 10', async () => {
        //movieId for Superman (1978)
        const movieId = 2640;
        const movieIds = await get_recommended_movieIds(movieId)
        expect(movieIds).toBeInstanceOf(Array)
        // const movieIds = data.
    })
})


// GET /recommend/:movieTitle
// Input: movie title
// Output: most similar movies to that one based on past user likes




test('Get the home path', (done) => {
    request(app).get('/').expect(200, done)
})