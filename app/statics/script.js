document.addEventListener("DOMContentLoaded", function () {
    const carouselContainer = document.querySelector(".carousel-container");
    const slides = document.querySelectorAll(".carousel-slide");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    let currentIndex = 3;
    const totalSlides = slides.length;
    let autoSlideInterval; // Variable to store auto-slide interval

    function updateCarousel() {
        const offset = -currentIndex * 100;
        carouselContainer.style.transform = `translateX(${offset}%)`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateCarousel();
    }

    function prevSlide() {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateCarousel();
    }

    // Restart auto-slide after manual navigation
    function resetAutoSlide() {
        clearInterval(autoSlideInterval); // Stop current auto-slide
        autoSlideInterval = setInterval(nextSlide, 3000); // Restart it
    }

    // Button click event listeners
    nextBtn.addEventListener("click", function () {
        nextSlide();
        resetAutoSlide();
    });

    prevBtn.addEventListener("click", function () {
        prevSlide();
        resetAutoSlide();
    });

    // Start auto-slide
    autoSlideInterval = setInterval(nextSlide, 3000);
});
