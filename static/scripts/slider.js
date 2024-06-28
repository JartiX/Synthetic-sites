document.addEventListener('DOMContentLoaded', () => {
    const slider = document.querySelector('.slider');
    const slides = Array.from(slider.children);
    const nextButton = document.querySelector('.next-button');
    const prevButton = document.querySelector('.prev-button');

    let currentIndex = 0;

    const updateSliderPosition = () => {
        const slideWidth = slides[0].getBoundingClientRect().width;
        slider.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
    };

    const moveToNextSlide = () => {
        if (currentIndex < slides.length - 1) {
            currentIndex++;
        } else {
            currentIndex = 0;
        }
        updateSliderPosition();
    };

    const moveToPrevSlide = () => {
        if (currentIndex > 0) {
            currentIndex--;
        } else {
            currentIndex = slides.length - 1;
        }
        updateSliderPosition();
    };

    nextButton.addEventListener('click', moveToNextSlide);
    prevButton.addEventListener('click', moveToPrevSlide);

    window.addEventListener('resize', updateSliderPosition);

    updateSliderPosition();
});
