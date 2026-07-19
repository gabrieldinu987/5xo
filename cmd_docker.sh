# 0. Se instalează toate pachetele necesare din requirements.txt (folosim in Dockerfile)
# pip install -r requirements.txt

# 1.Se creeaza imaginea 5xo:1.0 folosind Dockerfile
docker build -t 5xo-img:1.0 .

# 2. Se creeaza containerul folosind imaginea creată la punctul 1
docker run -d -p 5000:5000 --name 5xo-ctn1 5xo-img:1.0

# 3. Se verifică dacă containerul rulează
docker ps   

# 4. Se accesează aplicația web în browser la adresa http://localhost:5000
# 5. Se oprește containerul
docker stop 5xo-ctn1

# 6. Se porneste containerul
docker start 5xo-ctn1
docker exec -it 5xo-ctn1 bash

# 7. Se acceseaza containerul pentru a vedea logurile
docker logs 5xo-ctn1

# 8. Se șterge containerul
docker rm 5xo-ctn1

# 9. Se șterge imaginea
docker rmi 5xo-img:1.0

