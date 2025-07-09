const signupForm = document.getElementById('signupForm');
const messageDiv = document.getElementById('message');
const API_BASE_URL = 'http://127.0.0.1:5000';

signupForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    messageDiv.textContent = '';
    messageDiv.classList.add('hidden');

    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = data.message;
            messageDiv.classList.remove('hidden', 'message-box-error');
            messageDiv.classList.add('message-box-success');
            signupForm.reset();
            setTimeout(() => { window.location.href = `${API_BASE_URL}/login_page`; }, 2000);
            return
        } else {
            messageDiv.textContent = data.message;
            messageDiv.classList.remove('hidden','message-box-success');
            messageDiv.classList.add('message-box-error');
        }
    } catch (error) {
        messageDiv.textContent = `Network error: ${error.message}`;
        messageDiv.classList.remove('hidden', 'message-box-success');
        messageDiv.classList.add('message-box-error');
        console.error('Fetch error:', error);
    }
});