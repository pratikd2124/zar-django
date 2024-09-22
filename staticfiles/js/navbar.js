document.addEventListener('DOMContentLoaded', function () {
    const menuButton = document.getElementById('menuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    const profileButton = document.getElementById('profileButton');
    const dropdownMenu = document.getElementById('dropdownMenu');
    const profileDropdownButton = document.getElementById('profileDropdownButton');
    const profileDropdownMenu = document.getElementById('profileDropdownMenu');

    menuButton.addEventListener('click', function () {
        mobileMenu.classList.toggle('hidden');
        const menuIcon = document.getElementById('menuIcon');
        if (mobileMenu.classList.contains('hidden')) {
            menuIcon.setAttribute('viewBox', '0 0 24 24');
            menuIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M12 17.25h8.25" />';
        } else {
            menuIcon.setAttribute('viewBox', '0 0 24 24');
            menuIcon.innerHTML = '<path stroke-linecap="round" stroke-linejoin="round" d="M6 18 18 6M6 6l12 12" />';
        }
    });

    profileButton.addEventListener('click', function () {
        dropdownMenu.classList.toggle('hidden');
    });

    profileDropdownButton.addEventListener('click', function () {
        profileDropdownMenu.classList.toggle('hidden');
    });

    document.addEventListener('click', function (event) {
        if (!profileButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.add('hidden');
        }
        if (!profileDropdownButton.contains(event.target) && !profileDropdownMenu.contains(event.target)) {
            profileDropdownMenu.classList.add('hidden');
        }
    });
});