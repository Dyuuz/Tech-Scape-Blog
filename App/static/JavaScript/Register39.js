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
    var username = document.querySelector('input[name="username"]').value;
    var password = document.querySelector('input[name="password"]').value;
    var confirm_password = document.querySelector('input[name="confirm_password"]').value;
    var alert = document.querySelector('.blog-register-alert');
    var form = document.getElementById('registerForm');
    var formData = new FormData(form);
    var submit = document.querySelector('.blog-register-button');
    
    var passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*])[A-Za-z\d!@#$%^&*]{8,}$/;
    var usernamePattern = /^[0-9]+$/;
    var containsSymbol = /[!@#$%^&*():;'",.<>?/\\|`~+=-{}]/;
    if (password !== confirm_password) {
        alert.style.display = 'block';
        alert.textContent = 'Passwords does not match';
        event.preventDefault(); 
    } else if (!passwordPattern.test(password)) {
        alert.style.display = 'block';
        alert.textContent = 'Password must be at least 8 characters long, include both upper and lower case letters, a number, and a special character.';
        event.preventDefault();  
    } else {
        activateLoadingRegister();
        disableSubmitRegister();
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
                title: 'Verify your account',
                text: 'We sent a verification link to your mail to activate your account.',
                icon: 'success',
                showConfirmButton: true,
                confirmButtonText: 'Continue',
                confirmButtonColor: 'rgb(58, 138, 222)', // Change this to your desired color
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false
            }).then((result) => {
                activateSubmitRegister();
                disableLoadingRegister();
                if (result.isConfirmed) {
                    window.location.href = 'https://mail.google.com/mail/u/0/#inbox';
                }
            });
                
        } else if (response.data.userexists === true) {
            alert.textContent = response.data.message;
            activateSubmitRegister();
            disableLoadingRegister();

        } else if(response.data.emailexists === true) {
            alert.textContent = response.data.message;
            activateSubmitRegister();
            disableLoadingRegister();

        } else if(response.data.password === true) {
            alert.textContent = response.data.message;
            activateSubmitRegister();
            disableLoadingRegister();

        } else if(response.data.exceptionError === true) {
            alert.textContentz = response.data.message;
            activateSubmitRegister();
            disableLoadingRegister();

        } else {
            alert.textContent = response.data.message;
            activateSubmitRegister();
            disableLoadingRegister();
        }
    })
    .catch(error => {
        console.error(error);
        if (error.response) {
            Swal.fire({
                title: 'Registration Failed!',
                text: 'Request error, refresh page to sign up'+ error,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            activateSubmitRegister();
            disableLoadingRegister();
        } else if (error.request) {
        //if a request was made but no response was received
            Swal.fire({
                title: 'Registration Failed!',
                text: 'Please check your network connection.',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            activateSubmitRegister();
            disableLoadingRegister();
        } else {
        // Something happened in setting up the request that triggered an Error
            Swal.fire({
                title: 'Registration Failed!',
                text: 'An error occurred while setting up the request: ' + error.message,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            disableLoadingRegister();
            activateSubmitRegister();
        }
    });
    event.preventDefault();
}

function disableSubmitRegister(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = true;
    submit.classList.add("disabled");
}

function activateSubmitRegister(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = false;
    submit.classList.remove("disabled");
}

function activateLoadingRegister(){
    var loading = document.querySelector('.loading');
    loading.style.display = "flex";
}

function disableLoadingRegister(){
    var loading = document.querySelector('.loading');
    loading.style.display = "none";
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