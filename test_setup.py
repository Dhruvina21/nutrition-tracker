#!/usr/bin/env python3
"""
Test script to verify all required packages are installed correctly
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    
    print("=" * 60)
    print("Testing Nutrition Tracker - Environment Setup")
    print("=" * 60)
    print()
    
    # Test Python version
    print(f"✓ Python version: {sys.version}")
    print()
    
    # Test required packages
    packages = {
        'tkinter': 'Tkinter (GUI Framework)',
        'psycopg2': 'PostgreSQL Database Connector',
        'matplotlib': 'Data Visualization',
        'pandas': 'Data Manipulation',
        'tkcalendar': 'Date Picker Widget',
        'PIL': 'Image Processing (Pillow)'
    }
    
    failed = []
    
    for package, description in packages.items():
        try:
            if package == 'PIL':
                __import__(package)
            else:
                __import__(package)
            print(f"✓ {description:40} - OK")
        except ImportError as e:
            print(f"✗ {description:40} - FAILED")
            failed.append(package)
    
    print()
    print("=" * 60)
    
    if failed:
        print("❌ Setup INCOMPLETE - Missing packages:")
        for pkg in failed:
            print(f"   - {pkg}")
        print()
        print("Install missing packages with:")
        print("   pip install -r requirements.txt")
    else:
        print("✅ Setup COMPLETE - All packages installed successfully!")
        print()
        print("You can now proceed to Phase 2!")
    
    print("=" * 60)

if __name__ == "__main__":
    test_imports()