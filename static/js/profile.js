if (staff == "True") {
  $(".staff-button").removeClass("hidden");

  $("#view_orders").click(function () {
    $("#show-orders-admin").toggleClass("hidden");
  });
} else {
  $("#view_orders").click(function () {
    $("#show-orders").toggleClass("hidden");
  });
}

$(".shipping-status").each(function () {
  if ($(this).html().trim() === "True") {
    $(this).html(
      '<i class="fa-regular fa-circle-check" style="color: #059429;"></i>'
    );
  } else {
    $(this).html(
      '<i class="fa-solid fa-ellipsis" style="color: #FFD43B;"></i>'
    );
  }
});

$('.add-product').click(function(){
  window.location.href = '/product_upload';
})

$('.edit-products').click(function(){
  window.location.href = '/shop';
})
$(document).ready(function(){
  $('.shipping-status-checkbox').change(function(){
    const checkbox = $(this);
    const orderId = checkbox.data('order-id');
    const shipped = checkbox.is(':checked');
    let url = '/update_shipping_status'

  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken
      },
      body: JSON.stringify({
        order_id: orderId,
        shipped: shipped
      })
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.status !== 'success') {
        toastr.error('Failed to update shipping status');
        this.checked = !shipped; // Revert checkbox state
      }
    })
    .catch(error => {
      toastr.error('Error updating shipping status');
      this.checked = !shipped; // Revert checkbox state
    });
  })
})
