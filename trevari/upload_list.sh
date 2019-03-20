#! /bin/bash

# easy update the trevari book list to the github repo
# $ ./update_list.sh

DIR=$(dirname "$0")
SCRIPT="get_trevari_books.py"
TARGET="trevari_book_list.md"
function get_date {
	echo $(date +%Y-%m-%d)
}

cd $DIR

if [ -f $SCRIPT ]; then
	echo "LOG: sync up with origin/master"
	git fetch origin
	git rebase origin/master
	echo "LOG: $SCRIPT is doing."
	python $SCRIPT 
	echo "LOG: $SCRIPT done."
else 
	echo "LOG: wrong path, curr dir is: $DIR"
	exit
fi

DIFF=$(git diff $TARGET | grep "diff")
echo "LOG: diff: $DIFF"
echo "LOG: dir: $DIR pwd: $(pwd)"

if [[ -z "$DIFF" ]]
then
	echo "LOG: no diff"
	exit
else
	cd $DIR
	NOW=$(get_date)
	echo "LOG: update commit - script: trevari: update book list on $NOW"
	git add $TARGET
	git commit -sm "script: trevari: update book list on $NOW (auto generated commit)"
	git push origin master
fi
