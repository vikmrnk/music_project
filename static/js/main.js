// ============================================
// ТЕМНА ТЕМА
// ============================================

(function() {
    const themeToggle = document.getElementById('themeToggle');
    const currentTheme = localStorage.getItem('theme') || 'light';
    
    // Встановити початкову тему
    document.documentElement.setAttribute('data-theme', currentTheme);
    updateThemeIcon(currentTheme);
    
    // Обробник перемикання теми
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
        });
    }
    
    function updateThemeIcon(theme) {
        // Іконка теми тепер SVG, тому просто оновлюємо aria-label
        if (themeToggle) {
            themeToggle.setAttribute('aria-label', theme === 'dark' ? 'Увімкнути світлу тему' : 'Увімкнути темну тему');
        }
    }
})();

// ============================================
// LIVE SEARCH
// ============================================

(function() {
    const searchInput = document.getElementById('liveSearchInput');
    const searchResults = document.getElementById('liveSearchResults');
    let searchTimeout;
    
    if (searchInput && searchResults) {
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            clearTimeout(searchTimeout);
            
            if (query.length < 2) {
                searchResults.classList.remove('active');
                searchResults.innerHTML = '';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                fetch(`/api/live-search/?q=${encodeURIComponent(query)}`)
                    .then(response => response.json())
                    .then(data => {
                        displaySearchResults(data.results);
                    })
                    .catch(error => {
                        console.error('Search error:', error);
                    });
            }, 300);
        });
        
        // Закрити результати при кліку поза ними
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove('active');
            }
        });
    }
    
    function displaySearchResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="live-search-result">Нічого не знайдено</div>';
            searchResults.classList.add('active');
            return;
        }
        
        searchResults.innerHTML = results.map(result => `
            <a href="${result.url}" class="live-search-result">
                <strong>${result.title}</strong>
                <div style="font-size: 0.85rem; color: var(--text-secondary); margin-top: 0.25rem;">
                    ${result.short_description}
                </div>
                ${result.category ? `<span style="font-size: 0.75rem; color: var(--primary-color);">${result.category}</span>` : ''}
            </a>
        `).join('');
        
        searchResults.classList.add('active');
    }
})();

// ============================================
// LAZY LOADING ЗОБРАЖЕНЬ
// ============================================

(function() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                }
            });
        });
        
        // Спостереження за всіма зображеннями з data-src
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
})();

// ============================================
// MOBILE MENU
// ============================================

(function() {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const navList = document.getElementById('navList');
    
    if (mobileMenuToggle && navList) {
        mobileMenuToggle.addEventListener('click', function() {
            const isOpen = navList.classList.toggle('is-open');
            mobileMenuToggle.classList.toggle('is-open');
            mobileMenuToggle.setAttribute('aria-expanded', isOpen);
        });
    }
})();

// ============================================
// INFINITE SCROLL (опціонально)
// ============================================

(function() {
    const infiniteScrollEnabled = false; // Вимкнути за замовчуванням
    
    if (infiniteScrollEnabled && 'IntersectionObserver' in window) {
        const pagination = document.querySelector('.pagination');
        const nextLink = pagination?.querySelector('.pagination-link:last-child');
        
        if (nextLink) {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        // Завантажити наступну сторінку
                        window.location.href = nextLink.href;
                    }
                });
            });
            
            observer.observe(pagination);
        }
    }
})();

// ============================================
// SMOOTH SCROLL
// ============================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================
// FORM VALIDATION
// ============================================

(function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!this.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            this.classList.add('was-validated');
        });
    });
})();

// ============================================
// SHARE ARTICLE
// ============================================

function shareArticle() {
    if (navigator.share) {
        navigator.share({
            title: document.title,
            url: window.location.href
        }).catch(err => console.log('Error sharing', err));
    } else {
        // Fallback: copy to clipboard
        navigator.clipboard.writeText(window.location.href);
        alert('Посилання скопійовано в буфер обміну!');
    }
}

// ============================================
// SAVE ARTICLE
// ============================================

function saveArticle() {
    // Проста реалізація - можна розширити з localStorage або API
    const saved = localStorage.getItem('savedArticles') || '[]';
    const savedArticles = JSON.parse(saved);
    const currentUrl = window.location.href;
    
    if (savedArticles.includes(currentUrl)) {
        const index = savedArticles.indexOf(currentUrl);
        savedArticles.splice(index, 1);
        alert('Статтю видалено зі збережених');
    } else {
        savedArticles.push(currentUrl);
        alert('Статтю збережено!');
    }
    
    localStorage.setItem('savedArticles', JSON.stringify(savedArticles));
}
