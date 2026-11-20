import json
import re
import unicodedata
from pathlib import Path

from orientacao import Orientacao


def normalizar(texto):
    """Remove acentos e pontuação, preservando limites entre palavras."""
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    texto = re.sub(r'[^\w\s]', ' ', texto, flags=re.UNICODE)
    return ' '.join(texto.split())


def padronizar_termos(texto):
    """Trata a sigla CNH e a palavra habilitação como o mesmo termo."""
    return ' '.join('habilitacao' if palavra == 'cnh' else palavra
                    for palavra in normalizar(texto).split())


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = Path(caminho)
        self.orientacoes = []

    def carregar(self):
        """Falhas deixam a base vazia e permitem ao menu continuar."""
        self.orientacoes = []
        try:
            with self.caminho.open(encoding='utf-8') as arquivo:
                registros = json.load(arquivo)
            if not isinstance(registros, list):
                raise ValueError('O JSON deve conter uma lista.')
            campos_texto = ('categoria', 'titulo', 'resposta', 'onde', 'fonte', 'verificado_em')
            ids = set()
            for registro in registros:
                if not isinstance(registro, dict) or not isinstance(registro.get('id'), int):
                    raise ValueError('Registro ou id inválido.')
                if registro['id'] in ids:
                    raise ValueError('Há IDs repetidos.')
                ids.add(registro['id'])
                if any(not isinstance(registro.get(c), str) or not registro[c].strip() for c in campos_texto):
                    raise ValueError('Campo de texto ausente ou vazio.')
                for campo in ('palavras_chave', 'documentos'):
                    if not isinstance(registro.get(campo), list) or not registro[campo] or any(not isinstance(x, str) or not x.strip() for x in registro[campo]):
                        raise ValueError(f'Lista inválida: {campo}.')
            self.orientacoes = [Orientacao(registro) for registro in registros]
            if not self.orientacoes:
                print('A base está vazia. Confira o arquivo JSON.')
            return bool(self.orientacoes)
        except (OSError, UnicodeError, json.JSONDecodeError, ValueError, KeyError, TypeError) as erro:
            print(f'Não foi possível carregar a base: {erro}')
            print('Confira data/base_conhecimento.json e use a opção de recarregar.')
            return False

    def categorias(self):
        return sorted({o.categoria for o in self.orientacoes})

    def por_categoria(self, categoria):
        return [o for o in self.orientacoes if o.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_norm = ' ' + padronizar_termos(pergunta) + ' '
        titulo = set(padronizar_termos(orientacao.titulo).split())
        pontos = 0
        # Evita contar duas vezes expressões que diferem apenas por CNH/habilitação.
        chaves_vistas = set()
        for chave in orientacao.palavras_chave:
            chave_norm = padronizar_termos(chave)
            if chave_norm in chaves_vistas:
                continue
            chaves_vistas.add(chave_norm)
            if chave_norm and ' ' + chave_norm + ' ' in pergunta_norm:
                pontos += 3
        # Repetir a mesma palavra na pergunta não aumenta a pontuação.
        pontos += sum(1 for palavra in set(padronizar_termos(pergunta).split())
                      if len(palavra) >= 4 and palavra in titulo)
        return pontos

    def buscar(self, pergunta):
        resultados = [(self.pontuar(pergunta, o), o) for o in self.orientacoes]
        return sorted(resultados, key=lambda item: (-item[0], item[1].id))
