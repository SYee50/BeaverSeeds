/**
 * Input Formatting Functions
 *
 * Provides input formatting functionality for phone numbers, zip codes, and
 * state abbreviations by ensuring that the input only accepts digits or
 * specific characters and formats them into the desired structure.
 */

// Format the phone number input to only accept digits and format in three sections
const phoneInput = document.getElementById("phone");
phoneInput.addEventListener("input", (e) => {
  // Remove non-digit chars from input
  const input = e.target.value.replace(/\D/g, "");

  // Set input value, to formatted input digits, only allowing up to 10 digits using slice
  if (input.length > 10) {
    e.target.value = `(${input.slice(0, 3)}) ${input.slice(3, 6)}-${input.slice(
      6,
      10
    )}`;
  } else if (input.length > 6) {
    e.target.value = `(${input.slice(0, 3)}) ${input.slice(3, 6)}-${input.slice(
      6
    )}`;
  } else if (input.length > 3) {
    e.target.value = `(${input.slice(0, 3)}) ${input.slice(3)}`;
  } else if (input.length > 0) {
    e.target.value = `(${input.slice(0)}`;
  } else {
    e.target.value = "";
  }
});

// Format the zip input to only accept digits and format in two sections
const zipInput = document.getElementById("zip");
zipInput.addEventListener("input", (e) => {
  // Remove non-digit chars from input
  const input = e.target.value.replace(/\D/g, "");

  // Set input value to formatted input digits, only allowing up to 9 digits using slice
  if (input.length > 5) {
    e.target.value = `${input.slice(0, 5)}-${input.slice(5, 9)}`;
  } else if (input.length > 0) {
    e.target.value = input;
  } else {
    e.target.value = "";
  }
});

// Format the state to only accept 2 letters and make uppercase
const stateInput = document.getElementById("state");
stateInput.addEventListener("input", (e) => {
  // Remove non alpha chbars and convert to uppercase
  let input = e.target.value.replace(/[^a-zA-Z]/g, "");
  input = input.toUpperCase();

  // Set input value to formatted input, only using 2 letters using slice
  if (input.length > 2) {
    e.target.value = input.slice(0, 2);
  } else {
    e.target.value = input;
  }
});
