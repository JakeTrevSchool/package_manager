"use strict";
function load_version(url) {
    fetch(url)
        .then((response) => response.json())
        .then((data) => {
        console.log(data);
        if (data.status === "OK") {
            //handle ok
        }
        else {
            //handle not ok
        }
    });
}
