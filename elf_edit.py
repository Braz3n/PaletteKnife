import struct
import os
import os.path
import urllib.request
import zipfile
import shutil
import json

# Some key variables for controlling the script.
BINARY_FILE_NAME = "GameYob.elf"  # Name of the file to edit.
BINARY_ZIP_URL = "https://github.com/Steveice10/GameYob/releases/download/1.0.8/GameYob.zip"
PALETTE_JSON_FILE_NAME = "palettes.json"  # We can also use a .json file instead of entering things manually.
DEFAULT_PALETTE_COLOUR_ADDRESS = 0x000DA96C  # Start location of the target colour palete in memory.
DEFAULT_PALETTE_NAME_ADDRESS = 0x000DE3A8  # Start location of the colour palete name in memory.
DEFAULT_PALETTE_NAME_MAX_LENGTH = 10
DEFAULT_PALETTE_NAME_VALUE = "{name:<{width}}".format(name="Chris' Mix", width=DEFAULT_PALETTE_NAME_MAX_LENGTH)

def TO5BIT(x):
    # Perform the arcane 5-bit compression required for the Gameboy Color.
    return (x * 0x1F * 2 + 0xFF) // (0xFF * 2)

def TOCGB(r,g,b):
    # Pack the colours into a 16-bit integer for the Gameboy Color.
    R = TO5BIT(r) & 0xFF 
    G = TO5BIT(g) & 0xFF
    B = TO5BIT(b) & 0xFF
    return ((B << 10) | (G << 5) | (R)) & 0xFFFF

def compress_colour(rgb):
    # Compress an RGB value down for the Gameboy Color and convert it into 
    # the correct memory endianness for the GameYob binary.
    compressed = TOCGB(*rgb)
    little_endian = struct.unpack( '<H', struct.pack('>H', compressed) )[0]
    return little_endian

def generate_memory(rgb_array):
    # Given an array of 8-bit (R,G,B) tuples, convert them into the correct
    # memory layout for insersion into the GameYob binary.
    hex_string = ''

    for rgb in rgb_array:
        hex_string += '{:04X}'.format(compress_colour(rgb))
    
    memory = bytes.fromhex(hex_string)
    return memory, hex_string

def sanitize_user_input(value):
    # Ensure the user has entered valid data.
    if value[0:2].lower() == "0x":
        value = value[2:]
    
    if len(value) != 6:
        print("Expected 6 character hexadecimal colour code (for example 0xFFFFFF).")
        print("Too many or too few characters were entered. Please verify input.")
        exit()

    try:
        # Split up the hex code and convert the values into their component
        # integers.
        r = int(value[:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:], 16)
    except:
        print("Expected hexadecimal values (values in the range 0-9 and A-F).")
        print("There was a problem parsing the user's input. Please verify input.")
        exit()

    return r, g, b

