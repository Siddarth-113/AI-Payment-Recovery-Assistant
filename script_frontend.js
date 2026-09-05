const API = "http://127.0.0.1:8000";

const form = document.getElementById("invoiceForm");
const invoiceList = document.getElementById("invoiceList");

async function loadInvoices() {
    const response = await fetch(`${API}/invoices`);
    const invoices = await response.json();

    document.getElementById("total").textContent = invoices.length;
    document.getElementById("overdue").textContent =
        invoices.filter(x => x.overdue_days > 0).length;
    document.getElementById("high").textContent =
        invoices.filter(x => x.priority === "High").length;

    if (invoices.length === 0) {
        invoiceList.innerHTML = "<p>No invoices added yet.</p>";
        return;
    }

    invoiceList.innerHTML = invoices.map(invoice => `
        <div class="invoice">
            <h3>${invoice.customer}</h3>
            <p><b>Amount:</b> ₹${Number(invoice.amount).toLocaleString("en-IN")}</p>
            <p><b>Due Date:</b> ${invoice.due_date}</p>
            <p><b>Overdue:</b> ${invoice.overdue_days} days</p>
            <p class="priority ${invoice.priority.toLowerCase()}">
                Priority: ${invoice.priority} | Score: ${invoice.score}
            </p>
            <div class="reminder">
                <b>Suggested Reminder:</b><br>
                ${invoice.reminder}
            </div>
        </div>
    `).join("");
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const data = {
        customer: document.getElementById("customer").value,
        amount: Number(document.getElementById("amount").value),
        due_date: document.getElementById("dueDate").value
    };

    await fetch(`${API}/invoices`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(data)
    });

    form.reset();
    loadInvoices();
});

document.getElementById("clearBtn").addEventListener("click", async () => {
    await fetch(`${API}/invoices`, {method: "DELETE"});
    loadInvoices();
});

loadInvoices();
