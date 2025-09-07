-- ========================================
-- PAQUETES EL CLUB v3.5 - Inicialización de Base de Datos Local
-- ========================================

-- Configurar timezone
SET timezone = 'America/Bogota';

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear tipos ENUM
DO $$ BEGIN
    CREATE TYPE userrole AS ENUM ('admin', 'operator', 'user');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE packagestatus AS ENUM ('anunciado', 'recibido', 'en_transito', 'entregado', 'cancelado');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE packagetype AS ENUM ('normal', 'extra_dimensionado');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE packagecondition AS ENUM ('bueno', 'regular', 'malo');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE ratetype AS ENUM ('storage', 'delivery', 'package_type');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE notificationtype AS ENUM ('email', 'sms', 'push');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE notificationstatus AS ENUM ('pending', 'sent', 'failed', 'delivered');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE messagetype AS ENUM ('internal', 'support', 'system');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE activitytype AS ENUM ('LOGIN', 'LOGOUT', 'CREATE', 'UPDATE', 'DELETE', 'STATUS_CHANGE', 'PASSWORD_CHANGE');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Mensaje de confirmación
SELECT 'Base de datos inicializada correctamente para PAQUETES EL CLUB v3.5' as status;