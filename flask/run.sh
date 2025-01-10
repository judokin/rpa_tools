docker run -p 80:80 --rm --net=host -e prefix=free -e vkey=bbbhroynfjv7fexk flask-app


docker run --name npc --net=host --restart=always -e prefix=free -e vkey=yj7gv0ep0cqzr7m4  -d yunkunma/npc:latest