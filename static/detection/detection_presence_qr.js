var value_presence    = 0;
var qr_recorded_array = [];   // Array of dictionary of recorded users.
var qr_scanner        = null; // QR scanner JavaScript object.
var qr_still          = 120;  // In second.

function init_detection_presence_qr () {
  qr_scanner = new Instascan.Scanner({
    backgroundScan:true,
    video:document.getElementById("video")
  });

  Instascan.Camera.getCameras()
    .catch(function (e) {
      console.log(e);
    })
    .then(function (c) { // `c` is an array of available web cams.
      if (c.length) {
        qr_scanner.start(c[0]); // Use the first available web cam in the array.
      }
      else {
        console.error("no web cam found");
      }
    });
}

function loop_detection_presence_qr () {
  var result = qr_scanner.scan();

  // Decrease `countdown` value.
  increase_value_in_array_of_dictionary(
    qr_recorded_array,
    "countdown",
    -1
  );
  // Remove presence if the counter is 0.
  remove_value_lower_equal_than_in_array_of_dictionary(
    qr_recorded_array,
    "countdown",
    0
  );

  // Assign new `name_client` or reset `countdown` value.
  if (result) {
    // Check if `result.content` already listed as `name_client`.
    var qr_recorded = search_value_in_array_of_dictionary(
      qr_recorded_array,
      "name_client",
      result.content
    );
    if (qr_recorded) {
      // If `result.content` is already in the array reset the `countdown`.
      qr_recorded["countdown"]   = qr_still;
    }
    else if (name_client != result.content) {
      qr_recorded                = {};
      qr_recorded["name_client"] = result.content;
      qr_recorded["countdown"]   = qr_still;
      qr_recorded_array.push(qr_recorded);
    }
  }

  // Print into `document.getElementById()`.
  if (qr_recorded_array.length > 0) {
    value_presence = print_value_in_array_of_dictionary(
      qr_recorded_array,
      "name_client"
    );
  }
  else {
    value_presence = "";
  }
  if (value_presence) {
    document.getElementById("value_presence").innerHTML = value_presence;
  }
  else {
    document.getElementById("value_presence").innerHTML = "...";
  }
  if (qr_recorded_array.length > 0) {
    value_presence = print_value_in_array_of_dictionary(
      qr_recorded_array,
      "name_client",
      false
    );
  }
  else {
    value_presence = "";
  }
}

function increase_value_in_array_of_dictionary (_array, _key, _inc) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      _array[i][_key] += _inc;
    }
  }
}