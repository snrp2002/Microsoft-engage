// node modules
const express = require("express");
const bodyParser = require("body-parser");
const https = require("https");
const ejs = require("ejs");
const { spawn } = require("child_process");


const app = express();
const port = process.env.PORT || 5000;


app.set('view engine', 'ejs');
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));


// array of similar movie posters
let SimilarMovies = [];


app.get("/", function (req, res) {
    res.render("index", { movieList: SimilarMovies });
})


app.post("/", function (req, res) {
    SimilarMovies = [];
    const searchedMovie = req.body.searched;
    const options = {
        args: [searchedMovie]
    }

    // starting python program to get data from app.py
    const childPython = spawn('python', ['app.py', searchedMovie])


    childPython.stdout.on('data', function (data) {
        let ans = (`${data}`);
        ans = ans.split("\r\n");

        // making url
        const base_url = "https://api.themoviedb.org/3/movie/";
        const key = "?api_key=ffa475f629d2587a246e35aca6a653c7";

        if (ans === null || ans.length < 6) {                         // any error or no matches
            SimilarMovies.push("No match found !! ");
            res.redirect("/");
        }
        else {                                                   // valid matches
            for (let i = 0; i < 6; i++) {
                const url = base_url + ans[i] + key;

                https.get(url, function (response) {            // api call
                    let rawData = "";
                    response.on('data', (chunk) => { rawData += chunk; });
                    response.on('end', () => {
                        const jsonData = JSON.parse(rawData);
                        SimilarMovies.push("https://image.tmdb.org/t/p/w500/" + jsonData.poster_path);
                    });
                    response.on("error", (err) => {
                        console.log("Error: "+err.message);
                    })
                });
            }
            setTimeout(function () {
                res.redirect("/");
            }, 1000);
        }
    });
    childPython.stderr.on('data',(data) => {
        console.log("Error");
        res.redirect("/");
    })

});
app.listen(port, function () {
    console.log(`Server started listening at port ${port}`);
})
