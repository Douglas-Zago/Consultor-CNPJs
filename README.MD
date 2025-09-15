# 📂 Consulta e Classificação de CNPJs

Este projeto é uma aplicação de desktop desenvolvida em Python para automatizar a consulta de listas de CNPJs, classificá-los com base em seus CNAEs e exportar os resultados de forma organizada para uso comercial.

A ferramenta foi construída pensando na eficiência e na facilidade de uso, com uma interface gráfica moderna e um fluxo de trabalho simples, ideal para equipes que precisam qualificar listas de empresas rapidamente.

## ✨ Funcionalidades Principais

- **Consulta em Massa**: Processa uma lista de CNPJs a partir de um arquivo de texto (`.txt`).
- **Integração com API**: Utiliza a API pública da [CNPJá](https://cnpja.com/) para obter dados detalhados das empresas.
- **Classificação Inteligente**: Separa as empresas em **Desenvolvedores** e **Não Desenvolvedores** com base na descrição de suas atividades (CNAE).
- **Extração de Contatos**: Captura automaticamente Nome Fantasia, todos os Telefones e E-mails disponíveis.
- **Interface Gráfica Moderna**: Interface intuitiva e agradável, desenvolvida com `ttkbootstrap`.
- **Exportação para CSV Único e Ordenado**: Gera um único arquivo `resultado_final.csv` com todos os dados, organizando os resultados por status (Não Desenvolvedor, Já Consultado, Desenvolvedor, etc.), pronto para ser aberto no Excel.
- **Controle de Processamento**: Evita consultas duplicadas ao manter um histórico (`ja_consultados.txt`) dos CNPJs já processados.
- **Validações de Segurança**: O programa trata arquivos de entrada vazios e ignora linhas em branco.
- **Feedback Visual**: Exibe o progresso em tempo real com uma barra e um contador (`X de Y`).

---

## 🚀 Como Usar (Para Usuário Final)

Para utilizar o programa, você precisa apenas do arquivo executável (`.exe`).

1.  **Prepare o Ambiente**:
    - Crie uma nova pasta em qualquer lugar do seu computador (ex: na Área de Trabalho).
    - Coloque o arquivo `run.exe` (ou o nome que foi dado ao executável) dentro desta pasta.

2.  **Prepare a Lista de CNPJs**:
    - Crie um arquivo de texto (`.txt`) e coloque todos os CNPJs que deseja consultar, **um por linha**.
    - Salve este arquivo na **mesma pasta** onde você colocou o `.exe`.

3.  **Execute o Programa**:
    - Dê um duplo clique no arquivo `run.exe`.
    - Na janela que abrir, clique em **"1. Escolher Arquivo (.txt)"** e selecione o arquivo com a sua lista de CNPJs.
    - Após selecionar o arquivo, clique em **"2. Iniciar Processamento"**.

4.  **Aguarde e Colete os Resultados**:
    - O programa irá processar um CNPJ a cada 12 segundos para respeitar os limites da API. Você pode acompanhar o progresso na barra de status.
    - Ao final, uma nova pasta chamada `data` será criada. Dentro dela, você encontrará um único arquivo chamado **`resultado_final.csv`**. Ele conterá todos os CNPJs processados, organizados por status e com uma coluna para facilitar a filtragem.

---

## 🛠️ Para Desenvolvedores

### Estrutura do Projeto
consulta_cnpj/
├── run.py                 # Ponto de entrada da aplicação
├── requirements.txt         # Dependências do projeto
├── data/                    # Pasta para arquivos de entrada e saída (criada automaticamente)
└── src/
├── init.py
├── api.py             # Lógica de comunicação com a API
├── main.py            # Orquestrador principal do processamento
├── parser.py          # Lógica de extração e classificação dos dados da API
└── ui.py              # Código da interface gráfica com ttkbootstrap


### Configuração do Ambiente

1.  **Clone o repositório** (se aplicável) e navegue até a pasta do projeto.

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv .venv

    # Ativar no Windows (CMD)
    .\.venv\Scripts\activate.bat

    # Ativar no Linux/Mac
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

### Executando a Aplicação

Para rodar o programa em modo de desenvolvimento, execute:
```bash
python run.py