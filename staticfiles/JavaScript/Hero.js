document.addEventListener('DOMContentLoaded', function() {
    // Typing animation
    const typingElement = document.querySelector('.typing');
    const words = JSON.parse(typingElement.getAttribute('data-words'));
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    let isEnd = false;

    function type() {
        const currentWord = words[wordIndex];

        if (isDeleting) {
            typingElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        if (!isDeleting && charIndex === currentWord.length) {
            isEnd = true;
            isDeleting = true;
            setTimeout(type, 1500);
        } else if (isDeleting && charIndex === 0) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            setTimeout(type, 500);
        } else {
            const speed = isDeleting ? 100 : 150;
            setTimeout(type, isEnd ? speed * 2 : speed);
            isEnd = false;
        }
    }

    // Start typing animation after a short delay
    setTimeout(type, 1000);

    // Counter animation for stats
    const counters = document.querySelectorAll('.stat-value');
    const speed = 200;

    function animateCounters() {
        counters.forEach(counter => {
            const target = +counter.getAttribute('data-count');
            const count = +counter.innerText;
            const increment = target / speed;

            if (count < target) {
                counter.innerText = Math.ceil(count + increment);
                setTimeout(animateCounters, 1);
            } else {
                counter.innerText = target.toLocaleString();
            }
        });
    }

    // Start counter animation when stats are in view
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounters();
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    document.querySelector('.hero-stats').querySelectorAll('.stat-value').forEach(el => {
        observer.observe(el);
    });

    // Smooth scroll for scroll indicator
    document.querySelector('.scroll-indicator').addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollBy({
            top: window.innerHeight - 100,
            behavior: 'smooth'
        });
    });
});
