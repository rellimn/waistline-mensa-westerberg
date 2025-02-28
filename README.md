# waistline-mensa-westerberg
## Installation
### Venv
```shell
git clone https://github.com/rellimn/waistline-mensa-westerberg.git
cd waistline-mensa-westerberg
python -m venv .venv
source .venv/bin/activate # Für Windows .venv\Scripts\activate.bat
pip install -r requirements.txt
```

### Docker
```shell
make build
```

## Usage
* Venv: `python3 main.py`
* Docker: `make run`

Erstellte JSON in Waistline einfügen.
