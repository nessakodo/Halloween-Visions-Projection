#!/usr/bin/env python3
"""
Simple VLC test script for video playback verification
Tests basic VLC functionality and fullscreen projection
"""

import argparse
import time
import os
import vlc

def test_vlc_playback(video_path, fullscreen=False, display=None, duration=10):
    """Test VLC video playback"""
    
    if not os.path.exists(video_path):
        print(f"❌ Video file not found: {video_path}")
        print("💡 Create a test video file or specify an existing one")
        return False
    
    print(f"🎬 Testing VLC playback...")
    print(f"   Video: {video_path}")
    print(f"   Fullscreen: {fullscreen}")
    print(f"   Display: {display}")
    print(f"   Duration: {duration}s")
    
    # VLC setup
    vlc_args = [
        '--intf', 'dummy',  # No interface
        '--no-audio',       # Disable audio for testing
        '--video-on-top',   # Keep video on top
        '--no-video-title-show',  # Don't show filename
    ]
    
    # Add fullscreen display option if specified
    if display is not None:
        vlc_args.extend(['--monitor', str(display)])
    
    try:
        # Create VLC instance and player
        instance = vlc.Instance(vlc_args)
        player = instance.media_player_new()
        
        # Create media and set it
        media = instance.media_new(video_path)
        media.add_option('input-repeat=-1')  # Loop indefinitely
        player.set_media(media)
        
        # Set fullscreen if requested
        if fullscreen:
            player.set_fullscreen(True)
        
        # Start playback
        print("▶️  Starting playback...")
        player.play()
        
        # Wait a moment for playback to start
        time.sleep(1)
        
        # Check if playing
        if player.is_playing():
            print("✅ Playback started successfully")
            print(f"   Playing for {duration} seconds...")
            time.sleep(duration)
        else:
            print("❌ Playback failed to start")
            return False
        
        # Stop and cleanup
        print("⏹️  Stopping playback...")
        player.stop()
        player.release()
        instance.release()
        
        print("✅ VLC test completed successfully")
        return True
        
    except Exception as e:
        print(f"❌ VLC test failed: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Test VLC video playback")
    parser.add_argument("--video", default="videos/test.mp4", 
                       help="Path to test video file")
    parser.add_argument("--fullscreen", action="store_true", 
                       help="Test fullscreen playback")
    parser.add_argument("--display", type=int, 
                       help="Display index for fullscreen")
    parser.add_argument("--duration", type=int, default=10, 
                       help="Test duration in seconds")
    parser.add_argument("--create-test-videos", action="store_true",
                       help="Create test video directory structure")
    
    args = parser.parse_args()
    
    if args.create_test_videos:
        print("📁 Creating test video directory structure...")
        os.makedirs("videos", exist_ok=True)
        
        # Create placeholder files
        placeholder_content = "# Place your video files here:\n# - sleeping_face.mp4 (idle/calm video)\n# - angry_face.mp4 (scare/alert video)\n"
        
        with open("videos/README.md", "w") as f:
            f.write(placeholder_content)
        
        print("✅ Created videos/ directory")
        print("💡 Add your sleeping_face.mp4 and angry_face.mp4 files to the videos/ directory")
        return
    
    # Test VLC playback
    success = test_vlc_playback(
        video_path=args.video,
        fullscreen=args.fullscreen,
        display=args.display,
        duration=args.duration
    )
    
    if success:
        print("\n🎉 VLC is working correctly!")
        print("💡 You can now use the main projection script:")
        print("   python scripts/yolo_vlc_projection.py --show")
    else:
        print("\n❌ VLC test failed")
        print("💡 Troubleshooting:")
        print("   • Install VLC media player from videolan.org")
        print("   • Install python-vlc: pip install python-vlc")
        print("   • Check video file exists and is playable")

if __name__ == "__main__":
    main()