document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const submitButton = document.getElementById('submitButton');
    const responseText = document.getElementById('responseText');
    const responseContainer = document.getElementById('responseContainer'); // Get the response container element
    const progressBar = document.getElementById('progressBar');
    const progressFill = document.getElementById('progressFill');

    submitButton.addEventListener('click', () => {
        const file = fileInput.files[0];

        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            // Show the progress bar and set the "Processing..." message
            progressBar.style.display = 'block';
            responseText.textContent = 'Processing...';

            const xhr = new XMLHttpRequest();

            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percentComplete = (event.loaded / event.total) * 100;
                    // Update the progress bar's width
                    progressFill.style.width = percentComplete + '%';
                }
            };

            xhr.onload = () => {
                if (xhr.status === 200) {
                    responseText.textContent = JSON.stringify(JSON.parse(xhr.responseText), null, 2);
                } else {
                    responseText.textContent = 'Error: ' + xhr.statusText;
                }
                // Hide the progress bar when the response is received
                progressBar.style.display = 'none';
            };

            xhr.onerror = () => {
                responseText.textContent = 'Error: Network request failed';
                // Hide the progress bar in case of an error
                progressBar.style.display = 'none';
            };

            xhr.open('POST', 'http://localhost:8000/upload/');
            xhr.send(formData);
        }
    });
});
