#!/usr/bin/env python3
"""
Decodificar el token JWT de LIWA.co para ver la expiración
"""

import base64
import json
from datetime import datetime

def decode_jwt_payload(token):
    """Decodificar el payload de un JWT"""
    try:
        # Dividir el token en partes
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decodificar el payload (segunda parte)
        payload = parts[1]
        
        # Agregar padding si es necesario
        missing_padding = len(payload) % 4
        if missing_padding:
            payload += '=' * (4 - missing_padding)
        
        # Decodificar base64
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode('utf-8')
        
        return json.loads(decoded_str)
    except Exception as e:
        print(f"Error decodificando token: {e}")
        return None

# Token del test anterior
token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJqZXN1c0BwYXB5cnVzLmNvbS5jbyIsInVzZXIiOnsibmFtZXMiOm51bGwsImFjY291bnQiOm51bGwsImlkdiI6MjExNzAsImlkcyI6MTc5NzEsInRpcG9DbGllbnRlIjozMiwic2FsZG8iOjczODUwLCJjdWVudGEiOiIwMDQ4NjM5NjMwOSIsImVtcHJlc2EiOiJQQVBZUlVTIFNPTFVDSU9ORVMgSU5URUdSQUxFUyIsIm5vbWJyZSI6IlBBUFlSVVMgU09MVUNJT05FUyBJTlRFR1JBTEVTIiwicmF6b25Tb2NpYWwiOiJQQVBZUlVTIFNPTFVDSU9ORVMgSU5URUdSQUxFUyIsInRpcG9QYWdvIjoiUHJlcGFnbyIsImNpdWRhZCI6IkNhcnRhZ2VuYSIsImRpcmVjY2lvbiI6IkNyYSA5MSAjNTQtMTIwLCBMb2NhbCAxMiIsImRvY3VtZW50byI6IjkwMTIxMDAwOCIsImVtYWlsIjoiamVzdXNAcGFweXJ1cy5jb20uY28iLCJ0ZWxlZm9ubyI6IjU3MzAwMjU5NjMxOSIsImNvcnRlIjoiMjAyNC0xMi0xNSIsInRpcG9TdWJ1c3VhcmlvIjpudWxsLCJjbGF2ZSI6bnVsbH0sImlhdCI6MTc1NzQzMjg4MywiZXhwIjoxNzU3NTE5MjgzfQ.gqfnstEMIgBFOb30GQLTEfTJgQjI4sAFLgbkMeA_8Kg"

print("🔑 ANÁLISIS DEL TOKEN JWT DE LIWA.CO")
print("=" * 60)

payload = decode_jwt_payload(token)

if payload:
    print("📋 PAYLOAD DEL TOKEN:")
    print(json.dumps(payload, indent=2))
    
    # Extraer fechas importantes
    iat = payload.get('iat')  # Issued at
    exp = payload.get('exp')  # Expiration
    
    if iat:
        iat_date = datetime.fromtimestamp(iat)
        print(f"\n⏰ TOKEN CREADO: {iat_date}")
    
    if exp:
        exp_date = datetime.fromtimestamp(exp)
        now = datetime.now()
        print(f"⏰ TOKEN EXPIRA: {exp_date}")
        print(f"⏰ AHORA: {now}")
        
        if exp_date > now:
            time_left = exp_date - now
            print(f"✅ TOKEN VÁLIDO - Tiempo restante: {time_left}")
        else:
            time_expired = now - exp_date
            print(f"❌ TOKEN EXPIRADO - Expirado hace: {time_expired}")
    
    # Información del usuario
    user = payload.get('user', {})
    if user:
        print(f"\n👤 USUARIO:")
        print(f"   • Empresa: {user.get('empresa', 'N/A')}")
        print(f"   • Cuenta: {user.get('cuenta', 'N/A')}")
        print(f"   • Email: {user.get('email', 'N/A')}")
        print(f"   • Teléfono: {user.get('telefono', 'N/A')}")
else:
    print("❌ No se pudo decodificar el token")
