[Mozc - a Japanese Input Method Editor designed for multi-platform](https://github.com/google/mozc)
===================================

Copyright 2010-2016, Google Inc.

Mozc is a Japanese Input Method Editor (IME) designed for multi-platform such as
Android OS, Apple OS X, Chromium OS, GNU/Linux and Microsoft Windows.  This
OpenSource project originates from
[Google Japanese Input](http://www.google.com/intl/ja/ime/).

This branch is modified version of Mozc primarily for FreeBSD.
Changes include:

* Define OS_FREEBSD.  It is mixture of OS_LINUX and OS_MACOSX.
* fcitx support.  To enable this, --use-fcitx option is required.
* C++11 fixes for GCC and Clang.
* Support non-standard directories for tools and renderer via --tool_dir and --renderer_dir options.
* --localbase option has been added to specify location of commands instead of hard-coded "/usr/bin".
* Add options for compiler flags: --ldflas, --cflags, --cflags_cc, and --include-dirs.
* Add options for build concurreny: --jobs.

These patches are maintained by Hiroki Sato <hrs@FreeBSD.org>.

The original README can be found at [README_orig.md](README_orig.md)
