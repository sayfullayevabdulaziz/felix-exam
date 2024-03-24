How to use

### 1) Clone git repository
```bash
git clone https://github.com/sayfullayevabdulaziz/felix-exam.git
```

### 2) Create poetry environment and install packages
```bash
poetry shell
```
```bash
poetry install
```

### Or use pip
```bash
pip install -r requirements.txt
```

### Run server
```bash
uvicorn src.main:app --reload
```