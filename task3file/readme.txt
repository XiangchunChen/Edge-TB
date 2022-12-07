检查扣分点
1. 题目中提到”Design a function“，所以主要程序逻辑没有写在function中是要扣分的;函数的返回值不是boolean也要扣分
2. 重写原文件或者生成新文件都是可以接受的
3. 重写文件保持CPF，否则扣分
4. 检查重写内容，可能存在被替换的单词W1是另一个单词W2的一部分，比如he是she,the的一部分，如果要将he换成xxx，she不应该换成sxx,the不改换成txx
5. 大小写问题可忽略
6. 如果title, author字段的单词被替换，扣分


Solution思路：
1. 遍历每个单词，检查被遍历的单词是不是被替换的单词，如果是，则替换


其他说明：
1. test1
   input: tc1.txt learn know (learn为被替换的旧单词，know为新单词)
   新文件内容: tc1_rewrite.txt
2. test2
   input: tc2.txt to xx (learn为被替换的旧单词，know为新单词)
   新文件内容: tc2_rewrite.txt
