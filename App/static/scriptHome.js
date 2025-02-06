'use strict';



/**
 * Add event listener on multiple elements
 */

const addEventOnElements = function (elements, eventType, callback) {
  for (let i = 0, len = elements.length; i < len; i++) {
    elements[i].addEventListener(eventType, callback);
  }
}



/**
 * MOBILE NAVBAR TOGGLER
 */

const navbar = document.querySelector("[data-navbar]");
const navTogglers = document.querySelectorAll("[data-nav-toggler]");

const toggleNav = () => {
  navbar.classList.toggle("active");
  document.body.classList.toggle("nav-active");
}

addEventOnElements(navTogglers, "click", toggleNav);



/**
 * HEADER ANIMATION
 * When scrolled donw to 100px header will be active
 */

const header = document.querySelector("[data-header]");
const backTopBtn = document.querySelector("[data-back-top-btn]");

window.addEventListener("scroll", () => {
  if (window.scrollY > 100) {
    header.classList.add("active");
    backTopBtn.classList.add("active");
  } else {
    header.classList.remove("active");
    backTopBtn.classList.remove("active");
  }
});



/**
 * SLIDER
 */

const slider = document.querySelector("[data-slider]");
const sliderContainer = document.querySelector("[data-slider-container]");
const sliderPrevBtn = document.querySelector("[data-slider-prev]");
const sliderNextBtn = document.querySelector("[data-slider-next]");

let totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
let totalSlidableItems = sliderContainer.childElementCount - totalSliderVisibleItems;

let currentSlidePos = 0;

const moveSliderItem = function () {
  sliderContainer.style.transform = `translateX(-${sliderContainer.children[currentSlidePos].offsetLeft}px)`;
}

/**
 * NEXT SLIDE
 */

const slideNext = function () {
  const slideEnd = currentSlidePos >= totalSlidableItems;

  if (slideEnd) {
    currentSlidePos = 0;
  } else {
    currentSlidePos++;
  }

  moveSliderItem();
}

sliderNextBtn.addEventListener("click", slideNext);

/**
 * PREVIOUS SLIDE
 */

const slidePrev = function () {
  if (currentSlidePos <= 0) {
    currentSlidePos = totalSlidableItems;
  } else {
    currentSlidePos--;
  }

  moveSliderItem();
}

sliderPrevBtn.addEventListener("click", slidePrev);

/**
 * RESPONSIVE
 */
window.addEventListener("resize", function () {
  totalSliderVisibleItems = Number(getComputedStyle(slider).getPropertyValue("--slider-items"));
  totalSlidableItems = sliderContainer.childElementCount - totalSliderVisibleItems;

  moveSliderItem();
});

// JavaScript to toggle the Like and Bookmark button states

function toggleShareDropdown() {
    const shareContainer = document.querySelector('.post-share-container');
    const isMobile = window.matchMedia("(max-width: 768px)").matches;
    
    if (navigator.share) {
      // alert('Web Share API is supported in your browser.');
      navigator.share({
        title: document.title,
        text: 'Check out this awesome page!',
        url: window.location.href
      }).catch(console.error);
      sharesupdate();

    } else {
      const shareUrl = window.location.href;
      const tempInput = document.createElement('input');
      document.body.appendChild(tempInput);
      tempInput.value = shareUrl;
      tempInput.select();
      document.execCommand('copy');
      document.body.removeChild(tempInput);
      
      // const link = `https://wa.me/?text=Check%20this%20out:%20${encodeURIComponent(window.location.href)}`;
      // window.location.href = link;

      const dialog = document.createElement('dialog');
      dialog.textContent = 'URL copied to clipboard.';
      dialog.style.padding = '1em';
      dialog.style.border = 'none';
      dialog.style.borderRadius = '20px';
      dialog.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
      dialog.style.backgroundColor = '#fff';
      dialog.style.color = '#333';
      dialog.style.fontSize = '1em';
      dialog.style.textAlign = 'center';
      document.body.appendChild(dialog);
      dialog.showModal();
      setTimeout(() => {
        dialog.close();
        document.body.removeChild(dialog);
      }, 2000);

      sharesupdate();
    }
    
}

function sharesupdate() {
  const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
  const ShareCount = document.getElementById('share-count');

  axios.post('/update-shares/', 
    {
        post_id: window.userData.post_id,
    }, { headers: {
            'X-CSRFToken': csrf_token
        }
    })
  .then(response => {
  if (response.data.success === true) {
    ShareCount.textContent = parseInt(ShareCount.textContent) + 1;
  } else {
    console.log(response.data.message);
  }
  })
  .catch(error => {
      console.error('Error:', error.response.data);
  });
}

function toggleShareAll(postID) {
  const ShareCount = document.querySelector(`.post-shares-home[data-id='${postID}']`);
  const InnerShareCount = ShareCount.querySelector('.share-count');

  // const page_url = getpageUrl(name, slug);
  const page_url = ShareCount.getAttribute("data-url")
  
  if (navigator.share) {
    // alert('Web Share API is supported in your browser.');
    navigator.share({
      title: document.title,
      text: 'Check out this awesome page!',
      url: page_url
    }).catch(console.error);
    sharesupdateAll(postID);

  } else {
    const shareUrl = page_url;
    const tempInput = document.createElement('input');
    document.body.appendChild(tempInput);
    tempInput.value = shareUrl;
    tempInput.select();
    document.execCommand('copy');
    document.body.removeChild(tempInput);
    
    // const link = `https://wa.me/?text=Check%20this%20out:%20${encodeURIComponent(window.location.href)}`;
    // window.location.href = link;

    const dialog = document.createElement('dialog');
    dialog.textContent = 'URL copied to clipboard.';
    dialog.style.padding = '1em';
    dialog.style.border = 'none';
    dialog.style.borderRadius = '20px';
    dialog.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    dialog.style.backgroundColor = '#fff';
    dialog.style.color = '#333';
    dialog.style.fontSize = '1em';
    dialog.style.textAlign = 'center';
    document.body.appendChild(dialog);
    dialog.showModal();
    setTimeout(() => {
      dialog.close();
      document.body.removeChild(dialog);
    }, 2000);

    sharesupdateAll(postID);
  }
}

function sharesupdateAll(postID) {
  const ShareCount = document.querySelector(`.post-shares-home[data-id='${postID}']`);
  const InnerShareCount = ShareCount.querySelector('.share-count');
  const csrf_token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

  axios.post('/update-shares/', 
    {
        post_id: postID,
    }, { headers: {
            'X-CSRFToken': csrf_token
        }
    })
  .then(response => {
  if (response.data.success === true) {
    InnerShareCount.textContent = parseInt(InnerShareCount.textContent) + 1;
  } else {
    console.log(response.data.message);
  }
  })
  .catch(error => {
      console.error('Error:', error.response.data);
  });
}