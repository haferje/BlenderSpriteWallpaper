BlenderSpriteWallpaper
======================
A python script that renders a 3D desktop wallpaper from a small sprite image, using Blender.

Examples
--------
Turn this small sprite image

![Sprite input](/sprite.png)

Into this wallpaper

![Wallpaper output](/sprite_wallpaper.png)

Additional examples:
[Output Collection Album](http://imgur.com/a/QbolL)

Requirements
------------
* Blender software is installed (the free and open source 3D animation suite)
  * tested with Blender 2.68
* Python language is installed (the programming language)

Setup
-----
Ensure `blenderlib.py` and `sprite_wallpaper.py` are in the same directory

Config
------
#### Find an Image
Find a small image you wish to render as a desktop wallpaper.  Each pixel of the image will be rendered as a 3D cube.  Thus, the best images to use are icons or sprites from video games that are low resolution, with distinct edges that aren't anti-aliased or have shadowed edges that blend into the background color.

#### Configure the Script Parameters
Open the `sprite_wallpaper.py` file in a text editor, and edit the `config` object to your liking.
* `current_directory` - the full path of the directory containing `sprite_wallpaper.py`
* `sprite_file` - the path of the image file you wish to render, relative to the current script
* `exclude_color` - the background color in the image you wish to ignore when rendering the pixels
* `resolution_width` - the resolution width of your monitor
* `resolution_height` - the resolution height of your monitor
* `resolution_percentage` - the quality with which to render (most likely you want 100)
* `background_color` - the color you wish to serve as the background in the render
* `padding_percentage` - a percentage of the height of the image you wish to use as padding between the rendered image and the edges of the rendered space
* `camera_offset_angle` - the angle you wish to rotate the camera, if you would like to offset the plane that the image is rendered on (negative rotates left, positive rotates right)

Render
------
The resulting rendered wallpaper image file will render to the same directory as your input sprite image, also with the same filename but appeneded with `_render`, as the default PNG filetype format.

#### Using the Blender UI
1. Open Blender
2. Open a view to `Text Editor`
3. In the view menu `Text > Open Text Block` and select the `sprite_wallpaper.py` file
4. In the view menu `Text > Run Script`

#### Using the Command Line
1. Open the terminal/console
2. At the prompt - where `sprite_wallpaper.py` is the full path to the script file - enter the following line
```
blender --background --python sprite_wallpaper.py
```

Enjoy
-----
Set is as your desktop wallpaper and enjoy!

For even more fun, render a few images and use the collection in an automatic rotating wallpaper application.
