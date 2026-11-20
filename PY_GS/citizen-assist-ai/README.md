# Citizen Assist AI - Mobilidade

Assistente de terminal para orientar cidadãos sobre documentação e serviços de trânsito, veículos e transporte acessível. O público são pessoas que precisam encontrar caminhos oficiais para resolver dúvidas sobre mobilidade no Brasil. A informação costuma estar espalhada entre serviços, Detrans e programas; aqui, cada orientação mostra a fonte para conferência. Logo na abertura, o terminal apresenta os assuntos atendidos e exemplos de perguntas.

## Integrantes

- **Nome:** [preencher] — **RM:** [preencher]
- Acrescente os demais integrantes e respectivos RMs, se houver.

## Relação com os ODS

- **ODS 11 - Cidades e comunidades sustentáveis:** facilita o acesso à informação sobre mobilidade e transporte.
- **ODS 10 - Redução das desigualdades:** apresenta caminhos para benefícios e acessibilidade no transporte.
- **ODS 16 - Paz, justiça e instituições eficazes:** aproxima pessoas de serviços e informações públicas verificáveis.

## Como executar

Requisitos: Python 3.8 ou superior; não há bibliotecas externas. Abra o terminal dentro da pasta do projeto e execute:

```bash
python main.py
```

No Windows, se necessário, use `py main.py`. Digite o número do menu: **1** para perguntar, **2** para categorias, **3** para indicadores, **4** para exportar, **5** para recarregar a base e **0** para sair. Em perguntas e listas, **0** volta. Ao sair, informe uma nota de facilidade de 1 a 5 ou 0 para pular; o CSV é exportado automaticamente. A pasta `data` precisa permitir gravação.

Exemplos de perguntas: `Como consultar multas?`, `Com quantos anos posso tirar minha CNH?` e `Minha CNH está vencendo, como renovar?`. Perguntas com `@` ou oito ou mais dígitos, mesmo separados por pontuação, são recusadas e não são registradas. Não informe nomes, dados pessoais ou detalhes que identifiquem alguém: essa regra simples **não detecta todos os dados pessoais**. O programa é local e não consulta serviços externos automaticamente.

## Organização e busca

`main.py` monta os objetos. Cada `Orientacao` guarda um dicionário da base e sabe exibi-lo; `BaseConhecimento` carrega uma lista desses objetos, organiza categorias e busca; `Assistente` contém a base, realiza atendimentos e calcula indicadores. A composição é `Assistente -> BaseConhecimento -> lista de Orientacao`.

A função `normalizar()` remove acentos, troca pontuação por espaços e transforma em minúsculas. Antes da comparação, `padronizar_termos()` troca a palavra isolada `cnh` por `habilitacao` na pergunta, no título e nas palavras-chave, para reconhecer os dois termos como equivalentes. Cada expressão-chave padronizada que aparece inteira na pergunta vale **3 pontos**; cada palavra distinta da pergunta padronizada com pelo menos quatro letras que também aparece inteira no título vale **1 ponto**. Chaves sobrepostas contam separadamente, mas expressões que se tornam idênticas após a padronização contam apenas uma vez. O tamanho mínimo é medido depois da substituição. `buscar()` retorna tuplas `(pontos, orientacao)` em ordem decrescente; empates são resolvidos pelo menor ID. A melhor resposta é mostrada com até duas alternativas: **ALTA** para 6 pontos ou mais; **MÉDIA** para 3 a 5; abaixo de 3, não há resposta. As alternativas aparecem a partir de 3 pontos e podem ser abertas nas categorias. A pontuação é uma regra textual, não uma probabilidade real de acerto.

Se a pessoa digitar apenas `CNH` ou `habilitação`, a dúvida é ampla demais para escolher uma resposta automaticamente. O assistente mostra uma lista dos assuntos de habilitação, para a pessoa escolher diretamente; nesse caso não há pontuação ou confiança de busca. A seleção é registrada como atendimento por pergunta; 0 volta sem registrar.

Exemplo: `Como consultar multas?` para “Consultar infrações de trânsito” recebe 3 pontos pela expressão `consultar multas` e 1 pela palavra `consultar` no título: **4 pontos, confiança MÉDIA**.

## Histórico, indicadores e privacidade

O histórico é salvo em `data/historico.json` e exportado com `csv.DictWriter` para `data/atendimentos.csv`; avaliações de facilidade ficam em `data/avaliacoes.json`. Cada consulta por pergunta termina quando a pessoa aceita a resposta ou decide parar; reformulações dentro da mesma consulta aumentam `tentativas`. A última pergunta válida e o último resultado são registrados. Selecionar uma orientação por categoria conta como uma tentativa; sair com 0 antes de concluir ou perguntas bloqueadas não geram atendimento. O tempo começa ao entrar na função e termina ao registrar, incluindo leitura e resposta; não mede apenas a busca. Na navegação, ao finalizar um atendimento, é preciso entrar novamente para começar outro.

Os percentuais de encontrado e ajudou usam **todos os atendimentos concluídos** como denominador. O tempo médio usa apenas os que encontraram uma orientação; tentativas usa todos. A facilidade é a média das notas dadas ao sair. A lista sem solução inclui respostas não encontradas ou avaliadas como não úteis. São dados locais, sem identificação solicitada; perguntas válidas são guardadas literalmente, então é essencial não incluir dados pessoais. Para reiniciar os dados do experimento, com autorização da equipe, substitua o conteúdo dos dois JSONs de histórico e avaliações por `[]` e exporte novamente.

