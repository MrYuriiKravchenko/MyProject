document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.wishlist-button').forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();

            // Check if login is required
            if (this.dataset.loginRequired) {
                const loginUrl = '{% url "account_login" %}?next={{ request.path }}';
                window.location.href = loginUrl;
                return;
            }

            const productId = this.dataset.productId;
            const action = this.dataset.action;
            const url = action === 'add' ? '{% url "shop:add_to_wishlist" 0 %}'.slice(0, -2) + productId + '/' :
                                           '{% url "shop:remove_from_wishlist" 0 %}'.slice(0, -2) + productId + '/';

            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    this.dataset.action = 'remove';
                    this.classList.remove('heart-not-added');
                    this.classList.add('heart-added');
                } else if (data.status === 'removed') {
                    this.dataset.action = 'add';
                    this.classList.remove('heart-added');
                    this.classList.add('heart-not-added');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
