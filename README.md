# IAVE Landing page
IAVE - Landing page para o servidor offline


Esta ferramenta serve para facilitar a utilização do servidor offline do iave.
Em vez de fornecer o endereço do servidor offline (ip+porta), é fornecido o IP desta landing page. Ao fim de alguns segundos, é redirecionado para o endereço ip do servidor do iave.

Para além de servir de landing page, serve também para download dos ficheiros .exe|.dmg|.AppImage o que poderá ser mais rápido em caso de sobrecarga dos servidores officiais.



Como correr esta app usando **docker**.
0. Clonar este ripo
```bash
git clone https://github.com/jpedrodias/IAVE_Landing_page.git
cd IAVE_Landing_page
```


1. alterar valores das variáveis de sistema no ficheiro `.env`:
```bash
nano compose.yml
```
 - `FLASKAPP_REDIRECT_URL` - endereço do servidor do iave
 - `FLASKAPP_TITLE` - título que irá aparecer na página de loading


2. fazer download dos ficheiros executáveis do site official e colocar na pasta `flaskapp/download`
- `.exe` - para windows;
- `.dmg` - para macos;
- `.AppImage` - para linux.
Esses ficheiros estarão disponíveis em `/download`


3. correr o docker container com a instrução 

Ensaio 1: verificar se está tudo bem.
O primeiro arranque é demorado.
```bash
docker compose up
```

Interrumper com ctrl+c e voltar a correr em background
Ponderar correr usando gunicorn (ver Avançado)
```bash
docker compose up -d
```


4. Se for necessário parar o docker container que esteja a correr em background 
```bash
docker compose down -v
```

---
**Avançado:**
- editar o ficheiro `compose.yml`:
    - alterar `command` para usar `gunicorn` mas só depois do primeiro arranque. No primeiro arranque, deixar em `python`
- `/views` listará todos os dispositivos que usaram a landing page. E é ainda possível fazer downlaod dessa listagem no formato `.csv` 


---
**Limpeza docker**
```bash
df -h
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
docker network prune -f
docker system prune -a --volumes -f
df -h
```