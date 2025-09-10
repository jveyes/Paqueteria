// ========================================
// SISTEMA DE FILTRADO OPTIMIZADO - MESSAGES.HTML
// ========================================

class MessageFilterSystem {
    constructor() {
        this.cache = new Map();
        this.debounceTimer = null;
        this.isFiltering = false;
        this.currentFilters = {};
        this.messageElements = [];
        this.searchIndex = [];
        
        this.init();
    }

    init() {
        console.log('🚀 Inicializando sistema de filtrado optimizado...');
        this.setupEventListeners();
        this.buildSearchIndex();
        this.loadStoredFilters();
    }

    setupEventListeners() {
        // Búsqueda principal con debounce mejorado
        const searchInput = document.getElementById('searchFilter');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                this.handleSearch(e.target.value);
            });
            
            // Sugerencias de búsqueda
            searchInput.addEventListener('focus', () => {
                this.showSearchSuggestions();
            });
        }

        // Filtros rápidos
        document.getElementById('statusFilter')?.addEventListener('change', () => this.applyFilters());
        document.getElementById('priorityFilter')?.addEventListener('change', () => this.applyFilters());
        document.getElementById('typeFilter')?.addEventListener('change', () => this.applyFilters());
        document.getElementById('unreadOnlyToggle')?.addEventListener('click', () => this.toggleUnreadOnly());
        document.getElementById('clearFilters')?.addEventListener('click', () => this.clearAllFilters());
        document.getElementById('advancedFiltersToggle')?.addEventListener('click', () => this.toggleAdvancedFilters());

        // Filtros avanzados
        document.getElementById('dateFrom')?.addEventListener('change', () => this.applyFilters());
        document.getElementById('dateTo')?.addEventListener('change', () => this.applyFilters());
        document.getElementById('customerFilter')?.addEventListener('input', (e) => this.handleSearch(e.target.value));
        document.getElementById('packageFilter')?.addEventListener('input', (e) => this.handleSearch(e.target.value));

        // Exportar resultados
        document.getElementById('exportResults')?.addEventListener('click', () => this.exportResults());
    }

    buildSearchIndex() {
        console.log('📚 Construyendo índice de búsqueda...');
        this.messageElements = Array.from(document.querySelectorAll('[data-search]'));
        this.searchIndex = this.messageElements.map((element, index) => {
            const searchData = element.getAttribute('data-search') || '';
            const messageData = this.extractMessageData(element);
            
            return {
                index,
                element,
                searchData: searchData.toLowerCase(),
                messageData,
                // Índices específicos para búsqueda rápida
                customerName: (messageData.customer_name || '').toLowerCase(),
                customerPhone: (messageData.customer_phone || '').toLowerCase(),
                content: (messageData.content || '').toLowerCase(),
                subject: (messageData.subject || '').toLowerCase(),
                packageGuide: (messageData.package_guide_number || '').toLowerCase(),
                packageTracking: (messageData.package_tracking_code || '').toLowerCase(),
                status: messageData.status,
                priority: messageData.priority,
                type: messageData.type
            };
        });
        
        console.log(`✅ Índice construido con ${this.searchIndex.length} mensajes`);
    }

    extractMessageData(element) {
        // Extraer datos estructurados del elemento DOM
        const statusElement = element.querySelector('span[class*="bg-"]');
        const statusText = statusElement ? statusElement.textContent.trim() : '';
        
        return {
            customer_name: this.extractTextByIcon(element, 'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z'),
            customer_phone: this.extractTextByIcon(element, 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z'),
            content: element.querySelector('.line-clamp-2')?.textContent || '',
            subject: element.querySelector('h4')?.textContent || '',
            package_guide_number: this.extractTextByIcon(element, 'M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z'),
            status: this.mapStatusText(statusText),
            priority: this.extractPriority(element),
            type: this.extractType(element),
            isUnread: element.classList.contains('border-blue-500')
        };
    }

    extractTextByIcon(element, iconPath) {
        const iconElement = element.querySelector(`svg path[d*="${iconPath}"]`);
        if (iconElement) {
            const parent = iconElement.closest('span');
            return parent ? parent.textContent.trim() : '';
        }
        return '';
    }

    mapStatusText(statusText) {
        const statusMap = {
            'NO LEÍDO': 'unread',
            'PENDIENTE': 'pending',
            'CERRADO': 'closed'
        };
        return statusMap[statusText] || 'unknown';
    }

    extractPriority(element) {
        // Extraer prioridad del elemento (implementar según estructura)
        return 'normal'; // Placeholder
    }

    extractType(element) {
        // Extraer tipo del elemento (implementar según estructura)
        return 'customer_inquiry'; // Placeholder
    }

    handleSearch(searchTerm) {
        // Debounce mejorado
        clearTimeout(this.debounceTimer);
        this.debounceTimer = setTimeout(() => {
            this.currentFilters.search = searchTerm;
            this.applyFilters();
            this.updateSearchIndicator(false);
        }, 300);

        // Mostrar indicador de búsqueda
        this.updateSearchIndicator(true);
    }

    updateSearchIndicator(show) {
        const indicator = document.getElementById('searchIndicator');
        if (indicator) {
            indicator.classList.toggle('hidden', !show);
        }
    }

    applyFilters() {
        if (this.isFiltering) return;
        
        this.isFiltering = true;
        console.log('🔍 Aplicando filtros...', this.currentFilters);
        
        // Recopilar todos los filtros
        this.collectFilters();
        
        // Aplicar filtros con cache
        const cacheKey = this.getCacheKey();
        let visibleElements = this.cache.get(cacheKey);
        
        if (!visibleElements) {
            visibleElements = this.performFiltering();
            this.cache.set(cacheKey, visibleElements);
        }
        
        // Aplicar resultados
        this.updateDisplay(visibleElements);
        this.updateActiveFilters();
        this.updateResultsCount(visibleElements.length);
        
        this.isFiltering = false;
    }

    collectFilters() {
        this.currentFilters = {
            search: document.getElementById('searchFilter')?.value?.toLowerCase().trim() || '',
            status: document.getElementById('statusFilter')?.value || '',
            priority: document.getElementById('priorityFilter')?.value || '',
            type: document.getElementById('typeFilter')?.value || '',
            unreadOnly: document.getElementById('unreadOnlyToggle')?.classList.contains('bg-blue-100') || false,
            dateFrom: document.getElementById('dateFrom')?.value || '',
            dateTo: document.getElementById('dateTo')?.value || '',
            customer: document.getElementById('customerFilter')?.value?.toLowerCase().trim() || '',
            package: document.getElementById('packageFilter')?.value?.toLowerCase().trim() || ''
        };
    }

    getCacheKey() {
        return JSON.stringify(this.currentFilters);
    }

    performFiltering() {
        const visibleElements = [];
        
        this.searchIndex.forEach((item) => {
            if (this.matchesFilters(item)) {
                visibleElements.push(item.element);
            }
        });
        
        return visibleElements;
    }

    matchesFilters(item) {
        // Filtro de búsqueda principal
        if (this.currentFilters.search) {
            const searchTerms = this.currentFilters.search.split(' ').filter(term => term.length > 0);
            const searchFields = [
                item.customerName,
                item.customerPhone,
                item.content,
                item.subject,
                item.packageGuide,
                item.packageTracking
            ].join(' ');
            
            const allTermsFound = searchTerms.every(term => 
                searchFields.includes(term.toLowerCase())
            );
            
            if (!allTermsFound) return false;
        }

        // Filtro por estado
        if (this.currentFilters.status && item.status !== this.currentFilters.status) {
            return false;
        }

        // Filtro por prioridad
        if (this.currentFilters.priority && item.priority !== this.currentFilters.priority) {
            return false;
        }

        // Filtro por tipo
        if (this.currentFilters.type && item.type !== this.currentFilters.type) {
            return false;
        }

        // Filtro solo no leídos
        if (this.currentFilters.unreadOnly && !item.messageData.isUnread) {
            return false;
        }

        // Filtro por cliente
        if (this.currentFilters.customer) {
            const customerFields = [item.customerName, item.customerPhone].join(' ');
            if (!customerFields.includes(this.currentFilters.customer)) {
                return false;
            }
        }

        // Filtro por paquete
        if (this.currentFilters.package) {
            const packageFields = [item.packageGuide, item.packageTracking].join(' ');
            if (!packageFields.includes(this.currentFilters.package)) {
                return false;
            }
        }

        // Filtro por fecha (implementar según necesidad)
        if (this.currentFilters.dateFrom || this.currentFilters.dateTo) {
            // Implementar filtrado por fecha
        }

        return true;
    }

    updateDisplay(visibleElements) {
        // Ocultar todos los elementos
        this.messageElements.forEach(element => {
            element.style.display = 'none';
        });

        // Mostrar elementos visibles
        visibleElements.forEach(element => {
            element.style.display = 'block';
        });

        // Actualizar mensaje de "sin resultados"
        this.updateNoResultsMessage(visibleElements.length === 0);
    }

    updateNoResultsMessage(show) {
        const noMessagesDiv = document.getElementById('noMessages');
        if (noMessagesDiv) {
            noMessagesDiv.classList.toggle('hidden', !show);
        }
    }

    updateActiveFilters() {
        const activeFiltersDiv = document.getElementById('activeFilters');
        if (!activeFiltersDiv) return;

        const activeFilters = Object.entries(this.currentFilters)
            .filter(([key, value]) => value && value !== '')
            .map(([key, value]) => ({ key, value }));

        if (activeFilters.length === 0) {
            activeFiltersDiv.classList.add('hidden');
            return;
        }

        activeFiltersDiv.classList.remove('hidden');
        activeFiltersDiv.innerHTML = activeFilters.map(filter => `
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                ${this.getFilterLabel(filter.key)}: ${filter.value}
                <button onclick="messageFilterSystem.removeFilter('${filter.key}')" class="ml-2 text-blue-600 hover:text-blue-800">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </span>
        `).join('');
    }

    getFilterLabel(key) {
        const labels = {
            search: 'Búsqueda',
            status: 'Estado',
            priority: 'Prioridad',
            type: 'Tipo',
            unreadOnly: 'Solo No Leídos',
            customer: 'Cliente',
            package: 'Paquete',
            dateFrom: 'Desde',
            dateTo: 'Hasta'
        };
        return labels[key] || key;
    }

    removeFilter(key) {
        const element = document.getElementById(this.getElementId(key));
        if (element) {
            if (key === 'unreadOnly') {
                element.classList.remove('bg-blue-100');
            } else {
                element.value = '';
            }
        }
        this.applyFilters();
    }

    getElementId(key) {
        const elementIds = {
            search: 'searchFilter',
            status: 'statusFilter',
            priority: 'priorityFilter',
            type: 'typeFilter',
            unreadOnly: 'unreadOnlyToggle',
            customer: 'customerFilter',
            package: 'packageFilter',
            dateFrom: 'dateFrom',
            dateTo: 'dateTo'
        };
        return elementIds[key] || '';
    }

    updateResultsCount(visibleCount) {
        const resultsCount = document.getElementById('resultsCount');
        const filterStatus = document.getElementById('filterStatus');
        
        if (resultsCount) {
            resultsCount.textContent = `Mostrando ${visibleCount} de ${this.messageElements.length} mensajes`;
        }
        
        if (filterStatus) {
            const activeFiltersCount = Object.values(this.currentFilters).filter(v => v && v !== '').length;
            filterStatus.textContent = activeFiltersCount > 0 ? `${activeFiltersCount} filtro(s) activo(s)` : '';
        }
    }

    toggleUnreadOnly() {
        const button = document.getElementById('unreadOnlyToggle');
        if (button) {
            button.classList.toggle('bg-blue-100');
            this.applyFilters();
        }
    }

    toggleAdvancedFilters() {
        const panel = document.getElementById('advancedFiltersPanel');
        const button = document.getElementById('advancedFiltersToggle');
        
        if (panel && button) {
            panel.classList.toggle('hidden');
            button.classList.toggle('bg-gray-100');
        }
    }

    clearAllFilters() {
        // Limpiar todos los campos de filtro
        document.getElementById('searchFilter').value = '';
        document.getElementById('statusFilter').value = '';
        document.getElementById('priorityFilter').value = '';
        document.getElementById('typeFilter').value = '';
        document.getElementById('customerFilter').value = '';
        document.getElementById('packageFilter').value = '';
        document.getElementById('dateFrom').value = '';
        document.getElementById('dateTo').value = '';
        
        // Limpiar toggle de no leídos
        const unreadButton = document.getElementById('unreadOnlyToggle');
        if (unreadButton) {
            unreadButton.classList.remove('bg-blue-100');
        }
        
        // Limpiar cache
        this.cache.clear();
        
        // Aplicar filtros (mostrar todos)
        this.currentFilters = {};
        this.applyFilters();
        
        // Mostrar notificación
        this.showToast('success', 'Filtros Limpiados', 'Se han removido todos los filtros aplicados.');
    }

    showSearchSuggestions() {
        // Implementar sugerencias de búsqueda
        const suggestionsDiv = document.getElementById('searchSuggestions');
        if (suggestionsDiv) {
            suggestionsDiv.classList.remove('hidden');
            // Cargar sugerencias dinámicamente
        }
    }

    loadStoredFilters() {
        // Cargar filtros guardados del localStorage
        const stored = localStorage.getItem('messageFilters');
        if (stored) {
            try {
                const filters = JSON.parse(stored);
                this.applyStoredFilters(filters);
            } catch (e) {
                console.warn('Error cargando filtros guardados:', e);
            }
        }
    }

    saveFilters() {
        // Guardar filtros actuales en localStorage
        localStorage.setItem('messageFilters', JSON.stringify(this.currentFilters));
    }

    exportResults() {
        // Implementar exportación de resultados
        const visibleElements = this.performFiltering();
        const data = visibleElements.map(element => {
            const item = this.searchIndex.find(item => item.element === element);
            return item ? item.messageData : null;
        }).filter(Boolean);
        
        // Crear CSV o JSON para exportar
        console.log('Exportando resultados:', data);
        this.showToast('info', 'Exportación', 'Los resultados se han preparado para exportar.');
    }

    showToast(type, title, message) {
        // Usar el sistema de toast existente
        if (typeof showToast === 'function') {
            showToast(type, title, message);
        }
    }

    // Método público para reconstruir el índice cuando se cargan nuevos mensajes
    rebuildIndex() {
        console.log('🔄 Reconstruyendo índice de búsqueda...');
        this.buildSearchIndex();
        this.cache.clear();
        this.applyFilters();
    }
}

// Inicializar el sistema cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    window.messageFilterSystem = new MessageFilterSystem();
    
    // Reconstruir índice cuando se cargan nuevos mensajes
    const originalDisplayMessages = window.displayMessages;
    if (originalDisplayMessages) {
        window.displayMessages = function(messages, pagination) {
            originalDisplayMessages(messages, pagination);
            setTimeout(() => {
                window.messageFilterSystem.rebuildIndex();
            }, 100);
        };
    }
});

// Función de conveniencia para filtrado por estado desde las tarjetas
function filterByStatus(status) {
    if (window.messageFilterSystem) {
        document.getElementById('statusFilter').value = status;
        window.messageFilterSystem.applyFilters();
    }
}
