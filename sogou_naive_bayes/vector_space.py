import os
from sklearn.datasets.base import Bunch
import pickle #持久化类
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer #TF-IDF向量转换类
from sklearn.feature_extraction.text import TfidfVectorizer #TF-IDF向量生成类
import codecs

'''
本程序用来将训练集和测试集利用：
1、权重策略（TF-IDF方法：如果某个词或短语在一篇文章中出现的频率高，
并且在其他文章中很少出现，那么认为这个词或者短语具有很好的类别区分能力，适合用来分类。）
2、去除停用词；
3、得到词向量空间
'''

def _readbunchobj(path):
	file_obj=open(path,"rb")
	bunch=pickle.load(file_obj)
	file_obj.close()
	return bunch


def _writebunchobj(path,bunchobj):
	file_obj=open(path,"wb")
	pickle.dump(bunchobj,file_obj)
	file_obj.close()


def _readfile(path):
	fp = codecs.open(path, "r", 'utf-8')
	content = fp.read()
	fp.close()
	return content


def train_test_vector_space():
	# 先构建训练集词向量空间
	train_path = "train_word_bag/train_set.dat"
	bunch = _readbunchobj(train_path)

	#停用词
	stopword_path = "train_word_bag/hlt_stop_words.txt"
	stpwrdlst = _readfile(stopword_path).splitlines()
	#构建TF-IDF词向量空间对象
	tfidfspace=Bunch(target_name=bunch.target_name,label=bunch.label,\
					filenames=bunch.filenames,tdm=[],vocabulary={})
	#使用TfidVectorizer初始化向量空间模型
	vectorizer=TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf=True,max_df=0.5)
	transfoemer=TfidfTransformer()#该类会统计每个词语的TF-IDF权值

	#文本转为词频矩阵，单独保存字典文件
	tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
	tfidfspace.vocabulary = vectorizer.vocabulary_

	#创建词袋的持久化
	space_path = "train_word_bag/tfidfspace.dat"
	_writebunchobj(space_path,tfidfspace)
	print ("训练集(train)词向量空间创建成功！！！")


	# 再创建测试集词向量空间
	# 1. 导入分词后的词向量bunch对象
	test_path = "test_word_bag/test_set.dat"        # 词向量空间保存路径
	bunch = _readbunchobj(test_path)

	# 2. 构建测试集tfidf向量空间
	testspace = Bunch(target_name=bunch.target_name,label=bunch.label,\
					  filenames=bunch.filenames,tdm=[],vocabulary={})
	# 3. 导入训练集的词袋
	trainbunch = _readbunchobj("train_word_bag/tfidfspace.dat")
	# 4. 使用TfidfVectorizer初始化向量空间模型 
	vectorizer = TfidfVectorizer(stop_words=stpwrdlst,sublinear_tf = True,\
								 max_df = 0.5,vocabulary=trainbunch.vocabulary)
	transformer=TfidfTransformer() # 该类会统计每个词语的tf-idf权值
	# 文本转为tf-idf矩阵,单独保存字典文件 
	testspace.tdm = vectorizer.fit_transform(bunch.contents)
	testspace.vocabulary = trainbunch.vocabulary

	# 创建词袋的持久化
	space_path = "test_word_bag/testspace.dat"        # 词向量空间保存路径
	_writebunchobj(space_path,testspace)

	print ("测试集(test)词向量空间创建成功！！！")


if __name__ == '__main__':
	train_test_vector_space()