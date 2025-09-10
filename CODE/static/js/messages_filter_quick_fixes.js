// ========================================
// MEJORAS RÁPIDAS PARA EL SISTEMA DE FILTRADO ACTUAL
// ========================================

// 1. SISTEMA DE CACHE SIMPLE
const filterCache = new Map();
const CACHE_SIZE_LIMIT = 50; // Máximo 50 entradas en cache

// 2. CONFIGURACIÓN DE DEBUG
const DEBUG = false; // Cambiar a true para desarrollo
const log = DEBUG ? console.log : () => {};

// 3. CACHE DE ELEMENTOS DOM
const domElements = {
    searchInput: null,
    statusFilter: null,
    priorityFilter: null,
    typeFilter: null,
    unreadOnly: null,
    messageCards: null
};

// 4. INICIALIZAR CACHE DE ELEMENTOS
function initializeDOMElements() {
    domElements.searchInput = document.getElementById('searchFilter');
    domElements.statusFilter = document.getElementById('statusFilter');
    domElements.priorityFilter = document.getElementById('priorityFilter');
    domElements.typeFilter = document.getElementById('typeFilter');
    domElements.unreadOnly = document.getElementById('unreadOnly');
    domElements.messageCards = document.querySelectorAll('[data-search]');
}

// 5. DEBOUNCE OPTIMIZADO CON INDICADOR
function createOptimizedDebounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
            hideSearchIndicator();
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        showSearchIndicator();
    };
}

// 6. INDICADORES VISUALES
function showSearchIndicator() {
    const indicator = document.getElementById('searchIndicator');
    if (indicator) {
        indicator.classList.remove('hidden');
    }
}

function hideSearchIndicator() {
    const indicator = document.getElementById('searchIndicator');
    if (indicator) {
        indicator.classList.add('hidden');
    }
}

// 7. FUNCIÓN DE FILTRADO OPTIMIZADA
function applyMessageFilterOptimized() {
    const startTime = performance.now();
    
    // Inicializar elementos DOM si no están cacheados
    if (!domElements.messageCards) {
        initializeDOMElements();
    }
    
    // Recopilar filtros una sola vez
    const filters = {
        status: domElements.statusFilter?.value || '',
        search: domElements.searchInput?.value?.toLowerCase().trim() || '',
        priority: domElements.priorityFilter?.value || '',
        type: domElements.typeFilter?.value || '',
        unreadOnly: domElements.unreadOnly?.checked || false
    };
    
    // Generar clave de cache
    const cacheKey = JSON.stringify(filters);
    
    // Verificar cache
    if (filterCache.has(cacheKey)) {
        log('🎯 Usando cache para filtros:', filters);
        applyCachedResults(filterCache.get(cacheKey));
        return;
    }
    
    // Aplicar filtros
    const visibleElements = [];
    const messageCards = domElements.messageCards;
    
    if (!messageCards || messageCards.length === 0) {
        log('⚠️ No se encontraron mensajes para filtrar');
        return;
    }
    
    messageCards.forEach((card, index) => {
        if (matchesFiltersOptimized(card, filters)) {
            visibleElements.push(card);
        }
    });
    
    // Limpiar cache si excede el límite
    if (filterCache.size >= CACHE_SIZE_LIMIT) {
        const firstKey = filterCache.keys().next().value;
        filterCache.delete(firstKey);
    }
    
    // Guardar en cache
    filterCache.set(cacheKey, visibleElements);
    
    // Aplicar resultados
    applyCachedResults(visibleElements);
    
    // Log de rendimiento
    const duration = performance.now() - startTime;
    log(`⚡ Filtrado completado en ${duration.toFixed(2)}ms - ${visibleElements.length} resultados`);
}

// 8. FUNCIÓN DE MATCHING OPTIMIZADA
function matchesFiltersOptimized(card, filters) {
    // Filtro por estado (optimizado)
    if (filters.status) {
        const statusElement = card.querySelector('span[class*="bg-"]');
        const statusText = statusElement ? statusElement.textContent.trim() : '';
        const statusMap = {
            'unread': 'NO LEÍDO',
            'pending': 'PENDIENTE',
            'closed': 'CERRADO'
        };
        
        if (statusText !== statusMap[filters.status]) {
            return false;
        }
    }
    
    // Filtro de búsqueda (optimizado)
    if (filters.search) {
        const searchData = card.getAttribute('data-search') || '';
        const searchTerms = filters.search.split(' ').filter(term => term.length > 0);
        
        // Búsqueda optimizada: verificar todos los términos
        const allTermsFound = searchTerms.every(term => 
            searchData.includes(term.toLowerCase())
        );
        
        if (!allTermsFound) {
            return false;
        }
    }
    
    // Filtro por prioridad (optimizado)
    if (filters.priority) {
        const searchData = card.getAttribute('data-search') || '';
        if (!searchData.includes(filters.priority.toLowerCase())) {
            return false;
        }
    }
    
    // Filtro por tipo (optimizado)
    if (filters.type) {
        const searchData = card.getAttribute('data-search') || '';
        if (!searchData.includes(filters.type.toLowerCase())) {
            return false;
        }
    }
    
    // Filtro solo no leídos (optimizado)
    if (filters.unreadOnly) {
        if (!card.classList.contains('border-blue-500')) {
            return false;
        }
    }
    
    return true;
}

