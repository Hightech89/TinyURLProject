document.getElementById('urlForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const longUrl = document.getElementById('longUrl').value;
    const response = await fetch('/shorten', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ longUrl }),
    });

    const data = await response.json();
    if (data.shortUrl) {
        const shortUrlContainer = document.getElementById('shortUrlContainer');
        const shortUrlElement = document.getElementById('shortUrl');
        shortUrlElement.href = data.shortUrl;
        shortUrlElement.textContent = data.shortUrl;
        shortUrlContainer.style.display = 'block';
    }
});