# IAVE Landing page
IAVE - Landing page para o servidor offline


Esta ferramenta serve para facilitar a utilização do servidor offline do iave.
Em vez de fornecer o endereço do servidor offline (ip+porta), é fornecido o IP desta landing page. Ao fim de alguns segundos, é redirecionado para o endereço ip do servidor do iave.

Para além de servir de landing page, serve também para download dos ficheiros .exe|.dmg|.AppImage o que poderá ser mais rápido em caso de sobrecarga dos servidores officiais.



Como correr esta app usando **docker**.
1. alterar valores das variáveis de sistema no ficheiro `.env`:
 - `FLASKAPP_REDIRECT_URL` - endereço do servidor do iave
 - `FLASKAPP_TITLE` - título que irá aparecer na página de loading


2. fazer download dos ficheiros executáveis do site official e colocar na pasta `flaskapp/download`
- `.exe` - para windows;
- `.dmg` - para macos;
- `.AppImage` - para linux.
Esses ficheiros estarão disponíveis em `/download`


3. correr o docker container com a instrução 
```bash
docker compose up -d
```

4. parar o docker container com 
```bash
docker compose down
```

---
**Avançado:**
- editar o ficheiro `compose.yml`:
    - remover os serviço `adminer` e `pgadmin` pois não têm qualquer utilidade.
    - alterar `command` para usar `gunicorn` mas só depois do primeiro arranque. No primeiro arranque, deixar em `python`
- `/views` listará todos os dispositivos que usaram a landing page. E é ainda possível fazer downlaod dessa listagem no formato `.csv` 