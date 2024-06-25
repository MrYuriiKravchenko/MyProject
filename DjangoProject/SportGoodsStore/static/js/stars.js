document.addEventListener('DOMContentLoaded', function () {
    const ratingForm = document.getElementById('rating-form');
    const commentForm = document.getElementById('comment-form');

    if (ratingForm) {
        ratingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(ratingForm);
            fetch('.', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                const averageRatingElem = document.querySelector('.rating h3');
                averageRatingElem.textContent = 'Рейтинг: ' + (data.average_rating || 'нет оценок');
            })
            .catch(error => console.error('Ошибка:', error));
        });
    }

    if (commentForm) {
        commentForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(commentForm);
            fetch('.', {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    window.location.reload();
                } else {
                    console.error('Ошибка:', data);
                }
            })
            .catch(error => console.error('Ошибка:', error));
        });
    }

    // Добавляем проверку на авторизацию для формы оценки
    if (ratingForm && !{{ user.is_authenticated|lower }}) {
        ratingForm.addEventListener('submit', function (event) {
            event.preventDefault();
            window.location.href = '{% url "account_login" %}?next={{ request.path }}';
        });
    }
});
