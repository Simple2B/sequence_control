document.addEventListener("DOMContentLoaded", function () {
  const search_field = document.querySelector("#search_field");
  const search_button = document.querySelector("#search_button");
  const page_title = document.querySelector(".page_title");
  const type = "?type=";
  const query = "?";
  let arr = [];

  arr = page_title.innerHTML.split("/");
  let baseSearchUrl = "/info/" + arr[0] + type + arr[1];

  function isAlphaNumeric(str) {
    var code, i, len;

    for (i = 0, len = str.length; i < len; i++) {
      code = str.charCodeAt(i);
      if (
        !(code > 47 && code < 58) && // numeric (0-9)
        !(code > 64 && code < 91) && // upper alpha (A-Z)
        !(code > 96 && code < 123) && // lower alpha (a-z)
        !(code == 32) && // whitespace
        !(code == 44) && // comma
        !(code == 45) && // hyphen
        !(code == 95)
      ) {
        // underscore
        return false;
      }
    }
    return true;
  }

  function searchIt(data) {
    if (isAlphaNumeric(data)) {
      window.location = baseSearchUrl + query + data;
    } else {
      alert("Would be great if you type letters and numbers ;)");
    }
  }

  search_field.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      event.preventDefault();
      searchIt(search_field.value);
    }
  });

  search_button.addEventListener("click", function (event) {
    event.preventDefault();
    searchIt(search_field.value);
  });
});
