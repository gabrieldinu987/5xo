# 5XO — Five in a Row

Joc de tip "X și 0" extins, jucat pe o tablă de **50 × 50 celule**. Câștigă primul jucător care aliniază **5 simboluri consecutive**, pe orizontală, verticală sau diagonală. Aplicația este scrisă în **Flask** (backend Python) cu un frontend simplu în **HTML / CSS / JavaScript**, și este livrată printr-un pipeline **CI/CD** complet: Jenkins → Docker → Kubernetes (Minikube).

---

## Cuprins

- [Cum se joacă](#cum-se-joacă)
- [Arhitectura aplicației](#arhitectura-aplicației)
- [Structura proiectului](#structura-proiectului)
- [Rulare locală](#rulare-locală)
- [Rulare cu Docker](#rulare-cu-docker)
- [API](#api)
- [CI/CD — Jenkins, Docker, Kubernetes](#cicd--jenkins-docker-kubernetes)
- [Infrastructura Jenkins](#infrastructura-jenkins)
- [Deployment Kubernetes](#deployment-kubernetes)
- [Fluxul complet end-to-end](#fluxul-complet-end-to-end)

---

## Cum se joacă

- Tabla are **50 × 50** de celule, inițial goale.
- Jucătorii `X` și `O` mută pe rând, câte o celulă.
- După fiecare mutare se verifică 4 direcții (orizontală, verticală, cele 2 diagonale) pornind din celula jucată; dacă există **5 simboluri identice consecutive**, jocul se termină cu un câștigător.
- Dacă tabla se umple fără câștigător, jocul se termină la egalitate (`draw`).
- Butonul **Restart Game** apelează `/reset` și repornește partida.

## Arhitectura aplicației

Codul Python este organizat pe straturi, fiecare cu o singură responsabilitate:

```
app.py               → rute Flask: "/", "/state", "/move", "/reset"
   └── game/Game      → fațadă simplă peste GameService
         └── game/GameService → regulile jocului (rând curent, victorie, egalitate)
               ├── game/Board          → grid 50×50, plasare simbol, validare poziții
               └── game/WinnerChecker  → verifică 5 în linie pe 4 direcții
```

- **`Board`** știe doar despre grid: `is_inside`, `is_empty`, `place_symbol`.
- **`WinnerChecker`** este `@classmethod`/`@staticmethod`, fără stare proprie — primește tabla și poziția ultimei mutări și numără simbolurile consecutive în ambele sensuri ale fiecărei direcții.
- **`GameService`** orchestrează: plasează simbolul, verifică victoria, verifică egalitatea, schimbă jucătorul curent.
- **`Game`** este un wrapper subțire folosit de `app.py`, ca punct unic de intrare în logica jocului.

Frontend-ul (`game.js`) este *state-driven*: după fiecare acțiune (mutare/reset) preia starea completă de la server (`board`, `current_player`, `game_over`, `winner`) și redesenează tabla — nu ține propria logică de joc.

## Structura proiectului

```
.
├── app.py                 # Server Flask, rute HTTP
├── game/
│   ├── __init__.py
│   ├── game.py             # Game — fațadă
│   ├── service.py          # GameService — regulile jocului
│   ├── board.py            # Board — grid 50×50
│   └── winner.py           # WinnerChecker — detecție victorie
├── templates/
│   └── index.html          # Pagina principală (Jinja2)
├── static/
│   ├── css/style.css       # Layout + stilizare tablă
│   └── js/game.js          # Logică frontend (fetch API)
├── requirements.txt
├── Dockerfile              # Imagine aplicație (python:3.13-slim)
│
├── k8s/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
│
├── jenkins/
    ├── Jenkinsfile               # Pipeline CI/CD
    ├── docker-compose.yml        # Container Jenkins (agent DevOps)
    ├── Dockerfile (jenkins)      # Imagine Jenkins cu Docker CLI, kubectl, minikube
    └── plugins.txt               # Plugin-uri Jenkins instalate automat
```

> Notă: `app.py` importă `from game.game import Game`, deci fișierele `game.py`, `service.py`, `board.py`, `winner.py` trebuie să fie într-un pachet `game/` (alături de `__init__.py`).

## Rulare locală

Cerințe: Python 3.10+ (recomandat 3.13).

```bash
pip install -r requirements.txt
python3 app.py
```

Aplicația pornește pe `http://localhost:5000`.

## Rulare cu Docker

```bash
docker build -t 5xo:latest .
docker run -p 5000:5000 5xo:latest
```

Imaginea include un `HEALTHCHECK` care verifică periodic `http://localhost:5000`.

## API

| Metodă | Endpoint  | Descriere                                             |
|--------|-----------|--------------------------------------------------------|
| GET    | `/`       | Randează pagina principală (`index.html`)              |
| GET    | `/state`  | Returnează starea curentă a jocului (JSON)              |
| POST   | `/move`   | Body: `{ "row": int, "col": int }` — plasează o mutare  |
| POST   | `/reset`  | Repornește jocul                                        |

Exemplu răspuns `/state`:

```json
{
  "board": [[null, "X", null, ...], ...],
  "current_player": "O",
  "game_over": false,
  "winner": null
}
```

O mutare invalidă (poziție ocupată, în afara tablei, sau joc deja terminat) răspunde cu **HTTP 400** și `{ "success": false, "message": "..." }`.

---

## CI/CD — Jenkins, Docker, Kubernetes

Pipeline-ul (`Jenkinsfile`) rulează la fiecare `git push` și trece prin 8 etape:

1. **Checkout** — `checkout scm`
2. **Environment** — verifică `docker`, `kubectl`, `git`, `python3`, contextul cluster-ului curent
3. **Build Docker Image** — `docker build -t 5xo:latest .`
4. **Load Image into Minikube** — comută la daemon-ul Docker al Minikube (`minikube docker-env`), reconstruiește imaginea acolo, apoi verifică prezența ei cu `ctr images ls`
5. **Deploy Namespace** — `kubectl apply -f k8s/namespace.yaml`
6. **Deploy Application** — `kubectl apply -f k8s/deployment.yaml` + `k8s/service.yaml`
7. **Restart Deployment** — `kubectl rollout restart deployment/fivexo` + `kubectl rollout status --timeout=180s`
8. **Cluster Status** — afișează pods, services, deployments și evenimente din namespace-ul `fivexo`

Configurări suplimentare ale pipeline-ului:
- `disableConcurrentBuilds()` — nu rulează două build-uri simultan
- `buildDiscarder(logRotator(numToKeepStr: '10'))` — păstrează ultimele 10 build-uri
- **`post { failure { ... } }`** — la eșec, colectează automat `kubectl describe deployment/pods`, logurile aplicației și evenimentele recente, pentru debugging rapid
- **`post { always { cleanWs() } }`** — curăță workspace-ul după fiecare rulare

## Infrastructura Jenkins

Jenkins rulează el însuși într-un container (`docker-compose.yml`), construit dintr-o imagine dedicată (`Dockerfile` DevOps) care conține:

- **Docker CLI** — pentru a construi imaginea aplicației
- **kubectl** — pentru a comunica cu clusterul Kubernetes
- **Minikube CLI** — pentru a încărca imaginea locală în cluster
- Plugin-urile din `plugins.txt`: `docker-workflow`, `workflow-aggregator`, `pipeline-stage-view`, `git`, `github`, `credentials`, `ssh-credentials`, `matrix-auth`, `role-strategy`, `blueocean`, `ws-cleanup`

Pentru a putea construi imagini și accesa clusterul de pe host, containerul Jenkins montează:

| Volum / variabilă        | Rol                                                             |
|---------------------------|------------------------------------------------------------------|
| `jenkins-vol`              | volum persistent pentru `/var/jenkins_home`                     |
| `/var/run/docker.sock`     | acces direct la daemon-ul Docker al host-ului (Docker-in-Docker) |
| `~/.kube` (read-only)      | configurația clusterului Minikube (`KUBECONFIG`)                 |
| `~/.minikube` (read-only)  | certificate și context Minikube (`MINIKUBE_HOME`)                 |
| rețea `minikube` (externă) | conectivitate directă cu clusterul                                |

## Deployment Kubernetes

Resursele Kubernetes (`k8s/*.yaml`) definesc:

- **Namespace `fivexo`** — izolează toate resursele aplicației.
- **Deployment `fivexo`** — 1 replică, imaginea `5xo:latest` (`imagePullPolicy: Never`, deoarece imaginea e construită local în Minikube), cu:
  - `readinessProbe` / `livenessProbe` pe `GET /:5000`
  - resurse: **requests** 100m CPU / 128Mi memorie, **limits** 500m CPU / 512Mi memorie
- **Service `fivexo-service`** (tip `NodePort`) — expune portul intern `5000` pe `nodePort: 30080`, accesibil din afara clusterului.

## Fluxul complet end-to-end

```
Dezvoltator ──push──▶ Jenkins ──checkout──▶ Build imagine Docker
     ▲                                              │
     │                                              ▼
   Cod nou                                  Load imagine în Minikube
     │                                              │
     │                                              ▼
     │                              kubectl apply (namespace + deployment + service)
     │                                              │
     │                                              ▼
     └──────────────────────────  Rollout restart + health checks → Aplicație live
                                        (nodePort 30080)
```

La finalul pipeline-ului, aplicația 5XO rulează în clusterul Kubernetes local (Minikube), redeployată automat la fiecare commit, fără intervenție manuală.

---
