// Handle quantity increment/decrement on product detail page
document.addEventListener('DOMContentLoaded', function () {
    const quantityInput = document.getElementById('quantity');
    const incrementBtn = document.getElementById('increment-qty');
    const decrementBtn = document.getElementById('decrement-qty');

    if (incrementBtn && decrementBtn && quantityInput) {
        incrementBtn.addEventListener('click', function () {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue < 99) {
                quantityInput.value = currentValue + 1;
            }
        });

        decrementBtn.addEventListener('click', function () {
            let currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });
    }
});