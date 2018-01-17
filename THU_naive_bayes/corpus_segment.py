# -*- coding: utf-8 -*-
import os
import jieba
import codecs

'''
这是一个实现中文分词的程序。eg:小明是一个中国人 --> 小明 是 一个 中国人

'''

def _savefile(savepath, content):
	fp = codecs.open(savepath, "w",'utf-8')
	fp.write(content)
	fp.close()


def _readfile(path):
	fp = codecs.open(path, "r",'utf-8')
	content = fp.read()
	# print(content)
	fp.close()
	return content


def corpus_segment(corpus_path, seg_path):
	catelist = os.listdir(corpus_path)  # 获取改目录下所有子目录

	for mydir in catelist:
		class_path = corpus_path + mydir + "/"  # 拼出分类子目录的路径
		seg_dir = seg_path + mydir + "/"  # 拼出分词后预料分类目录
		if not os.path.exists(seg_dir):  # 是否存在，不存在则创建
			os.makedirs(seg_dir)
		file_list = os.listdir(class_path)
		for file_path in file_list:
			fullname = class_path + file_path
			content = _readfile(fullname).strip()  # 读取文件内容
			content = content.replace("\r\n", "").strip()  # 删除换行和多余的空格
			content = content.replace(" ", "")#删除空行、多余的空格  
			content_seg = jieba.cut(content)
			_savefile(seg_dir + file_path, " ".join(content_seg))

	
if __name__ == '__main__':
	train_corpus_path = "train_corpus_small/"  # 训练集未分词分类语料库路径
	train_seg_path = "train_corpus_seg/"      # 训练集分词后分类语料库路径
	corpus_segment(train_corpus_path, train_seg_path)
	print("训练集语料分词结束")

	test_corpus_path = "test_corpus_small/"  # 测试集未分词分类预料库路径
	test_seg_path = "test_corpus_seg/"  # 测试集分词后分类语料库路径
	corpus_segment(test_corpus_path, test_seg_path)
	print("测试集语料分词结束")
	
	# _readfile('just_test_seg/business/110.txt')