var mail = document.querySelector('input[name="email"]');
var alert = document.querySelector('.blog-register-alert');

mail.addEventListener('input', function() {
    alert.textContent = '';
    });

document.querySelector('#loginForm').onsubmit = function(event) {  
    event.preventDefault();        
    var form = document.getElementById('loginForm');
    var formData = new FormData(form);
    disablesubmitReset();
    activateLoadingResetLink();
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
                disableLoadingResetLink();
                activatesubmitReset();
                if (result.isConfirmed) {
                    window.location.reload();
                }
            });
        } else {
            alert.textContent = response.data.message;
            disableLoadingResetLink();
            activatesubmitReset();
            
        }
    }).catch((error) => {
        if (error.response) {
            Swal.fire({
                title: 'Reset Link Failed!',
                text: `Request error, please refresh the page and try again.`,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            disableLoadingResetLink();
            activatesubmitReset();
            
        } else if (error.request) {
        //if a request was made but no response was received
            Swal.fire({
                title: 'Reset Link Failed!',
                text: 'Please check your network connection.',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            disableLoadingResetLink();
            activatesubmitReset();
            
        } else {
        // Something happened in setting up the request that triggered an Error
            Swal.fire({
                title: 'Reset Link Failed!',
                text: 'Mail service down. Fix in progress.',
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
            disableLoadingResetLink();
            activatesubmitReset();
        }
    });
    event.preventDefault();
}

function disablesubmitReset(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = true;
    submit.classList.add("disabled");
}

function activatesubmitReset(){
    var submit = document.querySelector('.blog-register-button');
    submit.disabled = false;
    submit.classList.remove("disabled");
}

function activateLoadingResetLink(){
    var loading = document.querySelector('.loading');
    loading.style.display = "flex";
}

function disableLoadingResetLink(){
    var loading = document.querySelector('.loading');
    loading.style.display = "none";
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