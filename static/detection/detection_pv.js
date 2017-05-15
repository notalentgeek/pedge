var analyzer = null; // For pitch detection.
var audio_context = null;
var max_size = null;
var media_stream_source = null;
var raf_id = null;
var volume_meter = null;

// For pitch detection.
var buff_length = 1024;
var buff = new Float32Array(buff_length);
var minimum_samples = 0;
var threshold_auto_correlation = 0.9;

// Giving the signal to update DOM elements when
// `pitch_update` or `volume_update` is `true`.
var pitch_update = false;
var volume_update = false;
var value_pitch = 0;
var value_volume = 0;

function auto_correlation( _buff, _sample_rate ) {
  var best_correlation = 0;
  var best_offset = -1;
  var found_good_correlation = false;
  var last_correlation = 1;
  var rms = 0;
  var size = _buff.length;
  var maximum_samples = Math.floor(size/2);
  var correlations = new Array(maximum_samples);

  for (var i = 0; i < size; i ++) {
    var val = _buff[i];
    rms += val*val;
  }

  rms = Math.sqrt(rms/size);
  if (rms < 0.01) { // not enough signal
    return -1;
  }


  for (var offset = minimum_samples; offset < maximum_samples; offset ++) {
    var correlation = 0;

    for (var i=0; i<maximum_samples; i++) {
      correlation += Math.abs((_buff[i])-(_buff[i+offset]));
    }
    correlation = 1 - (correlation/maximum_samples);
    correlations[offset] = correlation; // Store it, for the tweaking we need to do below.
    if ((correlation > threshold_auto_correlation) && (correlation > last_correlation)) {
      found_good_correlation = true;
      if (correlation > best_correlation) {
        best_correlation = correlation;
        best_offset = offset;
      }
    } else if (found_good_correlation) {
      // Short - circuit, we found a good correlation, then a bad one, so we'd just be seeing copies from here.
      // Now we need to tweak the offset - by interpolating between the values to the left and right of the
      // best offset, and shifting it a bit. This is complex, and HACKY in this code (happy to take PRs!)
      // we need to do a curve fit on `correlations[]` around `best_offset` in order to better determine precise
      // (anti - aliased) `offset`.

      // We know `best_offset >= 1`,
      // since found_good_correlation cannot go to true until the second pass (`offset = 1`), and
      // we can't drop into this clause until the following pass (else if).
      var shift = (correlations[best_offset + 1] - correlations[best_offset - 1])/correlations[best_offset];
      return _sample_rate/(best_offset + (8*shift));
    }
    last_correlation = correlation;
  }
  if (best_correlation > 0.01) {
    return _sample_rate/best_offset;
  }
  return -1;
}

function got_stream (_stream) {
  analyzer = audio_context.createAnalyser();
  analyzer.fftSize = 2048;
  media_stream_source = audio_context.createMediaStreamSource(_stream);
  volume_meter = createAudioMeter(audio_context);
  media_stream_source.connect(analyzer);
  media_stream_source.connect(volume_meter);

  loop_pitch();
  loop_volume();
}

function init_detection_pv () {
  window.AudioContext = window.AudioContext || window.webkitAudioContext;
  audio_context = new AudioContext();
  max_size = Math.max(4,Math.floor(audio_context.sampleRate/5000)); // Corresponds to a 5 kHz signal.

  // Web audio permission.
  navigator.getUserMedia =
    navigator.getUserMedia ||
    navigator.webkitGetUserMedia ||
    navigator.mozGetUserMedia;

  navigator.getUserMedia({
    "audio": {
      "mandatory": {
        "googAutoGainControl": "false",
        "googEchoCancellation": "false",
        "googHighpassFilter": "false",
        "googNoiseSuppression": "false"
      },
      "optional": []
    }
  }, got_stream, function () { alert("cannot get audio stream"); });
}

function loop_pitch () {
  analyzer.getFloatTimeDomainData(buff);
  var ac = auto_correlation(buff, audio_context.sampleRate);

  if (pitch_update) {
    value_pitch = Number(ac) < 0 ? 0 : Number(ac.toFixed(3));
    document.getElementById("value_pitch").innerHTML = value_pitch;
    pitch_update = false;
  }
  window.requestAnimationFrame(loop_pitch);
}

function loop_volume () {
  if (volume_update) {
    value_volume = Number(volume_meter.volume.toFixed(3));
    document.getElementById("value_volume").innerHTML = value_volume;
    volume_update = false;
  }
  window.requestAnimationFrame(loop_volume);
}