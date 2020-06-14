function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i in uiBathrooms) {
    if (uiBathrooms[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i in uiBHK) {
    if (uiBHK[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // Invalid Value
}

$(function () {
  $("#uiSqft").change(function () {
    var max = parseInt($(this).attr("max"));
    var min = parseInt($(this).attr("min"));
    if ($(this).val() > max) {
      $(this).val(max);
      alert(
        "Enter Area less than 50000, otherwise default will be inserted i.e., 50000"
      );
    } else if ($(this).val() < min) {
      $(this).val(min);
      alert(
        "Enter Area greater than 1000, otherwise default will be inserted i.e., 1000"
      );
    }
  });
});

function onClickedEstimatePrice() {
  console.log("Estimated price button clicked");
  var sqft = parseFloat(document.getElementById("uiSqft").value);
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations").value;
  var estPrice = document.getElementById("uiEstimatedPrice");
  console.log(sqft);
  console.log(bhk);
  console.log(bathrooms);
  console.log(location);

  var url = "http://127.0.0.1:5000/predict_home_price";
  //var url = "/api/predict_home_price";

  $.post(
    url,
    {
      total_sqft: sqft,
      bhk: bhk,
      bath: bathrooms,
      location: location,
    },
    function (data, status) {
      console.log(data.estimated_price);
      if (data.estimated_price > 100) {
        data.estimated_price = data.estimated_price / 100;
        data.estimated_price = data.estimated_price.toFixed(2);
        console.log(data.estimated_price);
        estPrice.innerHTML =
          "<h2'>" + data.estimated_price.toString() + " Crore</h2>";
        console.log(status);
      } else {
        estPrice.innerHTML =
          "<h2 id='result'>" + data.estimated_price.toString() + " Lakhs</h2>";
        console.log(status);
      }
    }
  );
}

function onPageLoad() {
  console.log("document loaded");
  var url = "http://127.0.0.1:5000/get_location_names"; // Use this if you are NOT using nginx which is first 7 tutorials
  //var url = "/api/get_location_names"; // Use this if  you are using nginx. i.e tutorial 8 and onwards
  $.get(url, function (data, status) {
    console.log("got response for get_location_names request");
    if (data) {
      var locations = data.location;
      var uiLocations = document.getElementById("uiLocations");
      $("#uiLocations").empty();
      for (var i in locations) {
        var opt = new Option(locations[i]);
        $("#uiLocations").append(opt);
      }
    }
  });
}

window.onload = onPageLoad;
