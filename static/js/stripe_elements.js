// Get Stripe keys from template
var stripePublicKey = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
var clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1);

var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

// Card styling to match site design
var style = {
    base: {
        color: '#000',
        fontFamily: '"Roboto", sans-serif',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};

var card = elements.create('card', {
    style: style,
    hidePostalCode: true
});
card.mount('#card-element');

// Show card errors as user types
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        errorDiv.innerHTML = `<i class="fas fa-times"></i> ${event.error.message}`;
    } else {
        errorDiv.textContent = '';
    }
});

// Handle payment on form submit
var form = document.getElementById('payment-form');

form.addEventListener('submit', function (ev) {
    ev.preventDefault();
    card.update({ 'disabled': true });
    document.getElementById('submit-button').setAttribute('disabled', true);

    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            billing_details: {
                name: form.full_name.value.trim(),
                email: form.email.value.trim(),
                phone: form.phone_number.value.trim(),
                address: {
                    line1: form.street_address1.value.trim(),
                    line2: form.street_address2.value.trim(),
                    city: form.town_or_city.value.trim(),
                    country: form.country.value.trim(),
                    state: form.county.value.trim(),
                }
            }
        },
    }).then(function (result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            errorDiv.innerHTML = `<i class="fas fa-times"></i> ${result.error.message}`;
            card.update({ 'disabled': false });
            document.getElementById('submit-button').removeAttribute('disabled');
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
            }
        }
    });
});