var mail = document.querySelector('input[name="email"]');
var alert = document.querySelector('.blog-register-alert');

mail.addEventListener('input', function() {
    alert.textContent = '';
    });

document.getElementById('loginForm').onsubmit = function(event) {         
    var form = document.getElementById('loginForm');
    var formData = new FormData(form);
    Swal.fire({
        title: 'Processing Reset Link...',
        text: 'Please wait...',
        icon: 'info',
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
        showConfirmButton: false,
        onBeforeOpen: () => {
            Swal.showLoading();
        }
    });
    this.action = getMailResetUrl(formData);
};

function getMailResetUrl(formData) {
    var alert =  document.querySelector('.blog-register-alert');
    alert.style.display = 'block';
    var mail = document.querySelector('input[name="email"]');
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    axios.post('reset-link', formData, {    
        headers: {
            'X-CSRFToken': csrf_token,
        }
    }).then((response) => {
        if (response.data.success === true) {
            Swal.fire({
                title: 'Reset Link Sent!',
                text: 'Please check your email for the reset link.',
                icon: 'success',
                showConfirmButton: true,
                confirmButtonText: 'Continue',
                confirmButtonColor: 'rgb(58, 138, 222)', // Change this to your desired color
                allowOutsideClick: false,
                allowEscapeKey: false,
                allowEnterKey: false
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });
        } else {
            alert.textContent = response.data.message;
        }
    }).catch((error) => {
        if (error.response) {
            Swal.fire({
                title: 'Reset Link Failed!',
                text: `Request error, please refresh the page and try again. Error: ${error.message}`,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        } else if (error.request) {
        //if a request was made but no response was received
            Swal.fire({
                title: 'Reset Link Failed!',
                text: 'Please check your network connection.',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        } else {
        // Something happened in setting up the request that triggered an Error
            Swal.fire({
                title: 'Reset Link Failed!',
                text: 'An error occurred while setting up the request: ' + error.message,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        }
    });
    event.preventDefault();
}

function countdown() {
    let timer = 60;
    const texttimer = document.querySelector('.timer');
    texttimer.textContent = `Time remaining: ${timer} seconds`;
    const countdown = setInterval(() => {
        timer--;
        texttimer.innerText = `Time remaining: ${timer} seconds`;
        if (timer <= 0) {
            clearInterval(countdown);
            texttimer.innerText = 'Time is up!';
        }
    } , 1000);
}