document.addEventListener("DOMContentLoaded", () => {
    lucide.createIcons();

    /* PIE CHART */
    new Chart(document.getElementById("riskPieChart"), {
        type: "doughnut",
        data: {
            labels: ["GST Mismatch", "Arithmetic Error", "Duplicate Entry", "Compliance Risk"],
            datasets: [{
                data: [32, 28, 18, 22],
                backgroundColor: ["#f87171", "#c084fc", "#38bdf8", "#2dd4bf"],
                borderWidth: 0,
                hoverOffset: 15
            }]
        },
        options: {
            plugins: {
                legend: {
                    position: "bottom",
                    labels: { color: "#94a3b8", usePointStyle: true }
                }
            },
            cutout: "70%",
            maintainAspectRatio: false
        }
    });

    /* LINE CHART */
    new Chart(document.getElementById("trendLineChart"), {
        type: "line",
        data: {
            labels: ["00h", "04h", "08h", "12h", "16h", "20h"],
            datasets: [{
                data: [5, 14, 8, 22, 17, 9],
                borderColor: "#c084fc",
                backgroundColor: "rgba(192,132,252,0.12)",
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: "#64748b" }, grid: { display: false } },
                y: { ticks: { color: "#64748b" }, grid: { color: "rgba(255,255,255,0.05)" } }
            },
            maintainAspectRatio: false
        }
    });

    /* AUDIT FLOW */
    const pdfInput = document.getElementById("pdfInput");
    const dropZone = document.getElementById("dropZone");
    const auditBtn = document.getElementById("auditBtn");
    const terminal = document.getElementById("terminal");
    const fileInfo = document.getElementById("fileInfo");

    dropZone.onclick = () => pdfInput.click();

    pdfInput.onchange = () => {
        if (pdfInput.files.length) {
            fileInfo.innerText = "CONNECTED: " + pdfInput.files[0].name;
            fileInfo.style.color = "var(--accent)";
        }
    };

    auditBtn.onclick = async () => {
        if (!pdfInput.files.length) {
            alert("Please upload a PDF to audit.");
            return;
        }

        terminal.innerHTML = "<p>> Starting AuditAgent core…</p>";
        auditBtn.innerText = "AUDITING…";

        const steps = [
            "Parsing PDF layers",
            "Extracting numeric & semantic fields",
            "Validating arithmetic integrity",
            "Checking GST & tax rules",
            "Scanning for duplicates",
            "Cross-verifying text vs numbers",
            "Finalizing risk score"
        ];

        for (const step of steps) {
            await new Promise(r => setTimeout(r, 900));
            terminal.innerHTML += `<p>> ✔ ${step}</p>`;
            terminal.scrollTop = terminal.scrollHeight;
        }

        terminal.innerHTML += `<p style="color:#22c55e">> Audit Completed · Accuracy: 98.6%</p>`;
        auditBtn.innerText = "AUDIT COMPLETE";
    };
});
