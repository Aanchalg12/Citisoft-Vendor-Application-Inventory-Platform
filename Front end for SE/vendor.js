function navigate(page) {
    console.log("Navigate to:", page);
    const contentArea = document.querySelector('article'); // Selects the main content area
    contentArea.innerHTML = `<h1>${page}</h1><p>This is the ${page} page. Content will be added here.</p>`; // Updates content dynamically
}

function addNewVendor() {
    console.log("Adding new vendor product");
    const contentArea = document.querySelector('article');
    contentArea.innerHTML = `<h1>Add New Vendor Product</h1><p>Form to add a new vendor product will be implemented here.</p>`;
    // Here you would typically implement form display and submission logic
}

function showRecentSearches() {
    console.log("Showing recent searches");
    const contentArea = document.querySelector('article');
    contentArea.innerHTML = `<h1>Recent Searches</h1><p>List of recent searches will be displayed here.</p>`;
    // Logic to retrieve and display recent searches would go here
}

function showRecentViews() {
    console.log("Showing recent views");
    const contentArea = document.querySelector('article');
    contentArea.innerHTML = `<h1>Recent Views</h1><p>List of recently viewed items will be displayed here.</p>`;
    // Logic to retrieve and display recent views would go here
}
