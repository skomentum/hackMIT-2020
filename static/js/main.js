window.onload = function () {
    drawStars().then(r => console.log("Stars have been drawn"));
}

const starList = [
    [40, 50],
    [80, 120],
    [400, 20],
    [200, 300]
];

async function drawStars() {
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

        let radius = 10;
        let grd = ctx.createRadialGradient(star[0], star[1], 1, star[0], star[1], radius);
        grd.addColorStop(0, "white");
        grd.addColorStop(1, "black");

        // fill with gradient
        ctx.fillStyle = grd;
        ctx.fillRect(star[0] - radius, star[1] - radius, 2*radius, 2*radius);
    }
}