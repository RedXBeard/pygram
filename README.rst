pygram
======

Telegram messaging from your terminal.

Setup (In hard way)
-------------------

At first tg-cli must be installed.

.. code-block:: bash

    git clone --recursive https://github.com/vysheng/tg.git ~/.tg && cd ~/.tg
    ./configure
    make

Setup (More basic)
------------------

Just run the following.

.. code-block:: bash

    python client_installer.py

Setup (for both installation)
-----------------------------

After installing client package, must be called ones to save login information on local folder, all explained on client readme file

.. code-block:: bash

    .~/.tg/bin/telegram-cli server.pub

on coming screen, you should type your phone number then received activation code on your phone. then just type ``safe_quit`` or just ``quit``

Installing
----------

``python 3.5.1`` used.

there are two way, first;

.. code-block:: bash

    git clone https://github.com/RedXBeard/pygram.git
    cd pygram;pip3.5 install -r requirements

second;

.. code-block:: bash

    pip3.5 install -e /path/to/cloned/repo/

Usage
-----

Because of there are two ways to install, there are two ways to use, first;

.. code-block:: bash

    python3.5 main.py

second, much more easy;

.. code-block:: bash

    pygram


Collaborators
-----------

- Barbaros Yıldırım (`RedXBeard <https://github.com/RedXBeard>`_)
- Barış Güler (`hwclass <https://github.com/hwclass>`_)
- Dünya Değirmenci (`ddegirmenci <https://github.com/ddegirmenci>`_)
- Emre Yılmaz (`emre <https://github.com/emre>`_)
- Gürel Kaynak (`gurelkaynak <https://github.com/gurelkaynak>`_)
- Hazar İlhan (`batilc1 <https://github.com/batilc1>`_)
