let imageCanvas;

$(document).ready(function () {
    let image = document.getElementById('image');
    imageCanvas = getImageCanvas(image);
    fillScopeCanvas();

    $('#image').mousemove(function (e) {
        let x = e.pageX - image.offsetLeft;
        let y = e.pageY - image.offsetTop;
        let pixels = changeScope(x, y);
        updateCenterPixelInfo(x, y);
        updateScopeInfo(image, x, y, pixels);
    })
});

function fillScopeCanvas() {
    let canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        let ctx = canvas.getContext('2d');
        ctx.fillStyle = 'rgb(0, 0, 0)';
        ctx.fillRect(0, 0, 130, 130);
    }
}

function updateCenterPixelInfo(x, y) {
    let pixelData = getPixelData(x, y);
    let intensity = Math.trunc((pixelData[0] + pixelData[1] + pixelData[2]) / 3);
    $('#coordinates').html('x: ' + x + ' y: ' + y);
    $('#rgb-values').html('Red: ' + pixelData[0] + '<br>Green: ' + pixelData[1] + '<br>Blue: ' + pixelData[2]);
    $('#intensity').html('Intensity: ' + intensity);
}

function updateScopeInfo(image, x, y, pixels) {
    if (isScopeOutOfImage(image, x, y)) {
        $('#scope-info').html('Scope Incomplete');
    } else {
        $('#scope-info').html('Mean: ' + mean(pixels).toFixed(2) +
            '<br>Std: ' + std(pixels).toFixed(2) +
            '<br>Median: ' + median(pixels));
    }
}

function isScopeOutOfImage(image, x, y) {
    return x < 5 || y < 5 || x > image.width - 6 || y > image.height - 6;
}

function mean(pixels) {
    let sum = 0;
    for (const pixel of pixels) {
        let intensity = Math.trunc((pixel[0] + pixel[1] + pixel[2]) / 3);
        sum += intensity;
    }
    return sum / pixels.length;
}

function std(pixels) {
    let sum = 0;
    let mean_ = mean(pixels);
    for (const pixel of pixels) {
        let intensity = Math.trunc((pixel[0] + pixel[1] + pixel[2]) / 3);
        sum += Math.pow(intensity - mean_, 2);
    }
    return Math.sqrt(sum / pixels.length);
}

function median(pixels) {
    let intensities = [];
    for (const pixel of pixels) {
        let intensity = Math.trunc((pixel[0] + pixel[1] + pixel[2]) / 3);
        intensities.push(intensity);
    }
    intensities.sort();
    if (pixels.length % 2 === 1) {
        return intensities[(pixels.length + 1) / 2];
    } else {
        return (intensities[pixels.length / 2] + intensities[pixels.length / 2 + 1]) / 2;
    }
}

function getImageCanvas(image) {
    let imageCanvas = document.createElement('canvas');
    imageCanvas.width = image.width;
    imageCanvas.height = image.height;
    imageCanvas.getContext('2d').drawImage(image, 0, 0, image.width, image.height);
    return imageCanvas;
}

function changeScope(x, y) {
    let canvas = document.createElement('canvas');
    let pixels = [];
    let ctx = canvas.getContext('2d');
    pixels = fillScope(ctx, x - 5, y - 5);
    resizeScope(canvas);
    return pixels;
}

function fillScope(ctx, x, y) {
    let pixels = [];
    for (let i = 0; i < 110; i += 10) {
        for (let j = 0; j < 110; j += 10) {
            let pixelData = getPixelData(x + i / 10, y + j / 10);
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            pixels.push(pixelData);
            ctx.fillRect(i, j, 10, 10);
        }
    }
    return pixels;
}

function resizeScope(scopeCanvas) {
    let canvas = document.getElementById('canvas');
    let ctx = canvas.getContext('2d');

    ctx.drawImage(scopeCanvas, 10, 10);
}

function getPixelData(x, y) {
    return imageCanvas.getContext('2d').getImageData(x, y, 1, 1).data;
}