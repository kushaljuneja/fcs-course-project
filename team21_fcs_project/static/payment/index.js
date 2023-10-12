//'use strict'; what is this

var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
var paymentMethodId;
var submit_button = document.getElementById('submit');
var form = document.getElementById('payment-form');

// Disable the button until we have Stripe set up on the page
//document.querySelector("button").disabled = true;
submit_button.disabled = true

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
    base: {
        color: "#000",
        lineHeight: '2.4',
        fontSize: '16px'
    }
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

//document.querySelector("button").disabled = false;
submit_button.disabled = false

var displayError = document.getElementById('card-errors')
card.on('change', function(event) {
    if (event.error) {
        displayError.textContent = event.error.message;
        $('#card-errors').addClass('alert alert-info');
    } else {
      displayError.textContent = '';
      $('#card-errors').removeClass('alert alert-info');
    }
});


form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    pay();
});

var handleAction = function(clientSecret) {
    stripe.handleCardAction(clientSecret).then(function(data) {
    if (data.error) {
        showError("Your card was not authenticated, please try again");
    } else if (data.paymentIntent.status === "requires_confirmation") {
        fetch("/orders/add/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN
            },
            body: JSON.stringify({
                paymentIntentId: data.paymentIntent.id
            })
        })
        .then(function(result) {
          return result.json();
        })
        .then(function(json) {
            if (json.error) {
                showError(json.error);
            } else {
                orderComplete();
            }
        });
    } else {
        orderComplete();
    }
    });
};


var pay = function() {
    changeLoadingState(true);

    // Collects card details and creates a PaymentMethod
    stripe.createPaymentMethod("card", card)
    .then(function(result) {
        if (result.error) {
            console.log(result.error.message);
            changeLoadingState(false);        
        } else {
            paymentMethodId = result.paymentMethod.id;
            var product_qty = document.getElementById('quantity').value;
            return fetch("/orders/add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": CSRF_TOKEN
                },
                body: JSON.stringify({'paymentMethodId': paymentMethodId, 'product_id': product_id, 'product_qty': product_qty})
            });
        }
    })
    .then(function(result) {
        return result.json();
    })
    .then(function(response) {
        if (response.error) {
            showError(response.error);
        } else if (response.requiresAction) {
            // Request authentication
            handleAction(response.clientSecret);
        } else {
            orderComplete();
        }
    });
};

/* Shows a success / error message when the payment is complete */
var orderComplete = function() {
    window.location.replace("../account/dashboard/"); // to be changed later
};

var showError = function(errorMsgText) {
    alert(errorMsgText);
    submit_button.disabled = false;
};

// Show a spinner on payment submission - not complete
var changeLoadingState = function(isLoading) {
    if (isLoading) {
        submit_button.disabled = true;
    } else {
        submit_button.disabled = false;
    }
};
