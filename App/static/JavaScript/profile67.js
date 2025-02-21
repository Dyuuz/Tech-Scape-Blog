// script.js
document.addEventListener("DOMContentLoaded", function () {
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
  
    // Edit Profile Modal
    editProfileBtn.addEventListener("click", () => {
      editProfileModal.style.display = "flex";
    });
  
    closeModal.addEventListener("click", () => {
      editProfileModal.style.display = "none";
    });
  
    // editProfileForm.addEventListener("submit", (e) => {
    //   e.preventDefault();
    //   profileName.textContent = document.getElementById("name").value;
    //   profileEmail.textContent = document.getElementById("email").value;
    //   profileBio.textContent = document.getElementById("bio").value;
    //   editProfileModal.style.display = "none";
    // });
  
    document.getElementById('editProfileForm').onsubmit = function(event) {
      var username = document.querySelector('input[name="username"]').value;
      var email = document.querySelector('input[name="email"]').value;
      var alertmsg =  document.querySelector('.blog-register-alert');
      const csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
      var form = document.getElementById('editProfileForm');
      var formData = new FormData(form);

      if (username){
        alert("hola");
      }

      // axios.post('update-profile', formData, {
      //   headers : {
      //     'X-CSRFToken': csrf_token,
      //   }
      // }).then((response) => {
      //   if (response.data.success === true) {
      //     Swal.fire({
      //       title: response.data.message,
      //       text: 'You can now log in with your new password',
      //       icon: 'success',
      //       showConfirmButton: true,
      //       confirmButtonText: 'Continue',
      //       confirmButtonColor: 'rgb(58, 138, 222)', 
      //       allowOutsideClick: false,
      //       allowEscapeKey: false,
      //       allowEnterKey: false
      //     }).then((result) => {
      //         if (result.isConfirmed) {
      //             window.location.reload();
      //         }
      //     });
      //   } else {
      //       alertmsg.textContent = response.data.message;
      //   }
      // }).catch((error) => {
      //   let errorMessage = 'Mail service down. Fix in progress.';
      //   if (error.response) {
      //       errorMessage = `Request error, please refresh and try again.`;
      //   } else if (error.request) {
      //       errorMessage = 'Please check your network connection.';
      //   }
      //   alertmsg.textContent = errorMessage;
      // });
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
});