#!/usr/bin/env python3
"""
GitHub Repository Thumbnail Generator
Creates 1280x640px social preview images for GitHub repositories.
"""

from PIL import Image, ImageDraw, ImageFont
import json
import os

# Thumbnail specifications
WIDTH = 1280
HEIGHT = 640
PADDING = 60
BG_COLOR = (15, 23, 42)  # Slate-900
ACCENT_COLOR = (99, 102, 241)  # Indigo-500
TEXT_COLOR = (248, 250, 252)  # Slate-50
SUBTEXT_COLOR = (148, 163, 184)  # Slate-400
PROFILE_PHOTO = "repo-profile.jpg"  # Path to your profile photo
PROFILE_SIZE = 120  # Diameter of circular profile photo

def create_circular_profile(image_path, size):
    """
    Create a circular profile photo with transparent background.
    
    Args:
        image_path: Path to the profile photo
        size: Diameter of the circular image
    
    Returns:
        PIL Image with circular mask and transparent background
    """
    try:
        # Open and resize image
        img = Image.open(image_path).convert('RGB')
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Create output with transparency
        output = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        output.paste(img, (0, 0))
        output.putalpha(mask)
        
        return output
    except FileNotFoundError:
        print(f"⚠️  Profile photo '{image_path}' not found. Skipping profile image.")
        return None
    except Exception as e:
        print(f"⚠️  Error processing profile photo: {e}")
        return None

def create_thumbnail(repo_name, description, tech_stack, output_file):
    """
    Generate a thumbnail for a GitHub repository.
    
    Args:
        repo_name: Name of the repository
        description: Brief description of the project
        tech_stack: List of technologies used
        output_file: Output filename (PNG)
    """
    # Create image with background
    img = Image.new('RGBA', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Add accent bar on the left
    draw.rectangle([0, 0, 8, HEIGHT], fill=ACCENT_COLOR)
    
    # Try to load fonts (fallback to default if not available)
    try:
        title_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72)
        desc_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 36)
        tech_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
        label_font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 24)
    except:
        title_font = ImageFont.load_default()
        desc_font = ImageFont.load_default()
        tech_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
    
    y_position = PADDING + 40
    
    # Draw repository name
    draw.text((PADDING + 20, y_position), repo_name, fill=TEXT_COLOR, font=title_font)
    y_position += 100
    
    # Draw description (wrap text if too long)
    max_width = WIDTH - (PADDING * 2) - 40
    wrapped_description = wrap_text(description, desc_font, max_width, draw)
    for line in wrapped_description[:3]:  # Max 3 lines
        draw.text((PADDING + 20, y_position), line, fill=SUBTEXT_COLOR, font=desc_font)
        y_position += 50
    
    # Draw tech stack section
    y_position = HEIGHT - PADDING - 100
    draw.text((PADDING + 20, y_position), "Tech Stack", fill=SUBTEXT_COLOR, font=label_font)
    y_position += 40
    
    # Draw tech stack badges
    x_position = PADDING + 20
    for tech in tech_stack[:6]:  # Max 6 technologies
        badge_padding = 15
        
        # Calculate badge size
        bbox = draw.textbbox((0, 0), tech, font=tech_font)
        badge_width = bbox[2] - bbox[0] + (badge_padding * 2)
        badge_height = bbox[3] - bbox[1] + (badge_padding * 2)
        
        # Check if badge fits on current line
        if x_position + badge_width > WIDTH - PADDING - 20:
            break
        
        # Draw badge background
        draw.rounded_rectangle(
            [x_position, y_position, x_position + badge_width, y_position + badge_height],
            radius=8,
            fill=(30, 41, 59)  # Slate-800
        )
        
        # Draw badge text
        draw.text((x_position + badge_padding, y_position + badge_padding), 
                  tech, fill=ACCENT_COLOR, font=tech_font)
        
        x_position += badge_width + 15
    
    # Add profile photo in bottom-right corner
    profile_img = create_circular_profile(PROFILE_PHOTO, PROFILE_SIZE)
    if profile_img:
        # Position: bottom-right with padding
        profile_x = WIDTH - PROFILE_SIZE - PADDING
        profile_y = HEIGHT - PROFILE_SIZE - PADDING
        
        # Add subtle border/shadow effect
        border_size = 6
        border = Image.new('RGBA', 
                          (PROFILE_SIZE + border_size * 2, PROFILE_SIZE + border_size * 2), 
                          ACCENT_COLOR + (255,))
        border_mask = Image.new('L', 
                               (PROFILE_SIZE + border_size * 2, PROFILE_SIZE + border_size * 2), 
                               0)
        border_draw = ImageDraw.Draw(border_mask)
        border_draw.ellipse((0, 0, PROFILE_SIZE + border_size * 2, PROFILE_SIZE + border_size * 2), 
                           fill=255)
        border.putalpha(border_mask)
        
        # Paste border then profile
        img.paste(border, (profile_x - border_size, profile_y - border_size), border)
        img.paste(profile_img, (profile_x, profile_y), profile_img)
    
    # Convert to RGB for PNG saving (removes alpha channel)
    final_img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    final_img.paste(img, (0, 0), img)
    
    # Save image
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    final_img.save(output_file, 'PNG', optimize=True)
    print(f"✅ Created thumbnail: {output_file}")

def wrap_text(text, font, max_width, draw):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        width = bbox[2] - bbox[0]
        
        if width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines

def load_config(config_file='thumbnail_config.json'):
    """Load repository configurations from JSON file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Config file '{config_file}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"❌ Invalid JSON in '{config_file}'.")
        return None

def main():
    """Generate thumbnails for all repos in config file."""
    config = load_config()
    
    if not config or 'repositories' not in config:
        print("Please create a thumbnail_config.json file with repository details.")
        return
    
    # Create output directory
    output_dir = config.get('output_dir', 'thumbnails')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate thumbnails
    for repo in config['repositories']:
        output_file = os.path.join(
            output_dir, 
            f"{repo['name'].lower().replace(' ', '-')}.png"
        )
        
        create_thumbnail(
            repo_name=repo['name'],
            description=repo['description'],
            tech_stack=repo['tech_stack'],
            output_file=output_file
        )
    
    print(f"\n🎉 Generated {len(config['repositories'])} thumbnail(s) in '{output_dir}/' directory")
    print(f"\n📋 Next steps:")
    print(f"   1. Review thumbnails in '{output_dir}/' directory")
    print(f"   2. Go to your GitHub repo → Settings → Social preview")
    print(f"   3. Upload the thumbnail (1280x640px PNG)")

if __name__ == '__main__':
    main()
