$(document).ready(function () {
  counties_url =
    "https://raw.githubusercontent.com/njoguamos/kenya-demographics-units/467906ef2ebb2ad9c6b7071330da7e513885c6cc/src/counties/counties.json";

  subcounties_url =
    "https://raw.githubusercontent.com/njoguamos/kenya-demographics-units/master/src/sub-counties/sub-counties.json";

  wards_url =
    "https://raw.githubusercontent.com/LINUSOBURA/hosted_data/main/kenya_wards.json";
  // populate select
  function populateCounties() {
    const selectElement = $("#counties");
    fetch(counties_url)
      .then((response) => response.json())
      .then((data) => {
        data.forEach((item) => {
          const option = $("<option></option>").val(item.code).text(item.name);
          selectElement.append(option);
        });
      })
      .catch((error) => console.error("Error:", error));
  }

  // populate subcounties
  function populateSubcounties(countyCode) {
    const selectElement = $("#subcounties");

    selectElement.empty();
    selectElement.append(
      $("<option></option>").val("").text("Select Sub-County...")
    );

    fetch(subcounties_url)
      .then((response) => response.json())
      .then((data) => {
        data
          .filter((item) => item.county_code == countyCode)
          .forEach((item) => {
            const option = $("<option></option>")
              .val(item.code)
              .text(item.name);
            selectElement.append(option);
          });
      })
      .catch((error) => console.error("Error:", error));
  }

  // populate wards
  function populateWards(subcountyCode) {
    const selectElement = $("#wards");
    selectElement.empty();
    selectElement.append($("<option></option>").val("").text("Select Ward..."));

    fetch(wards_url)
      .then((response) => response.json())
      .then((data) => {
        data
          .filter((item) => item.constituency_code == subcountyCode)
          .forEach((item) => {
            const option = $("<option></option>")
              .val(item.code)
              .text(item.name);
            selectElement.append(option);
          });
      })
      .catch((error) => console.error("Error:", error));
  }

  //Event Listeners
  $("#counties").on("change", function () {
    const selectedCountyCode = $(this).val();
    if (selectedCountyCode) {
      populateSubcounties(selectedCountyCode);
    } else {
      $("#subcounties")
        .empty()
        .append($("<option></option>").val("").text("Select Sub-County..."));
      $("#wards")
        .empty()
        .append($("<option></option>").val("").text("Select Ward..."));
    }
  });

  $("#subcounties").on("change", function () {
    const selectedSubcountyCode = $(this).val();
    if (selectedSubcountyCode) {
      populateWards(selectedSubcountyCode);
    } else {
      $("#wards")
        .empty()
        .append($("<option></option>").val("").text("Select Ward..."));
    }
  });

  populateCounties();
});
