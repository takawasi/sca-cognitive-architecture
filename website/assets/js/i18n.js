// SCA Website Internationalization (i18n)
class SCAInternationalization {
    constructor() {
        this.currentLanguage = this.detectLanguage();
        this.translations = {
            en: {
                // Navigation
                'nav.overview': 'Overview',
                'nav.architecture': 'Architecture',
                'nav.research': 'Research',
                'nav.implementation': 'Implementation',
                'nav.github': 'GitHub',
                
                // Hero Section
                'hero.title': 'Symbiotic Cognitive Architecture',
                'hero.subtitle': 'Next-generation AI collaboration framework enabling true human-AI symbiosis',
                'hero.stats.quality': 'Higher Output Quality',
                'hero.stats.speed': 'Faster Problem Solving',
                'hero.stats.uptime': 'Uptime',
                'hero.btn.start': 'Get Started',
                'hero.btn.github': 'View on GitHub',
                
                // Overview Section
                'overview.title': 'System Overview',
                'overview.context.title': 'Context Mapping',
                'overview.context.desc': 'Analyzes problem structure and relationships using advanced semantic understanding',
                'overview.decomp.title': 'Intelligent Decomposition', 
                'overview.decomp.desc': 'Breaks down complex queries into actionable, prioritized subtasks',
                'overview.synthesis.title': 'Dialectical Synthesis',
                'overview.synthesis.desc': 'Integrates multiple perspectives through structured reasoning processes',
                'overview.memory.title': 'Persistent Memory',
                'overview.memory.desc': 'Maintains learning continuity across sessions with intelligent compression',
                
                // Architecture Section
                'architecture.title': 'Architecture',
                'architecture.tier3.title': 'Tier 3: Synthesis',
                'architecture.tier3.desc': 'Integration and holistic reasoning',
                'architecture.tier2.title': 'Tier 2: Analysis', 
                'architecture.tier2.desc': 'Deep analysis and pattern recognition',
                'architecture.tier1.title': 'Tier 1: Foundation',
                'architecture.tier1.desc': 'Context mapping and decomposition',
                'architecture.repo.title': 'Live Repository Status',
                'architecture.repo.loading': 'Loading repository data...',
                
                // Research Section
                'research.title': 'Research & Development',
                'research.highlight.title': 'Academic Foundation',
                'research.highlight.desc': 'Based on 47-page comprehensive system analysis with rigorous performance benchmarks',
                'research.highlight.btn': 'View Research Papers',
                'research.metrics.title': 'Performance Metrics',
                'research.metrics.response': 'Response time: < 2.5 seconds average',
                'research.metrics.memory': 'Memory efficiency: 98.5% compression ratio',
                'research.metrics.concurrent': 'Concurrent agents: 100+ tested',
                'research.metrics.quality': 'Quality improvement: 95% over baseline',
                
                // Implementation Section
                'implementation.title': 'Implementation Guide',
                'implementation.step1.title': 'Clone Repository',
                'implementation.step2.title': 'Install Dependencies',
                'implementation.step3.title': 'Configure MCP Servers',
                'implementation.step4.title': 'Launch System',
                'implementation.api.title': 'API Example',
                
                // Footer
                'footer.framework.title': 'SCA Framework',
                'footer.framework.desc': 'Next-generation AI collaboration',
                'footer.resources.title': 'Resources',
                'footer.community.title': 'Community',
                'footer.copyright': '© 2025 TAKAWASI Research Team. Licensed under MIT.',
                'footer.made': 'Made with ❤️ for human-AI collaboration'
            },
            ja: {
                // Navigation
                'nav.overview': '概要',
                'nav.architecture': 'アーキテクチャ',
                'nav.research': '研究開発',
                'nav.implementation': '実装ガイド',
                'nav.github': 'GitHub',
                
                // Hero Section  
                'hero.title': '共生認知アーキテクチャ',
                'hero.subtitle': '真の人間・AI協働を実現する次世代コラボレーションフレームワーク',
                'hero.stats.quality': '出力品質向上',
                'hero.stats.speed': '問題解決時間短縮',
                'hero.stats.uptime': '稼働率',
                'hero.btn.start': '始める',
                'hero.btn.github': 'GitHubで見る',
                
                // Overview Section
                'overview.title': 'システム概要',
                'overview.context.title': 'コンテキストマッピング',
                'overview.context.desc': '高度なセマンティック理解を用いて問題構造と関係性を分析',
                'overview.decomp.title': 'インテリジェント分解',
                'overview.decomp.desc': '複雑なクエリを実行可能で優先順位付けされたサブタスクに分解',
                'overview.synthesis.title': '弁証法的統合',
                'overview.synthesis.desc': '構造化された推論プロセスを通じて複数の観点を統合',
                'overview.memory.title': '永続的記憶',
                'overview.memory.desc': 'インテリジェントな圧縮により、セッション間で学習の継続性を維持',
                
                // Architecture Section
                'architecture.title': 'アーキテクチャ',
                'architecture.tier3.title': '第3層: 統合',
                'architecture.tier3.desc': '統合と全体論的推論',
                'architecture.tier2.title': '第2層: 分析',
                'architecture.tier2.desc': '深い分析とパターン認識',
                'architecture.tier1.title': '第1層: 基盤',
                'architecture.tier1.desc': 'コンテキストマッピングと分解',
                'architecture.repo.title': 'ライブリポジトリ状態',
                'architecture.repo.loading': 'リポジトリデータを読み込み中...',
                
                // Research Section
                'research.title': '研究開発',
                'research.highlight.title': '学術的基盤',
                'research.highlight.desc': '厳密なパフォーマンスベンチマークを含む47ページの包括的システム分析に基づく',
                'research.highlight.btn': '研究論文を見る',
                'research.metrics.title': 'パフォーマンス指標',
                'research.metrics.response': '応答時間: 平均2.5秒未満',
                'research.metrics.memory': 'メモリ効率: 98.5%圧縮率',
                'research.metrics.concurrent': '同時実行エージェント: 100+テスト済み',
                'research.metrics.quality': '品質改善: ベースラインより95%向上',
                
                // Implementation Section
                'implementation.title': '実装ガイド',
                'implementation.step1.title': 'リポジトリをクローン',
                'implementation.step2.title': '依存関係をインストール',
                'implementation.step3.title': 'MCPサーバーを設定',
                'implementation.step4.title': 'システムを起動',
                'implementation.api.title': 'API例',
                
                // Footer
                'footer.framework.title': 'SCAフレームワーク',
                'footer.framework.desc': '次世代AI協働システム',
                'footer.resources.title': 'リソース',
                'footer.community.title': 'コミュニティ',
                'footer.copyright': '© 2025 TAKAWASIリサーチチーム. MITライセンス下で配布.',
                'footer.made': '人間・AI協働への愛をこめて ❤️'
            }
        };
        this.init();
    }
    
