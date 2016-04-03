pygram
======

Telegram messaging from your terminal.

Setup
-----

Basic information, first tg-cli must be installed.

.. code-block:: bash

    git clone --recursive https://github.com/vysheng/tg.git && cd tg
    ./configure
    make

after installing client package, must be called first to save login information on local folder, all explained on client readme file 

.. code-block:: bash

    ./bin/telegram-cli server.pub

on coming screen, you should type your phone number then received activation code on your phone. then just type ``safe_quit`` or just ``quit``

``python 3.5.1`` used.

.. code-block:: bash

    git clone https://github.com/RedXBeard/pygram.git
    cd pygram;pip3.5 install -r requirements

Usage
-----

.. code-block:: bash

    python3.5 pygram/main.py


Conributors
-----------

- Barbaros Yıldırım (`RedXBeard <https://github.com/RedXBeard>`_)
- Barış Güler (`hwclass <https://github.com/hwclass>`_)
- Dünya Değirmenci (`ddegirmenci <https://github.com/ddegirmenci>`_)
- Emre Yılmaz (`emre <https://github.com/emre>`_)
- Gürel Kaynak (`gurelkaynak <https://github.com/gurelkaynak>`_)
