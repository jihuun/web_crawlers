#! /bin/bash

# easy update the trevari book list to the github repo
# $ ./update_list.sh

DIR=$(dirname "$0")
SCRIPT="get_trevari_books.py"
TARGET="trevari_book_list.md"

function get_date {
	echo $(date +%Y-%m-%d)
}

function get_time {
	echo $(date +%T)
}

cd $DIR

if [ -f $SCRIPT ]; then
	echo "[LOG]: sync up with origin/master"
	git checkout master
	git fetch origin
	git rebase origin/master
	CUR_TIME=$(get_time)
	echo "[LOG]: $SCRIPT is executed on $CUR_TIME"
	python $SCRIPT 
	CUR_TIME=$(get_time)
	echo "[LOG]: $SCRIPT is finished on $CUR_TIME."
else 
	echo "[LOG]: wrong path, curr dir is: $DIR"
	exit
fi

DIFF=$(git diff $TARGET | grep "diff")
echo "[LOG]: diff: $DIFF"
echo "[LOG]: dir: $DIR pwd: $(pwd)"

if [[ -z "$DIFF" ]]
then
	echo "[LOG]: no diff"
	exit
else
	cd $DIR
	git add $TARGET
	git commit -sm "script: trevari: update book list on $TODAY (auto generated commit)"
	git push origin master
	TODAY=$(get_date)
	CUR_TIME=$(get_time)
	echo "[LOG]: update commit - script: trevari: update book list on $TODAY, $CUR_TIME"
fi
