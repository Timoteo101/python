# Roteiro do vídeo técnico — Citizen Assist AI - Mobilidade

O vídeo deve ter **entre 5 e 8 minutos**. Mostre o código legível e o programa em funcionamento; a câmera é opcional. A apresentação deve ser feita pela própria equipe, com as próprias vozes. **Todos os integrantes devem falar**. Se o trabalho for individual, uma pessoa explica todas as partes. Se houver dois ou três integrantes, distribuam os blocos; cada integrante deve explicar uma parte técnica.

As falas abaixo são um apoio: entenda cada parte e adapte as palavras ao seu jeito de falar. Preencha nomes, RMs e resultados reais. Não use narração por IA e não invente resultados.

## Antes de gravar

1. Realize os testes com **ao menos três pessoas de fora da equipe e dez atendimentos no total**. Use o guia `GUIA_TESTE_USUARIOS.md`. Anote os indicadores e uma melhoria efetivamente feita a partir do teste. Atualize o README.
2. Abra o projeto no editor e aumente o tamanho da letra. Tenha um terminal pronto na pasta do projeto com `python main.py`.
3. Para não misturar os resultados reais com perguntas de demonstração, primeiro mostre os indicadores reais. Depois faça uma **cópia da pasta do projeto** para a demonstração e rode o programa dentro dessa cópia. Não mostre dados pessoais.
4. Prepare para abrir `data/base_conhecimento.json`, `orientacao.py`, `base_conhecimento.py`, `assistente.py`, `main.py`, `data/historico.json` e `data/atendimentos.csv`.

## 0:00–0:25 — Equipe, público e problema

**Mostre:** título do projeto ou README.

**Fala sugerida:** “Olá, eu sou [nome], RM [número]. [Apresente os demais integrantes e RMs, se houver.] Nosso projeto é o Citizen Assist AI - Mobilidade. Ele ajuda cidadãos a encontrar orientações sobre CNH, documentação de veículos e transporte acessível. O problema é que essas informações estão espalhadas em diferentes serviços. Reunimos orientações simples com links para fontes oficiais.”

## 0:25–1:10 — JSON, dicionários e tuplas

**Mostre:** um registro de `data/base_conhecimento.json` e depois o método `buscar()` em `base_conhecimento.py`.

**Fala sugerida:** “Nossa base é uma lista de dicionários em JSON. Cada dicionário é uma orientação com ID, categoria, título, palavras-chave, resposta, documentos, onde buscar o serviço, fonte e data da verificação. As palavras-chave e os documentos são listas. Ao pesquisar, o método `buscar` retorna uma lista de tuplas; cada tupla reúne a pontuação e o objeto da orientação.”

## 1:10–2:10 — Classes, atributos, métodos e composição

**Mostre:** `orientacao.py`, os métodos da classe `BaseConhecimento`, o início de `Assistente` e a criação dos objetos em `main.py`.

**Fala sugerida:** “O projeto tem três classes. `Orientacao` guarda os dados de um registro e o método `exibir` mostra a informação. `BaseConhecimento` lê o JSON, cria uma lista de objetos `Orientacao`, mostra categorias e realiza a busca. `Assistente` recebe a base, conversa com a pessoa, registra atendimentos e calcula indicadores. `self` representa o próprio objeto, permitindo acessar seus atributos e métodos. Isso forma uma composição: o assistente contém uma base e a base contém várias orientações.”

## 2:10–3:00 — Normalização e cálculo da busca

**Mostre:** `normalizar`, `padronizar_termos`, `pontuar` e `buscar` em `base_conhecimento.py`.

**Fala sugerida:** “A normalização deixa o texto minúsculo e remove acentos e pontuação. Também tratamos CNH e habilitação como o mesmo termo. Uma expressão-chave encontrada vale três pontos; uma palavra distinta da pergunta normalizada, com pelo menos quatro letras, que esteja no título vale um ponto. Expressões que viram a mesma coisa após a troca contam só uma vez.”

**Mostre o exemplo no código e diga:** “Em ‘Como consultar multas?’, a expressão ‘consultar multas’ vale três pontos e ‘consultar’ no título vale mais um: quatro pontos, confiança média. De três a cinco é média; a partir de seis, alta; abaixo de três o programa não encontra. A busca ordena as tuplas e exibe a melhor orientação e até duas alternativas. Se a pessoa digita só CNH, mostramos uma lista de assuntos para ela escolher.”

