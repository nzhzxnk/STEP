## 木構造とハッシュテーブルの比較
木構造を使えば O(log N)、ハッシュテーブルを使えばほぼ O(1) で検索・追加・削除を実現することができて、これだけ見ればハッシュテーブルのほうが優れているように見える。
ところが現実の大規模なデータベースでは、ハッシュテーブルではなく木構造が使われることが多い。
ハッシュテーブルが現実で使用されづらい理由について考察した。

### 1. 再ハッシュによる一時的な処理速度低下

* ハッシュテーブルは通常 $O(1)$ の高速な操作が期待されるが、再ハッシュが発生すると一時的に処理速度が大幅に低下する可能性がある。
* これは、テーブルの容量が不足した際に、既存のすべての要素（$N$個）に対してハッシュ値を再計算し、新しいサイズのバケットに再挿入する必要があるがそれに $O(N)$ の計算コストがかかるためである。
* 特にリアルタイム性が求められるシステムや、大量のデータ挿入が頻繁に発生する環境では、この $O(N)$ の操作が突然発生することで処理に大きなラグが生じる可能性があり実用的でないと考えた。
* 再ハッシュが複雑に行われていると、予期せぬエラーが発生した場合に、どの要素がどの過程で影響を受けたのかを追跡するなどのデバックが難しくなる可能性があると考えた。（homework1で私自身が経験しただけなので、スキルがあれば難しくないのかもしれない。）

### 2. ハッシュ関数やデータの傾向による衝突

* ハッシュテーブルの性能は、ハッシュ関数の品質とデータの分布に大きく依存してしまう。
* 特定のパターンを持つキーが集中して同じハッシュ値になる場合や、ハッシュ値の範囲が偏る場合、頻繁に衝突が発生する。例えば、連続した数値や似たような文字列が大量に与えられると、たとえ良いハッシュ関数を使っても衝突が多発する可能性がある。
* 衝突が多発すると、同じバケットに多くの要素が連結して格納され、探索に最悪 $O(N)$ の時間がかかり、確実に $O(logN)$の計算量が保証されている木構造に比べ実用的とはいえない。
* また、衝突をたくさん起こすことで処理速度が落ちるという性質を利用した攻撃に対して脆弱であり、セキュリティー面でも不安がある。

### 3. データの順序や前後関係を保持できない
* ハッシュテーブルは、データの挿入順序あるいは要素間の前後関係を内部的に保持するようには設計されていない。
* そのため、例えばある範囲 $(a, b)$ 内のすべてのデータといった範囲検索の操作は非効率になる。このような用途では、二分探索木（Binary Search Tree）のような木構造の方が、順序性を利用してより高速に検索を行うことができると考える。

---