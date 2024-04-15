function searchDocuments() {
    console.log("Searching for documents...");
    // Implement search logic or API call here
}

function downloadFile(format) {
    const status = document.getElementById('downloadStatus');
    status.textContent = `Starting download in ${format.toUpperCase()} format...`;
    setTimeout(() => {
        status.textContent = `Download in ${format.toUpperCase()} complete!`;
    }, 3000); // Simulates download time
}
document.addEventListener('DOMContentLoaded', function() {
    const alertsData = [
        { message: "Document XYZ needs review.", priority: "high" },
        { message: "Annual report has been updated.", priority: "medium" },
        { message: "New submission by Vendor 123 ready for review.", priority: "low" }
    ];

    const alertsList = document.getElementById('alertsList');
    alertsData.forEach(alert => {
        const listItem = document.createElement('li');
        listItem.textContent = alert.message;
        listItem.className = `priority-${alert.priority}`; // Adds a class for styling based on priority
        alertsList.appendChild(listItem);
    });
});

