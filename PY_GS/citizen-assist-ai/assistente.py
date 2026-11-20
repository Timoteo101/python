import csv
import json
import time
from datetime import datetime
from pathlib import Path

from base_conhecimento import normalizar


class Assistente:
    CAMPOS = ('data', 'origem', 'pergunta', 'id_orientacao', 'encontrou',
              'ajudou', 'tentativas', 'tempo_segundos')

    def __init__(self, nome, base, pasta):
        self.nome, self.base, self.pasta = nome, base, Path(pasta)
        self.historico = self._ler_lista('historico.json')
        self.notas = self._ler_lista('avaliacoes.json')

    def _ler_lista(self, nome):
        caminho = self.pasta / nome
        try:
            with caminho.open(encoding='utf-8') as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError('o arquivo deve conter uma lista')
            if nome == 'historico.json':
                for registro in dados:
                    if not isinstance(registro, dict) or any(campo not in registro for campo in self.CAMPOS):
                        raise ValueError('há atendimento com campos ausentes ou inválidos')
                    if (not isinstance(registro['pergunta'], str)
                            or not isinstance(registro['encontrou'], bool)
                            or not isinstance(registro['ajudou'], bool)
                            or not isinstance(registro['tentativas'], int)
                            or not isinstance(registro['tempo_segundos'], (int, float))):
                        raise ValueError('há atendimento com tipos de dados inválidos')
            elif nome == 'avaliacoes.json':
                if any(type(nota) is not int or not 1 <= nota <= 5 for nota in dados):
                    raise ValueError('há nota fora do intervalo de 1 a 5')
            return dados
        except FileNotFoundError:
            return []
        except (OSError, ValueError, UnicodeError) as erro:
            print(f'Não foi possível ler {nome}: {erro}. Ele não será sobrescrito nesta execução.')
            setattr(self, '_bloqueado_' + nome.replace('.', '_'), True)
            return []

    def _salvar_lista(self, nome, dados):
        if getattr(self, '_bloqueado_' + nome.replace('.', '_'), False):
            print(f'{nome} está protegido. Corrija o arquivo antes de reiniciar.')
            return
        try:
            self.pasta.mkdir(parents=True, exist_ok=True)
            caminho = self.pasta / nome
            temporario = caminho.with_suffix('.tmp')
            with temporario.open('w', encoding='utf-8') as arquivo:
                json.dump(dados, arquivo, ensure_ascii=False, indent=2)
            temporario.replace(caminho)
        except OSError as erro:
            print(f'Não foi possível salvar {nome}: {erro}')

    @staticmethod
    def _opcao(texto, minimo, maximo):
        while True:
            valor = input(texto).strip()
            if valor.isascii() and valor.isdecimal() and len(valor) <= 3 and minimo <= int(valor) <= maximo:
                return int(valor)
            print(f'Opção inválida. Digite um número entre {minimo} e {maximo}.')

    @staticmethod
    def _sim_nao(texto):
        while True:
            valor = input(texto).strip().lower()
            if valor in ('s', 'n'):
                return valor == 's'
            if valor == '0':
                return None
            print('Resposta inválida. Digite s, n ou 0 para voltar.')

    @staticmethod
    def _contem_dado_pessoal(texto):
        return '@' in texto or sum(c.isdigit() for c in texto) >= 8

    def registrar(self, origem, pergunta, orientacao, encontrou, ajudou, tentativas, inicio):
        registro = {
            'data': datetime.now().isoformat(timespec='seconds'),
            'origem': origem, 'pergunta': pergunta,
            'id_orientacao': orientacao.id if orientacao else None,
            'encontrou': encontrou, 'ajudou': ajudou,
            'tentativas': tentativas, 'tempo_segundos': round(time.time() - inicio, 1),
        }
        self.historico.append(registro)
        self._salvar_lista('historico.json', self.historico)
        print(f"Tempo do atendimento: {registro['tempo_segundos']:.1f} segundo(s).")

    def perguntar(self):
        if not self.base.orientacoes:
            print('Base indisponível. Recarregue o arquivo pelo menu.')
            return
        print('\nNão informe nome, CPF, telefone, e-mail ou outros dados pessoais.')
        inicio = time.time()
        tentativas = 0
        while True:
            pergunta = input('\nDigite sua dúvida (0 para voltar): ').strip()
            if pergunta == '0':
                return
            if not pergunta:
                print('A dúvida não pode ficar vazia.')
                continue
            if self._contem_dado_pessoal(pergunta):
                print('Atenção: não digite CPF, telefone ou e-mail. Reescreva.')
                continue
            if normalizar(pergunta) in ('cnh', 'habilitacao'):
                self._assuntos_habilitacao(pergunta, inicio, tentativas + 1)
                return
            tentativas += 1
            resultados = [(p, o) for p, o in self.base.buscar(pergunta) if p >= 3]
            if resultados:
                pontos, orientacao = resultados[0]
                print(f'\nConfiança da resposta: {"ALTA" if pontos >= 6 else "MÉDIA"} ({pontos} pontos)')
                orientacao.exibir()
                if len(resultados) > 1:
                    print('\nOutras orientações que podem ajudar:')
                    for p, alternativa in resultados[1:3]:
                        print(f'  - {alternativa.titulo} ({p} pontos; categoria: {alternativa.categoria})')
                    print('Para consultá-las, use a navegação por categorias.')
                ajudou = self._sim_nao('Essa orientação respondeu sua dúvida? (s/n; 0 para voltar): ')
                if ajudou is None:
                    return
                if ajudou:
                    self.registrar('pergunta', pergunta, orientacao, True, True, tentativas, inicio)
                    return
                tentar = self._sim_nao('Deseja tentar outras palavras nesta mesma consulta? (s/n; 0 para voltar): ')
                if tentar is None:
                    return
                if tentar:
                    continue
                self.registrar('pergunta', pergunta, orientacao, True, False, tentativas, inicio)
                return
            print('Não encontrei uma orientação. Tente outras palavras ou navegue pelas categorias.')
            tentar = self._sim_nao('Deseja tentar outras palavras nesta mesma consulta? (s/n; 0 para voltar): ')
            if tentar is None:
                return
            if tentar:
                continue
            self.registrar('pergunta', pergunta, None, False, False, tentativas, inicio)
            return

    def _assuntos_habilitacao(self, pergunta, inicio, tentativas):
        """Uma palavra sozinha é ampla; deixa a pessoa escolher o assunto."""
        orientacoes = self.base.por_categoria('Habilitação')
        if not orientacoes:
            print('Não encontrei assuntos de habilitação na base.')
            return
        print('\nEncontrei estes assuntos sobre CNH / habilitação:')
        for numero, orientacao in enumerate(orientacoes, 1):
            print(f'{numero}. {orientacao.titulo}')
        escolha = self._opcao('Escolha um assunto (0 para voltar): ', 0, len(orientacoes))
        if escolha == 0:
            return
        orientacao = orientacoes[escolha - 1]
        print('\nOrientação escolhida por assunto (sem pontuação de busca).')
        orientacao.exibir()
        ajudou = self._sim_nao('Essa orientação respondeu sua dúvida? (s/n; 0 para voltar): ')
        if ajudou is not None:
            self.registrar('pergunta', pergunta, orientacao, True, ajudou, tentativas, inicio)

    def navegar(self):
        inicio = time.time()
        categorias = self.base.categorias()
        if not categorias:
            print('Base indisponível ou sem categorias.')
            return
        while True:
            print('\nCategorias:')
            for numero, categoria in enumerate(categorias, 1):
                print(f'{numero}. {categoria}')
            numero = self._opcao('Escolha uma categoria (0 para voltar): ', 0, len(categorias))
            if numero == 0:
                return
            orientacoes = self.base.por_categoria(categorias[numero - 1])
            while True:
                print(f'\n{categorias[numero - 1]}:')
                for posicao, orientacao in enumerate(orientacoes, 1):
                    print(f'{posicao}. {orientacao.titulo}')
                escolha = self._opcao('Escolha uma orientação (0 para voltar): ', 0, len(orientacoes))
                if escolha == 0:
                    break
                orientacao = orientacoes[escolha - 1]
                print('\nOrientação selecionada por categoria (sem pontuação de busca).')
                orientacao.exibir()
                ajudou = self._sim_nao('Essa orientação respondeu sua dúvida? (s/n; 0 para voltar): ')
                if ajudou is None:
                    continue
                self.registrar('categoria', '', orientacao, True, ajudou, 1, inicio)
                return

    def indicadores(self):
        total = len(self.historico)
        print('\n--- Indicadores ---')
        if not total:
            print('Nenhum atendimento registrado ainda.')
        else:
            encontrados = sum(bool(r.get('encontrou')) for r in self.historico)
            ajudaram = sum(bool(r.get('ajudou')) for r in self.historico)
            tempos = [r['tempo_segundos'] for r in self.historico if r.get('encontrou')]
            tentativas = sum(r.get('tentativas', 0) for r in self.historico)
            print(f'Resposta encontrada: {encontrados / total * 100:.1f}% ({encontrados}/{total})')
            print(f'Taxa de acerto (ajudou): {ajudaram / total * 100:.1f}% ({ajudaram}/{total})')
            print('Tempo médio dos atendimentos com orientação: ' + (f'{sum(tempos) / len(tempos):.1f} s' if tempos else 'não disponível'))
            print(f'Tentativas por atendimento: {tentativas / total:.1f}')
            print('Dúvidas sem solução:')
            pendentes = [r for r in self.historico if not r.get('ajudou')]
            if not pendentes:
                print('  Nenhuma.')
            for registro in pendentes:
                print('  - ' + (registro.get('pergunta') or f"Navegação: orientação {registro.get('id_orientacao')}"))
        notas_validas = [n for n in self.notas if isinstance(n, int) and 1 <= n <= 5]
        print('Facilidade de uso (1 a 5): ' + (f'{sum(notas_validas) / len(notas_validas):.1f} ({len(notas_validas)} avaliação(ões))' if notas_validas else 'ainda não avaliada'))

    def exportar_csv(self):
        if getattr(self, '_bloqueado_historico_json', False):
            print('CSV não foi sobrescrito porque o histórico está inválido; corrija-o e reinicie.')
            return
        try:
            self.pasta.mkdir(parents=True, exist_ok=True)
            with (self.pasta / 'atendimentos.csv').open('w', encoding='utf-8-sig', newline='') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=self.CAMPOS, extrasaction='ignore')
                escritor.writeheader()
                escritor.writerows(self.historico)
            print('Atendimentos exportados para data/atendimentos.csv.')
        except OSError as erro:
            print(f'Não foi possível exportar o CSV: {erro}')

    def menu(self):
        print(f'\n{self.nome} - orientação para mobilidade e trânsito')
        print('Aqui você pode tirar dúvidas sobre documentação e serviços de trânsito, como:')
        print('  - Idade e requisitos para tirar a primeira CNH;')
        print('  - CNH vencida ou próxima do vencimento e como renovar;')
        print('  - CNH digital, pontos, multas e documento do veículo;')
        print('  - Transporte acessível e credencial para vaga especial.')
        print('Exemplos: "Com quantos anos posso tirar minha CNH?"')
        print('          "Minha CNH está vencendo, como renovar?"')
        print('Este assistente não é canal oficial. Não informe dados pessoais.')
        try:
            while True:
                print('\n1. Fazer uma pergunta\n2. Navegar por categorias\n3. Ver indicadores\n4. Exportar CSV\n5. Recarregar base\n0. Sair')
                escolha = self._opcao('Escolha: ', 0, 5)
                if escolha == 0:
                    nota = self._opcao('Facilidade de uso de 1 a 5 (0 para não avaliar): ', 0, 5)
                    if nota:
                        self.notas.append(nota)
                        self._salvar_lista('avaliacoes.json', self.notas)
                    self.exportar_csv()
                    print('Até mais!')
                    return
                if escolha == 1:
                    self.perguntar()
                elif escolha == 2:
                    self.navegar()
                elif escolha == 3:
                    self.indicadores()
                elif escolha == 4:
                    self.exportar_csv()
                else:
                    self.base.carregar()
        except (EOFError, KeyboardInterrupt):
            print('\nEncerramento interrompido. Os atendimentos concluídos já foram salvos.')
