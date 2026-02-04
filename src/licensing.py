# licensing.py
import json
import os
import hashlib
from datetime import datetime, timedelta
import base64

class LicensingSystem:
    def __init__(self):
        self.license_file = "license.json"
        self.config_file = "config.json"
        self.load_config()
    
    def load_config(self):
        """Carrega configurações do sistema"""
        default_config = {
            "trial_days": 15,
            "product_name": "RH Assistant Pro",
            "version": "1.0.0",
            "price_monthly": 297,
            "price_yearly": 2970,
            "contact_email": "suporte@rhassistantpro.com",
            "website": "https://rhassistantpro.com"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            except:
                self.config = default_config
        else:
            self.config = default_config
            self.save_config()
    
    def save_config(self):
        """Salva configurações"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
    
    def check_license(self):
        """Verifica status da licença"""
        if not os.path.exists(self.license_file):
            return self.create_trial_license()
        
        try:
            with open(self.license_file, 'r', encoding='utf-8') as f:
                license_data = json.load(f)
            
            license_type = license_data.get('type', 'trial')
            expiry_date = license_data.get('expiry_date')
            license_key = license_data.get('license_key')
            
            if license_type == 'trial':
                # Verifica se trial ainda é válido
                expiry = datetime.fromisoformat(expiry_date)
                if datetime.now() > expiry:
                    return {
                        'valid': False,
                        'type': 'trial',
                        'status': 'expired',
                        'message': 'Período de teste expirado!',
                        'days_left': 0,
                        'expiry_date': expiry_date
                    }
                else:
                    days_left = (expiry - datetime.now()).days
                    return {
                        'valid': True,
                        'type': 'trial',
                        'status': 'active',
                        'message': f'Teste grátis ({days_left} dias restantes)',
                        'days_left': days_left,
                        'expiry_date': expiry_date
                    }
            
            elif license_type == 'paid':
                # Verifica licença paga
                if self.validate_paid_license(license_key):
                    return {
                        'valid': True,
                        'type': 'paid',
                        'status': 'active',
                        'message': 'Licença ativa - Plano Starter',
                        'expiry_date': 'Permanente',
                        'plan': license_data.get('plan', 'starter')
                    }
                else:
                    return {
                        'valid': False,
                        'type': 'paid',
                        'status': 'invalid',
                        'message': 'Licença inválida!'
                    }
            
            else:
                return self.create_trial_license()
                
        except Exception as e:
            print(f"❌ Erro ao verificar licença: {e}")
            return self.create_trial_license()
    
    def create_trial_license(self):
        """Cria licença de teste de 15 dias"""
        expiry_date = datetime.now() + timedelta(days=self.config['trial_days'])
        
        license_data = {
            'type': 'trial',
            'created_date': datetime.now().isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'machine_id': self.get_machine_id(),
            'product': self.config['product_name'],
            'version': self.config['version']
        }
        
        with open(self.license_file, 'w', encoding='utf-8') as f:
            json.dump(license_data, f, indent=2, ensure_ascii=False)
        
        days_left = self.config['trial_days']
        return {
            'valid': True,
            'type': 'trial',
            'status': 'active',
            'message': f'Teste grátis ({days_left} dias restantes)',
            'days_left': days_left,
            'expiry_date': expiry_date.isoformat()
        }
    
    def get_machine_id(self):
        """Gera um ID único para a máquina"""
        try:
            import uuid
            import platform
            import socket
            
            # Combina várias informações da máquina
            machine_info = f"{platform.node()}{socket.gethostname()}"
            machine_hash = hashlib.md5(machine_info.encode()).hexdigest()
            return machine_hash[:16]
        except:
            return hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:16]
    
    def validate_paid_license(self, license_key):
        """Valida uma licença paga"""
        # Aqui você pode implementar validação online
        # ou usar criptografia simples para validar chaves
        
        # Por enquanto, validação básica
        if license_key and len(license_key) == 25 and license_key.startswith("RHA"):
            return True
        return False
    
    def activate_license(self, license_key, plan="starter"):
        """Ativa uma licença paga"""
        if self.validate_paid_license(license_key):
            license_data = {
                'type': 'paid',
                'license_key': license_key,
                'activation_date': datetime.now().isoformat(),
                'plan': plan,
                'machine_id': self.get_machine_id(),
                'product': self.config['product_name'],
                'version': self.config['version']
            }
            
            with open(self.license_file, 'w', encoding='utf-8') as f:
                json.dump(license_data, f, indent=2, ensure_ascii=False)
            
            return {
                'success': True,
                'message': f'Licença ativada com sucesso! Plano: {plan.upper()}',
                'plan': plan
            }
        else:
            return {
                'success': False,
                'message': 'Chave de licença inválida!'
            }
    
    def get_pricing_info(self):
        """Retorna informações de preços"""
        return {
            'starter': {
                'monthly': self.config['price_monthly'],
                'yearly': self.config['price_yearly'],
                'features': [
                    'Consultas ilimitadas',
                    'Suporte por email',
                    'Atualizações mensais',
                    '3 empresas'
                ]
            },
            'growth': {
                'monthly': self.config.get('price_growth', 597),
                'yearly': self.config.get('price_growth_yearly', 5970),
                'features': [
                    'Tudo do Starter',
                    'Conversor PDF→JSON',
                    'Suporte prioritário',
                    '10 empresas'
                ]
            },
            'enterprise': {
                'monthly': self.config.get('price_enterprise', 997),
                'yearly': self.config.get('price_enterprise_yearly', 9970),
                'features': [
                    'Tudo do Growth',
                    'API REST',
                    'Suporte 24/7',
                    'Empresas ilimitadas'
                ]
            }
        }
    
    def generate_license_key(self, plan="starter"):
        """Gera uma chave de licença (para uso no sistema de vendas)"""
        import random
        import string
        
        prefix = "RHA"
        timestamp = str(int(datetime.now().timestamp()))[-6:]
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
        plan_code = {"starter": "S", "growth": "G", "enterprise": "E"}.get(plan, "S")
        
        key = f"{prefix}{plan_code}{timestamp}{random_part}"
        return key[:25]  # Garante 25 caracteres