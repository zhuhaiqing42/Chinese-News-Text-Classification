# -*- coding: utf-8 -*-
import os


def _read_file(path):
	fp = open(path, 'r', encoding='utf-8', errors='ignore')
	content = fp.read()
	fp.close()
	return content


def _save_file(path, content):
	fp = open(path, 'w', encoding='utf-8', errors='ignore')
	fp.write(content)
	fp.close()


def file_seg(source_path, seg_train_path, seg_test_path, seg_val_path):
	catelist = os.listdir(source_path)
	
	# f_test = open(seg_test_path, encoding='utf-8', errors='ignore')
	for mydir in catelist:
		class_path = source_path + mydir + '/'
		file_list = os.listdir(class_path)
		file_len = len(file_list)
		print(file_list[:int(0.8*file_len)])

		# 前80%个txt文件为训练集
		for train_file_path in file_list[:int(0.8*file_len)]:
			train_full_name = class_path + train_file_path
			content_train = _read_file(train_full_name)
			train_dir = seg_train_path + mydir
			if not os.path.exists(train_dir):
				os.makedirs(train_dir)
			_save_file(train_dir +'/' + train_file_path, content_train)

		# 中间10%个txt文件为测试集
		for test_file_path in file_list[int(0.8*file_len):int(0.9*file_len)]:
			test_full_name = class_path + test_file_path
			content_test = _read_file(test_full_name)
			test_dir = seg_test_path + mydir
			if not os.path.exists(test_dir):
				os.makedirs(test_dir)
			_save_file(test_dir + '/' + test_file_path, content_test)

		# 后10%个txt文件为验证集
		for val_file_path in file_list[int(0.9*file_len):]:
			val_full_name = class_path + val_file_path
			content_val = _read_file(val_full_name)
			val_dir = seg_val_path + mydir
			if not os.path.exists(val_dir):
				os.makedirs(val_dir)
			_save_file(val_dir + '/' + val_file_path, content_val)


if __name__ == '__main__':
	data_path = "/home/guest/zhuhaiqing/study/nlp/thu_naive_bayes/THUCNews/"
	file_seg(data_path, 'train_corpus_small/', 'test_corpus_small/', 'validation_corpus_small/')