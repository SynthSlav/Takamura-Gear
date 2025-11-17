// Handle increment/decrement buttons in cart
document.addEventListener('DOMContentLoaded', function () {
    // Increment quantity
    document.querySelectorAll('.increment-qty').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const input = document.getElementById(`id_qty_${itemId}`);
            const currentValue = parseInt(input.value);
            if (currentValue < 99) {
                input.value = currentValue + 1;
                // Auto-submit form
                input.closest('form').submit();
            }
        });
    });

    // Decrement quantity
    document.querySelectorAll('.decrement-qty').forEach(button => {
        button.addEventListener('click', function (e) {
            e.preventDefault();
            const itemId = this.dataset.item_id;
            const input = document.getElementById(`id_qty_${itemId}`);
            const currentValue = parseInt(input.value);
            if (currentValue > 1) {
                input.value = currentValue - 1;
                // Auto-submit form
                input.closest('form').submit();
            }
        });
    });
});