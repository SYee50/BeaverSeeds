/**
 * Suppliers Page Functions
 *
 * Provides functionality to delete a supplier.
 *
 * Includes a function to handle deleting a supplier using a DELETE request,
 * and updaties the UI by removing the corresponding row from the table.
 */

// DELETE Suppliers

// Delete a Supplier from the Supplier table
const deleteSupplier = async (id, row) => {
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
    console.error("Error deleting supplier:", error);
  }
};

const deleteButtons = [...document.getElementsByClassName("delete-btn")];
deleteButtons.forEach((button) => {
  button.addEventListener("click", (e) => {
    const id = button.dataset.id;
    const row = e.target.parentElement.parentElement;
    deleteSupplier(id, row);
  });
});
