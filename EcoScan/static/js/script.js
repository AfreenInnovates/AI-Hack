// Navbar scroll effect
document.addEventListener('DOMContentLoaded', function() {
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // File upload handling
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('image-upload');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const imagePreview = document.getElementById('image-preview');
    const changeFileBtn = document.getElementById('change-file');
    const uploadForm = document.getElementById('upload-form');

    if (dropZone) {
        // Drag and drop functionality
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, highlight, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, unhighlight, false);
        });

        function highlight(e) {
            dropZone.classList.add('drag-over');
        }

        function unhighlight(e) {
            dropZone.classList.remove('drag-over');
        }

        dropZone.addEventListener('drop', handleDrop, false);

        function handleDrop(e) {
            const dt = e.dataTransfer;
            const files = dt.files;
            fileInput.files = files;
            handleFiles(files);
        }
    }

    // File input change handler
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            handleFiles(this.files);
        });
    }

    function handleFiles(files) {
        if (files.length > 0) {
            const file = files[0];
            
            // Show file preview
            const reader = new FileReader();
            reader.onload = function(e) {
                if (imagePreview) {
                    imagePreview.src = e.target.result;
                    document.querySelector('.file-preview').style.display = 'block';
                }
            };
            reader.readAsDataURL(file);

            // Update file name display
            if (fileName) {
                fileName.textContent = file.name;
            }

            // Show file info and hide upload placeholder
            if (fileInfo) {
                fileInfo.style.display = 'block';
                document.querySelector('.upload-placeholder').style.display = 'none';
            }
        }
    }

    // Change file button handler
    if (changeFileBtn) {
        changeFileBtn.addEventListener('click', function() {
            document.querySelector('.upload-placeholder').style.display = 'block';
            fileInfo.style.display = 'none';
            fileInput.value = '';
        });
    }

    // Form submit handler
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            document.querySelector('.loading-overlay').style.display = 'flex';
            document.querySelector('.upload-progress').style.display = 'block';
        });
    }
});

// Loading animation control
function showLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.style.display = 'flex';
    }
}

function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.style.display = 'none';
    }
}
