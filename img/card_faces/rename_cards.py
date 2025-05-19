import os

def get_new_filename(old_name):
    # Extract suit and value from the old filename
    parts = old_name.replace('.svg', '').split('_')
    suit = parts[0][0].upper()  # First letter of suit
    value = parts[1]
    
    # Convert value to new format
    value_map = {
        'ace': '1',
        'jack': 'J',
        'queen': 'Q',
        'king': 'K'
    }
    
    new_value = value_map.get(value, value)
    return f"{suit}{new_value}.svg"

def main():
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get all SVG files in the directory
    svg_files = [f for f in os.listdir(script_dir) if f.endswith('.svg')]
    
    # Rename each file
    for old_name in svg_files:
        new_name = get_new_filename(old_name)
        old_path = os.path.join(script_dir, old_name)
        new_path = os.path.join(script_dir, new_name)
        
        try:
            os.rename(old_path, new_path)
            print(f"Renamed: {old_name} -> {new_name}")
        except Exception as e:
            print(f"Error renaming {old_name}: {str(e)}")

if __name__ == "__main__":
    main()
