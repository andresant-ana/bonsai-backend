# BonsAI Backend com FastAPI - Containerizado com Docker

Este projeto contém o backend da aplicação BonsAI implementado com FastAPI e containerizado com Docker. O backend processa documentos e faz chamadas para a API da OpenAI.

## Pré-requisitos

Antes de executar este projeto, você precisará ter instalado em sua máquina:

- [Docker](https://www.docker.com/get-started)
- Uma chave de API válida da OpenAI

## Configuração

1. Clone este repositório em sua máquina local:
   ```bash
   git clone https://github.com/andresant-ana/bonsai-backend.git
   cd bonsai-backend
   ```

2. Crie um arquivo `.env` na raiz do projeto e adicione sua chave de API da OpenAI:
   ```
   OPENAI_API_KEY=sua_chave_api_aqui
   ```

3. Certifique-se de não compartilhar ou commitar o arquivo `.env` em repositórios públicos.

## Como executar o projeto com Docker

Siga as instruções abaixo para criar e executar o container:

### 1. Criar a imagem Docker

Dentro da pasta do projeto, execute o seguinte comando para criar a imagem Docker:

```bash
docker build -t bonsai-backend .
```

Este comando irá:
1. Usar o `Dockerfile` para criar uma imagem Docker com o backend FastAPI.
2. Instalar todas as dependências listadas no arquivo `requirements.txt`.

### 2. Rodar o container

Após a construção da imagem, rode o container com o comando:

```bash
docker run -d --name bonsai-backend -p 8000:8000 --env-file .env bonsai-backend
```

Este comando irá:
- Rodar o container em background (`-d`).
- Nomear o container como `bonsai-backend`.
- Mapear a porta `8000` do container para a porta `8000` do host.
- Usar as variáveis de ambiente do arquivo `.env`.

### 3. Acessar a API

Uma vez que o container está em execução, você pode acessar a documentação da API no navegador em:

- [http://localhost:8000/docs](http://localhost:8000/docs)

## Exemplos de uso da API

Aqui estão exemplos de como usar os principais endpoints da API:

### 1. Upload do documento da empresa

```json
POST /upload-document
Content-Type: multipart/form-data

file: [arquivo do documento]
```

### 2. Criar uma nova conversa

```json
POST /conversations
Content-Type: application/json

{
  "id": "conv1",
  "title": "Minha primeira conversa",
  "messages": []
}
```

### 3. Enviar uma mensagem para uma conversa

```json
POST /conversations/{conversation_id}/messages
Content-Type: application/json

{
  "role": "user",
  "content": "Quais são os principais serviços oferecidos pela empresa?"
}
```

### 4. Listar todas as conversas

```
GET /conversations
```

### 5. Obter uma conversa específica

```
GET /conversations/{conversation_id}
```

### 6. Editar uma mensagem existente

```json
PUT /conversations/{conversation_id}/messages/{message_index}
Content-Type: application/json

{
  "role": "user",
  "content": "Pode me dar mais detalhes sobre os serviços de IaaS?"
}
```

### 7. Atualizar o título de uma conversa

```json
PUT /conversations/{conversation_id}
Content-Type: application/json

{
  "title": "Conversa sobre serviços de cloud"
}
```

### 8. Deletar uma conversa

```
DELETE /conversations/{conversation_id}
```

## Tecnologias utilizadas

- **Python 3.10**
- **FastAPI**
- **Docker**
- **OpenAI API**

## Observações

- Este projeto faz uso da API da OpenAI. Certifique-se de configurar corretamente a chave de API no arquivo `.env`.
- Nunca compartilhe sua chave de API da OpenAI publicamente ou a inclua em repositórios de código.
- O arquivo `doc.txt` contém informações sobre a empresa fictícia e é usado para contextualizar as respostas do assistente AI.

## Segurança

- A chave de API da OpenAI é gerenciada através de variáveis de ambiente para maior segurança.
- O arquivo `.env` contendo a chave de API não é incluído no controle de versão.
- Certifique-se de não expor sua chave de API em logs, saídas de console ou repositórios públicos.
