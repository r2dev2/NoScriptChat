# NoScriptChat

A proof of concept that you can make semi-usable websites that stream data without javascript.

## Usage

A hosted version is at # insert link

### Local Usage

1. Install dependencies

```
python3 -m pip install flask gunicorn
```

2. Run

```
gunicorn -b 0.0.0.0:8080 --threads 100 main:app
```
