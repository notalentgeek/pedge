var name_client         = "";
var name_client_default = "testClient";
function init_qr_code (_document_ready=false) {
  var qr_code_height = document.getElementById("qr_code").clientHeight;
  var qr_code_width = document.getElementById("qr_code").clientWidth;
  var qr_code_dimension = qr_code_height < qr_code_width ? qr_code_height : qr_code_width;
  var value_qr = document.getElementById("value_qr");

  // If value in `value_qr` is invalid.
  if (!value_qr.value) {
    value_qr.focus();
    return;
  }

  // If value in `value_qr` is valid.
  // Remove previous QR code.
  $("#qr_code > canvas").remove();
  $("#qr_code > img").remove();

  // Set new QR code.
  new QRCode(document.getElementById("qr_code"), {
    height:qr_code_dimension,
    width:qr_code_dimension,
    text:value_qr.value
  });

  name_client = value_qr.value;
}
function insert_from_url_qr_code () {
    var value_name = String(window.location.href).split("?name=")[1];
    value_name = (value_name === undefined) ? undefined : value_name.split("?")[0];
    if (value_name !== undefined) {
      $("#value_qr").val(value_name);
      $("#qr_generate").click();
    }
    else {
      $("#value_qr").val(name_client_default);
      $("#qr_generate").click();
    }
    $("#value_qr").blur();
}