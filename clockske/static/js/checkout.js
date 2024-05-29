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
      state: $("#counties option:selected").text(),
      city: $("#subcounties option:selected").text(),
      district: $("#wards option:selected").text(),
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
        window.location.href = "order_complete";
      });
  }

  // Render the PayPal button into #paypal-button-container
  paypal
    .Buttons({
      // Call your server to set up the transaction

      style: {
        shape: "pill",
        height: 40,
      },
      createOrder: function (data, actions) {
        return actions.order.create({
          purchase_units: [
            {
              amount: {
                value: window.total,
              },
            },
          ],
        });
      },

      // Call your server to finalize the transaction
      onApprove: function (data, actions) {
        return actions.order.capture().then(function (Details) {
          console.log(Details);
          let errorDetail = Details.error;

          if (errorDetail && errorDetail.issue === "INSTRUMENT_DECLINED") {
            return actions.restart();
          }

          if (errorDetail) {
            var msg = "Sorry, your transaction could not be processed.";
            if (errorDetail.description)
              msg += "\n\n" + errorDetail.description;
            if (orderData.debug_id) msg += " (" + orderData.debug_id + ")";
            return toastr.error(msg);
          }
          if (Details.status == "COMPLETED") {
            submitFormData();
          }
        });
      },
    })
    .render("#paypal-button-container");
});
