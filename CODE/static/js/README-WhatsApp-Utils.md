# WhatsApp Utils - Documentación

## Descripción
Módulo JavaScript reutilizable para crear enlaces de WhatsApp de manera automática y configurable.

## Características
- ✅ Validación automática de números de teléfono
- ✅ Formateo automático con código de país
- ✅ Mensajes personalizables
- ✅ Múltiples métodos de implementación
- ✅ Auto-conversión basada en atributos de datos
- ✅ Configuración flexible
- ✅ Compatible con números internacionales

## Métodos de Uso

### 1. Uso Básico con Funciones Globales

```javascript
// Crear enlace simple
const link = createWhatsAppLink('+13002596319', 'Hola, tengo una consulta');

// Crear HTML de enlace
const linkHTML = createWhatsAppLinkHTML('3001234567', 'Mensaje personalizado');

// Crear botón
const buttonHTML = createWhatsAppButton('3001234567', 'Contactar', {
    text: 'Enviar WhatsApp',
    size: 'large'
});
```

### 2. Uso con Clase WhatsAppUtils

```javascript
// Crear instancia personalizada
const whatsapp = new WhatsAppUtils({
    defaultCountryCode: '+1', // Estados Unidos
    defaultMessage: 'Hello, I have a question about my package',
    iconSize: 'w-6 h-6'
});

// Usar métodos
const link = whatsapp.createLink('3001234567');
const html = whatsapp.createLinkHTML('3001234567', 'Mensaje personalizado');
```

### 3. Auto-conversión con Atributos de Datos

```html
<!-- Se convierte automáticamente -->
<span data-phone="3001234567" data-message="Consulta sobre paquete">
    3001234567
</span>

<!-- Con clases personalizadas -->
<div data-phone="+13002596319" 
     data-message="Hello" 
     data-class="text-lg font-bold">
    Contacto Internacional
</div>
```

### 4. Auto-conversión con Selectores

```javascript
// Convertir todos los elementos con clase .phone-number
WhatsAppUtils.autoConvert('.phone-number', 'Mensaje por defecto');

// Convertir elementos específicos
WhatsAppUtils.autoConvert('#customer-phone', 'Consulta sobre mi paquete');
```

## Configuración

### Opciones por Defecto
```javascript
{
    defaultCountryCode: '+57',        // Código de país por defecto
    defaultMessage: 'Hola, tengo una consulta sobre mi paquete',
    iconSize: 'w-4 h-4',             // Tamaño del icono
    linkClass: 'inline-flex items-center text-green-600 hover:text-green-700 transition-colors duration-200',
    fallbackText: 'Sin teléfono',    // Texto cuando no hay teléfono
    fallbackClass: 'text-sm text-gray-500'
}
```

### Personalización
```javascript
const whatsapp = new WhatsAppUtils({
    defaultCountryCode: '+1',
    defaultMessage: 'Hello from the US!',
    iconSize: 'w-6 h-6',
    linkClass: 'custom-whatsapp-link'
});
```

## Ejemplos de Implementación

### En Templates HTML
```html
<!-- Método 1: Atributos de datos (automático) -->
<span data-phone="3001234567" data-message="Consulta sobre paquete ABC123">
    3001234567
</span>

<!-- Método 2: JavaScript inline -->
<script>
document.getElementById('phone-display').innerHTML = 
    createWhatsAppLinkHTML('3001234567', 'Consulta sobre paquete');
</script>
```

### En JavaScript Dinámico
```javascript
// Para contenido cargado dinámicamente
function displayPackageInfo(packageData) {
    const phoneHTML = createWhatsAppLinkHTML(
        packageData.customer_phone, 
        `Consulta sobre paquete ${packageData.tracking_code}`
    );
    
    document.getElementById('phone-container').innerHTML = phoneHTML;
}
```

### Para Formularios
```javascript
// Crear botón de contacto
function addContactButton(phoneNumber) {
    const buttonHTML = createWhatsAppButton(phoneNumber, '', {
        text: 'Contactar Cliente',
        className: 'bg-green-500 text-white px-4 py-2 rounded',
        size: 'normal'
    });
    
    document.getElementById('contact-actions').innerHTML = buttonHTML;
}
```

## Validación de Números

El módulo valida automáticamente:
- ✅ Números con código de país (+57, +1, etc.)
- ✅ Números locales (se agrega código de país)
- ✅ Números con espacios, guiones y paréntesis
- ❌ Números vacíos o inválidos
- ❌ Números con menos de 7 dígitos

## Compatibilidad

- ✅ Navegadores modernos (Chrome, Firefox, Safari, Edge)
- ✅ Dispositivos móviles
- ✅ Aplicaciones web progresivas (PWA)
- ✅ Números internacionales
- ✅ WhatsApp Web y WhatsApp Mobile

## Casos de Uso

1. **Consulta de Paquetes**: Enlaces automáticos en resultados de búsqueda
2. **Dashboard**: Botones de contacto rápido para administradores
3. **Mensajes**: Enlaces en conversaciones de clientes
4. **Formularios**: Botones de contacto después de envío
5. **Listados**: Enlaces en tablas de paquetes o clientes

## Mantenimiento

Para futuras implementaciones:
1. Agregar `data-phone` a elementos HTML
2. Usar funciones globales para contenido dinámico
3. Configurar mensajes personalizados según contexto
4. Aprovechar auto-conversión para implementaciones masivas
