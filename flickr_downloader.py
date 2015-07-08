import os 
from urlparse import urlparse
import codecs
from flickr_api import *

def write_image_tags(f, img_name, tags):
	f.write(img_name+": ")

	if tags == None:
		f.write('\n')
		return

	for idx, tag in enumerate(tags):
		if idx != len(tags) - 1 :
			f.write(u"%s, "%tag.text)
		else:
			f.write(u"%s"%tag.text)
	f.write('\n')

def download_image(photo, tags_file, save_dir):
    url = photo.getURL(size='Medium', urlType='source')
    parsed = urlparse(url)
    img_name = os.path.basename(parsed.path)
    img_path = os.path.join(save_dir, img_name)
    f = urlopen(url)
    img = f.read()
    imgFile = open(img_path, 'wb+')
    imgFile.write(img)
    imgFile.close()

    write_image_tags(tags_file, img_name, photo.tags)


def search_and_download(image_label):
	if not os.path.exists(image_label):
		os.makedirs(image_label)
	tags_file_path = os.path.join(image_label, image_label+'_userTags.txt')
	tags_file = codecs.open(tags_file_path, 'wb+', "utf-8")	
	photos = photos_search(text = image_label, content_type=1, sort='relevance')
	for idx, photo in enumerate(photos):
		print 'downloading %d images... of %s'%(idx+1, image_label[:-1])
		download_image(photo, tags_file, image_label)


def readTasks(fileName):
	f = open(fileName, 'r')
	for line in f:
		print 'Begine to down load image of ', line
		search_and_download(line)

if __name__ == '__main__':
	readTasks('foodlist.txt')
   