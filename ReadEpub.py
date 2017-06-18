from ebooklib import epub
import boto3

client = boto3.client('s3')
book_file = r'OAuth_2_in_Action.epub'


#text/css
#text/html
#image/jpeg
#image/png

def read_book(file):
	book = epub.read_epub(file)
	for items in book.get_items():
		if items.get_type() == 1:
			print("Image {}".format(items.get_name()))
			put_bucket('html', 'image/jpeg', items.get_name(), items.get_content())
		if items.get_type() == 2:
			print("Style {}".format(items.get_name()))
			put_bucket('html', 'text/css', items.get_name(), items.get_content())
		if items.get_type() == 3:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 4:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 5:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 6:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 7:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 8:
			print("Type={} {}".format(items.get_type(),items.get_name()))
		if items.get_type() == 9:
			print("HTML {}".format(items.get_name()))
			put_bucket('html', 'text/html', items.get_name(), items.get_content())

def put_bucket(dir, cont_type, name, body):
	dir_name = "{}/{}".format(dir,name)
	client.put_object(
		Bucket='ratts-epub-web-docs',
		Body=body,
		ContentType=cont_type,
		Key=dir_name,
		ACL='public-read')


if __name__ == "__main__":
	read_book(book_file)
