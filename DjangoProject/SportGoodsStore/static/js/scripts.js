document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const searchForm = document.querySelector('.search-form');
    const cartIndicator = document.querySelector('.cart-indicator');

    // Проверяем наличие элементов перед добавлением обработчиков событий и изменением свойств
    if (menuToggle && navLinks && searchForm) {
        menuToggle.addEventListener('click', function () {
            navLinks.classList.toggle('active');
            searchForm.classList.toggle('active');
        });
    } else {
        console.error('Не все элементы меню найдены в DOM.');
    }

    if (cartIndicator) {
        // Пример функции для добавления элемента в корзину
        function addToCart() {
            let itemCount = parseInt(cartIndicator.textContent) || 0;
//            itemCount++; // Увеличиваем количество товаров в корзине
//            cartIndicator.textContent = itemCount;
            cartIndicator.style.display = 'inline';
        }

        // Вызываем эту функцию, когда элеменят добавлен в корзину
        // Для демонстрации предположим, что элемент добавлен в корзину при загрузке страницы
        addToCart();
    } else {
        console.error('Элемент "cartIndicator" не найден в DOM.');
    }
});
