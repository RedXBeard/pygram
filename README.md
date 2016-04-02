# pygram
Telegram messaging from your terminal.

## Setup
Basic information, first tg-cli must be installed.
```bash
git clone --recursive https://github.com/vysheng/tg.git && cd tg
./configure
make
```
after installing client package, must be called first to save login information on local folder, all explained on client readme file 
```bash
./bin/telegram-cli server.pub
```
on coming screen, you should type your phone number then received activation code on your phone. then just type <code>safe_quit</code> or just <code>quit</code>

<code>python 3.5.1</code> used.
```bash
git clone https://github.com/RedXBeard/pygram.git
cd pygram;pip3.5 install -r requirements
```
## Usage
```bash
python3.5 pygram/main.py
```

## Conributors
- Barbaros Yıldırım ([RedXBeard](https://github.com/RedXBeard))
- Barış Güler ([hwclass](https://github.com/hwclass))
- Dünya Değirmenci ([ddegirmenci](https://github.com/ddegirmenci))
- Emre Yılmaz ([emre](https://github.com/emre))
- Gürel Kaynak ([gurelkaynak](https://github.com/gurelkaynak))
