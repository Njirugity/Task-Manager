const API_BASE_URL = 'http://127.0.0.1:5000';
const taskList = document.getElementById('taskList');
const messageDiv = document.getElementById('message');
const addTaskButton = document.getElementById('addTaskButton');
const addTaskFormContainer = document.getElementById('addTaskFormContainer');
const newTaskForm = document.getElementById('newTaskForm');
const cancelAddTaskButton = document.getElementById('cancelAddTask');
const logoutButton = document.getElementById('logoutButton');


let jwtToken = localStorage.getItem('jwt_token'); 

if (!jwtToken) {
    alert('You are not logged in. Redirecting to login page.');
    window.location.href = `${API_BASE_URL}/login_page`; 
}

function displayMessage(text, type = 'success') {
    messageDiv.textContent = text;
    messageDiv.classList.remove('hidden', 'message-box-success', 'message-box-error');
    if (type === 'success') {
        messageDiv.classList.add('message-box-success');
    } else {
        messageDiv.classList.add('message-box-error');
    }
    messageDiv.classList.remove('hidden');
}

async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${jwtToken}`
            }
        });

        if (response.status === 401) {
            displayMessage('Session expired or unauthorized. Please log in again.', 'error');
            localStorage.removeItem('jwt_token');
            setTimeout(() => { window.location.href = `${API_BASE_URL}/login_page`; }, 2000);
            return;
        }

        const data = await response.json();

        if (response.ok) {
            renderTasks(data);
        } else {
            displayMessage(data.message);
            renderTasks([]);
        }
    } catch (error) {
        displayMessage(`Network error: ${error.message}`);
        console.error('Fetch tasks error:', error);
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = '';

    if (tasks.length === 0) {
        taskList.innerHTML = '<li class="task-list-placeholder">No tasks yet. Add one!</li>';
        return;
    }

    tasks.forEach(task => {
        const listItem = document.createElement('li');
        listItem.className = 'task-list-item';
        if (task.completed) {
            listItem.classList.add('task-completed');
        }
        listItem.setAttribute('data-task-id', task.id);

        listItem.innerHTML = `
            <div class="task-content-wrapper">
                <input type="checkbox" class="task-checkbox" ${task.completed ? 'checked' : ''}>
                <div class="task-text-container">
                    <span class="task-title">${task.title}</span>
                    ${task.description ? `<span class="task-description">${task.description}</span>` : ''}
                </div>
            </div>
            <button class="delete-task-btn">
                Delete
            </button>
        `;
        taskList.appendChild(listItem);
    });
    addEventListenersToTasks();
}

function addEventListenersToTasks() {
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', async (event) => {
            const taskId = event.target.closest('li').getAttribute('data-task-id');
            const completed = event.target.checked;
            await updateTaskStatus(taskId, completed);
        });
    });

    document.querySelectorAll('.delete-task-btn').forEach(button => {
        button.addEventListener('click', async (event) => {
            const taskId = event.target.closest('li').getAttribute('data-task-id');
            await deleteTask(taskId);
        });
    });
}

async function updateTaskStatus(taskId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${jwtToken}`
            },
            body: JSON.stringify({ completed: completed })
        });

        if (response.ok) {
            displayMessage('Task updated successfully!', 'success');
            fetchTasks();
        } else {
            const data = await response.json();
            displayMessage(data.message);
        }
    } catch (error) {
        displayMessage(`Network error: ${error.message}`);
        console.error('Update task error:', error);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) {
        return;
    }
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${jwtToken}`
            }
        });

        if (response.status === 204) {
            displayMessage('Task deleted successfully!', 'success');
            fetchTasks();
        } else {
            const data = await response.json();
            displayMessage(data.message || 'Failed to delete task.');
        }
    } catch (error) {
        displayMessage(`Network error: ${error.message}`);
        console.error('Delete task error:', error);
    }
}

newTaskForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const title = document.getElementById('newTaskTitle').value;
    const description = document.getElementById('newTaskDescription').value;

    if (!title) {
        displayMessage('Task title cannot be empty.', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${jwtToken}`
            },
            body: JSON.stringify({ title, description })
        });

        const data = await response.json();
        if (response.ok) {
            displayMessage(data.message);
            newTaskForm.reset();
            addTaskFormContainer.style.display = 'none';
            addTaskButton.style.display = 'block';
            fetchTasks();
        } else {
            displayMessage(data.message);
        }
    } catch (error) {
        displayMessage(`Network error: ${error.message}`);
        console.error('Add task error:', error);
    }
});

addTaskButton.addEventListener('click', () => {
    addTaskFormContainer.style.display = 'block';
    addTaskButton.style.display = 'none';
});

cancelAddTaskButton.addEventListener('click', () => {
    addTaskFormContainer.style.display = 'none';
    addTaskButton.style.display = 'block';
    newTaskForm.reset();
});


logoutButton.addEventListener('click', () => {
    localStorage.removeItem('jwt_token');
    alert('Logged out successfully!');
    window.location.href = `${API_BASE_URL}/login_page`;
});

document.addEventListener('DOMContentLoaded', fetchTasks);