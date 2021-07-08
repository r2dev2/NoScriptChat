# NoScriptChat

A proof of concept that you can make semi-usable websites that stream data without javascript.

## Why

According to noscripters, [javascript that alters the DOM is an Avengers level threat to your freedom](https://www.gnu.org/philosophy/javascript-trap.html). You are safe if you use noscript, however, and you definitely won't be tracked by non-js mechanisms.

Also, Javascript is

![bloat](./Bloat.png)

## Usage

A hosted version is at https://NoScriptChat.r2dev2bb8.repl.co

### Local Usage

1. Install dependencies

```
python3 -m pip install flask gunicorn
```

2. Run

```
gunicorn -b 0.0.0.0:8080 --threads 100 main:app
```
