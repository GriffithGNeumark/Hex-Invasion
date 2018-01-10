build:
	pip3.6 install -U -r requirements.txt

run: build
	python3.6 src/mapgame.py
