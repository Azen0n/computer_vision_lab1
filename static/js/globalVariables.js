const image = document.getElementById('image');
let imageCanvas;
let canvas;
let ctx;

if (image) {
    imageCanvas = getImageCanvas(image);
    canvas = document.getElementById('processed_image_canvas');
    canvas.width = image.width;
    canvas.height = image.height;
    ctx = canvas.getContext('2d');
}

function getImageCanvas(image) {
    let imageCanvas = document.createElement('canvas');
    imageCanvas.width = image.width;
    imageCanvas.height = image.height;
    imageCanvas.getContext('2d').drawImage(image, 0, 0, image.width, image.height);
    return imageCanvas;
}