def generate_vanilla_json():
    # Create a template palettes.json file for manipulating several entries at once.
    palettes = []
    
    data = {
    'name_address': '0x000DE3A8',
    'palette_address': '0x000DA96C',
    'name_length': 11,
    'name': "Pastel Mix",
    'palette': ['0xFFFFA5', '0xFF9494', '0x9494FF', '0x000000', 
                '0xFFFFA5', '0xFF9494', '0x9494FF', '0x000000', 
                '0xFFFFA5', '0xFF9494', '0x9494FF', '0x000000']
    }
    palettes.append(data)

    data = {
    'name_address': '0x000DE3B4',
    'palette_address': '0x000DA624',
    'name_length': 3,
    'name': "Red",
    'palette': ['0xFFFFFF', '0xFF8484', '0x943A3A', '0x000000', 
                '0xFFFFFF', '0x7BFF31', '0x008400', '0x000000', 
                '0xFFFFFF', '0x63A5FF', '0x0000FF', '0x000000']
    }
    palettes.append(data)

    data = {
    'name_address': '0x000DE3B8',
    'palette_address': '0x000DA9E4',
    'name_length': 7,
    'name': "Orange",
    'palette': ['0xFFFFFF', '0xFFFF00', '0xFF0000', '0x000000', 
                '0xFFFFFF', '0xFFFF00', '0xFF0000', '0x000000', 
                '0xFFFFFF', '0xFFFF00', '0xFF0000', '0x000000']
    }
    palettes.append(data)

    data = {
    'name_address': '0x000DE3C0',
    'palette_address': '0x000DA594',
    'name_length': 7,
    'name': "Yellow",
    'palette': ['0xFFFFFF', '0xFFFF00', '0x7B4A00', '0x000000', 
                '0xFFFFFF', '0x63A5FF', '0x0000FF', '0x000000', 
                '0xFFFFFF', '0x7BFF31', '0x008400', '0x000000']
    }
    palettes.append(data)

    data =  {
    'name_address': '0x000DE39C',
    'palette_address': '0x000DA99C',
    'name_length': 11,
    'name': "Inverted",
    'palette': ['0x000000', '0x008484', '0xFFDE00', '0xFFFFFF',
                '0x000000', '0x008484', '0xFFDE00', '0xFFFFFF',
                '0x000000', '0x008484', '0xFFDE00', '0xFFFFFF']
    }
    palettes.append(data)

    data =  {
    'name_address': '0x000DE3D8',
    'palette_address': '0x000DA78C',
    'name_length': 11,
    'name':"Dark Green",
    'palette': ['0xFFFFFF', '0x7BFF31', '0x0063C5', '0x000000',
              '0xFFFFFF', '0xFF8484', '0x943A3A', '0x000000',
              '0xFFFFFF', '0xFF8484', '0x943A3A', '0x000000']
    }
    palettes.append(data)

    data =  {
    'name_address': '0x000DE3E4',
    'palette_address': '0x000DA66C',
    'name_length': 11,
    'name': "Dark Blue",
    'palette': ['0xFFFFFF', '0x8C8CDE', '0x52528C', '0x000000',
              '0xFFFFFF', '0xFF8484', '0x943A3A', '0x000000',
              '0xFFFFFF', '0xFFAD63', '0x843100', '0x000000']
    }
    palettes.append(data)

    data =  {
    'name_address': '0x000DE3F0',
    'palette_address': '0x000DA7A4',
    'name_length': 11,
    'name': "Dark Brown",
    'palette': ['0xFFE6C5', '0xCE9C84', '0x846B29', '0x5A3108',
              '0xFFFFFF', '0xFFAD63', '0x843100', '0x000000',
              '0xFFFFFF', '0xFFAD63', '0x843100', '0x000000']
    }

    data =  {
    'name_address': '0x000DE3FC',
    'palette_address': '0x000DA188',
    'name_length': 15,
    'name': "Classic Green",
    'palette': ['0x9BBC0F', '0x8BAC0F', '0x306230', '0x0F380F',
              '0x9BBC0F', '0x8BAC0F', '0x306230', '0x0F380F',
              '0x9BBC0F', '0x8BAC0F', '0x306230', '0x0F380F']
    }
    palettes.append(data)

    with open(PALETTE_JSON_FILE_NAME, 'w') as json_file:
        json.dump(palettes, json_file)

def find_binary():
    # Check that we actually have the binary file.
    if not os.path.exists(BINARY_FILE_NAME):
        print("{} file not found. Downloading...".format(BINARY_FILE_NAME))
        urllib.request.urlretrieve(BINARY_ZIP_URL, 'GameYob.zip')
        print("Zip archive downloaded.")
        print("Extracting...")
        with zipfile.ZipFile("GameYob.zip", 'r') as zip_ref:
            with zip_ref.open('3ds-arm/GameYob.elf') as compressed, open(BINARY_FILE_NAME, 'wb') as binary:
                shutil.copyfileobj(compressed, binary)
        print("Complete. Now cleaning up leftover files.")
        os.remove("GameYob.zip")

def modify_binary(palette_name_address, palette_color_address, palette_name_value, palette_memory_bytes):
    # Update the palette name and address in the program binary.
    with open(BINARY_FILE_NAME, "rb+") as binary_file:
        # Update the palette colours.
        binary_file.seek(palette_color_address, 0)
        binary_file.write(palette_memory_bytes)
        # Update the palette name.
        binary_file.seek(palette_name_address, 0)
        binary_file.write(bytes(palette_name_value, 'utf-8'))

