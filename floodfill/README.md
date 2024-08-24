
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

python simulation --maze=mazefiles/classic/50.txt --logging=DEBUG
