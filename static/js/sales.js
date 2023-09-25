/**
 * Sales Page Functions
 *
 * Provides functionality for adding sales, viewing sales details, and deleting sales.
 *
 * Includes functions to add or remove new rows for sales details input,
 * clear input fields, fetch sales details, populate sales details tables, and
 * delete sales.
 */

/////////////////////////////////////////////////////////////////////
// Add Sale

// Adds a row to input a seed into Add Sales
const addSeedRow = () => {
  const tbody = document.getElementById("sales-details-table");
  const rowData = document.getElementById("add-seed-row");
  const newSeed = rowData.cloneNode(true);
  newSeed.id = `add-seed-row-${tbody.children.length}`;

  // Adds the delete button
  delBtn = document.createElement("button");
  delBtn.innerText = "Delete";
  delBtn.addEventListener("click", rmSeedRow);
  const tds = newSeed.querySelectorAll("td");
  tds[2].appendChild(delBtn);
  tbody.appendChild(newSeed);

  // Clears the cloned inputs
  const selectElement = tds[0].querySelector("select");
  const inputElement = tds[1].querySelector("input");
  selectElement.value = -1;
  inputElement.value = "";
};

// Removes the add seed row
const rmSeedRow = (e) => {
  const row = e.target.parentNode.parentNode;
  row.remove();
};

const addSeedBtn = document.getElementById("add-seed-btn");
addSeedBtn.addEventListener("click", addSeedRow);

// Clears new rows that may have been added on Cancel
const clearSeedRows = () => {
  const tbody = document.getElementById("sales-details-table");
  const firstRow = tbody.querySelector("tr"); // Get the first row
  const tds = firstRow.querySelectorAll("td");

  // Clear the inputs in the first row
  const selectElement = tds[0].querySelector("select");
  selectElement.value = -1;
  const inputElement = tds[1].querySelector("input");
  inputElement.value = "";

  // Create a new tbody element with the first row
  const newTbody = tbody.cloneNode(false);
  newTbody.appendChild(firstRow);
  tbody.parentNode.replaceChild(newTbody, tbody);
};
const addCancelBtn = document.getElementById("add-cancel");
addCancelBtn.addEventListener("click", clearSeedRows);

/////////////////////////////////////////////////////////////////////
// View Sales Details

// Get Sales Details for Selected Sale
const getSalesDetails = async (sale_id) => {
  try {
    const res = await fetch(`./${sale_id}`);
    if (res.ok) {
      const data = await res.json();
      return data;
    } else {
      throw new Error("Error Sales Details Response");
    }
  } catch (error) {
    console.error("Error getting Sales Details: ", error);
  }
};

// Populate the Sales Details top table with the basic Sales Data
const copyBasicSales = (sale_id) => {
  const saleRow = document.getElementById(sale_id);
  const copyRow = document.getElementById("basic-sale-row");

  // Copy the cols except the last 2 (last 2 should be buttons view details, and delete)
  for (let i = 0; i < saleRow.cells.length - 2; i++) {
    const newCol = document.createElement("td");
    newCol.textContent = saleRow.cells[i].textContent;
    copyRow.appendChild(newCol);
  }
};

// Populate the Sales Details Table using fetched data
const populateDetailsTable = (data) => {
  const tbody = document.getElementById("details-table-body");
  // Iterate over each Sale Detail and add it as a row
  for (sd of data["sales_details"]) {
    const newRow = document.createElement("tr");

    const seed = sd["seed_name"];
    const seedCol = document.createElement("td");
    seedCol.innerText = seed;

    const quantity = sd["quantity"];
    const quantityCol = document.createElement("td");
    quantityCol.innerText = quantity;

    newRow.appendChild(seedCol);
    newRow.appendChild(quantityCol);
    tbody.appendChild(newRow);
  }
};

const viewBtns = [...document.getElementsByClassName("view-details-btn")];
viewBtns.forEach((btn) => {
  btn.addEventListener("click", async (e) => {
    // Show the Sales Details Modal
    const detailModal = document.getElementById("sale-details");
    detailModal.style.display = "block";
    const id = btn.dataset.id;

    // Get the Sales Details
    const data = await getSalesDetails(id);

    // Fill Sales Details Modal with Data
    // Basic Sales Data from Sales table
    copyBasicSales(id);
    // Use fetched Sales Details data to fill Details table
    populateDetailsTable(data);
  });
});

// Close Sales Details
const clearSalesDetails = () => {
  const saleRow = document.getElementById("basic-sale-row");
  saleRow.innerHTML = "";

  const detailBody = document.getElementById("details-table-body");
  detailBody.innerHTML = "";
};

const closeBtn = document.getElementById("close-details");
closeBtn.addEventListener("click", () => {
  document.getElementById("sale-details").style.display = "None";
  clearSalesDetails();
});

/////////////////////////////////////////////////////////////////////
// DELETE
const deleteSale = async (id, row) => {
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
    console.error("Error deleting sale:", error);
  }
};
const deleteButtons = [...document.getElementsByClassName("delete-btn")];
deleteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const id = button.dataset.id;
    const row = e.target.parentElement.parentElement;
    deleteSale(id, row);
  });
});
