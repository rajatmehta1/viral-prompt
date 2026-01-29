// Viral Prompt - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Navigation scroll effect
    const navbar = document.querySelector('.glass-nav');
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Filter functionality
    const filterBtns = document.querySelectorAll('.filter-btn');
    const gridItems = document.querySelectorAll('.grid-item');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // Remove active from all
            filterBtns.forEach(b => b.classList.remove('active'));
            // Add active to clicked
            this.classList.add('active');

            const filter = this.dataset.filter;

            gridItems.forEach(item => {
                if (filter === 'all' || item.dataset.type === filter) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeInUp 0.6s ease both';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });

    // Copy prompt functionality
    const copyBtn = document.querySelector('.btn-outline-glow');
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const textarea = document.querySelector('.prompt-textarea');
            if (textarea) {
                navigator.clipboard.writeText(textarea.value).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check-lg me-2"></i> Copied!';
                    setTimeout(() => {
                        this.innerHTML = originalText;
                    }, 2000);
                });
            }
        });
    }

    // Add hover effects to play icons
    const playIcons = document.querySelectorAll('.play-icon');
    playIcons.forEach(icon => {
        icon.addEventListener('click', function() {
            // Placeholder for video play functionality
            console.log('Video play clicked');
        });
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    gridItems.forEach(item => {
        observer.observe(item);
    });
});
