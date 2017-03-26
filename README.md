R2COM
-----

This [radare2](https://www.radare.org/r/) script allows you to easily identify what type of COM object are you dealing with when reversing a binary calling
the [CoCreateInstance](https://msdn.microsoft.com/en-us/library/windows/desktop/ms686615(v=vs.85).aspx) function from
the OLE32.DLL library.

This plugin will add a comment in the instruction pushing the `rclsid` parameter helping you identify what the COM
object is.

To get more information regarding reverse engineering COM functionality, you
can take a look to the
[Controlling Internet Explorer with COM](https://www.fireeye.com/blog/threat-research/2010/08/reversing-malware-command-control-sockets.html) section in this post by FireEye.

Usage
-----

[![asciicast](https://asciinema.org/a/108918.png)](https://asciinema.org/a/108918)


You can either execute the script standalone or inside r2.

```bash
$ python r2com.py <binary>
```

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
