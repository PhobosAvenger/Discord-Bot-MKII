
# Discord Bot MKII

Um bot para Discord desenvolvido em Python 3.10, projetado para ser **modular**, **extensível** e com **suporte à inteligência artificial local**.

## Requisitos

- **Python**: Este bot foi desenvolvido utilizando Python 3.10. Certifique-se de ter essa versão instalada em sua máquina.
- **Ollama**: Para uso de LLMs locais, o [Ollama](https://ollama.com) precisa estar instalado e em execução.

## Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/PhobosAvenger/Discord-Bot-MKII.git
   cd Discord-Bot-MKII
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

## Funcionalidades

- 🎤 **TTS (Texto para Fala)**: Utiliza `edge_tts` para sintetizar e reproduzir mensagens em canais de voz.
- 🔊 **Comandos de Voz**:
  - `!join`: Conecta o bot ao canal de voz atual.
  - `!leave`: Desconecta o bot do canal de voz.
- 🤖 **Integração com LLM Local (Ollama)**:
  - O bot responde a menções utilizando um modelo local via [Ollama](https://ollama.com/).
  - Pode responder em **texto** e também **falar** a resposta se estiver conectado a um canal de voz.
- 📦 **Arquitetura Modular com Cogs**: Fácil adição de novos comandos e funcionalidades.

## Integração com Ollama (LLM Local)

Este bot possui integração com LLMs locais através do Ollama, permitindo respostas com linguagem natural diretamente de modelos executados na sua máquina.

### Pré-requisitos

- Baixe e instale o [Ollama](https://ollama.com/download).
- Execute o modelo desejado, por exemplo:
  ```bash
  ollama run llama3
  ```

### Como funciona

- Ao mencionar o bot com uma pergunta (ex: `@Bot qual é a capital da França?`), ele enviará o texto para o Ollama.
- A resposta será enviada ao canal como texto.
- Se o bot estiver em um canal de voz, a resposta também será falada usando TTS.

### Configurações adicionais

Você pode personalizar o modelo do Ollama utilizado e outras opções diretamente no código ou por variáveis de ambiente.

## Configuração

1. **Arquivo `.env`**

   Um arquivo `.env` será criado automaticamente. Edite-o para adicionar seu token do bot:

   ```env
   TOKEN_API=seu_token_aqui
   ```

   Substitua `seu_token_aqui` pelo seu token real do Discord.

## Como Usar

Para iniciar o bot:

```bash
python main.py
```

## Estrutura do Projeto

```
Discord-Bot-MKII/
├── cogs/                # Módulos separados por função (ex: TTS, LLM, etc)
├── main.py              # Ponto de entrada principal do bot
├── requirements.txt     # Lista de dependências
└── .env                 # Token e variáveis de ambiente (não commitado)
```

## Contribuição

Sinta-se à vontade para contribuir! Abra uma *issue* para sugestões ou problemas, ou envie um *pull request* com melhorias.

## Licença

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
