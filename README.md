# IAVE Landing page
IAVE - Landing page para o servidor offline

Esta ferramenta serve para facilitar a utilização do servidor offline do iave.

(1)
Em vez de fornecer o endereço do servidor offline (ip+porta), é fornecido o endereço ip desta landing page (sem ser necessário indicar a porta). 
É servida uma página que ao fim de alguns segundos, redireciona para o endereço ip+porta do servidor offline do iave.

(2)
Para além de servir de landing page, serve também para se poder fazer download dos ficheiros .exe|.dmg|.AppImage, o que em caso de sobrecarga dos servidores oficiais do iave,  poderá tornar mais rápida a instalação da aplicação.


**Serviços:**
- `/view/` listará todos os dispositivos que usaram a landing page
- `/view/stats/` mostra uma estatistica por sistama operativo 
- `/download/` - para download das aplicações que estiverem na pasta de `download`
- `/download/records.csv` - para download dessa listagem completa de acessos no formato `.csv`


***

Como correr esta app usando **docker**?


# Etapa 1: 📂 Clonar 
Clonar este repositório e entrar nessa pasta.
```bash
git clone https://github.com/jpedrodias/IAVE_Landing_page.git
cd IAVE_Landing_page
```


# Etapa 2: ⚙️ Definir variáveis de ambiente 
Alterar valores das variáveis de ambiente no ficheiro ⚙️ `.env`:
```bash
nano .env
```

 - `FLASKAPP_REDIRECT_URL` - endereço do servidor offline do iave
 - `FLASKAPP_TITLE` - título que irá aparecer na página de loading



# Etapa 3: ⬇️ Download das aplicações oficiais
Fazer download dos ficheiros executáveis do site official e colocar na pasta `flaskapp/download`:


```bash
wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.12/Provas+IAVE-0.0.12.exe

wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.12/Provas+IAVE-0.0.12.AppImage

wget -P flaskapp/download https://assets.iave.pt/production/apps/intuitivo-app/v0.0.12/Provas+IAVE-0.0.12.dmg

```


# Etapa 4: 🚀 Go Live

DRY RUN: verificar se está tudo bem. O primeiro arranque é demorado pois será feito o download da imagem docker do postgres e do python. 
O ficheiro `Dockerfile` contém as instruções para preparar uma imagem personalizada para correr a aplicação flask a partir da pasta flaskapp.


**Dry run:**

Correr o docker container pela primeira vez com a instrução: 
```bash
docker compose up
```



Depois do primeiro `dry-run`, testar o acesso através do ip da máquina onde é iniciada a aplicação e verificar se está tudo bem. 


Interrumper com `Ctrl+C` e voltar a correr a aplicação mas em `-d` detached mode (em background).

```bash
docker compose up -d
```

PS: É possível correr a aplicação em paralelo usando gunicorn (ver **Avançado**)


# Etapa 5: 🧹 Fecho e limpeza total:
Se for necessário parar o docker container que esteja a correr em background 
```bash
docker compose down -v
```

As seguintes instruções limpam a cache do docker:

**⚠️Limpeza docker**
```bash
docker compose down
df -h
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker rmi $(docker images -q) -f
docker volume rm $(docker volume ls -q)
docker network prune -f
docker system prune -a --volumes -f
df -h
```



---
# Avançado
**Avançado: gunicorn**

- 🔧 editar o ficheiro `docker-compose.yml`:
  alterar `command` para usar `gunicorn` mas só depois do primeiro arranque. 
  No primeiro arranque, deixar em `python`

```yml
    command: gunicorn -w 10 -b :5000 app:app
    #command: python ./${FLASKAPP_FILE}
```


- para correr **com extras** fazer
Para além da aplicação flask e da base de dados postgres, é instalada também pgAdmin, que é uma ferramenta para ligar ao servidor postgres instalado.

```bash
docker compose -f docker-compose_with_extras.yml up
```


---

**Avançado: 🔄 updates from git**
```bash
docker compose down
git pull --autostash
docker compose up -d
```

