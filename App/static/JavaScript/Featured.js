function premium() {
    // let premiumplus = document.querySelector('.premium');
    // premiumplus.textContent = 'Premium+';
    
    Swal.fire({
        title: 'Premium feature',
        text: 'We are currently working on this feature. Please check back later.',
        icon: 'info',
        showConfirmButton: true,
        confirmButtonColor: 'rgb(58, 138, 222)',
        allowOutsideClick: false,
        allowEscapeKey: false,
        allowEnterKey: false,
    });
}