All: create_directory log time start


create_directory:
	pip3 install twint
	mkdir Initialization
	mkdir Data

log:
	touch Initialization/log.txt

time:
	echo "2020-05-24" > Initialization/time.txt

start:
	python3 get_link_tree_tweets_from_twitter.py

clean:
	rm -rf Initialization
	rm -rf Data