## 3:00–4:30 — Demonstração do terminal

**Mostre primeiro os resultados reais dos testes:** abra o projeto usado pelos participantes, selecione a opção `3` e apresente os indicadores e as dúvidas sem solução. Diga: “Testamos com [número real] pessoas de fora da equipe, em [número real] atendimentos. Os resultados foram [leia os valores reais]. A melhoria que fizemos a partir do teste foi [explique a mudança real e como conferiu].” Se os testes ainda não foram feitos, faça-os antes de gravar.

**Depois abra a cópia de demonstração e execute:**

1. Digite uma opção de menu inválida, como `x`, para mostrar que o programa continua.
2. Escolha `1` e pergunte `Como consultar multas?`. Mostre a confiança, resposta, documentos, fonte, data e aviso. Responda `s`.
3. Escolha `1`, digite o exemplo fictício `123.456.789-00` e mostre o bloqueio. Ele não será registrado. Depois digite `abacaxi roxo`, mostre “Não encontrei” e responda `n`.
4. Escolha `2`, abra uma categoria e uma orientação. Mostre o `0` para voltar nas listas e o pedido de avaliação `s/n`.

**Fala sugerida:** “O programa não é um canal oficial. Ele recusa perguntas com arroba ou pelo menos oito dígitos, inclusive com pontuação. Esse filtro não detecta todos os dados pessoais, por isso avisamos para não informá-los.”

## 4:30–5:30 — Alteração ao vivo no JSON

**Mostre e execute:** na cópia de demonstração, escolha `1` e pergunte `revisao violeta`. Mostre que não encontra; responda `n`. Abra `data/base_conhecimento.json` e encontre o registro de recall do veículo. Adicione `"revisao violeta"` na lista `palavras_chave`, com a vírgula necessária. Salve. No menu do programa, escolha `5` para recarregar. Pergunte novamente `revisao violeta` e mostre que encontrou com três pontos.

**Fala sugerida:** “Incluímos esta expressão no JSON sem mudar o código Python. Depois de recarregar a base, o sistema passa a identificá-la. É uma expressão artificial apenas para esta demonstração; a melhoria do teste com usuários foi aquela que expliquei antes.”

Após gravar, remova a expressão da cópia ou descarte a cópia de demonstração. Não altere os resultados reais.

## 5:30–6:30 — Histórico, CSV e indicadores

**Mostre:** `data/historico.json`, `data/atendimentos.csv` e os métodos `registrar`, `indicadores` e `exportar_csv` em `assistente.py`.

**Fala sugerida:** “Cada atendimento concluído guarda data, origem, pergunta sem dados pessoais, ID da orientação, se encontrou, se ajudou, número de tentativas e tempo em segundos. O histórico é salvo em JSON e exportado para CSV com `csv.DictWriter`. O programa calcula a porcentagem encontrada e a porcentagem que ajudou sobre o total de atendimentos, o tempo médio dos que encontraram resposta, a média de tentativas, a facilidade de uso e a lista de dúvidas sem solução.”

**Mostre:** no menu, selecione `4` para exportar e abra o CSV. Ao sair, mostre a solicitação da nota de facilidade de 1 a 5. Se preferir pular a nota na cópia de demonstração, digite `0`.

## 6:30–7:00 — Decisão e limitação

**Fala sugerida:** “Escolhemos JSON porque ele permite atualizar as orientações sem alterar a lógica do programa. A busca usa regras transparentes e não usa IA generativa. Uma limitação é que ela depende das palavras cadastradas e pode sugerir uma resposta inadequada ou deixar de reconhecer uma dúvida. A pontuação não garante correção. A pessoa deve confirmar os detalhes na fonte oficial e no órgão responsável.”

## Depois da gravação

Publique o vídeo no YouTube como **não listado**, verifique se o link abre sem acesso especial e inclua-o no README e em `ENTREGA_FIAP.txt`. O enunciado informa que funcionalidades não demonstradas e explicadas no vídeo não serão pontuadas.
