R2COM  [![Build Status](https://travis-ci.org/newlog/r2com.svg?branch=master)](https://travis-ci.org/newlog/r2com)
-----

This [radare2](https://www.radare.org/r/) script allows you to easily identify what type of COM object are you dealing with when reversing a binary calling
the [CoCreateInstance](https://msdn.microsoft.com/en-us/library/windows/desktop/ms686615(v=vs.85).aspx) function from
the OLE32.DLL library.

This plugin will add a comment in the instruction pushing the `rclsid` parameter helping you identify what the COM
object is.

To get more information regarding reverse engineering COM functionality, you
can take a look to the
[Controlling Internet Explorer with COM](https://www.fireeye.com/blog/threat-research/2010/08/reversing-malware-command-control-sockets.html) section in this post by FireEye.

After using this script, you will still have to figure out what COM object function is being called. The manual process to do so - yep, not done here :( - is detailed [here](http://reverseengineering.stackexchange.com/a/2823/13290).

Usage
-----

The preferred way to use this plugin is by native radare2 plugin through r2pm:

[![asciicast](https://asciinema.org/a/4rd2r07pkkp69jxfy7tyhyis0.png)](https://asciinema.org/a/4rd2r07pkkp69jxfy7tyhyis0)

If you want, you can execute it as an external script:

[![asciicast](https://asciinema.org/a/108918.png)](https://asciinema.org/a/108918)


```bash
$ r2 <binary>
> . r2com.py
```

Authors
------

[giomismo](https://github.com/giomismo) & [newlog](https://twitter.com/newlog_)

Thanks to
---------

Special thanks to [nibble](https://github.com/jroimartin) and [zlowram]()
