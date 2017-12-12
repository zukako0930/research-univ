# Git〜 pull request が送られてきたら 編〜
## 1. `Pull Request`を取り込むには．

```
1.「Merge pull request」ボタンをクリックして取り込む→非常に危険な行為!
2. 送られたPull Requestが正常に動作するのか、安全なコードになっているかなど、手元の開発環境に持ってきて検証し、リポジトリに取り込む
3. Jenkinsなどを利用した継続的インテグレーションを実施して自動テストなどを実行し、既存の機能を破壊していないことを確かめてからリポジトリに取り込む
```

## 手元でコードの動作や内容を確認．
```
#差分を取得 fetchはpullと違ってデータのダウンロードのみ．ローカルへの影響はない．
#そもそも自分のローカルにないブランチ(誰かが作ったブランチ)を作り出してる．
$ git fetch origin pull/#xx<ID>/head:<BRANCHNAME>

#確認用ブランチへの切り替え
$ git checkout <BRANCHNAME>
```
### <コードの動作や内容を実際に確認のフェイズ>
okなら
```
# Issueがあればそれも同時にcloseしたほうが便利なので
$ git commit —allow-empty -m “closed #issue番号”
$ git push origin <BRANCHNAME>
```
そしてmasterにマージする．
ブラウザで「Merge pull request」ボタンをクリックしてマージでもいいが、CLI操作でマージするのが普通．
```
$ git checkout master
$ git merge --no-ff BRANCHNAME
$ git push origin master
```

## 参考文献
gtaiyou24