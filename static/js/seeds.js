/**
 * Seeds Page Functions
 *
 * Provides functionality for editing and delete Seeds.
 *
 * Includes functions to handle opening and closing the edit seed modal, filling
 * the edit form with the associated seeds values, submitting edits using PUT
 * requests, updating the UI with edited data, and deleting seeds.
 */

// Open/Close Edit Seed Modal and fill with values
const editButtons = [...document.getElementsByClassName("edit-btn")];
const edit = document.getElementById("edit");
const editForm = document.getElementById("edit-form");
const seedNameInput = document.getElementById("seed-name");
const seedTypeSelect = document.getElementById("seed-type");
const supplierSelect = document.getElementById("supplier");
const seedIDInput = document.getElementById("seed-id");

// Open Edit Form filled with values
editButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    // Values are in data
    const seedID = button.dataset.id;
    const seedName = button.dataset.name;
    const seedTypeID = button.dataset.type;
    const supplierID = button.dataset.supplier;

    // Add data to input values
    seedIDInput.value = seedID;
    seedNameInput.value = seedName;
    seedTypeSelect.value = seedTypeID;
    supplierSelect.value = supplierID !== "None" ? supplierID : "0";

    edit.style.display = "block";
  });
});

// Close Edit Seed Form
document.getElementById("cancel").addEventListener("click", () => {
  edit.style.display = "none";
});

// Submit Edit form using PUT
const editSeed = async (data) => {
  try {
    const res = await fetch(`./update`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (res.ok) {
      const seedId = data["seed-id"];
      const row = document.getElementById(seedId);
      // Update the row with the new data
      row.cells[0].textContent = data["seed-name"];

      const supplierID = data["supplier"];

      if (supplierID === null) {
        row.cells[2].textContent = "None";
        row.cells[3].textContent = "None";
      } else {
        row.cells[2].textContent = supplierID;
        // Get supplier name from the select value
        const supplierSelect = document.getElementById("supplier");
        const selectedSupplierOption = supplierSelect.querySelector(
          `option[value="${supplierID}"]`
        );
        const supplierName = selectedSupplierOption.textContent.split(": ")[1];
        row.cells[3].textContent = supplierName;
      }

      // Get seed type name from the select value
      const seedTypeSelect = document.getElementById("seed-type");
      const selectedSeedTypeOption = seedTypeSelect.querySelector(
        `option[value="${data["seed-type"]}"]`
      );
      const seedTypeName = selectedSeedTypeOption.textContent;
      row.cells[1].textContent = seedTypeName;

      // update data on edit button
      const editButton = document.querySelector(
        `.edit-btn[data-id="${seedId}"]`
      );
      editButton.dataset.name = data["seed-name"];
      editButton.dataset.type = data["seed-type"];
      if (supplierID === null) {
        editButton.dataset.supplier = "0";
      } else {
        editButton.dataset.supplier = data["supplier"];
      }

      // Hide the edit form
      edit.style.display = "none";
    }
  } catch (error) {
    console.error("Error updating seed:", error);
  }
};
// Process Edit Form Submit
editForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const newSeedName = e.target.elements["seed-name"].value;

  const newSeedTypeId = e.target.elements["seed-type"].value;
  let newSupplierId = e.target.elements["supplier"].value;
  const updateSeedId = e.target.elements["seed-id"].value;

  if (newSupplierId === "0") {
    newSupplierId = null;
  }

  const data = {
    "seed-name": newSeedName,
    "seed-type": newSeedTypeId,
    supplier: newSupplierId,
    "seed-id": updateSeedId,
  };

  editSeed(data);
});

// DELETE
const deleteSeed = async (id, row) => {
  try {
    const res = await fetch(`./delete/${id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });
    if (res.ok) {
      row.remove();
    }
  } catch (error) {
    console.error("Error deleting seed:", error);
  }
};
const deleteButtons = [...document.getElementsByClassName("delete-btn")];
deleteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const id = button.dataset.id;
    const row = e.target.parentElement.parentElement;
    deleteSeed(id, row);
  });
});