    detectLanguage() {
        // Check URL parameter first
        const urlParams = new URLSearchParams(window.location.search);
        const langParam = urlParams.get('lang');
        if (langParam && (langParam === 'en' || langParam === 'ja')) {
            return langParam;
        }
        
        // Check localStorage
        const savedLang = localStorage.getItem('sca-language');
        if (savedLang && (savedLang === 'en' || savedLang === 'ja')) {
            return savedLang;
        }
        
        // Detect browser language
        const browserLang = navigator.language || navigator.userLanguage;
        if (browserLang.startsWith('ja')) {
            return 'ja';
        }
        
        return 'en'; // Default to English
    }
    
    init() {
        this.createLanguageSwitcher();
        this.updateContent();
        this.bindEvents();
    }
    
    createLanguageSwitcher() {
        // Create language switcher in navigation
        const nav = document.querySelector('.nav-menu');
        if (nav) {
            const langSwitcher = document.createElement('li');
            langSwitcher.className = 'language-switcher';
            langSwitcher.innerHTML = `
                <div class="lang-toggle">
                    <button class="lang-btn ${this.currentLanguage === 'en' ? 'active' : ''}" data-lang="en">
                        <span class="lang-text">English</span>
                    </button>
                    <button class="lang-btn ${this.currentLanguage === 'ja' ? 'active' : ''}" data-lang="ja">
                        <span class="lang-text">日本語</span>
                    </button>
                </div>
            `;
            
            // Insert before GitHub link
            const githubLink = nav.querySelector('.github-link').parentElement;
            nav.insertBefore(langSwitcher, githubLink);
        }
    }
    
    updateContent() {
        // Update all translatable elements
        document.querySelectorAll('[data-i18n]').forEach(element => {
            const key = element.getAttribute('data-i18n');
            const translation = this.getTranslation(key);
            if (translation) {
                if (element.tagName === 'INPUT' && element.type === 'submit') {
                    element.value = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });
        
        // Update document language attribute
        document.documentElement.lang = this.currentLanguage;
        
        // Update page title
        if (this.currentLanguage === 'ja') {
            document.title = 'SCA - 共生認知アーキテクチャ';
        } else {
            document.title = 'SCA - Symbiotic Cognitive Architecture';
        }
        
        // Update meta description
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            if (this.currentLanguage === 'ja') {
                metaDesc.content = '真の人間・AI協働を実現する次世代コラボレーションフレームワーク';
            } else {
                metaDesc.content = 'Next-generation AI collaboration framework enabling true human-AI symbiosis';
            }
        }
    }
    
    getTranslation(key) {
        return this.translations[this.currentLanguage][key] || key;
    }
    
    switchLanguage(lang) {
        if (lang !== 'en' && lang !== 'ja') return;
        
        this.currentLanguage = lang;
        localStorage.setItem('sca-language', lang);
        
        // Update URL parameter without reload
        const url = new URL(window.location);
        url.searchParams.set('lang', lang);
        window.history.replaceState({}, '', url);
        
        this.updateContent();
        this.updateLanguageSwitcher();
    }
    
    updateLanguageSwitcher() {
        document.querySelectorAll('.lang-btn').forEach(btn => {
            const lang = btn.getAttribute('data-lang');
            btn.classList.toggle('active', lang === this.currentLanguage);
        });
    }
    
    bindEvents() {
        // Language switcher click events
        document.addEventListener('click', (e) => {
            if (e.target.closest('.lang-btn')) {
                const lang = e.target.closest('.lang-btn').getAttribute('data-lang');
                this.switchLanguage(lang);
            }
        });
        
        // Keyboard shortcut: Ctrl/Cmd + L to toggle language
        document.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                this.switchLanguage(this.currentLanguage === 'en' ? 'ja' : 'en');
            }
        });
    }
}

// Initialize i18n when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.scaI18n = new SCAInternationalization();
    });
} else {
    window.scaI18n = new SCAInternationalization();
}

// Export for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SCAInternationalization;
}