const editProfileBtn = document.getElementById("editProfileBtn");
const editProfileModal = document.getElementById("editProfileModal");
const closeModal = document.querySelector(".close");
const editProfileForm = document.getElementById("editProfileForm");
const profileName = document.getElementById("profileName");
const profileEmail = document.getElementById("profileEmail");
const profileBio = document.getElementById("profileBio");
const likesTab = document.getElementById("likesTab");
const bookmarksTab = document.getElementById("bookmarksTab");
const likesSection = document.getElementById("likesSection");
const bookmarksSection = document.getElementById("bookmarksSection");
const alertmsg =  document.querySelector('.blog-register-alert');
const username = document.querySelector('input[name="username"]');
const email = document.querySelector('input[name="email"]');

// Edit Profile Modal
editProfileBtn.addEventListener("click", () => {
  editProfileModal.style.display = "flex";
});

closeModal.addEventListener("click", () => {
  editProfileModal.style.display = "none";
  alertmsg.textContent = '';
});

username.addEventListener('input', function() {
  alertmsg.textContent = '';
});

email.addEventListener('input', function() {
  alertmsg.textContent = '';
});


document.getElementById('editProfileForm').onsubmit = function(event) {
  var username = document.querySelector('input[name="username"]').value;
  var email = document.querySelector('input[name="email"]').value;
  var alertmsg =  document.querySelector('.blog-register-alert');
  const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  var form = document.getElementById('editProfileForm');
  var formData = new FormData(form);
  activateLoadingPassReset();
  disablesubmitPassword();

  axios.post('update-profile', formData, {
    headers : {
      'X-CSRFToken': csrf_token,
    }
  }).then((response) => {
    if (response.data.success === true) {
      editProfileModal.style.display = "none";
      Swal.fire({
        title: '',
        text: response.data.message,
        icon: 'success',
        showConfirmButton: true,
        confirmButtonText: 'Continue',
        confirmButtonColor: 'rgb(58, 138, 222)', 
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false
      }).then((result) => {
          if (result.isConfirmed) {
              window.location.reload();
          }
      });
    } else {
        
        setTimeout(() => {
          alertmsg.textContent = response.data.message;
          disableLoadingPassReset();
          activatesubmitPassword();
        }, 1000);
        
    }
  }).catch((error) => {
    let errorMessage = 'Request error';
    if (error.response) {
        errorMessage = `Request error, please refresh and try again.`;
    } else if (error.request) {
        errorMessage = 'Please check your network connection.';
    }
    alertmsg.textContent = errorMessage + error.message;
    disableLoadingPassReset();
    activatesubmitPassword();
  });
  event.preventDefault(); 
};

// Tabs functionality
likesTab.addEventListener("click", () => {
  likesSection.classList.add("active");
  bookmarksSection.classList.remove("active");
  likesTab.classList.add("active");
  bookmarksTab.classList.remove("active");
});

bookmarksTab.addEventListener("click", () => {
  bookmarksSection.classList.add("active");
  likesSection.classList.remove("active");
  bookmarksTab.classList.add("active");
  likesTab.classList.remove("active");
});

function disablesubmitPassword(){
  var submit = document.querySelector('.prof-btn-save');
  submit.disabled = true;
  submit.classList.add("disabled");
}

function activatesubmitPassword(){
  var submit = document.querySelector('.prof-btn-save');
  submit.disabled = false;
  submit.classList.remove("disabled");
}

function activateLoadingPassReset(){
  var loading = document.querySelector('.roll');
  loading.style.display = "flex";
}

function disableLoadingPassReset(){
  var loading = document.querySelector('.roll');
  loading.style.display = "none";
}