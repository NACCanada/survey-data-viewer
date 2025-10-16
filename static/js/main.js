// File input handling
const fileInput = document.getElementById('fileInput');
const fileName = document.getElementById('fileName');

fileInput.addEventListener('change', function(e) {
    if (e.target.files.length > 0) {
        fileName.textContent = e.target.files[0].name;
    } else {
        fileName.textContent = 'Choose a file...';
    }
});

// Form submission
const uploadForm = document.getElementById('uploadForm');
const uploadStatus = document.getElementById('uploadStatus');

uploadForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    uploadStatus.textContent = 'Uploading...';
    uploadStatus.className = 'status-message';
    uploadStatus.style.display = 'block';

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.error) {
            uploadStatus.textContent = 'Error: ' + data.error;
            uploadStatus.className = 'status-message error';
        } else {
            uploadStatus.textContent = 'Upload successful! Redirecting...';
            uploadStatus.className = 'status-message success';
            setTimeout(() => {
                window.location.href = '/survey/' + data.survey_id;
            }, 1000);
        }
    } catch (error) {
        uploadStatus.textContent = 'Error: ' + error.message;
        uploadStatus.className = 'status-message error';
    }
});

// Delete survey
async function deleteSurvey(surveyId) {
    if (!confirm('Are you sure you want to delete this survey? This action cannot be undone.')) {
        return;
    }

    try {
        const response = await fetch('/delete/' + surveyId, {
            method: 'POST'
        });

        const data = await response.json();

        if (data.error) {
            alert('Error deleting survey: ' + data.error);
        } else {
            location.reload();
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}
