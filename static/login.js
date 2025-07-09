const loginForm = document.getElementById('loginForm');
const messageDiv = document.getElementById('message');
const tokenDisplayDiv = document.getElementById('tokenDisplay');
const jwtTokenSpan = document.getElementById('jwtToken');
const API_BASE_URL = 'http://127.0.0.1:5000';

loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    messageDiv.textContent = '';
    messageDiv.classList.add('hidden');
    tokenDisplayDiv.classList.add('hidden');

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            messageDiv.textContent = data.message;
            messageDiv.classList.remove('hidden', 'message-box-error');
            messageDiv.classList.add('message-box-success');
            
            if (data.token) {
                localStorage.setItem('jwt_token', data.token); 
                jwtTokenSpan.textContent = data.token;
                tokenDisplayDiv.classList.remove('hidden');
                setTimeout(() => { window.location.href = `${API_BASE_URL}/home`; }, 2000);
                return
            }
        } else {
            messageDiv.textContent = data.message;
            messageDiv.classList.remove('hidden','message-box-success');
            messageDiv.classList.add( 'message-box-error');
        }
    } catch (error) {
        
        console.error("Network error during login:", error)
        messageDiv.textContent = `Network error: ${error.message}`;
        messageDiv.classList.remove('hidden', 'message-box-success');
        messageDiv.classList.add('message-box-error');
        console.error('Fetch error:', error);
    }
});