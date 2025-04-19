# IAVE_Landing_page
IAVE - Landing page para o servidor offline


Esta ferramenta serve para facilitar a utilização do servidor offline do IAVE.
Em vez de fornecer o IP do servidor offline, é fornecido o IP desta landing page. E ao fim de alguns segundos, é redirecionado para o IP do servidor do IAVE.

Vantagens:
- dispensa a introdução da porta (especialmente útil para os 4.º anos);
- serve uma página de download como alternativa para download dos ficheiros .exe|.dmg|.AppImage pois poderá ser mais rápido que o download do site official.



Como correr os serviços usando **docker**.
1. alterar valor `FLASKAPP_REDIRECT_URL` no ficheiro `.env` para apontar para o servidor offline do IAVE

2. fazer download dos ficheiros do IAVE e colocar na pasta `download`

3. correr o docker container com 
```bash
docker compose up -d
```

4. parar o docker container com 
```bash
docker compose down
```