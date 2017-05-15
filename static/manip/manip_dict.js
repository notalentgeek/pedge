function print_value_in_array_of_dictionary (_array, _key, _with_space=true) {
  var print = "";
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      if (with_space) { print += _array[i][_key] + ", "; }
      else            { print += _array[i][_key] + ","; }
    }
  }

  // If `print` valid remove two last characters.
  if (print) {
    print = print.substring(0, print.length - 2);
  }

  return print;
}

function remove_value_lower_equal_than_in_array_of_dictionary (_array, _key, _value) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      if (_array[i][_key] <= _value) {
        _array.splice(i, 1);
      }
    }
  }
}

function search_value_in_array_of_dictionary (_array, _key, _value) {
  for (var i = 0; i < _array.length; i ++) {
    if (_array[i].hasOwnProperty(_key)) {
      if (_array[i][_key] == _value) {
        return _array[i];
      }
    }
  }

  return null;
}