document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const taskInput = document.getElementById("task-input");
    const taskTable = document.getElementById("task-table").getElementsByTagName('tbody')[0];

    taskForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const taskName = taskInput.value;
        if (taskName) {
            const response = await fetch("/tasks", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ name: taskName })
            });
            const newTask = await response.json();
            const row = taskTable.insertRow();
            row.setAttribute("data-id", newTask._id);
            row.innerHTML = `<td>${taskName}</td><td><button class="delete-btn">Delete</button></td>`;
            row.querySelector('.delete-btn').addEventListener('click', async function() {
                await fetch(`/tasks/${newTask._id}`, {
                    method: "DELETE"
                });
                taskTable.deleteRow(row.rowIndex);
            });
            taskInput.value = "";
        }
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', async function() {
            const row = button.closest('tr');
            const taskId = row.getAttribute('data-id');
            await fetch(`/tasks/${taskId}`, {
                method: "DELETE"
            });
            row.remove();
        });
    });
});
