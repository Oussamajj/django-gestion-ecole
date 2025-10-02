// JavaScript principal pour EduManager

document.addEventListener('DOMContentLoaded', function() {
    // Initialisation des tooltips Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialisation des popovers Bootstrap
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Animation des cartes au scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    // Observer toutes les cartes
    document.querySelectorAll('.card').forEach(card => {
        observer.observe(card);
    });

    // Gestion des notifications
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(notification);

        // Auto-suppression après 5 secondes
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    }

    // Gestion des formulaires AJAX
    function handleAjaxForm(formSelector, successCallback) {
        const form = document.querySelector(formSelector);
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                
                const formData = new FormData(form);
                const submitBtn = form.querySelector('button[type="submit"]');
                const originalText = submitBtn.innerHTML;
                
                // Afficher le loading
                submitBtn.innerHTML = '<span class="loading-spinner me-2"></span>Enregistrement...';
                submitBtn.disabled = true;

                fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        showNotification(data.message || 'Opération réussie !', 'success');
                        if (successCallback) successCallback(data);
                        form.reset();
                        // Fermer le modal si présent
                        const modal = form.closest('.modal');
                        if (modal) {
                            bootstrap.Modal.getInstance(modal).hide();
                        }
                    } else {
                        showNotification(data.message || 'Une erreur est survenue', 'danger');
                    }
                })
                .catch(error => {
                    console.error('Erreur:', error);
                    showNotification('Erreur de connexion', 'danger');
                })
                .finally(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                });
            });
        }
    }

    // Gestion de la recherche en temps réel
    function setupLiveSearch(inputSelector, resultsSelector, searchUrl) {
        const searchInput = document.querySelector(inputSelector);
        const resultsContainer = document.querySelector(resultsSelector);
        
        if (searchInput && resultsContainer) {
            let searchTimeout;
            
            searchInput.addEventListener('input', function() {
                const query = this.value.trim();
                
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    if (query.length >= 2) {
                        fetch(`${searchUrl}?q=${encodeURIComponent(query)}`)
                            .then(response => response.json())
                            .then(data => {
                                resultsContainer.innerHTML = data.html;
                            })
                            .catch(error => {
                                console.error('Erreur de recherche:', error);
                            });
                    } else {
                        resultsContainer.innerHTML = '';
                    }
                }, 300);
            });
        }
    }

    // Gestion des filtres dynamiques
    function setupDynamicFilters() {
        const filterSelects = document.querySelectorAll('.dynamic-filter');
        
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                const form = this.closest('form');
                if (form) {
                    // Ajouter un indicateur de chargement
                    const loadingDiv = document.createElement('div');
                    loadingDiv.className = 'text-center my-3';
                    loadingDiv.innerHTML = '<div class="loading-spinner"></div> Filtrage en cours...';
                    
                    const resultsContainer = document.querySelector('.results-container');
                    if (resultsContainer) {
                        resultsContainer.prepend(loadingDiv);
                    }
                    
                    // Soumettre le formulaire
                    form.submit();
                }
            });
        });
    }

    // Gestion des graphiques interactifs
    function setupInteractiveCharts() {
        // Configuration globale pour Chart.js
        if (typeof Chart !== 'undefined') {
            Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
            Chart.defaults.color = '#6c757d';
            Chart.defaults.plugins.legend.labels.usePointStyle = true;
            Chart.defaults.plugins.legend.labels.padding = 20;
        }
    }

    // Gestion du mode sombre
    function setupDarkMode() {
        const darkModeToggle = document.querySelector('#darkModeToggle');
        const body = document.body;
        
        // Vérifier la préférence sauvegardée
        const isDarkMode = localStorage.getItem('darkMode') === 'true';
        if (isDarkMode) {
            body.classList.add('dark-mode');
        }
        
        if (darkModeToggle) {
            darkModeToggle.addEventListener('click', function() {
                body.classList.toggle('dark-mode');
                const isDark = body.classList.contains('dark-mode');
                localStorage.setItem('darkMode', isDark);
                
                // Mettre à jour l'icône
                const icon = this.querySelector('i');
                if (icon) {
                    icon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
                }
            });
        }
    }

    // Gestion des tableaux interactifs
    function setupInteractiveTables() {
        const tables = document.querySelectorAll('.table-interactive');
        
        tables.forEach(table => {
            // Tri des colonnes
            const headers = table.querySelectorAll('th[data-sort]');
            headers.forEach(header => {
                header.style.cursor = 'pointer';
                header.addEventListener('click', function() {
                    const column = this.dataset.sort;
                    sortTable(table, column);
                });
            });
            
            // Sélection multiple
            const selectAllCheckbox = table.querySelector('.select-all');
            if (selectAllCheckbox) {
                selectAllCheckbox.addEventListener('change', function() {
                    const checkboxes = table.querySelectorAll('.select-row');
                    checkboxes.forEach(cb => cb.checked = this.checked);
                    updateBulkActions();
                });
            }
            
            const rowCheckboxes = table.querySelectorAll('.select-row');
            rowCheckboxes.forEach(checkbox => {
                checkbox.addEventListener('change', updateBulkActions);
            });
        });
    }

    function sortTable(table, column) {
        // Implémentation du tri des tableaux
        const tbody = table.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        
        rows.sort((a, b) => {
            const aValue = a.querySelector(`[data-value="${column}"]`)?.textContent || '';
            const bValue = b.querySelector(`[data-value="${column}"]`)?.textContent || '';
            return aValue.localeCompare(bValue);
        });
        
        rows.forEach(row => tbody.appendChild(row));
    }

    function updateBulkActions() {
        const selectedRows = document.querySelectorAll('.select-row:checked');
        const bulkActions = document.querySelector('.bulk-actions');
        
        if (bulkActions) {
            if (selectedRows.length > 0) {
                bulkActions.style.display = 'block';
                bulkActions.querySelector('.selected-count').textContent = selectedRows.length;
            } else {
                bulkActions.style.display = 'none';
            }
        }
    }

    // Gestion des uploads de fichiers
    function setupFileUploads() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        
        fileInputs.forEach(input => {
            input.addEventListener('change', function() {
                const file = this.files[0];
                if (file) {
                    // Validation de la taille
                    const maxSize = 5 * 1024 * 1024; // 5MB
                    if (file.size > maxSize) {
                        showNotification('Le fichier est trop volumineux (max 5MB)', 'warning');
                        this.value = '';
                        return;
                    }
                    
                    // Prévisualisation pour les images
                    if (file.type.startsWith('image/')) {
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            const preview = document.querySelector(`#preview-${input.id}`);
                            if (preview) {
                                preview.src = e.target.result;
                                preview.style.display = 'block';
                            }
                        };
                        reader.readAsDataURL(file);
                    }
                }
            });
        });
    }

    // Gestion des raccourcis clavier
    function setupKeyboardShortcuts() {
        document.addEventListener('keydown', function(e) {
            // Ctrl/Cmd + S pour sauvegarder
            if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                e.preventDefault();
                const saveBtn = document.querySelector('.btn-save, button[type="submit"]');
                if (saveBtn) saveBtn.click();
            }
            
            // Échap pour fermer les modals
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.show');
                if (openModal) {
                    bootstrap.Modal.getInstance(openModal).hide();
                }
            }
            
            // Ctrl/Cmd + K pour la recherche
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = document.querySelector('.search-input, input[type="search"]');
                if (searchInput) {
                    searchInput.focus();
                    searchInput.select();
                }
            }
        });
    }

    // Gestion de la pagination AJAX
    function setupAjaxPagination() {
        const paginationLinks = document.querySelectorAll('.pagination a');
        
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                const url = this.href;
                
                fetch(url)
                    .then(response => response.text())
                    .then(html => {
                        const parser = new DOMParser();
                        const doc = parser.parseFromString(html, 'text/html');
                        const newContent = doc.querySelector('.results-container');
                        const currentContent = document.querySelector('.results-container');
                        
                        if (newContent && currentContent) {
                            currentContent.innerHTML = newContent.innerHTML;
                            // Réinitialiser les event listeners
                            setupInteractiveTables();
                        }
                    })
                    .catch(error => {
                        console.error('Erreur de pagination:', error);
                        showNotification('Erreur lors du chargement de la page', 'danger');
                    });
            });
        });
    }

    // Initialisation de tous les composants
    function initializeComponents() {
        setupDynamicFilters();
        setupInteractiveCharts();
        setupDarkMode();
        setupInteractiveTables();
        setupFileUploads();
        setupKeyboardShortcuts();
        setupAjaxPagination();
        
        // Initialiser les formulaires AJAX spécifiques
        handleAjaxForm('#studentForm', function(data) {
            // Callback pour l'ajout d'étudiant
            location.reload();
        });
        
        handleAjaxForm('#teacherForm', function(data) {
            // Callback pour l'ajout d'enseignant
            location.reload();
        });
        
        handleAjaxForm('#courseForm', function(data) {
            // Callback pour l'ajout de cours
            location.reload();
        });
        
        handleAjaxForm('#noteForm', function(data) {
            // Callback pour l'ajout de note
            location.reload();
        });
    }

    // Utilitaires globaux
    window.EduManager = {
        showNotification: showNotification,
        setupLiveSearch: setupLiveSearch,
        handleAjaxForm: handleAjaxForm
    };

    // Initialiser tous les composants
    initializeComponents();

    // Afficher un message de bienvenue
    console.log('🎓 EduManager - Système de Gestion Scolaire initialisé avec succès !');
});

// Fonctions utilitaires globales
function formatDate(date) {
    return new Intl.DateTimeFormat('fr-FR', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    }).format(new Date(date));
}

function formatNumber(number) {
    return new Intl.NumberFormat('fr-FR').format(number);
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Gestion des erreurs globales
window.addEventListener('error', function(e) {
    console.error('Erreur JavaScript:', e.error);
    // Ne pas afficher d'erreur à l'utilisateur en production
});

// Gestion des promesses rejetées
window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rejetée:', e.reason);
    e.preventDefault();
});
