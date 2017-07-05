from flask import Flask,request,session,g,redirect,url_for,abort,render_template,flash,jsonify
import json

app=Flask(__name__)  

@app.route('/')  
def index():
	return render_template('index.html')

def is_chinese(uchar):
    return uchar >= u'\u4e00' and uchar<=u'\u9fa5'

def countwords(bookname):
	with open('books/'+bookname+'.txt', mode='r', encoding='utf-8') as inFile:
		stat ={}
		characters=[]
		for line in inFile:
			line = line.strip()
			if len(line) == 0:
				continue
			for x in range(0,len(line)):
				if not is_chinese(line[x]):
					continue
				if not line[x] in characters:
					characters.append(line[x])
				if not line[x] in stat:
					stat[line[x]] = 0
				stat[line[x]] += 1
		chars_len = len(characters)
		stat = sorted(stat.items(), key=lambda d:d[1], reverse=True)
	return stat
	#return render_template('index.html',chars_len=chars_len)

@app.route("/getSortedWords/<bookname>", methods=["GET","POST"])
def getSortedWords(bookname):
	stat = countwords(bookname)
	allwords=[]
	allnum=[]
	for item in stat:
		allwords.append(item[0])
		allnum.append(item[1])
	topwords=allwords[:10]
	topnum=allnum[:10]
	keys=['topwords','topwordsnum']
	values=[topwords,topnum]
	dictionary = dict(zip(keys, values))	
	jsondata = jsonify(dictionary)
	print(jsondata)
	return jsondata

if __name__ == '__main__':  
    app.run(debug=True)