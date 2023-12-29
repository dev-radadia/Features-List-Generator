// Set the Textbox value to Project Name in the HTML page
document.getElementById('pjname_filled').value = pjname;

// Function to navigate to a new page
function navigate() {
    window.location = '/';
}

// Function to download the excel sheet
function download() {
    fetch('/download?value=' + pjname)
    .then(response => response.blob())
    .then(blob => {
        const link = document.createElement("a");
        link.href = window.URL.createObjectURL(blob);
        link.download = filename;
        link.click();
    })
    .catch(error => alert(`Error downloading!!\n${error}`));
}