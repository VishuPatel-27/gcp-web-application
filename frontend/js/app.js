const API_BASE_URL = 'http://localhost:3000';

// Handle Sign In Form Submission
const signInForm = document.getElementById('signInForm');

signInForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission

    // Get form values
    const email = document.getElementById('login_email').value;
    const password = document.getElementById('login_password').value;

    // Make a POST request to log in the user
    const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    });

    if (response.ok) {
        // Redirect to the dashboard if login is successful
        window.location.href = `${API_BASE_URL}/dashboard`;
    } else {
        const errorData = await response.json();
        alert(errorData.message || 'Login failed. Please check your credentials.');
    }
});


// Handle Sign Up Form Submission
const signUpForm = document.getElementById('signUpForm');

signUpForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent default form submission

    // Get form values
    const name = document.getElementById('reg_name').value;
    const email = document.getElementById('reg_email').value;
    const password = document.getElementById('reg_password').value;

     console.log({ name, email, password });
    // Make a POST request to register the user

    const response = await fetch(`${API_BASE_URL}/signup`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            name: name,
            email: email,
            password: password
        })
    });

    if (response.ok) {
        const data = await response.json();
        console.log('Registration successful, redirecting to dashboard...');

        // Redirect to the dashboard page if registration is successful
        window.location.href = `${API_BASE_URL}/login`;
    } else {
        const errorData = await response.json();
        alert(errorData.message || 'Sign up failed. Please try again.');
    }
});

const uploadButton = document.getElementById("upload-doc");

uploadButton.addEventListener('click', async () => {
    const file = fileInput.files[0]; // Get the selected file

    console.log("reached!")
    if (!file) {
        alert('Please select a file to upload.');
        return;
    }

    // Create form data to send to the backend
    const formData = new FormData();
    formData.append('file', file);

    // Send the file to the backend
    const response = await fetch(`${API_BASE_URL}/upload-document`, {
        method: 'POST',
        body: formData
    });

    const result = await response.json();

    if (response.ok) {
        alert(result.message);  // Alert the user on successful upload
    } else {
        alert(result.message || 'File upload failed.');
    }
});