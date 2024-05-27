$(document).ready(function () {
  if (cart_total <= 0) {
    $("#checkout-form").hide();
  }
  $("#checkout-form").submit(function (e) {
    e.preventDefault();
    $("#form-button").hide();
    console.log("Form Submitted...");
    $(".payment-options").removeClass("hidden");
  });

  function submitFormData() {
    let form = document.getElementById("checkout-form");
    let userFormData = {
      total: window.total,
    };

    let shippingInfo = {
      state: form.state.value,
      city: form.city.value,
      district: form.district.value,
      address: form.address.value,
      phone: form.phone.value,
    };

    let url = "/process_order";
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ form: userFormData, shipping: shippingInfo }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
        alert("Transaction completed");
        window.location.href = "/";
      });
  }

  $("#make-payment").click(function () {
    submitFormData();
  });

  // Render the PayPal button into #paypal-button-container
  paypal
    .Buttons({
      // Call your server to set up the transaction

      style: {
        shape: "pill",
        height: 40,
      },
      createOrder: function (data, actions) {
        return fetch("/demo/checkout/api/paypal/order/create/", {
          method: "post",
        })
          .then(function (res) {
            return res.json();
          })
          .then(function (orderData) {
            return orderData.id;
          });
      },

      // Call your server to finalize the transaction
      onApprove: function (data, actions) {
        return fetch(
          "/demo/checkout/api/paypal/order/" + data.orderID + "/capture/",
          {
            method: "post",
          }
        )
          .then(function (res) {
            return res.json();
          })
          .then(function (orderData) {
            // Three cases to handle:
            //   (1) Recoverable INSTRUMENT_DECLINED -> call actions.restart()
            //   (2) Other non-recoverable errors -> Show a failure message
            //   (3) Successful transaction -> Show confirmation or thank you

            // This example reads a v2/checkout/orders capture response, propagated from the server
            // You could use a different API or structure for your 'orderData'
            var errorDetail =
              Array.isArray(orderData.details) && orderData.details[0];

            if (errorDetail && errorDetail.issue === "INSTRUMENT_DECLINED") {
              return actions.restart(); // Recoverable state, per:
              // https://developer.paypal.com/docs/checkout/integration-features/funding-failure/
            }

            if (errorDetail) {
              var msg = "Sorry, your transaction could not be processed.";
              if (errorDetail.description)
                msg += "\n\n" + errorDetail.description;
              if (orderData.debug_id) msg += " (" + orderData.debug_id + ")";
              return alert(msg); // Show a failure message (try to avoid alerts in production environments)
            }

            // Successful capture! For demo purposes:
            console.log(
              "Capture result",
              orderData,
              JSON.stringify(orderData, null, 2)
            );
            var transaction = orderData.purchase_units[0].payments.captures[0];
            alert(
              "Transaction " +
                transaction.status +
                ": " +
                transaction.id +
                "\n\nSee console for all available details"
            );

            // Replace the above to show a success message within this page, e.g.
            // const element = document.getElementById('paypal-button-container');
            // element.innerHTML = '';
            // element.innerHTML = '<h3>Thank you for your payment!</h3>';
            // Or go to another URL:  actions.redirect('thank_you.html');
          });
      },
    })
    .render("#paypal-button-container");
});
