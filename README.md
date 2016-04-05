# pygram
Telegram messaging from your terminal.

## Setup
#### In hard way
At first tg-cli must be installed.
```bash
git clone --recursive https://github.com/vysheng/tg.git ~/.tg && cd ~/.tg
./configure
make
```
#### More basic
Just run the following.
```bash
python client_installer.py
```

After installing client package, must be called ones to save login information on local folder, all explained on client readme file
```bash
.~/.tg/bin/telegram-cli server.pub
```
on coming screen, you should type your phone number then received activation code on your phone. then just type <code>safe_quit</code> or just <code>quit</code>

<code>python 3.5.1</code> used.

## Installing
there are two way, first;
```bash
git clone https://github.com/RedXBeard/pygram.git
cd pygram;pip3.5 install -r requirements
```
second;
```bash
pip3.5 install -e /path/to/cloned/repo/
```

## Usage
Because of there are two ways to install, there are two ways to use, first;
```bash
python3.5 main.py
```
second, much more easy;
```bash
pygram
```

## Conributors
- Barbaros Yıldırım ([RedXBeard](https://github.com/RedXBeard))
- Barış Güler ([hwclass](https://github.com/hwclass))
- Dünya Değirmenci ([ddegirmenci](https://github.com/ddegirmenci))
- Emre Yılmaz ([emre](https://github.com/emre))
- Gürel Kaynak ([gurelkaynak](https://github.com/gurelkaynak))
