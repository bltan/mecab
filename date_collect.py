#!/usr/bin/perl
#coding:utf-8
import sys, codecs, MeCab
data = {} #配列[]は代入で配列数を増やせないので辞書で登録
i = 0

f = open('Graph/UnemploymentRate/Original980130264.txt') #テキストファイルの読み込み
mecab = MeCab.Tagger("-Ochasen -u usrdic.dic")
text = f.read() #変数に格納
f.close()

lines = text.split('。',) #行ごとに区切る

for t in lines:
	print t

d = open('DataSet/date.txt') #日付に関する単語ファイルを格納
for line in d.readlines():
	data[i] = line.rstrip()
	i +=1

for line in lines: #行ごとに処理を行う
	node = mecab.parseToNode(line).next #形態素解析結果を双方向に格納

	keywords = [] #助数詞のみを格納
	num = [] #数字部分を格納

	while node:
		if node.feature.split(",")[2] == "助数詞": #助数詞とその前の数詞を抽出
			for j in range(0,i):
				#print j
				if node.surface == data[j]: #助数詞のうちdataに格納した日付ワードのみ抽出
					keywords.append(node.surface) #特定の助数詞を抽出
					node = node.prev
					num.append(node.surface) #掛かっている数字の抽出	
					node = node.next
		node = node.next

	for k in range(0,len(num)):
		print num[k],keywords[k]
