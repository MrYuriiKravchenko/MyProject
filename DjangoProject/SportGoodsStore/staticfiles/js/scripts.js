document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const searchForm = document.querySelector('.search-form');
    const cartIndicator = document.querySelector('.cart-indicator');

    menuToggle.addEventListener('click', function () {
        navLinks.classList.toggle('active');
        searchForm.classList.toggle('active');
    });

    // Example function to add an item to the cart
    function addToCart() {
        let itemCount = parseInt(cartIndicator.textContent) || 0;
//        itemCount++;
        cartIndicator.textContent = itemCount;
        cartIndicator.style.display = 'inline';
    }

    // Call this function when an item is added to the cart
    // For demonstration, let's assume an item is added to the cart when the page loads
    addToCart();
});
