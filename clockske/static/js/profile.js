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
