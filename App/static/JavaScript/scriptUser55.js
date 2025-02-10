function Subscribe() {
    const emailInput = document.querySelector('input[name="email_address"]');
    const emailValue = emailInput.value;
    if (!emailValue) {
        emailInput.placeholder = "Email is required";
    } else {
        axiosSubsribe(emailValue);
    }
}

function SubscribeFooter() {
    const emailInput = document.querySelector('input[name="email_address2"]');
    const emailValue = emailInput.value;
    if (!emailValue) {
        emailInput.placeholder = "Email is required";
    } else {
        axiosSubsribe(emailValue);
    }
}

function axiosSubsribe(emailValue) {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const emailInput = document.querySelector('input[name="email_address"]');
    axios.post('/update-subscribe/', 
        {
            emailVal: emailValue,
        }, 
        { 
            headers: {
                'X-CSRFToken': csrf_token
            }
        }
    )
    .then(response => {
        if (response.data.success === true) {
            Swal.fire({
                title: 'Success',
                text: 'You have successfully subscribed to our newsletter', 
                icon: 'success', 
                iconHtml: '<img src="/static/Images/sub5.png" class="custom-swal" >',
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
            // alert(response.data.success);
            Swal.fire({
                title: 'Error',
                text: response.data.message,
                icon: 'error',
                timer: 4000,
                showConfirmButton: false
            });
        }
    })
    .catch(error => {
        console.error('Error:', error.response.data);
    });
}

function suboptions(suboption){
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    axios.post('/subscribe-option/',
        {
            suboption: suboption,
        },{
            headers: {
                'X-CSRFToken': csrf_token
            }
        })
    .then(response => {
        if (response.data.subscribe === true) {
            Swal.fire({
                title: 'Success',
                text: 'You have successfully subscribed to our newsletter',  
                iconHtml: '<img src="/static/Images/sub5.png" class="custom-swal">',
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
            Swal.fire({
                title: 'Success',
                text: 'You have successfully unsubscribed from our newsletter', 
                iconHtml: '<img src="/static/Images/unsubscribe.png" class="custom-swal">',
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
        }
    })
    .catch(error => {
        console.error('Error:', error.response.data);
    });      
}

function toggleLike(postID) {
    let isLiked = false;
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const likeElement = document.querySelector(`.post-likes[data-id='${postID}']`);
    const authStatus = likeElement.dataset.isAuthenticated;
    const likeBoolean = likeElement.getAttribute("likedBoolean");
    const likeCountElement = likeElement.querySelector('#like-count');

    if (authStatus === "true") {
      isLiked = likeBoolean === 'false';
      likeElement.classList.toggle('active', isLiked);
      likeCountElement.textContent = isLiked ? parseInt(likeCountElement.textContent) + 1 : parseInt(likeCountElement.textContent) - 1;
      likeElement.setAttribute("likedBoolean", isLiked.toString());
      
        if (isLiked === true) {
            buttonBoolean = "true";
            postID = parseInt(postID);
            axios.post('/update-like/', 
                {
                    post_id: postID,
                buttonBoolean: buttonBoolean,
                }, { headers: {
                        'X-CSRFToken': csrf_token
                    }
                })
            .then(response => {
            console.log(response.data);
            })
            .catch(error => {
                console.error('Error:', error.response.data);
            });
        } else{
                buttonBoolean = "false";
                postID = parseInt(postID);
                axios.post('/update-like/', 
                    {
                    post_id: postID,
                    buttonBoolean: buttonBoolean,
                    }, { headers: {
                            'X-CSRFToken': csrf_token
                        }
                    })
                .then(response => {
                    console.log(response.data);
                })
                .catch(error => {
                    console.error('Error:', error.response.data);
                });
        }
  
    } else {
        redirectUser();
    }  
}

function toggleLikePost() {
    const likeButton = document.querySelector('.post-likes');
    const likeCount = document.getElementById('like-count');
    const authStatus = likeButton.dataset.isAuthenticated;

    if (authStatus === "true") {
        isLiked = !isLiked;
        likeButton.classList.toggle('active', isLiked);
        likeCount.textContent = isLiked ? parseInt(likeCount.textContent) + 1 : parseInt(likeCount.textContent) - 1;

        if (isLiked === true) {
            buttonBoolean = "true";
            updateLike(buttonBoolean);
        } else{
            buttonBoolean = "false";
            updateLike(buttonBoolean);
        }
    
    } else {
        redirectUrl();
    }
}

function toggleBookmarkPost() {
    const bookmarkButton = document.querySelector('.post-bookmark');
    const authStatus = bookmarkButton.dataset.isAuthenticated;
    if (authStatus === "true") {
        isBookmarked = !isBookmarked;
        bookmarkButton.classList.toggle('active', isBookmarked);
        if (isBookmarked === true) {
            buttonBoolean = "true";
            updateBookmark(buttonBoolean);
        } else{
            buttonBoolean = "false";
            updateBookmark(buttonBoolean);
        }
    
    } else {
        redirectUrl();
    }
    
}

function updateLike(buttonBoolean) {
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/update-like/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token  
        },
        body: JSON.stringify({ post_id: window.userData.post_id , buttonBoolean : buttonBoolean })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.message); 
        } else {
            console.log('Error: ' + data.message);
        }
    })
    .catch(error => console.log('Error:', error));
}

function updateBookmark(buttonBoolean){
    const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    fetch('/update-bookmark/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token  
        },
        body: JSON.stringify({ post_id: window.userData.post_id , buttonBoolean : buttonBoolean })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.message); 
        } else {
            console.log('Error: ' + data.message);
        }
    })
    .catch(error => console.log('Error:', error));
}
