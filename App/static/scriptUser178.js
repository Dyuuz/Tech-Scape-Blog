function Subscribe() {
    const emailInput = document.querySelector('input[name="email_address"]');
    const emailValue = emailInput.value;
    if (!emailValue) {
        emailInput.placeholder = "Email is required";
    } else {
        axiosSubsribe(emailValue);
    }
}

const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

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
            const dialogBox = document.createElement('div');
            dialogBox.style.position = 'fixed';
            dialogBox.style.top = '50%';
            dialogBox.style.left = '50%';
            dialogBox.style.transform = 'translate(-50%, -50%)';
            dialogBox.style.backgroundColor = '#333';
            dialogBox.style.color = '#fff';
            dialogBox.style.padding = '20px';
            dialogBox.style.borderRadius = '8px';
            dialogBox.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.1)';
            dialogBox.style.zIndex = '1000';
            
            const message = document.createElement('p');
            message.textContent = response.data.message;
            dialogBox.appendChild(message);
            
            const okButton = document.createElement('button');
            okButton.textContent = 'Proceed';
            okButton.style.marginTop = '10px';
            okButton.style.padding = '5px 10px';
            okButton.style.border = 'none';
            okButton.style.borderRadius = '4px';
            okButton.style.backgroundColor = '#007bff';
            okButton.style.color = '#fff';
            okButton.style.cursor = 'pointer';
            okButton.addEventListener('click', () => {
                dialogBox.remove();
                window.location.reload();
            });
            dialogBox.appendChild(okButton);
            
            document.body.appendChild(dialogBox);
            // setTimeout(() => {
            //     suggestionBox.remove();
                
            //     // Delay the page reload by 5 more seconds after removal
            //     setTimeout(() => {
            //         window.location.reload();
            //     }, 1000);  // 5 seconds delay before reload
        
            // }, 7000);  // Suggestion box stays for 7 seconds

        } else {
            // alert(response.data.success);
            const suggestionBox = document.createElement('div');
            suggestionBox.textContent = response.data.message;
            suggestionBox.style.position = 'absolute';
            suggestionBox.style.backgroundColor = 'rgba(219, 105, 105, 0.96)';
            suggestionBox.style.color = '#fff';
            suggestionBox.style.fontSize = '14px';
            suggestionBox.style.padding = '10px 20px';
            suggestionBox.style.borderRadius = '8px';
            suggestionBox.style.boxShadow = '0 4px 8px rgba(238, 254, 249, 0.1)';
            suggestionBox.style.marginTop = '55px';
            suggestionBox.style.marginRight = '50px';
            suggestionBox.style.transition = 'opacity 0.3s ease';
            suggestionBox.style.opacity = '0.9';
            // suggestionBox.style.zIndex = '1000';
            emailInput.insertAdjacentElement('afterend', suggestionBox);
            setTimeout(() => {
                suggestionBox.remove();
            }, 2000);
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
