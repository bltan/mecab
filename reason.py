#!/usr/bin/python
#coding:utf-8

#注意 : ここで最終的に吐き出されるreasonは逆順に格納されます

import sys, codecs, MeCab
compare_words = [] #優先ワードの登録(二次元配列)
#count = 0 #カウント用変数

reason_words = [] #理由単語を入れる配列(今後前後の文章を入れたい)

def doushi_judge(node, compared_word): #動詞-自立に対する処理
	if(compared_word == "動詞-自立"):
		if node.feature.split(",")[0] == "動詞" and node.feature.split(",")[1] == "自立":
			return node.surface


f = open('../date/Documents/UnemploymentRate/Original980130264.txt') #テキストファイルの読み込み
mecab = MeCab.Tagger("-Ochasen -u ../date/usrdic.dic")
text = f.read() #変数に格納
f.close()

print text #原文表示
node = mecab.parseToNode(text).next #形態素解析結果を双方向に格納

d = open('DataSet/reasons.txt') #理由に関する単語ファイルを格納
for lines in d.readlines():
	line = lines.rstrip() #理由を行ごとに読み取り

	temporarily_words = []
	for word in line.split(","): #単語単位でtemporarily_wordsに一時格納
		temporarily_words.append(word)
		

	#for i in range(0, len(temporarily_words)): #単語を二次元配列に格納
	compare_words.append(temporarily_words)

	#count += 1

print ""
for i in range(0, len(compare_words)): #compare_wordsの中身確認用
	#print compare_words[i]
	for j in range(0, len(compare_words[i])):
		sys.stdout.write(compare_words[i][j]+" ")
	print ""

print "-----------------------"


#特定ワードの読み取り
for i in range(0,len(compare_words)):
	#print len(compare_words),compare_words[i][0] #テスト用
	while node:
		key1 = ""
		key2 = ""
		key1 = doushi_judge(node, compare_words[i][0])

		if node.feature.split(",")[6] == compare_words[i][0] or key1 != None : #特定ワードの判定
			#print "step1" #判定段階テスト用
			#print node.feature.split(",")[6]#テスト用
			if len(compare_words[i]) == 1: #判定要素が一つの時はすぐに終了
				#print "1ワード判定で終了" #終了条件表示用
				reason_words.append(node.surface)
				for i in range(0, len(reason_words)):
					print reason_words[i]
				break

			elif len(compare_words[i]) > 1: #判定要素が2以上の時は、二つ目のcompare_words[i][1]と比較する
				try: #最後のnodeはnextがないため例外処理を行う
					key2 = doushi_judge(node.next, compare_words[i][1])
					if node.next.feature.split(",")[6] == compare_words[i][1] or key2 != None:
						#print(node.surface)
						print "2ワード判定で終了"
						#print key2
						reason_words.append(node.next.surface) #逆順で格納
						reason_words.append(node.surface)
						for i in range(0,len(reason_words)):
							print reason_words[i]
						break
				except:
					break

		node = node.next

	if len(reason_words) != 0:

		try:
			node = node.prev
		except:
			break
		
		while node.surface != "。": #キーワード前の一文をreasonに保存(逆順に)
			reason_words.append(node.surface)
			node = node.prev
		
		break

	node = mecab.parseToNode(text).next #nodeを先頭に戻す



for i in reversed(range(0, len(reason_words))): #理由部分を逆からprint
	sys.stdout.write(reason_words[i])
print ""