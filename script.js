document.addEventListener("DOMContentLoaded", () => {
    // Login
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        loginForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            const res = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username, password })
            });

            if (res.ok) {
                window.location.href = "dashboard.html";
            } else {
                alert("Invalid credentials");
            }
        });
    }

    // Add application
    const addButton = document.getElementById("addButton");
    if (addButton) {
        addButton.addEventListener("click", async () => {
            const name = document.querySelector("[name='name']").value;
            const applicationDate = document.getElementById("application-date").value;
            const position = document.querySelector("[name='position']").value;
            const upcomingDeadlines = document.getElementById("upcoming-deadlines").value;

            const res = await fetch("http://127.0.0.1:5000/add_application", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, applicationDate, position, upcomingDeadlines })
            });

            if (res.ok) {
                alert("Application added!");
                window.location.href = "current-application.html";
            } else {
                alert("Failed to add application");
            }
        });
    }

    // Display current applications
    const appList = document.getElementById("applicationList");
    if (appList) {
        fetch("http://127.0.0.1:5000/applications")
            .then(res => res.json())
            .then(applications => {
                applications.forEach(app => {
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${app.name}</td>
                        <td>${app.date}</td>
                        <td>${app.position}</td>
                        <td>${app.deadline}</td>
                    `;
                    appList.appendChild(row);
                });
            });
    }
});
