export FILE_DIR=./postwita/
export FILE_NAME=it_postwita-ud-train

python -m spacy convert $FILE_DIR$FILE_NAME.conllu $FILE_DIR --converter conllu --file-type spacy --lang it

export FILE_NAME=it_postwita-ud-dev

python -m spacy convert $FILE_DIR$FILE_NAME.conllu $FILE_DIR --converter conllu --file-type spacy --lang it

export FILE_NAME=it_postwita-ud-test

python -m spacy convert $FILE_DIR$FILE_NAME.conllu $FILE_DIR --converter conllu --file-type spacy --lang it



write cuda visible devices

python -m spacy train config.cfg --output ./postwita/ --paths.train ./postwita/it_postwita-ud-train.spacy --paths.dev ./postwita/it_postwita-ud-dev.spacy --gpu-id 0