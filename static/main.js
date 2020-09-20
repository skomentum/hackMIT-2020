window.onload = function () {
    drawStars().then(r => console.log("Stars have been drawn"));
}

const starList = [
    [0, 40, 50],
    [6.94, 80, 120],
    [4, 400, 20],
    [2, 600, 300]
];

async function drawStars(data) {
    let canvas = document.getElementById("stars");
    let ctx = canvas.getContext("2d");

    // fill background
    let width = canvas.width;
    let height = canvas.height;
    ctx.fillRect(0, 0, width, height);

    // loop through the stars
    for (let starIndex = 0; starIndex < starList.length; starIndex++) {
        // create a star
        let star = starList[starIndex];

        let radius = 12; // max value of brightness
        let grd = ctx.createRadialGradient(star[1], star[2], 1, star[1], star[2], Math.pow(radius - star[0], .75));
        grd.addColorStop(0, "white");
        grd.addColorStop(1, "black");

        // fill with gradient
        ctx.fillStyle = grd;
        ctx.fillRect(star[1] - radius, star[2] - radius, 2 * radius, 2 * radius);
    }
}