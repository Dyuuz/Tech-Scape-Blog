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
        this.action = getResetPasswordUrl(formData);
    }
};

function getResetPasswordUrl(formData) {
    var alert =  document.querySelector('.blog-register-alert');
    alert.style.display = 'block';
    const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    const urlParts = window.location.pathname.split('/');  
    const userToken = urlParts[urlParts.length - 2];
    alert.textContent = userToken;

    
    event.preventDefault();
}
