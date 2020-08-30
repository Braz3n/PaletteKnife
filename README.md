# Palette Knife
Palette Knife is a hack for modifying the compiled binary of [Steveice10's GameYob v1.0.8](https://github.com/Steveice10/GameYob) so that custom GBC palettes could be inserted into the emulator.
It also uses release v0.17 of the `makerom` application from [3DSguy's Project_CTR repository](https://github.com/3DSGuy/Project_CTR).

At present, it written to run on either Linux or OSX, although the included makerom binary is the OSX version.
This can be easily replaced from one of the releases at the above repository.

This was written because it was easier to figure out where the colour palette data is stored in the binary than it was to recompile 5 year old source code on updated toolchains.

## Using the application
Run `PaletteKnife.sh` from the terminal to begin.

In the case that "palettes.json" is in the same directory, all name and colour data will be read from that file.
Otherwise, the user will be prompted for the relevant data at the terminal.

## Some Important Notes
If using the palettes.json route, do not edit `name_address`, `palette_address` or `name_length`. Otherwise you're going to start clobbering random application data, the results of which are unknown and potentially destructive to game data.