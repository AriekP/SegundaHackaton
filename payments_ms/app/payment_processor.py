import random
import string
from typing import Dict

def process_payment(provider_code: str, account_number: str, amount: float, reference: str) -> Dict:
    """Simula el procesamiento de un pago a un servicio externo"""
    
    # Simular fallo aleatorio (10% de probabilidad)
    if random.random() < 0.1:
        return {
            "success": False,
            "message": "Error en el procesamiento del pago",
            "confirmation_code": None
        }
    
    # Generar código de confirmación aleatorio
    confirmation_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    
    return {
        "success": True,
        "message": "Pago procesado exitosamente",
        "confirmation_code": confirmation_code
    }