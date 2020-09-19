async function fillParagraph() {
    fetch('/data').then((response) => response.json())
        .then((dataMap) => document.getElementById('body').innerText = dataMap['people']);
}

window.onload = function() {
    fillParagraph();
}