var user = document.querySelector('input[name="username"]');
var mail = document.querySelector('input[name="email"]');
var password = document.querySelector('input[name="password"]');
var confirmpassword = document.querySelector('input[name="confirm_password"]');
var alert = document.querySelector('.blog-register-alert');

user.addEventListener('input', function() {
alert.textContent = '';
});

mail.addEventListener('input', function() {
alert.textContent = '';
});

password.addEventListener('input', function() {
alert.textContent = '';
});

confirmpassword.addEventListener('input', function() {
alert.textContent = '';
});

document.getElementById('registerForm').onsubmit = function(event) {
    var password = document.querySelector('input[name="password"]').value;
    var confirm_password = document.querySelector('input[name="confirm_password"]').value;
    var alert = document.querySelector('.blog-register-alert');
    var form = document.getElementById('registerForm');
    var formData = new FormData(form);
    
    var passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
    if (password !== confirm_password) {
        alert.style.display = 'block';
        alert.textContent = 'Passwords does not match';
        event.preventDefault(); 
    } else if (!passwordPattern.test(password)) {
        alert.style.display = 'block';
        alert.textContent = 'Password must be at least 8 characters long, include both upper and lower case letters, a number, and a special character.';
        event.preventDefault(); 
    } else {
        this.action = getRegisterUrl(formData);
    }
    //this.action = getRegisterUrl(formData);
};

function getRegisterUrl(formData) {
    var alert =  document.querySelector('.blog-register-alert');
    alert.style.display = 'block';
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    axios.post('register', formData,
    { headers: {
        'X-CSRFToken': csrf_token
    }}
    )
    .then(response => {
        if (response.data.success === true) {
            Swal.fire({
                title: 'Registration Successful!',
                text: 'You have successfully created an account.',
                icon: 'success',
                showConfirmButton: true,
                confirmButtonText: 'Proceed to Login',
                confirmButtonColor: 'rgb(58, 138, 222)' // Change this to your desired color
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = response.data.redirect_url;
                }
            });
                
        } else if (response.data.userexists === true) {
            alert.textContent = response.data.message;

        } else if(response.data.emailexists === true) {
            alert.textContent = response.data.message;

        } else if(response.data.password === true) {
            alert.textContent = response.data.message;

        } else if(response.data.exceptionError === true) {
            window.location.href = response.data.message;

        } else {
            alert.textContent = response.data.message;
        }
    })
    .catch(error => {
        console.error(error);
        if (error.response) {
            Swal.fire({
                title: 'Registration Failed!',
                text: 'Request error, refresh page to sign up',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        } else if (error.request) {
        //if a request was made but no response was received
            Swal.fire({
                title: 'Registration Failed!',
                text: 'Please check your network connection.',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        } else {
        // Something happened in setting up the request that triggered an Error
            Swal.fire({
                title: 'Registration Failed!',
                text: 'An error occurred while setting up the request: ' + error.message,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        }
    });
    event.preventDefault();
}

function submitForm() {
    var passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
    if (!passwordPattern.test(password)) {
        alert.style.display = 'block';
        alert.textContent = 'Password must be at least 8 characters long, include both upper and lower case letters, a number, and a special character.';
        
        setTimeout(function() {
        alert.style.display = 'none';
        }, 10000); 
        event.preventDefault(); 
    }
}