// 9. APLICAR RESULTADOS CACHEADOS
function applyCachedResults(visibleElements) {
    // Ocultar todos los elementos
    domElements.messageCards.forEach(card => {
        card.style.display = 'none';
    });
    
    // Mostrar elementos visibles
    visibleElements.forEach(card => {
        card.style.display = 'block';
    });
    
    // Actualizar contador
    updateMessageCounterOptimized(visibleElements.length);
    
    // Mostrar mensaje si no hay resultados
    showNoMessagesMessage(visibleElements.length === 0);
}

// 10. CONTADOR OPTIMIZADO
function updateMessageCounterOptimized(visibleCount) {
    const totalMessages = domElements.messageCards ? domElements.messageCards.length : 0;
    const counterElement = document.querySelector('.text-sm.text-gray-500');
    
    if (counterElement) {
        counterElement.textContent = `Mostrando ${visibleCount} de ${totalMessages} mensajes`;
    }
}

// 11. FUNCIÓN DE BÚSQUEDA OPTIMIZADA
function createOptimizedSearchHandler() {
    const debouncedSearch = createOptimizedDebounce(applyMessageFilterOptimized, 200);
    
    return function(event) {
        log('🔍 Evento de búsqueda disparado');
        debouncedSearch();
    };
}

// 12. LIMPIAR CACHE
function clearFilterCache() {
    filterCache.clear();
    log('🗑️ Cache de filtros limpiado');
}

// 13. INICIALIZAR SISTEMA OPTIMIZADO
function initializeOptimizedFiltering() {
    log('🚀 Inicializando sistema de filtrado optimizado...');
    
    // Inicializar elementos DOM
    initializeDOMElements();
    
    // Crear manejador de búsqueda optimizado
    const searchHandler = createOptimizedSearchHandler();
    
    // Reemplazar event listeners existentes
    if (domElements.searchInput) {
        domElements.searchInput.removeEventListener('input', searchHandler);
        domElements.searchInput.addEventListener('input', searchHandler);
    }
    
    // Aplicar filtro inicial
    applyMessageFilterOptimized();
    
    log('✅ Sistema de filtrado optimizado inicializado');
}

// 14. FUNCIÓN DE REEMPLAZO PARA applyMessageFilter
function replaceApplyMessageFilter() {
    // Guardar referencia a la función original
    if (typeof window.applyMessageFilter === 'function') {
        window.applyMessageFilterOriginal = window.applyMessageFilter;
    }
    
    // Reemplazar con versión optimizada
    window.applyMessageFilter = applyMessageFilterOptimized;
    
    log('🔄 applyMessageFilter reemplazada con versión optimizada');
}

// 15. FUNCIÓN DE LIMPIEZA MEJORADA
function clearFiltersOptimized() {
    // Limpiar campos
    if (domElements.searchInput) domElements.searchInput.value = '';
    if (domElements.statusFilter) domElements.statusFilter.value = '';
    if (domElements.priorityFilter) domElements.priorityFilter.value = '';
    if (domElements.typeFilter) domElements.typeFilter.value = '';
    if (domElements.unreadOnly) domElements.unreadOnly.checked = false;
    
    // Limpiar cache
    clearFilterCache();
    
    // Aplicar filtros (mostrar todos)
    applyMessageFilterOptimized();
    
    // Mostrar notificación
    if (typeof showInfoToast === 'function') {
        showInfoToast('Filtros Limpiados', 'Se han removido todos los filtros aplicados.', 2000);
    }
}

// 16. INICIALIZACIÓN AUTOMÁTICA
document.addEventListener('DOMContentLoaded', function() {
    // Esperar un poco para que se carguen los mensajes
    setTimeout(() => {
        initializeOptimizedFiltering();
        replaceApplyMessageFilter();
        
        // Reemplazar función de limpiar filtros
        const clearButton = document.getElementById('clearFilters');
        if (clearButton) {
            clearButton.onclick = clearFiltersOptimized;
        }
    }, 1000);
});

// 17. FUNCIÓN DE DIAGNÓSTICO
function diagnoseFilteringPerformance() {
    console.log('🔍 Diagnóstico del sistema de filtrado:');
    console.log(`- Elementos DOM cacheados: ${Object.keys(domElements).length}`);
    console.log(`- Mensajes disponibles: ${domElements.messageCards ? domElements.messageCards.length : 0}`);
    console.log(`- Entradas en cache: ${filterCache.size}`);
    console.log(`- Modo debug: ${DEBUG}`);
    
    // Probar rendimiento
    const startTime = performance.now();
    applyMessageFilterOptimized();
    const duration = performance.now() - startTime;
    console.log(`- Tiempo de filtrado: ${duration.toFixed(2)}ms`);
}

// 18. EXPORTAR FUNCIONES PARA USO GLOBAL
window.filteringOptimizations = {
    initialize: initializeOptimizedFiltering,
    clearCache: clearFilterCache,
    diagnose: diagnoseFilteringPerformance,
    applyFilters: applyMessageFilterOptimized
};
