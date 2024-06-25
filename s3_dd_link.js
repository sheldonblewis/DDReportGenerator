document.addEventListener('DOMContentLoaded', function () {
    const currentPage = window.location.pathname.split('/').pop();
    
    if (currentPage === 's3_upload.html') {
        handleFileUpload();
    } else if (currentPage === 'dd_analysis.html') {
        handleReportGeneration();
    }

    function handleFileUpload() {
        const uploadUrl = "https://equitary-uploads.ngrok.io/";
        const checkEndpoint = `${uploadUrl}get-latest-report`;

        const fileInput = document.getElementById('fileInput');
        const uploadButton = document.getElementById('uploadButton');
        const uploadIframe = document.getElementById('uploadIframe');
        const spinner = document.getElementById('loadingSpinner');

        uploadButton.addEventListener('click', function () {
            const files = fileInput.files;
            if (files.length > 0) {
                const formData = new FormData();
                for (let i = 0; i < files.length; i++) {
                    formData.append(files[i].name, files[i]);
                }
                startUpload(formData);
            } else {
                alert('Please select files to upload.');
            }
        });

        function startUpload(formData) {
            spinner.style.display = 'block';
            spinner.classList.add('spin');
            fetch(uploadUrl, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "uploadCompleted") {
                    checkForUploadCompletion();
                } else {
                    console.log("Upload started, waiting for completion...");
                }
            })
            .catch(err => {
                console.error("Error during file upload:", err);
            });
        }

        function checkForUploadCompletion() {
            const pollingInterval = 1000;

            const intervalId = setInterval(() => {
                fetch(checkEndpoint, { method: 'GET' })
                    .then(response => response.json())
                    .then(data => {
                        if (data.error) {
                            console.log("Polling for completion, but data is not ready yet.");
                        } else {
                            console.log("Data received:", data);
                            clearInterval(intervalId); // Stop polling
                            updateHtmlComponent(data);
                        }
                    })
                    .catch(err => {
                        console.error("Error polling for upload completion:", err);
                        clearInterval(intervalId);
                    });
            }, pollingInterval);
        }

        function updateHtmlComponent(data) {
            // Encode the thesis prompt
            const encodedThesisPrompt = encodeURIComponent(data.thesisPrompt.trim());

            // Redirect to the report generation page with the encoded thesis prompt
            if (data.thesisPrompt) {
                window.location.href = `/dd_analysis.html?thesis_prompt=${encodedThesisPrompt}`;
            }
        }
    }

    function handleReportGeneration() {
        const spinner = document.getElementById('loadingSpinner');
        const iframe = document.getElementById('reportIframe');
        const searchButton = document.getElementById('searchButtonDisplay');

        // Hide the iframe and search button initially
        iframe.style.display = 'none';
        searchButton.style.display = 'none';

        // Start spinner animation
        spinner.style.display = 'block';
        spinner.classList.add('spin');

        const params = new URLSearchParams(window.location.search);
        const thesisPrompt = params.get('thesis_prompt');

        if (thesisPrompt) {
            const reportUrl = `https://equitary-reports.ngrok.io/generate_economic_report?thesis_prompt_text=${thesisPrompt}`;
            iframe.src = reportUrl;

            iframe.onload = function () {
                spinner.style.display = 'none';
                spinner.classList.remove('spin');
                iframe.style.display = 'block';
                searchButton.style.display = 'block';
            };
        } else {
            window.location.href = '/no-ticker-found';
        }
    }
});
