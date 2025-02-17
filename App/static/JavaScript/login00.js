var user = document.querySelector('input[name="username"]');
var password = document.querySelector('input[name="password"]');
var alert = document.querySelector('.blog-register-alert');

user.addEventListener('input', function() {
    alert.textContent = '';
});

password.addEventListener('input', function() {
    alert.textContent = '';
});

document.getElementById('loginForm').onsubmit = function(event) {
    var password = document.getElementById('password').value;
    var alert = document.querySelector('.blog-register-alert');
    var form = document.getElementById('loginForm');
    var formData = new FormData(form);
    alert.textContent = '';
    disablesubmitLogin();
    activateLoadingLogin();
    this.action = getLoginUrl(formData);
};

function getLoginUrl(formData) {
    var alert =  document.querySelector('.blog-register-alert');
    alert.style.display = 'block';
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    axios.post('login', formData,
    { headers: {
      'X-CSRFToken': csrf_token
    }}
    )
    .then(response => {
        if (response.data.success === true) {
            Swal.fire({
            title: 'Login Successful',
            text: 'Redirecting to homepage...',
            icon: 'success',
            timer: 4000,
            showConfirmButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false
            });
            setTimeout(function() {
            window.location.href = response.data.redirect_url;
            }, 4000);
            disableLoadingLogin();
            activatesubmitLogin();
            
            //window.location.href = response.data.redirect_url;
            
        } else if (response.data.successpostpage === true) {
            Swal.fire({
            title: 'Login Successful',
            text: 'Redirecting to previous page...',
            icon: 'success',
            timer: 4000,
            showConfirmButton: false,
            allowOutsideClick: false,
            allowEscapeKey: false,
            allowEnterKey: false
            });
            setTimeout(function() {
            window.location.href = response.data.redirect_url;
            }, 4000);
            disableLoadingLogin();
            activatesubmitLogin();
            
            //window.location.href = response.data.redirect_url;
            
        } else if (response.data.exceptionError === true) {
            alert.textContent = response.data.message;
            disableLoadingLogin();
            activatesubmitLogin();

        } else if(response.data.userError === true) {
            alert.textContent = response.data.message;
            disableLoadingLogin();
            activatesubmitLogin();

        } else if(response.data.passworderror === true) {
            alert.textContent = response.data.message;
            disableLoadingLogin();
            activatesubmitLogin();  
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (error.response) {
            Swal.fire({
            title: 'Login Failed!',
            text: 'Request error, refresh page to login',
            icon: 'error',
            timer: 4000,
            showConfirmButton: false
            });
            disableLoadingLogin();
            activatesubmitLogin();

        } else if (error.request) {
            //if a request was made but no response was received
            Swal.fire({
            title: 'Login Failed!',
            text: 'Please check your network connection.',
            icon: 'error',
            timer: 4000,
            showConfirmButton: false
            });
            disableLoadingLogin();
            activatesubmitLogin();
        } else {
            // Something happened in setting up the request that triggered an Error
            Swal.fire({
            title: 'Login Failed!',
            text: 'An error occurred while setting up the request: ' + error.message,
            icon: 'error',
            timer: 4000,
            showConfirmButton: false
            });
            disableLoadingLogin();
            activatesubmitLogin();
        }
    });
    event.preventDefault();
}

function disablesubmitLogin(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = true;
    submit.classList.add("disabled");
}

function activatesubmitLogin(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = false;
    submit.classList.remove("disabled");
}

function activateLoadingLogin(){
    var loading = document.querySelector('.loading');
    loading.style.display = "flex";
}

function disableLoadingLogin(){
    var loading = document.querySelector('.loading');
    loading.style.display = "none";
}

