/**
 * Add Modal Functions
 *
 * Adds functionality to open and close any modal with an id of "add".
 *
 */

// Event listeners to open and close Add modal
const add = document.getElementById("add");
const addForm = document.getElementById("add-form");
const addBtn = document.getElementById("add-btn");

addBtn.addEventListener("click", () => (add.style.display = "block"));

// Close Add Modal
document.getElementById("add-cancel").addEventListener("click", () => {
  add.style.display = "none";
  clear();
});

const clear = () => {
  const inputs = addForm.querySelectorAll("input");
  const selects = addForm.querySelectorAll("select");

  inputs.forEach((input) => {
    input.value = "";
  });

  selects.forEach((select) => {
    select.selectedIndex = 0;
  });
};
