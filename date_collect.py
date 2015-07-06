#!/usr/bin/python
#coding:utf-8
import sys, codecs, MeCab
day = [] #配列[]で日付登録
key = [] #優先ワードの登録 

opening = 0 #文頭からの句点カウンター

f = open('Documents/UnemploymentRate/Original980130264.txt') #テキストファイルの読み込み
mecab = MeCab.Tagger("-Ochasen -u usrdic.dic")
text = f.read() #変数に格納
f.close()

print text #原文表示

d = open('DataSet/date.txt') #日付に関する単語ファイルを格納
for line in d.readlines():
	day.append(line.rstrip())

k = open('DataSet/Opening_keyword.txt') #文頭の優先ワード(発表した等)を格納
for line in k.readlines():
	key.append(line.rstrip())

node = mecab.parseToNode(text).next #形態素解析結果を双方向に格納

date = [] #助数詞のみを格納
num = [] #数字部分を格納
keyword = [] #優先ワードを格納
ymd = ["年","月","日"] #日付の表示

while node:
	if node.surface == "。": #文頭2文分の日付単語のみを取る。句点が二回来たら処理終了
		opening += 1
		if opening == 2:
			break

	if node.feature.split(",")[2] == "助数詞": #助数詞とその前の数詞を抽出
		if node.surface in day: #in演算子を用いて書き換え #助数詞のうちdataに格納した日付ワードのみ抽出
			date.append(node.surface)
			num.append(node.prev.surface)

	elif node.feature.split(",")[1] != "形容詞":
		if node.feature.split(",")[6] in key:#優先ワードの判別
			keyword.append(node.surface)
			break #関数化してreturnで終了させる

	if(len(keyword) != 0): #stop配列に要素入れば終了
		break

	node = node.next

for i in range(0,len(date)):
	for j in range(0,len(day)): #格納した日付を年月日に分別して一つの配列(ymd)に格納
		if(date[i] == day[j]):
			ymd[j] = num[i] + date[i]

for i in range(len(ymd)): #抽出した日付の表示
	print ymd[i]

if(len(keyword) != 0):
	print keyword[0]