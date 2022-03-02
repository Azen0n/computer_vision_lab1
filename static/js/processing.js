const image = document.getElementById('image');
const canvas = document.getElementById('processed_image_canvas');
canvas.width = image.width;
canvas.height = image.height;
const ctx = canvas.getContext('2d');

$(document).ready(function () {
    document.getElementById('image_row').placeholder = 'From 0 to ' + image.height;
});

function flipVertically() {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(i, image.height - 1 - j, 1, 1);
        }
    }
}

function flipHorizontally() {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(image.width - 1 - i, j, 1, 1);
        }
    }
}

function blurByEightPixels() {
    blur(8);
}

function blurByFourPixels() {
    blur(4);
}

function blur(method) {
    let getBlurPixels;
    if (method === 4) {
        getBlurPixels = getFourBlurPixels;
    } else {
        getBlurPixels = getEightBlurPixels;
    }

    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let blur_pixels = getBlurPixels(i, j, image, imageCanvas);
            let rgb = getMeanRGB(blur_pixels);
            ctx.fillStyle = 'rgb(' + rgb[0] + ', ' + rgb[1] + ', ' + rgb[2] + ')';
            ctx.fillRect(i, j, 1, 1);
        }
    }
}

function getMeanRGB(blur_pixels) {
    let rgb = [0, 0, 0];
    for (const pixel of blur_pixels) {
        for (let k = 0; k < 3; k++) {
            rgb[k] += pixel[k];
        }
    }
    for (let k = 0; k < 3; k++) {
        rgb[k] /= blur_pixels.length;
        rgb[k] = Math.round(rgb[k]);
    }
    return rgb;
}

function isInImage(x, y, image) {
    return 0 <= x && x < image.width && 0 <= y && y < image.height;
}

function getEightBlurPixels(x, y, image, imageCanvas) {
    let pixels = [];
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            if (isInImage(x + i, y + j, image)) {
                let pixelData = imageCanvas.getContext('2d').getImageData(x + i, y + j, 1, 1).data;
                pixels.push(pixelData);
            }
        }
    }
    return pixels;
}

function getFourBlurPixels(x, y, image, imageCanvas) {
    let pixels = [];
    for (let i = -1; i <= 1; i++) {
        for (let j = -1; j <= 1; j++) {
            if (Math.abs(i) + Math.abs(j) !== 2) {
                if (isInImage(x + i, y + j, image)) {
                    let pixelData = imageCanvas.getContext('2d').getImageData(x + i, y + j, 1, 1).data;
                    pixels.push(pixelData);
                }
            }
        }
    }
    return pixels;
}

function changeIntensity() {
    changeChannelGeneral([0, 1, 2]);
}

function changeRed() {
    changeChannelGeneral([0]);
}

function changeGreen() {
    changeChannelGeneral([1]);
}

function changeBlue() {
    changeChannelGeneral([2]);
}

function changeChannelGeneral(channels) {
    let diff = parseInt(document.getElementById('change_channel').value);
    if (isValidDiff(diff)) {
        changeChannel(channels, diff);
    }
}

function isValidDiff(diff) {
    if (Number.isInteger(diff)) {
        if (diff >= -255 && diff <= 255) {
            return true;
        }
    }
    return false;
}

function changeChannel(channels, diff) {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            for (const channel of channels) {
                if (pixelData[channel] + diff < 0) {
                    pixelData[channel] = 0;
                } else if (pixelData[channel] + diff > 255) {
                    pixelData[channel] = 255;
                } else {
                    pixelData[channel] += diff;
                }
            }
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(i, j, 1, 1);
        }
    }
}

function exchangeChannelsGeneral() {
    let channel1 = parseInt(document.getElementById('channel_from').value);
    let channel2 = parseInt(document.getElementById('channel_to').value);

    if (Number.isInteger(channel1) && Number.isInteger(channel2) && channel1 !== channel2) {
        exchangeChannels(channel1, channel2);
    }
}

function exchangeChannels(channel1, channel2) {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            swapPixelChannels(pixelData, channel1, channel2);
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(i, j, 1, 1);
        }
    }
}

function swapPixelChannels(pixelData, channel1, channel2) {
    let temp = pixelData[channel1];
    pixelData[channel1] = pixelData[channel2];
    pixelData[channel2] = temp;
}

function intensityChannelNegative() {
    channelsNegative([0, 1, 2]);
}

function redChannelNegative() {
    channelsNegative([0]);
}

function greenChannelNegative() {
    channelsNegative([1]);
}

function blueChannelNegative() {
    channelsNegative([2]);
}

function channelsNegative(channels) {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            for (const channel of channels) {
                pixelData[channel] = 255 - pixelData[channel];
            }
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(i, j, 1, 1);
        }
    }
}

function contrast() {
    let value = parseInt(document.getElementById('contrast_value').value);
    if (value >= -100 && value <= 100) {
        contrastImage(value);
    }
}

function contrastImage(value) {
    for (let i = 0; i < image.width; i++) {
        for (let j = 0; j < image.height; j++) {
            let pixelData = imageCanvas.getContext('2d').getImageData(i, j, 1, 1).data;
            pixelData = changePixelContrast(pixelData, value);
            ctx.fillStyle = 'rgb(' + pixelData[0] + ', ' + pixelData[1] + ', ' + pixelData[2] + ')';
            ctx.fillRect(i, j, 1, 1);
        }
    }
}

function changePixelContrast(pixelData, value) {
    for (let i = 0; i < 3; i++) {
        pixelData[i] = (1 + value / 100) * (pixelData[i] - 128) + 128;
        if (pixelData[i] < 0) {
            pixelData[i] = 0;
        } else if (pixelData[i] > 255) {
            pixelData[i] = 255;
        }
    }
    return pixelData;
}

function getLuminosityOfRow() {
    let row = parseInt(document.getElementById('image_row').value);
    if (Number.isInteger(row)) {
        if (row >= 0 && row < imageCanvas.height) {
            let intensities = [];
            for (let j = 0; j < image.width; j++) {
                let pixelData = imageCanvas.getContext('2d').getImageData(row, j, 1, 1).data;
                let intensity = (pixelData[0] + pixelData[1] + pixelData[2]) / 3;
                intensities.push(intensity);
            }
            let luminositySum = 0;
            for (const i in intensities) {
                luminositySum += intensities[i];
            }
            console.log(luminositySum);
            console.log(intensities.length);
            $("#luminosity_value").html('Luminosity: ' + Math.round(luminositySum / intensities.length));
        }
    }
}