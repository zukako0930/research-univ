# dockerの使い方まとめ
## １．基本操作 
```
$ docker pull centos
Using default tag: latest
latest: Pulling from library/centos
d9aaf4d82f24: Pull complete 
Digest: sha256:eba772bac22c86d7d6e72421b4700c3f894ab6e35475a34014ff8de74c10872e
Status: Downloaded newer image for centos:latest
```
デフォルトではDockerHubからダウンロードされる．
tagの指定ができるので(defaultではlatest),
```
$ docker pull centos:6
```
とするとCentOS 6のイメージがダウンロードされる．

```
$ docker images
```
とすると`centos:latest`と`centos:6`の両方があることが確認できる．
これらのimageが誰によって作られたかを確認するには，`$ docker history <image ID>`とすれば良い．

## ２．コンテナを使ってみる．
### とりあえず使う．
`Hello World!`と表示するだけのコンテナを作ってみる．
コンテナの起動は`$ docker run <option> <image_name:tag> <command> <引数>`
```
$ docker run centos echo 'Hello World!'
```
centosのイメージ上で`echo 'Hello World!'`という命令を実行するという意味．
コンテナ内のプロセス状況を見てみる．PIDが1でコマンドが実行されていることがわかる．
```
$ docker run centos ps ax
 PID TTY      STAT   TIME COMMAND
    1 ?        Rs     0:00 ps ax
```
今稼働中のコンテナを確認するには，
```
$ docker ps
CONTAINER ID        IMAGE                     COMMAND                 CREATED             STATUS                      PORTS               NAMES
```
何も稼働していないのでこのようになる.
終了したコンテナも含めて表示する場合はオプションに`-a`を指定.
```
$ docker ps -a
CONTAINER ID        IMAGE                     COMMAND                 CREATED             STATUS                      PORTS               NAMES
94e906c8c447        centos                    "/bin/bash"             36 seconds ago      Exited (0) 35 seconds ago                       musing_hopper
66d647d6123e        centos                    "ps ax"                 6 minutes ago       Exited (0) 6 minutes ago                        stupefied_mcnulty
3197d9a9766b        centos                    "ps az"                 6 minutes ago       Exited (1) 6 minutes ago                        elegant_khorana
edb47e50f9f2        centos                    "echo 'Hello World!'"   8 minutes ago       Exited (0) 8 minutes ago                        musing_wescoff
366f23b0d2fd        centos                    "echo 'Hello World'"    9 minutes ago       Exited (0) 9 minutes ago                        nervous_khorana
```
### ターミナルでコンテナをいじる．
`-i`(標準入力)，`-t`(擬似ターミナル)のオプションを指定する．ubuntuのイメージ上でコンテナを起動．ローカルにubuntuのイメージが存在しない場合は自動的にDockerHub上からダウンロードされる．
```
$ docker run -i -t ubuntu bash
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
Digest: sha256:d45655633486615d164808b724b29406cb88e23d9c40ac3aaaa2d69e79e3bd5d
Status: Downloaded newer image for ubuntu:latest
root@f21fafca8c53:/# 
```
コンテナを起動すると`root@<コンテナ名>:/#`が表示され，コンテナ内の操作ができるようになる．
ここで`exit`と入力するとコンテナが停止する．
コンテナを停止せずに元のterminalに戻るには，`Ctrl+P+Q`を押す．
("コンテナをデタッチする"という．detouch:手を離す)
- そもそもデタッチモードでコンテナを起動することもできる
ここまではコンテナは実行して終了するか、直接コンテナを操作してた。画面に何も表示させず、バックグラウンドでデーモンとして動作させる`-d`オプションを使うこともできます。これはデタッチ・モードとしてコンテナを起動する．

```
$ docker run -d ubuntu ping 127.0.0.1 -c 120
31206896b6b9327b67b0830d85d55716b318bfc2a18be2316388e0e404e85e4c
docker: Error response from daemon: oci runtime error: container_linux.go:262: starting container process caused "exec: \"ping\": executable file not found in $PATH".
```
できてないっぽいので後で確認が必要です.`-c 120`は120秒で停止の意味のはず．
追記:デフォルトでは`ping`が入っていないのでそれをインストールしないとpingが使えない．
今回は飛ばします.


ここで`docker ps`でコンテナが起動していることを確認できる．一個前の．
```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
f21fafca8c53        ubuntu              "bash"              17 minutes ago      Up 17 minutes                           boring_wiles
```
ここにあるCONTAINER IDは何度も使用するため環境変数として保存しておいたほうがいい．
```
$ export CONTAINER=<CONTAINER ID>
```
コンテナの中でどのように処理が行われているのかは，
```
$ docker logs $CONTAINER
```
で確認できる．

- リアルタイムで見たい場合は`docker logs -f <コンテナID>`を実行する．あるいは`docker attach <PID>`を実行してコンテナにアタッチし、直接コンテナ内のターミナルから内容を確認することもできる．このとき実行中に`Ctrl + C`を押すと`ping`は中断し、コンテナも終了する．

稼働中のコンテナを停止するには`docker stop`または`doker kill`を使う．

なお，デタッチモードのコンテナに入るには

```
$ docker exec -ti <コンテナ名orID> bash
```

