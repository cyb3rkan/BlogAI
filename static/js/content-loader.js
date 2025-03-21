function loadContent(button, slug, language) {
    // Parametreleri kontrol et
    if (!slug || !language) {
        console.error('Eksik parametreler:', { slug, language });
        return;
    }

    // URL oluştur
    const url = `/courses/${language}/${slug}/`;
    console.log('İstek URL:', url);

    // Tüm butonlardan active sınıfını kaldır
    document.querySelectorAll('#lessonNav .nav-link').forEach(btn => {
        btn.classList.remove('active');
    });

    // Tıklanan butona active sınıfı ekle
    button.classList.add('active');

    // Loading göster
    const contentDiv = document.getElementById('contentDetail');
    contentDiv.innerHTML = `
        <div class="text-center p-5">
            <div class="spinner-border text-primary"></div>
            <p class="mt-2">İçerik yükleniyor...</p>
        </div>
    `;

    // İçeriği getir
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP Hata: ${response.status}`);
            }
            return response.text();
        })
        .then(html => {
            contentDiv.innerHTML = html;
        })
        .catch(error => {
            console.error('Hata:', error);
            contentDiv.innerHTML = `
                <div class="alert alert-danger">
                    <i class="fas fa-exclamation-circle"></i> 
                    Hata: ${error.message}
                </div>
            `;
        });
}

// İlk yüklemede çalışacak kod
document.addEventListener('DOMContentLoaded', () => {
    const firstButton = document.querySelector('#lessonNav .nav-link');
    if (firstButton) {
        const slug = firstButton.getAttribute('data-slug');
        const language = firstButton.getAttribute('data-language');
        if (slug && language) {
            console.log('Initial load:', { slug, language });
            loadContent(firstButton, slug, language);
        }
    }
});
