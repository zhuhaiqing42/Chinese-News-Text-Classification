import os
import codecs


def open_file(filename, mode='r'):
    """
    Commonly used file reader, change this to switch between python2 and python3.
    mode: 'r' or 'w' for read or write
    """
    return codecs.open(filename, mode, 'utf-8')

def _savefile(savepath, label, content):
	fp = codecs.open(savepath, "a+",'utf-8')
	fp.write(label+'\t')
	fp.write(content +'\n')
	fp.close()


def _readfile(path):
	fp = codecs.open(path, "r",'utf-8')
	content = fp.read()
	fp.close()
	return content


def file2txt(path, txt_path):
	catelist = os.listdir(path)

	content_all = []

	for mydir in catelist:
		class_path = path + mydir + '/'
		file_list = os.listdir(class_path)
		for file_path in file_list:
			# print(file_path)
			full_name = class_path + file_path
			print(full_name)
			content = _readfile(full_name).strip()
			# print(content)
			content = content.replace("\r\n", "").strip()  # 删除换行和多余的空格
			content = content.replace(" ", "") # 删除空行、多余的空格
			_savefile(txt_path, mydir, content)


def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                contents.append(list(content))
                labels.append(label)
            except:
                pass
    # print("****************** the contents is", contents)
    return contents, labels


if __name__ == '__main__':
	# file2txt('test_corpus_small/')
	# content = _readfile('test_corpus_small/Tourism/8837.txt')
	
	#将训练集语料放入一个txt文件中
	file2txt('train_corpus_small/', 'thu_news_data/train.txt')
	
	#将测试集语料放入一个txt文件中
	# file2txt('test_corpus_small/', 'thu_news_data/test.txt')

	#将验证集语料放入一个txt文件中
	# file2txt('validation_corpus_small/', 'thu_news_data/validation.txt')
