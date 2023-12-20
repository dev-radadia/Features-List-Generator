// Initialize global variables
const textbox = document.getElementById('pjname');

// Function to navigate to a new page
function navigate() {
  var input = textbox.value;
  input = input.trim();

  if(input == "") {
    alert("Please enter a valid project name");
  }
  else {
    // sendData(input);
    window.location = '/generate?value=' + input;
  }
}

// Event listener to detect whether the Enter key was pressed
textbox.addEventListener("keypress", function(event) {
  if(event.key === "Enter") {
    event.preventDefault();
    navigate();
  }
});

// function sendData(pjname) {
//   const request = new XMLHttpRequest();
//   request.open('POST', `/getdata/${JSON.stringify(pjname)}`);
//   request.send();
// }