# The Strucuture of this repository

現在のmain branch内の各directlyは以下のようになっています。

```mermaid
graph BT
    subgraph Week4
        direction LR
        W4G(week4_general)
    end
    subgraph Week3
        direction LR
        W3G(week3_general)
        W3H12(week3_homework_1and2)
        W3H3(week3_homework_3)
        W3H4(week3_homework_4)
    end

    subgraph Week2
        direction LR
        W2G(week2_general)
        W2H1(week2_homework_1)
        W2H2(week2_homework_2)
        W2H34(week2_homework_3and4)
    end

    subgraph Week1
        direction LR
        W1G(week1_general)
        W1A1(week1_anagram1_1)
        W1A2(week1_anagram1_2)
        W1A3(week1_anagram2_1)
        W1H1(week1_homework_1) --> W1A1 & W1A2 & W1A3
    end
```

# Repository Explanation

## general

* homework_summary: 宿題の提出ファイルについての説明（目標、方針、メゾット、工夫した点など）を見てもらう意識でわかりやすく書く！取り組んだ中で出てきた疑問点。
* classmemo: 授業中に学んだこと、気になったこと。
* review: メンターさんとの面談、授業での宿題のreviewで学んだこと。自分のコードや他人のコードを読んで、気になったところや真似したいと思ったこと。

## homework
* 詳しい内容や構造については、general内のhomework_summaryをご覧ください。

