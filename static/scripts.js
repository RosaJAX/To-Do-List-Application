document.addEventListener("DOMContentLoaded", () => {
    const taskForm = document.getElementById("task-form");
    const taskInput = document.getElementById("task-input");
    const taskList = document.getElementById("task-list");

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
            const li = document.createElement("li");
            li.setAttribute("data-id", newTask._id);
            li.innerHTML = `${taskName} <button class="delete-btn">Delete</button>`;
            taskList.appendChild(li);
            taskInput.value = "";
        }
    });

    taskList.addEventListener("click", async (e) => {
        if (e.target.classList.contains("delete-btn")) {
            const li = e.target.closest("li");
            const taskId = li.getAttribute("data-id");
            await fetch(`/tasks/${taskId}`, {
                method: "DELETE"
            });
            li.remove();
        }
    });
});
