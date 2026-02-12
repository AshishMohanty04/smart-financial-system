async function uploadFile() {
    let fileInput = document.getElementById("fileInput");
    let formData = new FormData();
    formData.append("file", fileInput.files[0]);

    let response = await fetch("/upload", {
        method: "POST",
        body: formData
    });

    let result = await response.json();

    displayFrauds(result.frauds);
    loadSummary();
}

async function loadSummary() {
    let response = await fetch("/summary");
    let data = await response.json();

    document.getElementById("summary").innerHTML =
        `<h3>Total Debit: ₹${data.total_debit}</h3>
         <h3>Total Credit: ₹${data.total_credit}</h3>`;

    let labels = data.monthly_data.map(item => item[0]);
    let values = data.monthly_data.map(item => item[1]);

    new Chart(document.getElementById("expenseChart"), {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Debit Amount",
                data: values
            }]
        }
    });
}

function displayFrauds(frauds) {
    let section = document.getElementById("fraudSection");

    if (frauds.length > 0) {
        section.innerHTML = "<h2>Fraud Alerts</h2>";
        frauds.forEach(f => {
            section.innerHTML += `<p>${f.date} - ${f.description} - ₹${f.debit}</p>`;
        });
    } else {
        section.innerHTML = "<h3>No Fraud Detected</h3>";
    }
}
