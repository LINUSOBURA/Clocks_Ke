$(document).ready(function () {
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
});
