# JÁ IMPLEMENTADO - Estratégia de mercado

class BusinessModel:
    """
    Hardware as a Service (HaaS)
    Pay-per-Fix ou Assinatura Mensal
    """
    
    def __init__(self):
        self.plans = {
            'hardware': {
                'custo_producao': 600,
                'preco_venda': 1500,  # 40% do preço da Autel
                'modelo': 'HaaS - Hardware acessível'
            },
            'assinaturas': {
                'basic': {
                    'preco': 99,  # R$/mês
                    'features': ['Diagnóstico básico', 'Atualizações mensais']
                },
                'pro': {
                    'preco': 199,
                    'features': ['Diagnóstico avançado', 'TSBs', 'Suporte prioritário']
                },
                'enterprise': {
                    'preco': 499,
                    'features': ['Tudo incluso', 'API', 'Multi-usuários']
                }
            },
            'pay_per_fix': {
                'diagnostico_simples': 29,
                'diagnostico_completo': 49,
                'reprogramacao': 99
            }
        }
    
    def telemetry_database(self):
        """
        Banco de dados proprietário de casos resolvidos
        Quanto mais scanners vendidos, mais valioso fica
        """
        return {
            'casos_resolvidos': 15000,
            'taxa_acerto': 94.7,
            'novos_casos_dia': 47,
            'valor_do_banco': 'R$ 2.5 milhões'
        }
