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

#10. Porneste aplicatia folosind docker-compose
docker-compose up -d

#11. Opreste aplicatia folosind docker-compose
docker-compose down 

#12 Build Jenkins container cu acces la Docker
docker run -d \
  --name jenkins-ctn \
  --restart unless-stopped \
  -p 8080:8080 \
  -p 50000:50000 \
  -v jenkins-vol:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v $(which docker):/usr/bin/docker \
  jenkins/jenkins:lts