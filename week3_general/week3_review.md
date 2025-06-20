### exit()やめる
* 続けて処理はできる
* ちっちゃいプログラムならいいけど、下流の関数
* 大きいプログラム、ライブラりでは死なずにエラー出す方がいい、あまりよくわからなかった

### 他のウィンドウ？として実行する。
* 同時に同じファイルを実行するイメージ 
* subprocess.run([ターミナルにつコマンドをここに打つ])を使う
* stdout: subprocess.PIPE　print commandを変える？？
* processとは
* OSの知識を勉強して、テストフレームワークの作り方を作ってみて経験を積むしかない
* CI：テスト走らせるサーバー

### python3の裏をかいた方法
* python限定
* pyhtonのexceptionを使う
* 他の失敗したときに強制脱出
* pythonのexit()try

### [再帰降下法](https://github.com/xharaken/step2/blob/master/calculator_ll.py)

### 文脈自由文法
* 写真見て
* +をE *をT
* S:=E
* E:=T | E+T | E-T -左再帰> E = TE' 
* T*=F | T*F | T/F
* F:=N | (E)
* 実際に実装してみる

* LL1percer 再帰降下法
* LRpercer
* LL3 Java
* C はなんなのか
* コンパイラ、インタープリタ
* tree　写真

### Homework review
* はじめの閉じカッコ見つけて逆順に計算する
* カッコ内を計算する関数を作って、再帰で内側のかっこを処理
* 逆ポーランド記法（後置記法）ではかっこがなくなる、普通の数式は中間記法という
* すたっく作って＋が来たら直前の2個を取り出す
* テストケースはユニットテスト　[スライド](https://docs.google.com/presentation/d/1SurFYaYqNJ3wWi1fbDkpy7JHvrtymE37n7HcstoNhS4/edit?slide=id.g237468fbe24_1_104#slide=id.g237468fbe24_1_104)
* 網羅しているっていうのは一つの機能を一つテストで
* 関数ごとのテストかく
* テスト書くのはめんどくさいが、開発効率が上がる！
* if文があったら両方のケースをテスト
* 大きな流れを一番トップレベルにかく
* Yuikaさんのevaluate関数のところ、コメントは短くの方がいい？
