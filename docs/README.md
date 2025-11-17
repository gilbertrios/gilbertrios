# GitHub Thumbnail Generator Documentation

Create professional 1280x640px social preview images for your GitHub repositories to make them stand out on LinkedIn and other social platforms.

---

## Repository Structure

```
gilbertrios/
├── thumb-nail-creation/
│   ├── generate_thumbnail.py      # Main thumbnail generator script
│   ├── thumbnail_config.json      # Repository configuration file
│   ├── repo-profile.jpg          # Your profile photo (optional)
│   └── thumbnails/               # Generated thumbnails output directory
│       ├── azure-app-service-logging.png
│       ├── azure-terraform-foundation.png
│       └── terraform-provider-utils.png
├── docs/
│   └── README.md                 # This documentation
├── linkedin-posts/
│   ├── linkedin-post-1.md
│   ├── linkedin-post-2.md
│   └── linkedin-post-3.md
└── README.md                      # Main profile README
```

**Note**: The thumbnail generator creates thumbnails relative to its current directory. All generated images will be saved in `thumb-nail-creation/thumbnails/`.

---

## Table of Contents
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Generating Thumbnails](#generating-thumbnails)
- [Uploading to GitHub](#uploading-to-github)
- [Refreshing LinkedIn Cache](#refreshing-linkedin-cache)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- **Python 3.x** installed on your system
- **Pillow** library for image generation
- A profile photo (optional): `repo-profile.jpg`

---

## Installation

### 1. Install Python (if not already installed)

Check if Python 3 is installed:
```bash
python3 --version
```

If not installed, install via Homebrew (macOS):
```bash
brew install python3
```

### 2. Install Pillow Library

```bash
pip3 install Pillow
```

---

## Configuration

### 1. Navigate to Thumbnail Directory

```bash
cd thumb-nail-creation
```

### 2. Edit `thumbnail_config.json`

Update the configuration file with your repository details:

```json
{
  "output_dir": "thumbnails",
  "repositories": [
    {
      "name": "Your Repo Name",
      "description": "Brief description of your project (keep under 100 characters)",
      "tech_stack": ["Python", "React", "Docker", "AWS", "PostgreSQL"]
    },
    {
      "name": "Another Repo",
      "description": "Another project description",
      "tech_stack": ["Go", "Terraform", "GitHub Actions"]
    }
  ]
}
```

**Configuration Tips:**
- **name**: Repository display name (will appear as large heading)
- **description**: Keep under 100 characters for readability
- **tech_stack**: List 3-6 main technologies (more will be truncated)
- **output_dir**: Directory where thumbnails will be saved (relative to `thumb-nail-creation/`)

### 3. Add Profile Photo (Optional)

Place your profile photo in the `thumb-nail-creation/` directory:
```bash
# Photo should be named: repo-profile.jpg
# Location: thumb-nail-creation/repo-profile.jpg
# Supported formats: JPG, PNG
# Recommended: Square photo, at least 400x400px
```

The script will automatically:
- Resize the photo
- Create a circular mask
- Add a colored border
- Position it in the bottom-right corner

---

## Generating Thumbnails

### 1. Navigate to Thumbnail Directory

```bash
cd thumb-nail-creation
```

### 2. Run the Generator

```bash
python3 generate_thumbnail.py
```

### Expected Output

```
✅ Created thumbnail: thumbnails/azure-app-service-logging.png
✅ Created thumbnail: thumbnails/azure-terraform-foundation.png
✅ Created thumbnail: thumbnails/terraform-provider-utils.png

🎉 Generated 3 thumbnail(s) in 'thumbnails/' directory

📋 Next steps:
   1. Review thumbnails in 'thumbnails/' directory
   2. Go to your GitHub repo → Settings → Social preview
   3. Upload the thumbnail (1280x640px PNG)
```

### 3. View Generated Thumbnails

All thumbnails are saved in the `thumb-nail-creation/thumbnails/` directory as optimized PNG files.

```bash
# View thumbnails (macOS)
open thumbnails/

# Or navigate to the directory
ls thumbnails/
```

---

## Uploading to GitHub

### Steps to Upload Social Preview

1. **Go to your repository on GitHub**
   ```
   https://github.com/yourusername/your-repo
   ```

2. **Click the Settings tab** (must have repo admin access)

3. **Scroll to "Social preview" section**

4. **Click "Edit"**

5. **Upload your thumbnail**
   - Select the PNG file from `thumb-nail-creation/thumbnails/` directory
   - Must be 1280x640px (script generates correct size)
   - Max file size: 1MB

6. **Click "Save"**

### Verify Upload

Visit your repository's main page and check the OpenGraph meta tags:
```bash
curl -s https://github.com/yourusername/your-repo | grep "og:image"
```

---

## Refreshing LinkedIn Cache

LinkedIn aggressively caches social preview images. After uploading a new thumbnail to GitHub, you need to force LinkedIn to refresh its cache.

### Method 1: LinkedIn Post Inspector (Recommended)

1. **Go to LinkedIn Post Inspector**
   ```
   https://www.linkedin.com/post-inspector/
   ```

2. **Enter your GitHub repository URL**
   ```
   https://github.com/yourusername/your-repo
   ```

3. **Click "Inspect"**
   - LinkedIn will fetch the current metadata
   - You'll see a preview of what will appear in posts

4. **Click "Request a scrape"** (if old image appears)
   - Forces LinkedIn to re-fetch the thumbnail
   - Usually updates within 1-5 minutes

5. **Verify the new thumbnail appears**

### Method 2: URL Parameter Trick

Add a version parameter to your URL when sharing:
```
https://github.com/yourusername/your-repo?v=2
```

This makes LinkedIn treat it as a new URL and fetch fresh metadata.

### Method 3: Delete and Reshare

If you've already posted the link:
1. Delete the old post
2. Wait 5-10 minutes
3. Create a new post with the repository URL
4. LinkedIn should fetch the updated thumbnail

### Cache Duration

- **Without forcing refresh**: 7-30 days
- **With Post Inspector**: 1-5 minutes
- **With URL parameter**: Immediate (new URL)

### Best Practice

**Always use Post Inspector BEFORE sharing** any repository link to ensure LinkedIn has the latest thumbnail cached.

---

## Customization

### Color Scheme

Edit colors in `generate_thumbnail.py`:

```python
BG_COLOR = (15, 23, 42)         # Background - Slate-900
ACCENT_COLOR = (99, 102, 241)    # Accent/Border - Indigo-500
TEXT_COLOR = (248, 250, 252)     # Title text - Slate-50
SUBTEXT_COLOR = (148, 163, 184)  # Description - Slate-400
```

Colors use RGB format: `(Red, Green, Blue)` with values 0-255.

### Profile Photo Size

Change the circular profile photo diameter:

```python
PROFILE_SIZE = 120  # Default: 120px diameter
```

### Fonts

The script uses system fonts. On macOS:
- **Default**: Helvetica (built-in)
- **Location**: `/System/Library/Fonts/Helvetica.ttc`

To use custom fonts, replace the font paths:
```python
title_font = ImageFont.truetype('/path/to/your/font.ttf', 72)
```

### Layout Adjustments

Modify spacing and padding:
```python
PADDING = 60        # Edge padding
WIDTH = 1280        # Canvas width (don't change - GitHub requirement)
HEIGHT = 640        # Canvas height (don't change - GitHub requirement)
```

---

## Troubleshooting

### "Module 'PIL' not found"

**Solution**: Install Pillow
```bash
pip3 install Pillow
```

### "Profile photo not found"

**Solution**: 
- Ensure `repo-profile.jpg` is in the `thumb-nail-creation/` directory
- Or remove profile photo code if not needed
- Script will continue without profile photo if missing

### Thumbnails look blurry on LinkedIn

**Check**:
- Ensure image is exactly 1280x640px (script generates correct size)
- File size should be under 1MB
- Use PNG format (better quality than JPG)
- Force LinkedIn cache refresh using Post Inspector

### Text is cut off

**Solution**:
- Shorten description in `thumbnail_config.json`
- Keep descriptions under 80-100 characters
- Reduce number of technologies in `tech_stack` (max 6 visible)

### Colors don't match my brand

**Solution**: Edit color constants in `generate_thumbnail.py` using your brand colors in RGB format.

### Font not loading

The script falls back to default fonts if system fonts aren't found. This is normal and thumbnails will still generate correctly.

---

## Example Workflow

```bash
# 1. Navigate to thumbnail directory
cd thumb-nail-creation

# 2. Edit configuration
nano thumbnail_config.json

# 3. Add profile photo (optional)
# Place repo-profile.jpg in thumb-nail-creation/ directory

# 4. Generate thumbnails
python3 generate_thumbnail.py

# 5. Review output
open thumbnails/

# 6. Upload to GitHub
# Go to each repo → Settings → Social preview → Upload

# 7. Force LinkedIn refresh
# Visit https://www.linkedin.com/post-inspector/
# Enter repo URL and click "Request a scrape"

# 8. Share on LinkedIn
# Your new thumbnail will appear!
```

---

## Additional Resources

- [GitHub Social Preview Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)
- [LinkedIn Post Inspector](https://www.linkedin.com/post-inspector/)
- [OpenGraph Protocol](https://ogp.me/)
- [Pillow Documentation](https://pillow.readthedocs.io/)

---

## Support

For issues or questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review your `thumbnail_config.json` syntax
- Ensure all prerequisites are installed
- Verify Python and Pillow versions are up to date

---

**Created by Gilbert Rios** | [GitHub Profile](https://github.com/gilbertrios)