### コンテナ情報の詳細確認
```
$ docker inspect $CONTAINER
[
    {
        "Id": "f21fafca8c53d1360f7da13c96bbed6ef0e943fe88900b7f6ef918e9579df918",
        "Created": "2017-10-06T03:19:26.707882714Z",
        "Path": "bash",
        "Args": [],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 15067,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2017-10-06T04:43:12.853662321Z",
            "FinishedAt": "2017-10-06T04:09:26.737862775Z"
        },
        "Image": "sha256:2d696327ab2e15a3354ca258249358e244f3219eef76c653d0e6d3bd87f7830f",
...
```
かなりたくさんの情報が出力されるので`--format`によってフィルタリングできる．
```
$ docker inspect --format='{{.Config.Cmd}}' $CONTAINER
[bash]

JSON形式で表示する場合
$ docker inspect --format='{{json .Config.Cmd}}' $CONTAINER
["bash"]
```

### 不要なコンテナの削除
Dockerコンテナを停止してもログなどの情報は撮り続ける.
PCのメモリを圧迫する原因にもなるのでいらないコンテナは消してしまおう．
以下のコマンドは状態が`exited`のものを全て削除するコマンド.
`--format`によりフィルタリングしている．
```
$ docker rm $(docker ps -aq --filter='status=exited')
8f2e9f6c5491
94e906c8c447
66d647d6123e
3197d9a9766b
edb47e50f9f2
366f23b0d2fd
9400cb2988fc
0b4b403e223a
9b722b60a759
e69b667867d3

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS               NAMES
554ce2119517        ubuntu              "ping google.com"        About an hour ago   Created                                 ecstatic_sinoussi
6d93ec2db3ad        ubuntu              "ping 127.0.0.1 -c..."   About an hour ago   Created                                 tender_varahamihira
3d4530dba36f        ubuntu              "ping 127.0.0.1 -c..."   About an hour ago   Created                                 friendly_montalcini
31206896b6b9        ubuntu              "ping 127.0.0.1 -c..."   2 hours ago         Created                                 jovial_pasteur
f21fafca8c53        ubuntu              "bash"                   2 hours ago         Up About an hour                        boring_wiles

```
しっかり停止しているコンテナが削除されている．

### イメージの内容確定(commit)と変更差分(diff)
コンテナは起動し直すと内容が削除される．
```
$ docker run -ti ubuntu bash
root@f456cec9cee4:/# echo "hello world">/hello.txt
root@f456cec9cee4:/# ls -al /hello.txt
-rw-r--r-- 1 root root 12 Oct  6 05:44 /hello.txt
root@f456cec9cee4:/# exit
```
もう一度イメージ起動すると，(imageの起動がrun，コンテナの起動がstart)
```
$ docker run -ti ubuntu bash
root@5a5d27b3d983:/# ls -l /hello.txt
ls: cannot access '/hello.txt': No such file or directory
```
見つからない.
もう一度`/hello.txt`を作り，コンテナを停止する.
```
$ docker run -ti ubuntu bash
root@afbeed801ba7:/# echo "hello world">/hello.txt
root@afbeed801ba7:/# ls -al /hello.txt            
-rw-r--r-- 1 root root 12 Oct  6 05:53 /hello.txt
root@afbeed801ba7:/# exit
```
`docker ps -l`で最後にしようしたコンテナを確認．`-l`はlatestかlast
```
$ docker ps -l
CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS                      PORTS               NAMES
afbeed801ba7        ubuntu              "bash"              About a minute ago   Exited (0) 59 seconds ago                       condescending_borg
```
`docker diff`で差分を確認．
```
$ docker diff afbeed801ba7
A /hello.txt
C /root
A /root/.bash_history
```
この差分を保持するにはgit同様に`commit`する必要がある．`docker commit <コンテナID> <レポジトリ名:タグ>`で指定．レポジトリ名とタグは任意のものを作れるので，バージョンを自由につけることができる．
```
$ docker commit $CONTAINER test:1.0
sha256:a3dcb5d3adc7e15907e37e1838bc56f7f0d76fd065bca34ea25f4e6d317b4b66
```
`commit`したimageは`docker images`で確認できる．
```
$ docker images
REPOSITORY                TAG                 IMAGE ID            CREATED             SIZE
test                      1.0                 a3dcb5d3adc7        23 seconds ago      122MB
```
IMAGEIDを環境変数に代入.
このコンテナを使えば作成した`/hello.txt`を確認できる．
```
$ export IMAGEID=a3dcb5d3adc7
$ docker run test:1.0 cat /hello.txt
hello world
```
`docker history`で情報も確認できる．
```
$ docker history $IMAGEID
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
a3dcb5d3adc7        5 minutes ago       bash                                            65B                 
2d696327ab2e        2 weeks ago         /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B                  
<missing>           2 weeks ago         /bin/sh -c mkdir -p /run/systemd && echo '...   7B                  
<missing>           2 weeks ago         /bin/sh -c sed -i 's/^#\s*\(deb.*universe\...   2.76kB              
<missing>           2 weeks ago         /bin/sh -c rm -rf /var/lib/apt/lists/*          0B                  
<missing>           2 weeks ago         /bin/sh -c set -xe   && echo '#!/bin/sh' >...   745B                
<missing>           2 weeks ago         /bin/sh -c #(nop) ADD file:5ed435208da6621...   122MB               

```

## 今後
- dockerコンテナ内からpingが通らないのでその辺も勉強したい．
### cf
`nginx`はエンジンエックスと読みます．
`Apache`と並ぶOSSのWebサーバ．
