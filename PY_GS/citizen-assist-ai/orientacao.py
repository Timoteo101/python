class Orientacao:
    """Representa um registro da base de conhecimento."""

    def __init__(self, registro):
        self.id = registro['id']
        self.categoria = registro['categoria']
        self.titulo = registro['titulo']
        self.palavras_chave = registro['palavras_chave']
        self.resposta = registro['resposta']
        self.documentos = registro['documentos']
        self.onde = registro['onde']
        self.fonte = registro['fonte']
        self.verificado_em = registro['verificado_em']

    def exibir(self):
        print(f'\n>> {self.titulo} [{self.categoria}]')
        print(self.resposta)
        print('Documentos e requisitos para o serviço:')
        for documento in self.documentos:
            print(f'  - {documento}')
        print(f'Onde: {self.onde}')
        print(f'Fonte: {self.fonte} (verificado em {self.verificado_em})')
        print('Aviso: este assistente não é canal oficial.')
