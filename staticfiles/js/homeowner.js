document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('homeOwnerForm');
    const nameInput = document.getElementById('name');
    const numberInput = document.getElementById('number');
    const emailInput = document.getElementById('email');
    const messageInput = document.getElementById('message');
    const nameError = document.getElementById('nameError');
    const numberError = document.getElementById('numberError');
    const emailError = document.getElementById('emailError');
    const messageError = document.getElementById('messageError');

    form.addEventListener('submit', function (e) {
        e.preventDefault();
        if (validate()) {
            // Handle form submission
            alert('Form submitted successfully, Your account is Under Review');
            setTimeout(() => {
                window.location.href = '/';
            }, 3000);
        }
    });

    function validate() {
        let isValid = true;
        const nameRegex = /^[A-Za-z\s]+$/;
        const phoneRegex = /^\d{10}$/;
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

        const name = nameInput.value.trim();
        const number = numberInput.value.trim();
        const email = emailInput.value.trim();
        const message = messageInput.value.trim();

        nameError.textContent = name ? (nameRegex.test(name) ? '' : 'Name should contain only alphabets.') : 'This field is required.';
        numberError.textContent = number ? (phoneRegex.test(number) ? '' : 'Phone number should be 10 digits.') : 'This field is required.';
        emailError.textContent = email ? (emailRegex.test(email) ? '' : 'Invalid email format.') : 'This field is required.';
        messageError.textContent = message ? '' : 'This field is required.';

        if (nameError.textContent || numberError.textContent || emailError.textContent || messageError.textContent) {
            isValid = false;
        }

        return isValid;
    }
});