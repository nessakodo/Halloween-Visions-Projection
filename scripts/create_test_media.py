#!/usr/bin/env python3
"""
Create test media files for VPT demo
"""

import cv2
import numpy as np
import os

def create_test_images():
    """Create simple test images for idle and scare states"""
    
    # Create media directory if it doesn't exist
    media_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "media")
    os.makedirs(media_dir, exist_ok=True)
    
    # Image dimensions
    width, height = 800, 600
    
    # Create idle image (calm blue gradient)
    print("Creating idle.png...")
    idle_img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a blue gradient
    for y in range(height):
        intensity = int(255 * (1 - y / height) * 0.3)  # Dark blue gradient
        idle_img[y, :] = [intensity, intensity//2, min(255, intensity + 100)]
    
    # Add text
    cv2.putText(idle_img, "IDLE STATE", (width//2 - 120, height//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
    
    idle_path = os.path.join(media_dir, "idle.png")
    cv2.imwrite(idle_path, idle_img)
    print(f"✓ Created {idle_path}")
    
    # Create scare image (intense red with flashing effect)
    print("Creating scare.png...")
    scare_img = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create a red/orange gradient
    for y in range(height):
        intensity = int(255 * (1 - y / height) * 0.8)  # Bright red gradient
        scare_img[y, :] = [0, intensity//3, min(255, intensity)]
    
    # Add scary text
    cv2.putText(scare_img, "SCARE!", (width//2 - 80, height//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 255, 255), 4)
    cv2.putText(scare_img, "BOO!", (width//2 - 50, height//2 + 80), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 0), 3)
    
    scare_path = os.path.join(media_dir, "scare.png")
    cv2.imwrite(scare_path, scare_img)
    print(f"✓ Created {scare_path}")
    
    return idle_path, scare_path

def create_test_video(image_path, output_path, duration_seconds=5, fps=30):
    """Create a simple video by repeating an image"""
    
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"✗ Could not read image: {image_path}")
        return False
    
    height, width = img.shape[:2]
    total_frames = duration_seconds * fps
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    print(f"Creating {output_path} ({duration_seconds}s @ {fps}fps)...")
    
    for frame_num in range(total_frames):
        # For scare video, add some flicker effect
        if "scare" in output_path and frame_num % 10 < 3:
            # Make it flicker by adjusting brightness
            flicker_img = cv2.convertScaleAbs(img, alpha=1.5, beta=50)
            out.write(flicker_img)
        else:
            out.write(img)
    
    out.release()
    print(f"✓ Created {output_path}")
    return True

def main():
    print("Creating test media files...")
    print("=" * 40)
    
    try:
        # Create test images
        idle_img, scare_img = create_test_images()
        
        # Create test videos from images
        media_dir = os.path.dirname(idle_img)
        
        idle_video = os.path.join(media_dir, "idle.mp4")
        scare_video = os.path.join(media_dir, "scare.mp4")
        
        create_test_video(idle_img, idle_video, duration_seconds=10)
        create_test_video(scare_img, scare_video, duration_seconds=5)
        
        print("\n" + "=" * 40)
        print("✓ All test media created successfully!")
        print("\nFiles created:")
        print(f"  - {idle_img}")
        print(f"  - {scare_img}")
        print(f"  - {idle_video}")
        print(f"  - {scare_video}")
        print("\nYou can now use these in VPT for testing.")
        
        return 0
        
    except Exception as e:
        print(f"✗ Failed to create test media: {e}")
        return 1

if __name__ == "__main__":
    exit(main())