Se a base estiver ausente, corrompida ou com campos inválidos, o programa informa o problema sem derrubar o menu; após corrigi-la, use a opção 5. Se o histórico ou as avaliações estiverem corrompidos ou malformados, o arquivo não é sobrescrito na execução: corrija ou restaure o arquivo antes de reiniciar. Com histórico inválido, o CSV também não é sobrescrito, para preservar dados anteriores.

## Teste com usuários reais — pendente

**Ainda não realizado. Não substitua esta seção por resultados inventados.** Antes do vídeo, convide pelo menos **3 pessoas de fora da equipe**, com **10 atendimentos ou mais no total**, sem coletar nomes ou dados pessoais. O arquivo `GUIA_TESTE_USUARIOS.md` explica o procedimento. Oriente cada pessoa a usar o programa, avaliar se a resposta ajudou e, ao final da sessão, dar a nota. Veja os indicadores no menu 3 depois que as notas forem registradas; exporte com o menu 4. Cada pessoa pode realizar mais de um atendimento. Registre apenas os dados agregados:

- Pessoas externas: [preencher número, mínimo 3]
- Atendimentos: [preencher número, mínimo 10]
- Resposta encontrada: [preencher % e proporção]
- Taxa de acerto (ajudou): [preencher % e proporção]
- Tempo médio dos atendimentos com resposta: [preencher segundos]
- Tentativas por atendimento: [preencher média]
- Facilidade de uso: [preencher média e número de avaliações]
- Dúvidas sem solução, sem dados pessoais: [preencher]
- Melhoria efetivamente feita a partir do teste e como foi verificada: [preencher]

Se usar atendimentos de demonstração antes do teste real, reinicie os arquivos de dados para não misturar os resultados. Antes de publicar o repositório, revise o histórico e o CSV: não publique perguntas que contenham qualquer dado pessoal, mesmo que o filtro automático não o tenha detectado.

## Fontes oficiais

Conferidas em **16/11/2026**, com revisão de registros específicos em **17/11/2026**. Cada registro da base traz sua própria data de verificação e o link específico:

- [Ministério dos Transportes: primeira CNH e aplicativo](https://www.gov.br/transportes/pt-br/assuntos/noticias/2025/12/cnh-do-brasil-como-solicitar-a-primeira-habilitacao-pelo-aplicativo)
- [Ministério dos Transportes: idade e requisitos para ser condutor](https://www.gov.br/transportes/pt-br/assuntos/transito/cnh-do-brasil)
- [Ministério dos Transportes: perguntas frequentes sobre renovação e regras especiais](https://www.gov.br/transportes/pt-br/acesso-a-informacao/perguntas-frequentes)
- [Senatran: perguntas sobre pontuação e Detran](https://www.gov.br/transportes/pt-br/assuntos/transito/conteudo-Senatran/coordenacao-geral-de-informatizacao-e-estatistica-cgie)
- [Gov.br: consultar infrações](https://www.gov.br/pt-br/servicos/consultar-online-suas-infracoes-de-transito)
- [Gov.br: emissão do CRLV digital](https://www.gov.br/pt-br/servicos/emitir-o-certificado-de-registro-e-licenciamento-de-veiculo-digital-crlv-e)
- [Governo de Minas Gerais: consultar recall](https://www.mg.gov.br/servico/verificar-situacao-de-recall-do-veiculo)
- [Gov.br: credencial digital de estacionamento](https://www.gov.br/pt-br/servicos/emitir-credencial-de-estacionamento-digital)
- [Gov.br: Passe Livre Interestadual](https://www.gov.br/pt-br/servicos/obter-passe-livre-interestadual-digital)
- [Gov.br: Carteira da Pessoa Idosa](https://www.gov.br/pt-br/servicos/adquirir-carteira-do-idoso)
- [Secretaria-Geral: carta de serviços, ID Jovem](https://www.gov.br/secretariageral/pt-br/acesso-a-informacao/acoes-e-programas/carta-de-servicos/carta-de-servicos-sgpr-20230929.pdf)

As fontes podem mudar; confirme regras, documentos e disponibilidade no órgão responsável antes de tomar uma decisão. Este projeto **não é canal oficial**, não executa serviços, não acessa dados governamentais e não usa IA generativa. Seu filtro de dados pessoais é limitado. A busca pode produzir correspondências inadequadas ou não reconhecer sinônimos; confiança alta não garante que a resposta seja correta. Regras locais podem variar.

## Integração com outras disciplinas

A temática de mobilidade conversa com o projeto de simulação de fluxo de trânsito com ESP32 e sensor. **Não há integração técnica implementada** entre os projetos; a busca por regras funciona de forma independente, conforme a disciplina.

## Vídeo técnico

Link do YouTube não listado: **[preencher após a gravação]**. A equipe deve gravar com suas próprias vozes, explicar o código e mostrar todos os requisitos. Consulte `ROTEIRO_VIDEO.md` para uma sequência de 5 a 8 minutos.
