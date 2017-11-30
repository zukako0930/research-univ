環境を有効化(source activate)済みの状態で`conda env export`を実行することで、環境設定をYAML形式で書き出すことができる。
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

## 他人の環境でやったときにpyenvと競合していた問題
本来なら
`source activate py35`
で環境が切り替わるはずだがactivateがpyenvと競合しているので，
Activateのパスを明示的に指定．
`source $PYENV_ROOT/versions/anaconda4.3.1/bin/activate py35`
とする.
deactivateは競合していないっぽかった.
[!ここで解決]https://qiita.com/y__sama/items/f732bb7bec2bff355b69
