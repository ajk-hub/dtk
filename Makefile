install-dependencies:
	python -m pip install --upgrade pip
	pip install flake8
	pip install -r requirements.txt

lint:
	flake8 src/ --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 src/ --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

run:
	python -m src

build:
	pyinstaller --noconfirm --onefile --clean --distpath=artifacts --workpath=/tmp --specpath=/tmp src/__main__.py --name dtk

build-artifacts:build
	cp ./completions/_dtk.zsh artifacts/_dtk.zsh
	zip dtk.zip artifacts/*

install-dtk:build
	sudo mv ./artifacts/dtk /usr/local/bin/dtk
	sudo chmod +x /usr/local/bin/dtk

test:
	python -m src k6 run test.js
