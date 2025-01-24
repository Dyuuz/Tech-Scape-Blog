function Subscribe() {
    const user = window.userData.username;
    const emailInput = document.querySelector('input[name="email_address"]');
    const emailValue = emailInput.value;
    alert(emailValue);
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
        const redirectUrl = "{% url 'login' %}";
        window.location.href = redirectUrl;
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
        const redirectUrl = "{% url 'loginsession' name=blog.category.name slug=blog.slug %}";
        window.location.href = redirectUrl;
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
        const redirectUrl = "{% url 'loginsession' name=blog.category.name slug=blog.slug %}";
        window.location.href = redirectUrl;
        
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
