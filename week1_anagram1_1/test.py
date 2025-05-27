import unittest
from dictionary import create_dict
from main import find_anagram

class TestFindAnagram(unittest.TestCase):
# unittest.Testcaseではdef test_...という関数を全て実行する
    @classmethod
    # class内で一回だけ呼び出す関数でang_dictを作る
    def setUpClass(cls):
        cls.ang_dict = create_dict()
    # test_1:文字列の順番が異なってもきちんとangramを認識できるか、自己と同じものを除外できるか
    def test_1(self):
        test_case = [
            ("esy",["yes"]),
            ("eys",["yes"]),
            ("sey",["yes"]),
            ("sye",["yes"]),
            ("esy",["yes"]),
            ("yes",[]),
            ("yse",["yes"])
        ]
        for Input,expected in test_case:
            with self.subTest(Input=Input):
                ans,count = find_anagram(Input,self.ang_dict)
                if count != 0:
                    self.assertEqual(sorted(ans),sorted(expected))
                else:
                    self.assertEqual(count,len(expected))
    # test_2:部分文字列は別物として認識できているか
    def test_2(self):
        test_case = [
            ("i", []),
            ("ik", []),
            ("ikn", ["ink","kin"]),
            ("iknw", ["wink"]),
            ("iknwa", []),
            ("iknwab", []),
            ("iknwabc", [])
        ]
        for Input,expected in test_case:
            with self.subTest(Input=Input):
                ans,count = find_anagram(Input,self.ang_dict)
                if count != 0:
                    self.assertEqual(sorted(ans),sorted(expected))
                else:
                    self.assertEqual(count,len(expected))
    # test_3:anagramが多い(valueの数が多い)ものでも過不足なく認識できているか
    def test_3(self):
        test_case = [
            ("aerst",['aster', 'rates', 'resat', 'satre', 'stare', 'tares', 'tears']),
            ("aetsr",['aster', 'rates', 'resat', 'satre', 'stare', 'tares', 'tears']),
            ("aster",['rates', 'resat', 'satre', 'stare', 'tares', 'tears'])
        ]
        for Input,expected in test_case:
            with self.subTest(Input=Input):
                ans,count = find_anagram(Input,self.ang_dict)
                self.assertEqual(sorted(ans),sorted(expected))
    # test_4:keyが長いものでも適切に認識できているか
    def test_4(self):
        test_case = [
            ("aacceeeeghhllnoopprrt",['electroencephalograph']),
            ("eeghehalelnaoopprcrct",['electroencephalograph']),
            ("aacceeeeghhllnoopprrte",[])
        ]
        for Input,expected in test_case:
            with self.subTest(Input=Input):
                ans,count = find_anagram(Input,self.ang_dict)
                if count != 0:
                    self.assertEqual(sorted(ans),sorted(expected))
                else:
                    self.assertEqual(count,len(expected))
    # test_5:入力の異常例に対応できているか
    def test_5(self):
        test_case = [
            ("",[]),
            ("012",[]),
            ("ab56あおk%%&",[]),
            ("   iwnk  ",["wink"]),
            ("i w n k",[]),
            ("i,w,n,k",[])
        ]
        for Input,expected in test_case:
            with self.subTest(Input=Input):
                ans,count = find_anagram(Input,self.ang_dict)
                if count != 0:
                    self.assertEqual(sorted(ans),sorted(expected))
                else:
                    self.assertEqual(count,len(expected))
if __name__ == "__main__":
    unittest.main()