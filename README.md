# i3-lemonbar

Status script and configuration for [Lemonbar] (https://github.com/LemonBoy/bar) and [i3wm] (https://i3wm.org/).

Configuration is taken from beautiful powerline setup by [electro7] (https://github.com/electro7/dotfiles/tree/master/.i3/lemonbar).

Status feeder script is written completely in Python and uses [i3ipc] (https://github.com/acrisci/i3ipc-python) for most of the interaction with i3.

### Features

* Event-based, rather than periodically updated
* Multiple display output support

### Installation

* Install [lemonbar] (https://github.com/LemonBoy/bar).
* Install [i3ipc-python] (https://github.com/acrisci/i3ipc-python) library.
        
        pip install i3ipc

* Make sure you have terminus and terminesspowerline fonts installed. You can get them [here] (https://github.com/electro7/dotfiles).
* Clone this repo (e.g. to your .i3 directory).

        mkdir ~/.i3/lemonbar && git clone https://github.com/mirekys/i3-lemonbar.git ~/.i3/lemonbar

* Configure i3 to use Lemonbar.

        bar {
                i3bar_command ~/.i3/lemonbar/i3_lemonbar.py
        }


