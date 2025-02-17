var password = document.querySelector('input[name="password"]');
var confirmpassword = document.querySelector('input[name="confirm_password"]');
var alert = document.querySelector('.blog-register-alert');

password.addEventListener('input', function() {
    alert.textContent = '';
});

confirmpassword.addEventListener('input', function() {
    alert.textContent = '';
});

document.getElementById('registerForm1').onsubmit = function(event) {
    var password = document.querySelector('input[name="password"]').value;
    var confirm_password = document.querySelector('input[name="confirm_password"]').value;
    var alert = document.querySelector('.blog-register-alert');
    var form = document.getElementById('registerForm1');
    var submit = document.querySelector('.blog-register-button');
    alert.textContent = '';
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
        activateLoadingPassReset();
        disablesubmitPassword();
        this.action = getResetPasswordUrl(formData);
        event.preventDefault();
    }
};

function getResetPasswordUrl(formData) {
    var alertmsg =  document.querySelector('.blog-register-alert');
    alertmsg.style.display = 'block';
    var submit = document.querySelector('.blog-register-button');
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const urlParts = window.location.pathname.split('/');  
    const userToken = urlParts[urlParts.length - 2];
    
    axios.post(`/reset-password/${userToken}/`, formData, {
        headers: {
            'X-CSRFToken': csrf_token,
        }
    }).then((response) => {
        if (response.data.success === true) {
            Swal.fire({
                title: response.data.message,
                text: 'You can now log in with your new password',
                icon: 'success',
                showConfirmButton: true,
                confirmButtonText: 'Continue',
                confirmButtonColor: 'rgb(58, 138, 222)', 
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = response.data.redirect_url;  // Redirect user to login page
                }
            });
        } else {
            alertmsg.textContent = response.data.message;
            disableLoadingPassReset();
            activatesubmitPassword();
        }
    }).catch((error) => {
        let errorMessage = 'An error occurred. Please try again.';
        if (error.response) {
            errorMessage = `Request error, please refresh and try again.`;
        } else if (error.request) {
            errorMessage = 'Please check your network connection.';
        }
    
        Swal.fire({
            title: 'Reset Link Failed!',
            text: errorMessage,
            icon: 'error',
            timer: 4000,
            showConfirmButton: false
        });
        disableLoadingPassReset();
        activatesubmitPassword();
    });

    
    event.preventDefault();
}

function disablesubmitPassword(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = true;
    submit.classList.add("disabled");
}

function activatesubmitPassword(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = false;
    submit.classList.remove("disabled");
}

function activateLoadingPassReset(){
    var loading = document.querySelector('.loading');
    loading.style.display = "flex";
}

function disableLoadingPassReset(){
    var loading = document.querySelector('.loading');
    loading.style.display = "none";
}