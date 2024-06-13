$(document).ready(function () {
  const dataUrl = window.demographicsUrl;
  let dataCache = {};

  // Fetch and populate data
  function populateData() {
    fetch(dataUrl)
      .then((response) => response.json())
      .then((data) => {
        dataCache = data;
        populateCounties(data.counties);
      })
      .catch((error) => console.error("Error:", error));
  }

  // Populate Counties dropdown
  function populateCounties(counties) {
    const selectElement = $("#counties");

    counties.forEach((county) => {
      const option = $("<option></option>")
        .val(county.county_id)
        .text(county.name);
      selectElement.append(option);
    });
  }

  // Populate Subcounties (Constituencies) dropdown based on selected County
  function populateSubcounties(countyId) {
    const selectElement = $("#subcounties");

    selectElement.empty();
    selectElement.append(
      $("<option></option>").val("").text("Select Sub-County...")
    );

    dataCache.constituencies
      .filter((constituency) => constituency.county_id == countyId)
      .forEach((constituency) => {
        const option = $("<option></option>")
          .val(constituency.constituency_id)
          .text(constituency.name);
        selectElement.append(option);
      });
  }

  // Populate Wards dropdown based on selected Subcounty (Constituency)
  function populateWards(subcountyId) {
    const selectElement = $("#wards");

    selectElement.empty();
    selectElement.append($("<option></option>").val("").text("Select Ward..."));

    dataCache.wards
      .filter((ward) => ward.constituency_id == subcountyId)
      .forEach((ward) => {
        const option = $("<option></option>").val(ward.ward_id).text(ward.name);
        selectElement.append(option);
      });
  }

  // Event listener for Counties dropdown
  $("#counties").on("change", function () {
    const selectedCountyId = $(this).val();

    if (selectedCountyId) {
      populateSubcounties(selectedCountyId);
      $("#wards")
        .empty()
        .append($("<option></option>").val("").text("Select Ward..."));
    } else {
      $("#subcounties")
        .empty()
        .append($("<option></option>").val("").text("Select Sub-County..."));
      $("#wards")
        .empty()
        .append($("<option></option>").val("").text("Select Ward..."));
    }
  });

  // Event listener for Subcounties (Constituencies) dropdown
  $("#subcounties").on("change", function () {
    const selectedSubcountyId = $(this).val();

    if (selectedSubcountyId) {
      populateWards(selectedSubcountyId);
    } else {
      $("#wards")
        .empty()
        .append($("<option></option>").val("").text("Select Ward..."));
    }
  });

  // Initialize data
  populateData();
});
