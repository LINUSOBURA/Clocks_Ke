$(document).ready(function () {
  // display product
  $(".show-product-details").click(function () {
    let product_id = $(this).data("product");
    console.log("productId", product_id);
    window.location.href = `/product/${product_id}`;
  });
  // add to cart
  $(".update-cart").click(function () {
    let product_id = $(this).data("product");
    let action = $(this).data("action");
    console.log("productId", product_id, "Action", action);
    console.log("User", user);

    if (user == "AnonymousUser") {
      window.location.href = "/login";
    } else {
      updateUserOrder(product_id, action);
    }
  });

  function updateUserOrder(product_id, action) {
    console.log("User is authenticated, sending data...");

    let url = "/update_item";

    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrftoken,
      },
      body: JSON.stringify({ productId: product_id, action: action }),
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log("Data", data);
        location.reload();
      });
  }
});
