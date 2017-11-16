### Q.`$ docker [command]` を実行すると，
`Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?`となるのですが．  
### A.
```
$ docker images
Cannot connect to the Docker daemon. Is the docker daemon running on this host?
$ docker-machine start default  # 立ち上げ(そもそもdefaultが起動していないと動かない)
(default) Starting VM...
Started machines may have new IP addresses. You may need to re-run the `docker-machine env` command.
$ docker-machine env default  # 環境変数が設定されていないと、dockerコマンドが動かないため
$ eval "$(docker-machine env default)"  # dockerコマンドが動くようにする
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             VIRTUAL SIZE
```
### コンテナの一括削除
`$ docker rm -f $(docker ps -aq)`
