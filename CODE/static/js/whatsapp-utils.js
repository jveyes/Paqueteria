/**
 * WhatsApp Utils - Módulo para manejo de enlaces de WhatsApp
 * Versión: 1.0.0
 * Autor: PAQUETES EL CLUB v3.5
 * 
 * Este módulo proporciona funcionalidades para crear enlaces de WhatsApp
 * de manera reutilizable y configurable.
 */

class WhatsAppUtils {
    constructor(options = {}) {
        // Configuración por defecto
        this.config = {
            defaultCountryCode: '+57', // Colombia por defecto
            defaultMessage: 'Hola, tengo una consulta sobre mi paquete',
            iconSize: 'w-4 h-4',
            linkClass: 'inline-flex items-center text-green-600 hover:text-green-700 transition-colors duration-200',
            fallbackText: 'Sin teléfono',
            fallbackClass: 'text-sm text-gray-500',
            ...options
        };
        
        // Icono SVG de WhatsApp
        this.whatsappIcon = `
            <svg class="${this.config.iconSize} mr-1" fill="currentColor" viewBox="0 0 24 24">
                <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893A11.821 11.821 0 0020.885 3.488"/>
            </svg>
        `;
    }

    /**
     * Valida si un número de teléfono es válido
     * @param {string} phoneNumber - Número de teléfono a validar
     * @returns {boolean} - True si es válido, false si no
     */
    isValidPhoneNumber(phoneNumber) {
        if (!phoneNumber || 
            phoneNumber === 'undefined' || 
            phoneNumber === 'Sin teléfono' ||
            phoneNumber.trim() === '') {
            return false;
        }
        
        // Limpiar el número
        const cleanPhone = phoneNumber.replace(/[\s\-\(\)]/g, '');
        
        // Verificar que tenga al menos 7 dígitos
        const digitsOnly = cleanPhone.replace(/\D/g, '');
        return digitsOnly.length >= 7;
    }

    /**
     * Formatea un número de teléfono para WhatsApp
     * @param {string} phoneNumber - Número de teléfono original
     * @returns {string|null} - Número formateado o null si no es válido
     */
    formatPhoneNumber(phoneNumber) {
        if (!this.isValidPhoneNumber(phoneNumber)) {
            return null;
        }
        
        // Limpiar el número
        const cleanPhone = phoneNumber.replace(/[\s\-\(\)]/g, '');
        
        // Si ya tiene código de país, mantenerlo
        if (cleanPhone.startsWith('+')) {
            return cleanPhone;
        }
        
        // Agregar código de país por defecto
        return `${this.config.defaultCountryCode}${cleanPhone}`;
    }

    /**
     * Crea un enlace de WhatsApp
     * @param {string} phoneNumber - Número de teléfono
     * @param {string} message - Mensaje personalizado (opcional)
     * @returns {string|null} - URL de WhatsApp o null si no es válido
     */
    createLink(phoneNumber, message = '') {
        const formattedPhone = this.formatPhoneNumber(phoneNumber);
        
        if (!formattedPhone) {
            return null;
        }
        
        const finalMessage = message || this.config.defaultMessage;
        const encodedMessage = encodeURIComponent(finalMessage);
        
        return `https://wa.me/${formattedPhone}?text=${encodedMessage}`;
    }

    /**
     * Crea HTML de enlace de WhatsApp
     * @param {string} phoneNumber - Número de teléfono
     * @param {string} message - Mensaje personalizado (opcional)
     * @param {object} options - Opciones adicionales
     * @returns {string} - HTML del enlace
     */
    createLinkHTML(phoneNumber, message = '', options = {}) {
        const whatsappLink = this.createLink(phoneNumber, message);
        
        if (!whatsappLink) {
            return `<span class="${this.config.fallbackClass}">${this.config.fallbackText}</span>`;
        }
        
        const {
            className = '',
            showIcon = true,
            showText = true,
            customText = phoneNumber,
            target = '_blank',
            rel = 'noopener noreferrer'
        } = options;
        
        const iconHTML = showIcon ? this.whatsappIcon : '';
        const textHTML = showText ? customText : '';
        
        return `
            <a href="${whatsappLink}" 
               target="${target}" 
               rel="${rel}"
               class="${this.config.linkClass} ${className}"
               aria-label="Contactar por WhatsApp">
                ${iconHTML}
                ${textHTML}
            </a>
        `;
    }

    /**
     * Convierte automáticamente números de teléfono en enlaces de WhatsApp
     * @param {string} selector - Selector CSS para elementos a convertir
     * @param {string} message - Mensaje personalizado (opcional)
     * @param {object} options - Opciones adicionales
     */
    autoConvert(selector, message = '', options = {}) {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            const phoneNumber = element.textContent.trim();
            const linkHTML = this.createLinkHTML(phoneNumber, message, options);
            element.innerHTML = linkHTML;
        });
    }

    /**
     * Convierte números de teléfono en enlaces de WhatsApp basado en atributos de datos
     * @param {string} selector - Selector CSS para elementos con atributo data-phone
     */
    convertFromDataAttributes(selector = '[data-phone]') {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach(element => {
            const phoneNumber = element.getAttribute('data-phone');
            const message = element.getAttribute('data-message') || '';
            const className = element.getAttribute('data-class') || '';
            
            const linkHTML = this.createLinkHTML(phoneNumber, message, {
                className,
                customText: element.textContent.trim() || phoneNumber
            });
            
            element.innerHTML = linkHTML;
        });
    }

    /**
     * Crea un botón de WhatsApp
     * @param {string} phoneNumber - Número de teléfono
     * @param {string} message - Mensaje personalizado (opcional)
     * @param {object} options - Opciones adicionales
     * @returns {string} - HTML del botón
     */
    createButton(phoneNumber, message = '', options = {}) {
        const {
            text = 'Contactar por WhatsApp',
            className = 'bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors duration-200',
            size = 'normal'
        } = options;
        
        const sizeClasses = {
            small: 'px-2 py-1 text-sm',
            normal: 'px-4 py-2',
            large: 'px-6 py-3 text-lg'
        };
        
        const finalClassName = `${className} ${sizeClasses[size] || sizeClasses.normal}`;
        
        return this.createLinkHTML(phoneNumber, message, {
            className: finalClassName,
            customText: text,
            showIcon: true
        });
    }
}

// Crear instancia global
window.WhatsAppUtils = new WhatsAppUtils();

// Funciones de conveniencia globales
window.createWhatsAppLink = (phoneNumber, message) => window.WhatsAppUtils.createLink(phoneNumber, message);
window.createWhatsAppLinkHTML = (phoneNumber, message, options) => window.WhatsAppUtils.createLinkHTML(phoneNumber, message, options);
window.createWhatsAppButton = (phoneNumber, message, options) => window.WhatsAppUtils.createButton(phoneNumber, message, options);

// Auto-inicialización para elementos con atributos de datos
document.addEventListener('DOMContentLoaded', function() {
    window.WhatsAppUtils.convertFromDataAttributes();
});

// Exportar para uso en módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = WhatsAppUtils;
}
