// SCA Website JavaScript
class SCAWebsite {
    constructor() {
        this.init();
    }

    init() {
        this.setupNavigation();
        this.setupSmoothScrolling();
        this.loadGitHubData();
        this.setupAnimations();
    }

    // Navigation functionality
    setupNavigation() {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        const navMenu = document.querySelector('.nav-menu');
        
        if (mobileToggle && navMenu) {
            mobileToggle.addEventListener('click', () => {
                navMenu.classList.toggle('active');
                mobileToggle.classList.toggle('active');
            });
        }

        // Active nav link highlighting
        const navLinks = document.querySelectorAll('.nav-link');
        const sections = document.querySelectorAll('.section');
        
        window.addEventListener('scroll', () => {
            let current = '';
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (window.pageYOffset >= sectionTop - 200) {
                    current = section.getAttribute('id');
                }
            });
            
            navLinks.forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${current}`) {
                    link.classList.add('active');
                }
            });
        });
    }

    // Smooth scrolling for anchor links
    setupSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');
        
        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                
                if (targetElement) {
                    const headerOffset = 80;
                    const elementPosition = targetElement.offsetTop;
                    const offsetPosition = elementPosition - headerOffset;
                    
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });
                }
            });
        });
    }

    // Load GitHub repository data
    async loadGitHubData() {
        try {
            const repoStatus = document.getElementById('repoStatus');
            if (!repoStatus) return;

            // GitHub API endpoint for repository data
            const repoUrl = 'https://api.github.com/repos/takawasi/sca-cognitive-architecture';
            
            repoStatus.innerHTML = '<span class="status-loading">Loading repository data...</span>';
            
            const response = await fetch(repoUrl);
            
            if (response.ok) {
                const data = await response.json();
                this.displayGitHubData(data, repoStatus);
            } else {
                throw new Error('Failed to fetch repository data');
            }
        } catch (error) {
            console.error('GitHub data loading error:', error);
            const repoStatus = document.getElementById('repoStatus');
            if (repoStatus) {
                repoStatus.innerHTML = `
                    <div class="repo-info">
                        <span class="repo-name">sca-cognitive-architecture</span>
                        <span class="repo-description">Next-generation AI collaboration framework</span>
                        <div class="repo-stats">
                            <span>Status: Active Development</span>
                            <span>License: MIT</span>
                        </div>
                        <a href="https://github.com/takawasi/sca-cognitive-architecture" target="_blank" class="repo-link">View on GitHub</a>
                    </div>
                `;
            }
        }
    }

    // Display GitHub repository data
    displayGitHubData(data, container) {
        const lastUpdated = new Date(data.updated_at).toLocaleDateString();
        const createdAt = new Date(data.created_at).toLocaleDateString();
        
        container.innerHTML = `
            <div class="repo-info">
                <div class="repo-header">
                    <span class="repo-name">${data.name}</span>
                    <span class="repo-visibility ${data.private ? 'private' : 'public'}">${data.private ? 'Private' : 'Public'}</span>
                </div>
                <p class="repo-description">${data.description}</p>
                <div class="repo-stats">
                    <span class="stat-item">
                        <strong>${data.stargazers_count}</strong> stars
                    </span>
                    <span class="stat-item">
                        <strong>${data.forks_count}</strong> forks
                    </span>
                    <span class="stat-item">
                        <strong>${data.size}</strong> KB
                    </span>
                    <span class="stat-item">
                        Language: <strong>${data.language || 'Multiple'}</strong>
                    </span>
                </div>
                <div class="repo-dates">
                    <span>Created: ${createdAt}</span>
                    <span>Updated: ${lastUpdated}</span>
                </div>
                <div class="repo-actions">
                    <a href="${data.html_url}" target="_blank" class="btn btn-outline btn-small">View Repository</a>
                    <a href="${data.clone_url}" class="btn btn-outline btn-small" onclick="this.select(); document.execCommand('copy'); alert('Clone URL copied!');">Clone</a>
                </div>
            </div>
        `;
        
        // Add styles for repository display
        this.addRepoStyles();
    }

    // Add dynamic styles for repository information
    addRepoStyles() {
        if (document.getElementById('repo-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'repo-styles';
        styles.textContent = `
            .repo-info {
                text-align: left;
                background: rgba(255, 255, 255, 0.1);
                padding: 1.5rem;
                border-radius: 0.5rem;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .repo-header {
                display: flex;
                align-items: center;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .repo-name {
                font-size: 1.25rem;
                font-weight: 600;
                color: #10b981;
            }
            
            .repo-visibility {
                padding: 0.25rem 0.75rem;
                border-radius: 1rem;
                font-size: 0.75rem;
                font-weight: 500;
                text-transform: uppercase;
            }
            
            .repo-visibility.public {
                background: rgba(16, 185, 129, 0.2);
                color: #10b981;
            }
            
            .repo-description {
                margin-bottom: 1rem;
                color: #d1d5db;
                font-size: 0.9rem;
            }
            
            .repo-stats {
                display: flex;
                flex-wrap: wrap;
                gap: 1rem;
                margin-bottom: 1rem;
            }
            
            .stat-item {
                font-size: 0.875rem;
                color: #9ca3af;
            }
            
            .stat-item strong {
                color: #f59e0b;
            }
            
            .repo-dates {
                display: flex;
                gap: 1rem;
                margin-bottom: 1rem;
                font-size: 0.75rem;
                color: #9ca3af;
            }
            
            .repo-actions {
                display: flex;
                gap: 1rem;
                flex-wrap: wrap;
            }
            
            .btn-small {
                padding: 0.5rem 1rem;
                font-size: 0.875rem;
            }
            
            @media (max-width: 768px) {
                .repo-header {
                    flex-direction: column;
                    align-items: flex-start;
                }
                
                .repo-stats {
                    flex-direction: column;
                    gap: 0.5rem;
                }
                
                .repo-dates {
                    flex-direction: column;
                    gap: 0.25rem;
                }
            }
        `;
        
        document.head.appendChild(styles);
    }

    // Setup scroll animations
    setupAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        const animateElements = document.querySelectorAll(
            '.overview-item, .arch-tier, .step, .research-highlight, .performance-metrics'
        );
        
        animateElements.forEach(el => {
            el.classList.add('animate-element');
            observer.observe(el);
        });
        
        // Add animation styles
        this.addAnimationStyles();
    }

    // Add animation styles
    addAnimationStyles() {
        if (document.getElementById('animation-styles')) return;
        
        const styles = document.createElement('style');
        styles.id = 'animation-styles';
        styles.textContent = `
            .animate-element {
                opacity: 0;
                transform: translateY(30px);
                transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            }
            
            .animate-element.animate-in {
                opacity: 1;
                transform: translateY(0);
            }
            
            .animate-element:nth-child(2) {
                transition-delay: 0.1s;
            }
            
            .animate-element:nth-child(3) {
                transition-delay: 0.2s;
            }
            
            .animate-element:nth-child(4) {
                transition-delay: 0.3s;
            }
        `;
        
        document.head.appendChild(styles);
    }

    // Utility function to copy text to clipboard
    copyToClipboard(text) {
        if (navigator.clipboard && navigator.clipboard.writeText) {
            return navigator.clipboard.writeText(text);
        } else {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();
            try {
                document.execCommand('copy');
                return Promise.resolve();
            } catch (err) {
                return Promise.reject(err);
            } finally {
                document.body.removeChild(textArea);
            }
        }
    }
}

// Initialize the website when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SCAWebsite();
});

// Performance optimization: Preload critical resources
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(() => {
            // Service worker registration failed, but this is optional
        });
    });
}

// Export for testing purposes
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SCAWebsite;
}