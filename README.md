# Discord Bot MKII

Um bot para Discord desenvolvido em Python 3.10, projetado para ser modular e extensível. Este README fornece instruções sobre como instalar e usar o bot.

## Requisitos

- **Python**: Este bot foi desenvolvido utilizando Python 3.10. Certifique-se de ter a versão correta instalada em sua máquina.

## Instalação

1. **Clone o repositório**
   ```bash
   git clone https://github.com/PhobosAvenger/Discord-Bot-MKII.git
   cd Discord-Bot-MKII
   ```

2. **Crie um ambiente virtual**
   É recomendado criar um ambiente virtual para isolar as dependências do seu projeto. Para criar um ambiente virtual chamado `.venv`, execute:
   ```bash
   python -m venv .venv
   ```

3. **Ative o ambiente virtual**
   - No **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - No **Linux/Mac**:
     ```bash
     source .venv/bin/activate
     ```

4. **Instale as dependências**
   As dependências necessárias para o bot estão listadas no arquivo `requirements.txt`. Para instalá-las, execute:
   ```bash
   pip install -r requirements.txt
   ```

## Funcionalidades

- **TTS**: O bot possui funcionalidades básicas de Texto para Fala (TTS) usando `edge_TTS`, permitindo que o bot converse em canais de voz.
- **Conexão e desconexão**: O bot pode se conectar e desconectar de canais de voz utilizando os comandos:
  - `!join`: Conecta o bot ao canal de voz onde o comando foi chamado.
  - `!leave`: Desconecta o bot do canal de voz.

- **Integração com IA**: O bot pode se integrar com uma IA local usando `ollama`. Quando um membro menciona o bot (@bot) e faz uma pergunta, ele responde em texto e, se estiver em um canal de voz, reproduz o som da resposta.

## Configuração

1. **Arquivo `.env`**
   O bot requer um token do Discord para funcionar. Um arquivo chamado `.env` será criado automaticamente na pasta do projeto. Edite esse arquivo e insira seu token:
   ```plaintext
   TOKEN_API=seu_token_aqui
   ```

   Certifique-se de substituir `seu_token_aqui` pelo token real do seu bot.

## Como Usar

Para iniciar o bot, execute o seguinte comando:
```bash
python main.py
```

### Estrutura do Projeto

- **main.py**: O arquivo principal que inicia o bot.
- **cogs/**: Pasta onde os cogs (módulos) do bot estão armazenados. Você pode adicionar ou modificar funcionalidades aqui.
- **requirements.txt**: Lista de dependências do Python necessárias para o bot.

## Contribuição

Se você gostaria de contribuir para este projeto, sinta-se à vontade para abrir uma *issue* ou criar um *pull request*. Agradecemos qualquer contribuição!

## Licença

Este projeto é licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.
