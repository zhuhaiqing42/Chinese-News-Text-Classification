# -*- coding: utf-8 -*-
import pickle
from sklearn.naive_bayes import MultinomialNB # 导入多项式贝叶斯算法包
import jieba
import time
from datetime import timedelta
from corpus_segment import corpus_segment
from segment2Bunch import segment2Bunch
from vector_space import train_test_vector_space
from sklearn.metrics import confusion_matrix, classification_report


def _readbunchobj(path):
	file_obj = open(path, "rb")
	bunch = pickle.load(file_obj)
	file_obj.close()
	return bunch


def predict():
	# 导入训练集向量空间
	trainpath = "train_word_bag/tfidfspace.dat"
	train_set = _readbunchobj(trainpath)
	# 导入测试集向量空间
	testpath = "test_word_bag/testspace.dat"
	test_set = _readbunchobj(testpath)

	# 应用贝叶斯算法
	# alpha:0.001 alpha 越小，迭代次数越多，精度越高
	clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)

	# 预测分类结果
	predicted = clf.predict(test_set.tdm)
	total = len(predicted);
	rate = 0
	for flabel, file_name, expct_cate in zip(test_set.label, test_set.filenames, predicted):
			print(file_name, ": 实际类别：", flabel, "-->预测分类：", expct_cate)
			if flabel != expct_cate:
				rate += 1

	# 精度
	print(rate, total)
	print("Error_rate:", float(rate)*100 / float(total), "%")
	print("Accuracy:", 100.0-float(rate)*100 / float(total), "%")

	# 评估
	print("Precision, Recall and F1-Score...")
	categories = list(set(test_set.label))
	categories.sort(key=test_set.label.index)
	print(classification_report(test_set.label, predicted, target_names=categories))
	# 混淆矩阵
	print("Confusion Matrix...")
	cm_test = confusion_matrix(test_set.label, predicted)
	print(cm_test)
	
	print ("预测完毕!!!")


if __name__ == '__main__':
	start = time.time()

	# 训练集、测试集分词程序: corpus_segment.py
	train_corpus_path = "train_corpus_small/"  # 训练集未分词分类语料库路径
	train_seg_path = "train_corpus_seg/"      # 训练集分词后分类语料库路径
	corpus_segment(train_corpus_path, train_seg_path)
	print("训练集语料分词结束")

	test_corpus_path = "test_corpus_small/"  # 测试集未分词分类预料库路径
	test_seg_path = "test_corpus_seg/"  # 测试集分词后分类语料库路径
	corpus_segment(test_corpus_path, test_seg_path)
	print("测试集语料分词结束")

	# 把分词后的数据存为Bunch格式: segment2Bunch.py
	segment2Bunch()

	# 构建向量空间,使用TF-IDF权重策略: vector_space.py
	train_test_vector_space()

	# 测试集预测
	predict()
	
	end = time.time()
	print("Time usage:", timedelta(seconds=int(round(end - start))))