def load_from_json():
    # Load in palette information from a JSON file instead of stdin.

    print("{} exists. Using this information to update the binary.\n\n".format(PALETTE_JSON_FILE_NAME))
    with open(PALETTE_JSON_FILE_NAME, 'r') as json_file:
        palettes = json.load(json_file)
        
    for palette in palettes:
        # Some basic error checking.
        assert len(palette['name']) <= palette['name_length'], "Entered name is too long. Please check \"{}\" entry.".format(palettes['name'])
        assert len(palette['palette']) == 12, "Expected 12 hexadecimal colours. Please check \"{}\" entry.".format(palettes['name'])

        # Convert the hex strings into integers for proper addressing.
        name_address = int(palette['name_address'], 16)
        palette_address = int(palette['palette_address'], 16)

        # Convert the hexadecimal colours into (r,g,b) tuples.
        rgb_colors = []
        for color in palette['palette']:
            rgb_colors.append(sanitize_user_input(color))

        # Format the new string and colour memory.
        new_name = "{name:<{width}}".format(name=palette['name'], width=palette['name_length'])
        new_memory, palette_hex_string = generate_memory(rgb_colors)
        print("Overwriting palette name at address 0x{:04X} with \"{}\"".format(name_address, new_name))
        print("New palette hexadecimal string: 0x{}".format(palette_hex_string))

        find_binary()  # Fetch the binary if it doesn't already exist.

        modify_binary(name_address, palette_address, new_name, new_memory)
    
    print("Successfully updated the GameYob binary.")

def manual_entry():
    # Ask the user directly for the necessary information to update the binary.
    # Note that this approach is limited to modifying a single palette.

    print("{} does not exist. Falling back to manual mode.\n\n".format(PALETTE_JSON_FILE_NAME))

    if len(DEFAULT_PALETTE_NAME_VALUE) > DEFAULT_PALETTE_NAME_MAX_LENGTH:
        print("Error: Palette Name is too long. It must be no more than {} characters.".format(DEFAULT_PALETTE_NAME_MAX_LENGTH))
        print("Please fix the issue and rerun the script.")
        exit()

    palette0 = sanitize_user_input(input("Input palette0 first colour: "))
    palette1 = sanitize_user_input(input("Input palette0 second colour: "))
    palette2 = sanitize_user_input(input("Input palette0 third colour: "))
    palette3 = sanitize_user_input(input("Input palette0 fourth colour: "))

    palette4 = sanitize_user_input(input("Input palette1 first colour: "))
    palette5 = sanitize_user_input(input("Input palette1 second colour: "))
    palette6 = sanitize_user_input(input("Input palette1 third colour: "))
    palette7 = sanitize_user_input(input("Input palette1 fourth colour: "))

    palette8 = sanitize_user_input(input( "Input palette2 first colour: "))
    palette9 = sanitize_user_input(input( "Input palette2 second colour: "))
    palette10 = sanitize_user_input(input("Input palette2 third colour: "))
    palette11 = sanitize_user_input(input("Input palette2 fourth colour: "))

    new_colours = [palette0, palette1, palette2, palette3,
                    palette4, palette5, palette6, palette7,
                    palette8, palette9, palette10, palette11]
    new_memory, palette_hex_string = generate_memory(new_colours)

    find_binary()  # Fetch the program binary if it's not already here.

    print("Now editing the GameYob binary.")
    print("New palette name: {}".format(DEFAULT_PALETTE_NAME_VALUE))
    print("New palette memory: {}".format(palette_hex_string))
    modify_binary(DEFAULT_PALETTE_NAME_ADDRESS, DEFAULT_PALETTE_COLOUR_ADDRESS, DEFAULT_PALETTE_NAME_VALUE, new_memory)
    print("Successfully updated the GameYob binary.")

def main():
    if os.path.exists(PALETTE_JSON_FILE_NAME):
        load_from_json()
    else:
        manual_entry()
    
if __name__ == "__main__":
    main()
    # generate_vanilla_json()
