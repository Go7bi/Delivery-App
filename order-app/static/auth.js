
function updateUserInfo() {
    const userNameElement = document.getElementById('userName');
    const userIdElement = document.getElementById('userId');
    const registerLink = document.getElementById('registerLink');
    const loginLink = document.getElementById('loginLink');
    const logoutLink = document.getElementById('logoutLink');


    const userToken = localStorage.getItem('token');

    if (userToken) {
        
        const userName = localStorage.getItem('userName') || "Welcome Back!";
        const userId = localStorage.getItem('userId') || "Unknown ID"; 

        userNameElement.textContent = `Hello, ${userName}`;
        userIdElement.textContent = `User ID: ${userId}`; 
        registerLink.style.display = 'none';
        loginLink.style.display = 'none';
        logoutLink.style.display = 'inline-block';
    } else {
       
        userNameElement.textContent = '';
        userIdElement.textContent = ''; 
        registerLink.style.display = 'inline-block';
        loginLink.style.display = 'inline-block';
        logoutLink.style.display = 'none';
    }
}

function logout() {
    
    localStorage.removeItem('token');
    localStorage.removeItem('userName');
    localStorage.removeItem('userId'); 

    updateUserInfo();

    window.location.href = 'add_to_cart.html';
}


updateUserInfo();
