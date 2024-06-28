document.getElementById('image-form').onsubmit = async function (event) {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('image-input', document.getElementById('image-input').files[0]);
    formData.append('num-colors', document.getElementById('num-colors').value);

    const response = await fetch('compress', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    const outputImage = document.getElementById('output-image');
    outputImage.src = 'data:image/png;base64,' + data.image;
    document.getElementById('output').style.display = 'block';
    document.getElementById('download-button').style.display = 'block';
    
    document.getElementById('download-button').onclick = function () {
        const a = document.createElement('a');
        a.href = outputImage.src;
        a.download = 'compressed_image.png';
        a.click();
    };
};
