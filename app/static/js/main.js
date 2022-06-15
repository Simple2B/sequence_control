// custom javascript
(function () {
  "use strict";

  feather.replace({ "aria-hidden": "true" });
})();

const close_flash = document.querySelector(".close");
const flash_block = document.querySelector(".hit_flash");
if (flash_block) {
  close_flash.addEventListener("click", function () {
    flash_block.classList.add("invisible");
  });
}

const ms_selectors = document.querySelectorAll(".milestoneSelector");

if (ms_selectors) {
  ms_selectors.forEach(function (el) {
    el.addEventListener("change", function (e) {
      const formData = new FormData();
      formData.set("ms_id", e.target.value);
      formData.set("work_id", el.name);
      fetch("/work_select_milestone/", {
        method: "POST",
        body: formData,
        redirect: "manual",
        mode: "no-cors",
      })
        .then((res) => {
          console.log(res);
        })
        .catch((err) => {
          console.error("ERROR", err.message);
        });
    });
  });
}
