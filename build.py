import os
import sys
import shutil
from PyInstaller.__main__ import run

def clean_build_dirs():
    """Clean build and dist directories"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        
def build_app():
    """Build the application for the current platform"""
    # Get the current platform
    platform = sys.platform
    
    # Clean previous builds
    clean_build_dirs()
    
    # Get absolute paths
    app_dir = os.path.abspath('app')
    resources_dir = os.path.abspath('resources')
    
    # Ensure paths use the correct separator for the platform
    sep = ';' if platform == 'win32' else ':'
    
    # Base PyInstaller options
    options = [
        os.path.join(app_dir, 'main.py'),  # Your main script
        '--name=Warehouse',  # Name of the executable
        '--windowed',  # Use windowed mode
        '--onedir',  # Create a directory containing the executable
        f'--add-data={app_dir}{sep}app',  # Include entire app directory
        f'--add-data={resources_dir}{sep}resources',  # Include resources
        '--icon=resources/icon.icns',  # Application icon
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without confirmation
    ]

    # Platform-specific options
    if platform == 'darwin':  # macOS
        options.extend([
            '--target-arch=universal2',  # Build for both Intel and Apple Silicon
            '--codesign-identity=',  # Skip code signing
            '--osx-bundle-identifier=com.warehouse.app'  # Bundle identifier
        ])
    elif platform == 'win32':  # Windows
        options.extend([
            '--runtime-tmpdir=.'
        ])

    # Run PyInstaller
    try:
        run(options)
        print(f"\nBuild completed successfully for {platform}")
        print(f"Executable can be found in the 'dist' directory")
    except Exception as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    build_app()
