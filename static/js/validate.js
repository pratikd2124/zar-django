document.addEventListener('DOMContentLoaded', function() {
    const otpInputs = Array.from(document.querySelectorAll('input[type="text"]'));
    const emailInput = document.getElementById('email');
    const submitButton = document.getElementById('submitButton');

    // Handle OTP input change
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function(e) {
            const value = e.target.value;
            if (/[^0-9]/.test(value)) return; // Prevent non-numeric input

            // Move to the next input box if the current one is filled
            if (value && index < 5) {
                otpInputs[index + 1].focus();
            }
        });
    });

    // Check if all OTP inputs and email are filled
    const isSubmitDisabled = () => {
        return otpInputs.some(input => input.value === '') || !emailInput.value;
    };

    // Update submit button state
    const updateSubmitButtonState = () => {
        submitButton.disabled = isSubmitDisabled();
    };

    // // Handle form submission
    // document.getElementById('codeValidationForm').addEventListener('submit', function(e) {
    //     e.preventDefault();
    //     const otp = otpInputs.map(input => input.value).join('');
    //     const email = emailInput.value;
    //     console.log('OTP:', otp);
    //     console.log('Email:', email);
    //     // Navigate to the registration page upon successful submission
    // });

    // Update submit button state on input change
    Array.from(document.querySelectorAll('input')).forEach(input => {
        input.addEventListener('input', updateSubmitButtonState);
    });
    emailInput.addEventListener('input', updateSubmitButtonState);

    // Initial state update
    updateSubmitButtonState();
});