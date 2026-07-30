# 5XO — Five in a Row

Aplicație web care implementează jocul „X și O" (Five in a Row) pe o tablă de **50×50** celule. Câștigă primul jucător care aliniază **5 simboluri identice**, pe orizontală, verticală sau diagonală.

Proiectul include backend-ul jocului (Python/Flask), interfața web (HTML/CSS/JS), containerizarea (Docker), desfășurarea în Kubernetes (Minikube) și un pipeline CI/CD complet (Jenkins).

---

## Cuprins

- [Arhitectură](#arhitectură)
- [Structura proiectului](#structura-proiectului)
- [Reguli de joc](#reguli-de-joc)
- [Rulare locală](#rulare-locală)
- [Rulare cu Docker](#rulare-cu-docker)
- [Desfășurare pe Kubernetes](#desfășurare-pe-kubernetes)
- [Pipeline CI/CD (Jenkins)](#pipeline-cicd-jenkins)
- [API](#api)
- [Tehnologii folosite](#tehnologii-folosite)

---

## Arhitectură

```
Browser (index.html + game.js + style.css)
        │  fetch() → POST /move, GET /state, POST /reset
        ▼
Flask (app.py)
        │
        ▼
Game (game.py)              — fațadă simplă
        │
        ▼
GameService (service.py)    — regulile jocului
        │
        ├── Board (board.py)          — grila 50×50
        └── WinnerChecker (winner.py) — verificare victorie
```

Logica jocului (pachetul `game/`) este complet independentă de stratul web — Flask doar o expune printr-un API REST minimal.

---

## Structura proiectului

```
.
├── game/
│   ├── __init__.py     # marchează game/ ca pachet Python
│   ├── game.py         # clasa Game — fațadă peste GameService
│   ├── service.py      # clasa GameService — regulile jocului
│   ├── board.py        # clasa Board — grila 50x50
│   └── winner.py       # clasa WinnerChecker — verificare aliniere de 5
│
├── static/
│   ├── css/style.css    # stilizare tablă, celule, panouri
│   └── js/game.js       # logică frontend, comunicare cu API-ul
├── templates/
│   └── index.html       # pagina principală (Jinja2)
│
├── app.py                # aplicația Flask + rutele API
├── requirements.txt      # dependințe Python (Flask ≥ 3.1)
├── Dockerfile             # imaginea aplicației 5XO
│
├── k8s/
│   ├── namespace.yaml     # namespace „fivexo”
│   ├── deployment.yaml    # Deployment (1 replică, probes, resurse)
│   └── service.yaml       # Service NodePort (port extern 30080)
│
├── Jenkinsfile             # pipeline CI/CD declarativ
├── docker-compose.yml      # rulează containerul Jenkins local
├── Dockerfile (jenkins)     # imagine Jenkins personalizată (docker, kubectl, minikube)
└── plugins.txt              # plugin-uri Jenkins instalate automat
```

> Notă: structura de directoare (`game/`, `static/`, `templates/`, `k8s/`) este cea presupusă de importurile din cod (`from game.board import Board`) și de `url_for('static', ...)` din `index.html`.

---

## Reguli de joc

- Tabla are **50 × 50** celule.
- Jucătorii alternează, `X` mută primul.
- La fiecare mutare se verifică 4 direcții posibile de aliniere: orizontală, verticală, diagonala `\` și diagonala `/`.
- Jocul se termină cu **victorie** când un jucător aliniază 5 (sau mai multe) simboluri consecutive pe oricare din cele 4 direcții.
- Jocul se termină cu **egalitate** dacă tabla se umple complet fără câștigător.
- O mutare pe o celulă ocupată, în afara tablei, sau după terminarea jocului este respinsă cu eroare (HTTP 400).

---

## Rulare locală

Cerințe: Python 3.13+ (recomandat).

```bash
pip install -r requirements.txt
python app.py
```

Aplicația pornește pe `http://localhost:5000`.

---

## Rulare cu Docker

```bash
docker build -t 5xo:latest .
docker run -p 5000:5000 5xo:latest
```

Aplicația va fi disponibilă la `http://localhost:5000`.

---

## Desfășurare pe Kubernetes

Presupune un cluster Minikube pornit local.

```bash
# 1. Construiește imaginea direct în Minikube
eval $(minikube docker-env)
docker build -t 5xo:latest .
eval $(minikube docker-env -u)

# 2. Aplică manifestele
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# 3. Verifică statusul
kubectl get pods -n fivexo
kubectl get svc -n fivexo
```

Aplicația va fi accesibilă pe portul `30080` al nodului Minikube (`imagePullPolicy: Never`, deoarece imaginea este locală, nu dintr-un registry extern).

---

## Pipeline CI/CD (Jenkins)

`Jenkinsfile` definește un pipeline declarativ cu 8 etape, rulat automat la fiecare build:

| # | Stage | Descriere |
|---|-------|-----------|
| 1 | **Checkout** | Clonează codul sursă din repository (`checkout scm`). |
| 2 | **Environment** | Afișează diagnostic: unelte instalate, context Kubernetes, noduri cluster. |
| 3 | **Build Docker Image** | Construiește imaginea `5xo:latest` din `Dockerfile`. |
| 4 | **Load Image into Minikube** | Reconstruiește imaginea în demonul Docker intern al Minikube și verifică prezența ei. |
| 5 | **Deploy Namespace** | Aplică `k8s/namespace.yaml`. |
| 6 | **Deploy Application** | Aplică `k8s/deployment.yaml` și `k8s/service.yaml`. |
| 7 | **Restart Deployment** | `kubectl rollout restart` + `rollout status` (timeout 180s) pentru a garanta rularea imaginii noi. |
| 8 | **Cluster Status** | Afișează poduri, servicii, deployment-uri și evenimente din namespace-ul `fivexo`. |

La eșec (`post { failure }`), pipeline-ul colectează automat log-uri, descrieri de resurse și evenimente pentru depanare rapidă. `post { always }` curăță workspace-ul (`cleanWs()`).

### Mediul Jenkins

Jenkins rulează într-o imagine personalizată (`Dockerfile` + `plugins.txt`), pornind de la `jenkins/jenkins:lts`, cu Docker CLI, `kubectl` și Minikube preinstalate. `docker-compose.yml` pornește acest container local, montând `/var/run/docker.sock` și configurația `kubectl`/Minikube a mașinii gazdă, astfel încât Jenkins să poată construi imagini și comunica direct cu clusterul.

---

## API

| Metodă | Rută | Descriere |
|--------|------|-----------|
| `GET`  | `/`       | Randează pagina principală (`index.html`). |
| `GET`  | `/state`  | Returnează starea curentă a jocului (JSON). |
| `POST` | `/move`   | Efectuează o mutare. Body: `{"row": int, "col": int}`. Returnează starea actualizată sau eroare (400). |
| `POST` | `/reset`  | Resetează jocul la starea inițială. |

**Exemplu răspuns `/state`:**

```json
{
  "board": [[null, null, ...], ...],
  "current_player": "X",
  "game_over": false,
  "winner": null
}
```

---

## Tehnologii folosite

- **Backend:** Python 3.13, Flask
- **Frontend:** HTML5, CSS3, JavaScript (vanilla, fetch API)
- **Containerizare:** Docker
- **Orchestrare:** Kubernetes (Minikube)
- **CI/CD:** Jenkins (pipeline declarativ)
