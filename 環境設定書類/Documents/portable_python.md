環境を有効化済みの状態で`conda env export`を実行することで、環境設定をYAML形式で書き出すことができる。
<br>`$ conda env export > xxxx.yaml`
```yaml:xxxx.yaml

name: xxxx
dependencies:
- mkl=11.3.3=0
- numpy=1.11.1=py35_0
- openssl=1.0.2h=1
- pip=8.1.2=py35_0
- python=3.5.1=5
- readline=6.2=2
- scipy=0.17.1=np111py35_1
- setuptools=23.0.0=py35_0
- sqlite=3.13.0=0
- tk=8.5.18=0
- wheel=0.29.0=py35_0
- xz=5.2.2=0
- zlib=1.2.8=3
- pip:
  - peewee==2.8.1

```
※カレントディレクトリに保存される
<br>`xxxx.yaml`が存在するディレクトリで，
<br>`$ conda env create --file xxxx.yaml`
<br>を実行するとその記載通りの仮想環境が構築される．

