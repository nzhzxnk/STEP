STEP/

├── week1_class/
├── week1_homework_1/
│ ├── week1_anagram1_1/
│ ├── week1_anagram1_2/
│ └── week1_anagram2_1/
│
├── week2_class/
├── week2_homework_1/
├── week2_homework_2/
├── week2_homework_3and4/
│
├── week3_class/
├── week3_homework_1and2/
├── week3_homework_3/
├── week3_homework_4/
│

graph BT

```mermaid
    A(STEP/)
    subgraph Week 1
        direction BT
        W1A3(week1_anagram2_1/) --> W1H1(week1_homework_1/)
        W1A2(week1_anagram1_2/) --> W1H1
        W1A1(week1_anagram1_1/) --> W1H1
    end
    A --> W1H1 
    subgraph Week 1 Class
        direction BT
        W1C(week1_class/)
    end
    A --> W1C 

    subgraph Week 2
        direction BT
        W2H34(week2_homework_3and4/)
        W2H2(week2_homework_2/)
        W2H1(week2_homework_1/)
    end
    A --> W2H1
    A --> W2H2
    A --> W2H34

    subgraph Week 2 Class
        direction BT
        W2C(week2_class/)
    end
    A --> W2C

    subgraph Week 3
        direction BT
        W3H4(week3_homework_4/)
        W3H3(week3_homework_3/)
        W3H12(week3_homework_1and2/)
    end
    A --> W3H12
    A --> W3H3
    A --> W3H4

    subgraph Week 3 Class
        direction BT
        W3C(week3_class/)
    end
    A --> W3C
