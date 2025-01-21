// This function will check if the user is logged in by checking the token in localStorage
function updateUserInfo() {
    const userNameElement = document.getElementById('userName');
    const registerLink = document.getElementById('registerLink');
    const loginLink = document.getElementById('loginLink');
    const logoutLink = document.getElementById('logoutLink');

    // Check if user is logged in
    const userToken = localStorage.getItem('token');

    if (userToken) {
        // If the user is logged in, show their username
        const userName = localStorage.getItem('userName') || "User";
        userNameElement.textContent = `Hello, ${userName}`;
        registerLink.style.display = 'none';
        loginLink.style.display = 'none';
        logoutLink.style.display = 'inline-block';
    } else {
        // If the user is not logged in, show the register and login links
        userNameElement.textContent = '';
        registerLink.style.display = 'inline-block';
        loginLink.style.display = 'inline-block';
        logoutLink.style.display = 'none';
    }
}

// Logout function to remove user data from localStorage and redirect
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userName');
    window.location.href = 'login.html'; // Redirect to login page
}

// Call this function when the page loads
updateUserInfo();
