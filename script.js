// Spy x Family Online - Secure Line Orchestration
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // --- Dossier Menu Toggle (Site-wide) ---
    window.toggleDossier = (e) => {
        if (e) e.stopPropagation();
        const menu = document.getElementById('dossierMenu');
        if (menu) {
            menu.classList.toggle('active');
            console.log('[INTEL]: Dossier archive access toggled.');
        }
    };

    // --- Global Click Management (Menus & Dropdowns) ---
    document.addEventListener('click', (e) => {
        // Dossier Menu / Sidebar
        const dossierMenu = document.getElementById('dossierMenu');
        const dossierTabBtn = document.querySelector('.dossier-tab-btn');
        if (dossierMenu && dossierMenu.classList.contains('active')) {
            const isClickInsideMenu = dossierMenu.contains(e.target);
            const isClickOnToggle = dossierTabBtn && dossierTabBtn.contains(e.target);
            
            if (!isClickInsideMenu && !isClickOnToggle) {
                dossierMenu.classList.remove('active');
                console.log('[INTEL]: Dossier archive auto-closed.');
            }
        }

        // Mission Log Dropdown (Index)
        const missionDropdown = document.getElementById('mission-log-dropdown');
        const missionLogBtn = document.querySelector('.MissionLogBtn');
        if (missionDropdown && missionDropdown.classList.contains('active')) {
            const isClickInsideDropdown = missionDropdown.contains(e.target);
            const isClickOnToggle = missionLogBtn && (missionLogBtn.contains(e.target) || e.target === missionLogBtn);
            
            if (!isClickInsideDropdown && !isClickOnToggle) {
                missionDropdown.classList.remove('active');
                console.log('[INTEL]: Mission log auto-closed.');
            }
        }
    });

    // 2. Scroll Progress & HUD Elements
    const progressBar = document.querySelector('.read-progress-bar');
    const stellaStar = document.querySelector('.stella-star-indicator');
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    const scrollBottomBtn = document.getElementById('scroll-bottom-btn');
    
    const updateScrollProgress = () => {
        const winScroll = window.scrollY;
        const height = document.documentElement.scrollHeight - window.innerHeight;
        if (height <= 0) return;
        const scrolled = (winScroll / height) * 100;
        
        if (progressBar) progressBar.style.width = scrolled + '%';
        if (stellaStar) {
            stellaStar.style.top = scrolled + '%';
            stellaStar.style.opacity = scrolled > 1 ? '1' : '0.2';
        }

        // Show/Hide Scroll Top FAB
        if (scrollTopBtn) {
            if (winScroll > 400) {
                scrollTopBtn.classList.remove('opacity-0', 'pointer-events-none');
            } else {
                scrollTopBtn.classList.add('opacity-0', 'pointer-events-none');
            }
        }
    };

    window.addEventListener('scroll', updateScrollProgress, { passive: true });
    updateScrollProgress();

    // 3. Floating Action Buttons Listeners
    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    if (scrollBottomBtn) {
        scrollBottomBtn.addEventListener('click', () => {
            window.scrollTo({ top: document.documentElement.scrollHeight, behavior: 'smooth' });
        });
    }

    // 4. Mission Archive Grid Management
    const missionItems = Array.from(document.querySelectorAll('.mission-item'));
    const loadMoreBtn = document.getElementById('load-more-missions');
    const intelSearch = document.getElementById('intel-search');
    const gridContainer = document.getElementById('intelligence-grid');
    const sortDesc = document.getElementById('sort-desc');
    const sortAsc = document.getElementById('sort-asc');
    
    let visibleCount = 20;
    const INCREMENT = 24;

    const animateItems = (targets) => {
        if (typeof anime !== 'undefined') {
            anime({
                targets: targets,
                opacity: [0, 1],
                translateY: [20, 0],
                scale: [0.95, 1],
                delay: anime.stagger(50),
                duration: 800,
                easing: 'easeOutExpo'
            });
        }
    };

    const updateGridVisibility = (term = '', animate = false) => {
        const q = term.toLowerCase().trim();
        let matchesFound = 0;
        const newlyVisible = [];

        missionItems.forEach((item, index) => {
            const title = item.getAttribute('data-title') || '';
            const id = item.getAttribute('data-id') || '';
            const isMatch = title.toLowerCase().includes(q) || id.toLowerCase().includes(q);
            
            const wasHidden = item.style.display === 'none';

            if (q !== '') {
                const show = isMatch;
                item.style.display = show ? 'block' : 'none';
                if (show) {
                    matchesFound++;
                    if (wasHidden && animate) newlyVisible.push(item);
                }
            } else {
                if (index < visibleCount) {
                    item.style.display = 'block';
                    matchesFound++;
                    if (wasHidden && animate) newlyVisible.push(item);
                } else {
                    item.style.display = 'none';
                }
            }
        });

        if (animate && newlyVisible.length > 0) {
            animateItems(newlyVisible);
        }

        // Toggle Load More button
        if (loadMoreBtn) {
            const container = loadMoreBtn.closest('.load-more-container') || loadMoreBtn.parentElement;
            if (q !== '' || visibleCount >= missionItems.length) {
                container.style.display = 'none';
            } else {
                container.style.display = 'flex';
            }
        }
    };

    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', () => {
            visibleCount += INCREMENT;
            updateGridVisibility(intelSearch?.value || '', true);
            console.log(`[INTEL]: Expanded visibility to top ${visibleCount} missions.`);
        });
    }

    if (intelSearch) {
        intelSearch.addEventListener('input', (e) => {
            updateGridVisibility(e.target.value);
        });
    }

    // 5. Sorting Orchestration
    const applySort = (order) => {
        if (!gridContainer) return;
        
        // Brief fade out before reorder
        if (typeof anime !== 'undefined') {
            anime({
                targets: '#intelligence-grid',
                opacity: [1, 0.5],
                duration: 200,
                easing: 'linear',
                complete: () => {
                    performSort(order);
                    anime({
                        targets: '#intelligence-grid',
                        opacity: [0.5, 1],
                        duration: 400,
                        easing: 'linear'
                    });
                }
            });
        } else {
            performSort(order);
        }
    };

    const performSort = (order) => {
        const sorted = [...missionItems].sort((a, b) => {
            const valA = parseFloat(a.dataset.id);
            const valB = parseFloat(b.dataset.id);
            return order === 'desc' ? valB - valA : valA - valB;
        });
        
        const fragment = document.createDocumentFragment();
        sorted.forEach(el => fragment.appendChild(el));
        gridContainer.innerHTML = '';
        gridContainer.appendChild(fragment);
        
        // Update the stored reference array to match the new DOM order
        missionItems.length = 0;
        missionItems.push(...sorted);
        
        updateGridVisibility(intelSearch?.value || '', true);
    };

    if (sortDesc) sortDesc.addEventListener('click', () => applySort('desc'));
    if (sortAsc) sortAsc.addEventListener('click', () => applySort('asc'));

    // Synchronize Hero/Header Buttons with Grid
    const heroStartBtn = document.querySelector('a[href*="chapter-001"]');
    const heroLatestBtn = document.querySelector('a[href*="chapter-131"]');

    if (heroStartBtn && heroStartBtn.textContent.includes('START')) {
        heroStartBtn.addEventListener('click', (e) => {
            if (!e.target.closest('nav')) { // Only if clicking the hero button, not nav links if any
                e.preventDefault();
                applySort('asc');
                document.getElementById('mission-archive-root').scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    if (heroLatestBtn && heroLatestBtn.textContent.includes('LATEST')) {
        heroLatestBtn.addEventListener('click', (e) => {
            if (!e.target.closest('nav')) {
                e.preventDefault();
                applySort('desc');
                document.getElementById('mission-archive-root').scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // --- Mission Log Dropdown Toggle ---
    const missionLogBtn = document.querySelector('.MissionLogBtn');
    const missionDropdown = document.getElementById('mission-log-dropdown');
    
    if (missionLogBtn && missionDropdown) {
        missionLogBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            missionDropdown.classList.toggle('active');
            console.log('[INTEL]: Mission log dropdown toggled.');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', (e) => {
            if (!missionDropdown.contains(e.target) && !missionLogBtn.contains(e.target)) {
                missionDropdown.classList.remove('active');
            }
        });
    }

    // 5b. Author Dossier Toggle Logic
    const authorToggle = document.getElementById('author-dossier-toggle');
    const authorContent = document.getElementById('author-dossier-content');
    if (authorToggle && authorContent) {
        authorToggle.addEventListener('click', (e) => {
            e.preventDefault();
            authorToggle.classList.toggle('active');
            authorContent.classList.toggle('active');
            
            // Rotate icon if lucide is present
            const icon = authorToggle.querySelector('i');
            if (icon) {
                icon.style.transform = authorContent.classList.contains('active') ? 'rotate(180deg)' : 'rotate(0deg)';
            }
        });
    }

    // 6. Universal Mission Search Orchestration
    const initializeSearch = () => {
        const searchInputs = document.querySelectorAll('#mission-header-search, #mission-sidebar-search, #mission-sidebar-search-trigger, #intel-search');
        
        searchInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const term = e.target.value.toLowerCase().trim();
                const inputId = input.getAttribute('id');
                
                // Determine which container to filter
                let container;
                if (inputId === 'intel-search') {
                    if (typeof updateGridVisibility === 'function') {
                        updateGridVisibility(term);
                    }
                    return;
                } else if (inputId === 'mission-sidebar-search-trigger' || inputId === 'mission-sidebar-search') {
                    // For chapter pages sidebar or legacy sidebar IDs
                    container = document.getElementById('missionLogList') || document.getElementById('mission-dropdown-list');
                } else if (inputId === 'mission-header-search') {
                    // For header dropdown
                    container = document.getElementById('mission-dropdown-list');
                } else {
                    container = document.getElementById('mission-dropdown-list') || document.getElementById('missionLogList');
                }

                if (container) {
                    const links = container.querySelectorAll('a');
                    links.forEach(link => {
                        const text = link.textContent.toLowerCase();
                        if (text.includes(term)) {
                            link.style.display = 'block';
                            link.classList.remove('hidden');
                        } else {
                            link.style.display = 'none';
                            link.classList.add('hidden');
                        }
                    });
                }
            });

            // Prevent closing menus when clicking search bar
            input.addEventListener('click', (e) => e.stopPropagation());
        });
    };
    initializeSearch();

    // 7. Tactical Scroll Navigation
    const scrollNav = document.querySelector('.scroll-nav');
    const scrollTopBtn = document.getElementById('scroll-top-btn');
    const scrollBottomBtn = document.getElementById('scroll-bottom-btn');

    window.addEventListener('scroll', () => {
        if (scrollNav) {
            if (window.scrollY > 400) {
                scrollNav.classList.add('visible');
            } else {
                scrollNav.classList.remove('visible');
            }
        }
    });

    if (scrollTopBtn) {
        scrollTopBtn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    if (scrollBottomBtn) {
        scrollBottomBtn.addEventListener('click', () => {
            window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
        });
    }

    // 6b. Mobile Search Trigger
    const mobileSearchTrigger = document.getElementById('mobile-search-trigger');
    if (mobileSearchTrigger) {
        mobileSearchTrigger.addEventListener('click', (e) => {
            e.preventDefault();
            const desktopSearchBtn = document.querySelector('.MissionLogBtn');
            if (desktopSearchBtn) {
                // Focus and show the search dropdown by simulating hover or just focusing the input
                const input = document.getElementById('mission-sidebar-search');
                if (input) {
                    input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    input.focus();
                }
            }
        });
    }

    // 7. Reveal Scroll Observer
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('reveal-active');
                
                // Special handling for tactical reports to trigger anime.js
                if (entry.target.classList.contains('tactical-report-box')) {
                    const textContent = entry.target.querySelector('.prose');
                    if (textContent && typeof anime !== 'undefined') {
                        anime({
                            targets: textContent,
                            opacity: [0, 1],
                            translateY: [20, 0],
                            duration: 1200,
                            easing: 'easeOutExpo'
                        });
                    }
                }
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.reveal, .mission-item, .tactical-report-box').forEach(el => {
        revealObserver.observe(el);
    });

    // 8. Hero Parallax & HUD Motion (Disabled as per user request for static image)
    const heroBg = document.querySelector('.hero-silhouette');
    const heroCard = document.querySelector('.glass-hero-card');
    /* 
    if (heroBg) {
        window.addEventListener('scroll', () => {
            const scroll = window.pageYOffset;
            heroBg.style.backgroundPositionY = (scroll * 0.4) + 'px';
            if(heroCard) {
                heroCard.style.transform = `translateY(${scroll * 0.1}px)`;
            }
        }, { passive: true });
    }
    */

    // 9. Author Dossier Logic
    const authorToggle = document.getElementById('author-dossier-toggle');
    const authorContent = document.getElementById('author-dossier-content');
    
    if (authorToggle && authorContent) {
        authorToggle.addEventListener('click', () => {
            const isActive = authorContent.classList.contains('active');
            authorContent.classList.toggle('hidden', isActive);
            authorContent.classList.toggle('active'); 
            
            if (typeof anime !== 'undefined') {
                anime({
                    targets: authorToggle.querySelector('i'),
                    rotate: authorContent.classList.contains('active') ? 180 : 0,
                    duration: 400,
                    easing: 'easeOutBack'
                });
                
                if (authorContent.classList.contains('active')) {
                   anime({
                       targets: authorContent,
                       opacity: [0, 1],
                       translateY: [-10, 0],
                       duration: 600,
                       easing: 'easeOutExpo'
                   });
                }
            }
        });
    }

    // 10. Tactical Archive Report Injection with Decrypt Effect
    const tacticalReport = document.getElementById('home-tactical-report');
    if (tacticalReport) {
        const reportContent = `
            <div class="space-y-8 text-white/70 leading-relaxed font-light opacity-0" id="tactical-text-wrapper">
                <p class="text-lg first-letter:text-5xl first-letter:font-bold first-letter:text-[#064e3b] first-letter:mr-3 first-letter:float-left">
                    Operation Strix represents the most complex geopolitical chess move in the modern history of the Ostania-Westalis cold war. Orchestrated by the Westalis Intelligence Service's Eastern Division, the objective is centered around capturing the reclusive Donovan Desmond, chairman of the National Unity Party. However, the mechanism of proximity—the Eden Academy's social ecosystem—requires a multi-layered infiltration unit composed of contrasting psychological profiles.
                </p>
                
                <h3 class="text-2xl font-['DM_Serif_Display'] text-white mt-12 mb-4 border-l-4 border-[#064e3b] pl-6">I. The Forger Dossier: Multi-Layered Deception</h3>
                <p>
                    The core of the unit, Loid Forger (Agent Twilight), operates under a zero-compromise Prime Directive. His specialized training in psycho-analysis and tactical combat is constantly tested by the chaotic variables of the 'found family' dynamic. Twilight's ability to maintain a fabricated civilian persona while managing high-stakes intelligence extraction is unparalleled, yet the report suggests a gradual erosion of his purely clinical detachment—a variable Wise command must monitor closely.
                </p>
                <p>
                    Complementing the primary agent is Yor Forger (Codename: Thorn Princess). While her civilian background as a Berlint City Hall clerk provides the perfect cover, her primary utility lies in her role as the premier wetwork operative for the Garden. Her inclusion in the Forger unit was an accidental synergy; she provides the necessary deterrent force and physical security for the unit while maintaining a facade of domestic normalcy that even Twilight's keen senses find difficult to fully deconstruct.
                </p>

                <h3 class="text-2xl font-['DM_Serif_Display'] text-white mt-12 mb-4 border-l-4 border-[#064e3b] pl-6">II. The Esper Variable: Subject 007</h3>
                <p>
                    Anya Forger, officially the unit's daughter, serves as the most critical yet volatile element of Operation Strix. Unknown to Wise, Anya possesses telepathic capabilities resulting from experimental research. This allows her to bridge the intelligence gap between Loid and Yor, often intervening to prevent the unit's dissolution or compromising exposure. Her objective—becoming an Imperial Scholar at Eden Academy—is the bottleneck through which the entire mission's success flows.
                </p>
                <p>
                    Tactical analysis of her performance at Eden Academy reveals a high incidence of social friction but an impressive resilience. Her pursuit of 'Stella Stars'—the Academy's highest honors—is currently the primary metric for mission progress.
                </p>

                <h3 class="text-2xl font-['DM_Serif_Display'] text-white mt-12 mb-4 border-l-4 border-[#064e3b] pl-6">III. Geopolitical Implications of a Potential Leak</h3>
                <p>
                    Should Operation Strix face catastrophic failure, the resulting diplomatic fallout would likely trigger a full-scale kinetic conflict. Berlint, the focal point of this tension, sits on a powder keg of extremist National Unity Party supporters and Westalian hawks. The preservation of the Forger family facade is not merely a mission requirement; it is a global security imperative.
                </p>
                
                <div class="p-8 border-y border-[#064e3b]/20 bg-[#064e3b]/5 italic text-sm text-[#064e3b] my-12">
                    "[FINAL_JUDGMENT]: Operation Strix remains at high risk but shows significant potential for intelligence breakthrough. Recommend continued funding and oversight of the Forger Asset." – WISE Command Zero.
                </div>

                <p>
                    As the narrative of Spy x Family unfolds, the definition of 'mission success' continues to evolve. What began as a clinical infiltration has transformed into a profound exploration of human connection, isolation, and the sacrifices made in the pursuit of a future where children don't have to cry. This portal will continue to monitor all developments in the Berlint Sector as new intel becomes available.
                </p>
            </div>
        `;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    tacticalReport.innerHTML = reportContent;
                    if (typeof anime !== 'undefined') {
                        anime({
                            targets: '#tactical-text-wrapper',
                            opacity: [0, 1],
                            translateY: [30, 0],
                            duration: 1500,
                            easing: 'easeOutExpo'
                        });
                        
                        // Decrypt glitch effect for headings
                        anime({
                            targets: '#tactical-text-wrapper h3',
                            translateY: [10, 0],
                            opacity: [0, 1],
                            delay: anime.stagger(500),
                            duration: 1000,
                            easing: 'easeOutQuad'
                        });
                    }
                    if (typeof lucide !== 'undefined') lucide.createIcons();
                    observer.unobserve(tacticalReport);
                }
            });
        }, { threshold: 0.2 });

        observer.observe(tacticalReport);
    }

    // 11. Initial HUD Sync
    updateGridVisibility('', true);

    // 12. PWA Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js').then(registration => {
                console.log('WISE SW Registered with scope:', registration.scope);
            }).catch(err => {
                console.log('WISE SW Registration failed:', err);
            });
        });
    }
});
