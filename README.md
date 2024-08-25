# Midinous Autobot

The purpose of this tool is to make some level of automation for many of the pointless things that I want to do with Midinous.  
Things like logic gates, extremely dense logical controls, controllable screens, images, and animations.

I wired a screen with a controler by hand before making an attempt at this in an automated way.

This should be obvious, but this requires Midinous as a software, which can be obtained from Steam or from itch.io.\*  
\* <sup>if you are on Linux, the itch.io install is preferred. I was unable to get Midinous to connect via MIDI using the Steam download, but the itch.io download was immediately visible to my MIDI setup.</sup>

## Requirements

- Midinous (to use the files, this isn't required to generate them)
- Python 3+
- Pillow (should be pre-installed with Python)

## Um Actually

`app.py` isn't an app right now. It's just a file that I've been editing to make it easier to load/unload/call the `Midinous` class and run stuff from it.

It will likely become a curses app but who knows what the future brings. It may even wind up being **_nothing at all_**.

For definitions of things that I've figured out from just digging around - particularly node types and some light explainers, check out [the dictionary thing](./dictionary.md) that I've slapped together. It is incomplete.

## How to Use it

If all you want to do is make an image show up in Midinous, it's actually pretty straightforward.

```Python
# import the Midinous class from src/black_box
from src.black_box import Midinous

# create a Midinous class instance
blorbo = Midinous()

# run the magic
blorbo.translate_image("image.jpg",dims=(20,20))

# export the save
blorbo.export()
```

From there, you'll have a `json` file in the project folder that you would need to put into your saves folder.

- you can view the local files by clicking the "local files" button in Midinous - I highly recommend making a symlink if possible if you are wanting to try multiple images out.

### As a quick note...

Midinous isn't really designed to do this, like... at all. Not by any stretch of the imagination.

If your image is too big, or your animation has too many frames on too big of a screen... Midinous WILL crash when it loads.  
If you are unloading one save and then loading another, you may experience a crash as well - whether Midinous can handle the file that's being loaded or not.  
You may have to try loading it a few times.

It is theoretically possible to import the image into an existing save if you know what offset everything should be at to not conflict in any way - you just have to copy all of the nodes between the Type 0 node and Type 6 node and place everything in front of the first Type 5 node in your existing save.

- ^^^ MAKE A BACKUP MAKE A BACKUP MAKE A BACKUP MAKE A BACKUP MAKE A BACKUP MAKE A BACKUP ^^^

## Lastly

I am still going through and commenting in the code right now. I am in no rush to do this.
