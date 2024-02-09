//when first loaded page move the images scroll to the middle index image
function scrollToMiddleImage() {
    var images = document.querySelectorAll('.port-elem-sel-image');
    if (images.length > 0) {
        var middleIndex = Math.floor(images.length / 2);
        var middleImage = images[middleIndex];
        if (middleImage) {
            var container = document.querySelector('.portfolio-element-selected-images');
            var imageWidth = images[0].offsetWidth + 20; // Assumes all images have the same width and 20px total margin
            var scrollLeft = middleIndex * imageWidth;
            container.scrollLeft = scrollLeft - (container.clientWidth / 2) + (imageWidth / 2);
        } else {
            console.error('No image with index ' + middleIndex + ' found');
        }
    } else {
        console.error('No images found');
    }
}

window.onload = scrollToMiddleImage;

document.addEventListener('DOMContentLoaded', function() {
    // Define imageLines as a collection of all .image-line elements
    var imageLines = document.querySelectorAll('.image-line');

    // Set data-index attribute on each image-line
    imageLines.forEach(function(imageLine, index) {
        imageLine.dataset.index = index;
    });

    // Check if imageLines is not undefined
    if (imageLines) {
        // Add click event listener to each image-line
        imageLines.forEach(function(imageLine) {
            imageLine.addEventListener('click', function() {
                document.querySelector('.image-line.active').classList.remove('active');
                this.classList.add('active');
                setTimeout(scrollToActiveImage, 0);
            });
        });

        // Move the active class to the left
        document.querySelector('.portfolio-element-selected-images-arrow-left').addEventListener('click', function() {
            var active = document.querySelector('.image-line.active');
            if (active.previousElementSibling) {
                active.classList.remove('active');
                active.previousElementSibling.classList.add('active');
            } else {
                active.classList.remove('active');
                imageLines[imageLines.length - 1].classList.add('active');
            }
            setTimeout(scrollToActiveImage, 0);
        });

        // Move the active class to the right
        document.querySelector('.portfolio-element-selected-images-arrow-right').addEventListener('click', function() {
            var active = document.querySelector('.image-line.active');
            if (active.nextElementSibling) {
                active.classList.remove('active');
                active.nextElementSibling.classList.add('active');
            } else {
                active.classList.remove('active');
                imageLines[0].classList.add('active');
            }
            setTimeout(scrollToActiveImage, 0);
        });
    }

    // Function to scroll the .portfolio-element-selected-images container to the active image
    function scrollToActiveImage() {
        var activeLine = document.querySelector('.image-line.active');
        if (activeLine) {
            var activeIndex = activeLine.dataset.index;
            var activeImage = document.querySelector('.port-elem-sel-image[data-index="' + activeIndex + '"]');
            console.info('--------------- ' + activeIndex + ' ---------------', activeImage);
            if (activeImage) {
                var container = document.querySelector('.portfolio-element-selected-images');
                var images = document.querySelectorAll('.port-elem-sel-image');
                var imageWidth = images[0].offsetWidth + 20; // Assumes all images have the same width and 20px total margin
                var activeIndex = Array.from(images).indexOf(activeImage);
                var scrollLeft = activeIndex * imageWidth;
              
                container.scrollLeft = scrollLeft - (container.clientWidth / 2) + (imageWidth / 2);
                
            } else {
                console.error('No image with index ' + activeIndex + ' found');
            }
        } else {
            console.error('No active image found');
        }
    }
});

