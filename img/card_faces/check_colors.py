import pygame
import os

def analyze_image_colors(image_path):
    # Initialize pygame
    pygame.init()
    
    # Load the image
    img = pygame.image.load(image_path)
    
    # Get the surface data
    surface_data = pygame.surfarray.array3d(img)
    
    # Get unique colors
    unique_colors = set()
    for x in range(surface_data.shape[0]):
        for y in range(surface_data.shape[1]):
            color = tuple(surface_data[x, y])
            unique_colors.add(color)
    
    # Print all unique colors
    print(f"Found {len(unique_colors)} unique colors in {image_path}:")
    for color in sorted(unique_colors):
        print(f"RGB: {color}")
    
    # Check specifically for white-like colors
    print("\nWhite-like colors (R, G, B all > 240):")
    for color in sorted(unique_colors):
        if all(c > 240 for c in color):
            print(f"RGB: {color}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "EC.png")
    analyze_image_colors(image_path) 