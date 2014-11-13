Video Split
=============

FFMPEG front-end to batch split videos into JPEG frames.

# Installation
## Windows
Grab the latest installer from the [releases page](https://github.com/itsravenous/videosplitter/releases). Once downloaded, run the installer and follow the instructions. The program itself is fairly self-explanatory. If you run into any trouble, feel free to [file an issue](https://github.com/itsravenous/videosplitter/issues/new), or [drop me a tweet](https://twitter.com/itsravenous).

## Other platforms
Video Split is targeted mainly at Windows users not comfortable with using the command line (splitting videos into frames using ffmpeg is very straightforward, as a quick search will tell you).

That said, Video Split will run on Linux, and should also run on other unix-y systems such as Mac OSX, though I haven't tested this, and don't currently have any binary releases for Mac.

To run on a unix-y platform, make sure you have the following installed:

* [ffmpeg](http://ffmpeg.org) (or avconv, but you'll need to `ln -s /usr/bin/avconv * /usr/bin/ffmpeg' because I was too lazy to check which is installed)
* [python](http://python.org)
* [PyQT](http://www.riverbankcomputing.co.uk/software/pyqt/download)

Obviously check your package manager; most - if not all - of the above should be available via `apt-get`, `yum`, etc.