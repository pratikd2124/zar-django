let currentStep = 1;

        function showStep(step) {
            document.querySelectorAll('.step').forEach(s => s.style.display = 'none');
            document.getElementById(`step${step}`).style.display = 'block';

            document.getElementById('stepLabel').innerText = step === 1 ? 'Basic Information' : step === 2 ? 'Additional Details' : 'Visual / Profile Uploads';

            document.getElementById('stepIndicator1').classList.toggle('bg-white', step === 1);
            document.getElementById('stepIndicator2').classList.toggle('bg-white', step === 2);
            document.getElementById('stepIndicator3').classList.toggle('bg-white', step === 3);

            document.getElementById('prevBtn').style.display = step > 1 ? 'block' : 'none';
            document.getElementById('nextBtn').style.display = step < 3 ? 'block' : 'none';
            document.getElementById('submitBtn').style.display = step === 3 ? 'block' : 'none';
        }

        function nextStep() {
            if (currentStep < 3) {
                currentStep++;
                showStep(currentStep);
            }
        }

        function prevStep() {
            if (currentStep > 1) {
                currentStep--;
                showStep(currentStep);
            }
        }

        function handleSubmit(event) {
            event.preventDefault();
            // Add form submission logic here
            alert('Form submitted!');
        }

        function handleFileChange(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    container.innerHTML = `
                        <img src="${e.target.result}" alt="Uploaded" class="mb-2 w-96 mx-auto h-auto" />
                        <button type="button" class="bg-red-500 text-white px-4 py-2" onclick="removeFile('${inputId}', '${containerId}')">Remove</button>
                    `;
                };
                reader.readAsDataURL(file);
            }
        }

        function removeFile(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            fileInput.value = '';
            container.innerHTML = `
                Drag and Drop<br/> or
                <button type="button" class="w-fit mx-auto border rounded-lg text-white px-4 py-2 cursor-pointer" onclick="document.getElementById('${inputId}').click()">Upload</button>
            `;
        }

        function handleMultipleFileChange(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const files = Array.from(fileInput.files);
            if (files.length) {
                container.innerHTML = '';
                files.forEach((file, index) => {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        container.innerHTML += `
                            <div class="relative inline-block m-2">
                                <img src="${e.target.result}" alt="Showcase ${index}" class="mb-2 w-20 h-20 object-cover" />
                                <button type="button" class="absolute top-0 right-0 bg-red-500 text-white text-xs px-2 py-1" onclick="removeMultipleFile('${inputId}', '${containerId}', ${index})">X</button>
                            </div>
                        `;
                    };
                    reader.readAsDataURL(file);
                });
            }
        }

        function removeMultipleFile(inputId, containerId, index) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const files = Array.from(fileInput.files);
            files.splice(index, 1);
            fileInput.files = new DataTransfer().files;
            container.innerHTML = '';
            handleMultipleFileChange(inputId, containerId);
        }

        document.getElementById('profilePicInput').addEventListener('change', () => handleFileChange('profilePicInput', 'profilePicContainer'));
        document.getElementById('brandLogoInput').addEventListener('change', () => handleFileChange('brandLogoInput', 'brandLogoContainer'));
                document.getElementById('profileDocInput').addEventListener('change', () => handleFileChange('profileDocInput', 'profileDocContainer'));
        document.getElementById('showcaseGalleryInput').addEventListener('change', () => handleMultipleFileChange('showcaseGalleryInput', 'showcaseGalleryContainer'));

        function handleFileChange(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const file = fileInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    container.innerHTML = `
                        <img src="${e.target.result}" alt="Uploaded" class="mb-2 w-96 mx-auto h-auto" />
                        <button type="button" class="bg-red-500 text-white px-4 py-2" onclick="removeFile('${inputId}', '${containerId}')">Remove</button>
                    `;
                };
                reader.readAsDataURL(file);
            }
        }

        function removeFile(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            fileInput.value = '';
            container.innerHTML = `
                Drag and Drop<br/> or
                <button type="button" class="w-fit mx-auto border rounded-lg text-white px-4 py-2 cursor-pointer" onclick="document.getElementById('${inputId}').click()">Upload</button>
            `;
        }

        function handleMultipleFileChange(inputId, containerId) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const files = Array.from(fileInput.files);
            if (files.length) {
                container.innerHTML = '';
                files.forEach((file, index) => {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        container.innerHTML += `
                            <div class="relative inline-block m-2">
                                <img src="${e.target.result}" alt="Showcase ${index}" class="mb-2 w-20 h-20 object-cover" />
                                <button type="button" class="absolute top-0 right-0 bg-red-500 text-white text-xs px-2 py-1" onclick="removeMultipleFile('${inputId}', '${containerId}', ${index})">X</button>
                            </div>
                        `;
                    };
                    reader.readAsDataURL(file);
                });
            }
        }

        function removeMultipleFile(inputId, containerId, index) {
            const fileInput = document.getElementById(inputId);
            const container = document.getElementById(containerId);
            const files = Array.from(fileInput.files);
            files.splice(index, 1);
            const dt = new DataTransfer();
            files.forEach(file => dt.items.add(file));
            fileInput.files = dt.files;
            container.innerHTML = '';
            handleMultipleFileChange(inputId, containerId);
        }

        document.addEventListener('DOMContentLoaded', () => {
            showStep(currentStep);
        });