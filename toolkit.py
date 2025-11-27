#!/usr/bin/env python3
import os
import shutil
import time
import platform
import psutil
import socket
import datetime
import argparse
from pathlib import Path

# ================================
# FILE ORGANIZER
# ================================

def organize_files(directory="."):
    """Organize files by type into folders"""
    
    file_types = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.csv'],
        'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'],
        'Music': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
        'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
        'Code': ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.php'],
        'Executables': ['.exe', '.msi', '.dmg', '.pkg', '.deb'],
        'Fonts': ['.ttf', '.otf', '.woff', '.woff2']
    }
    
    path = Path(directory)
    organized_count = 0
    
    print(f"📁 Organizing files in: {path.absolute()}")
    print("=" * 50)
    
    for file_path in path.iterdir():
        if file_path.is_file() and file_path.name != __file__:
            file_extension = file_path.suffix.lower()
            moved = False
            
            for folder, extensions in file_types.items():
                if file_extension in extensions:
                    target_dir = path / folder
                    target_dir.mkdir(exist_ok=True)
                    
                    counter = 1
                    new_name = file_path.name
                    while (target_dir / new_name).exists():
                        name_parts = file_path.stem, counter, file_path.suffix
                        new_name = f"{name_parts[0]}_{name_parts[1]}{name_parts[2]}"
                        counter += 1
                    
                    shutil.move(str(file_path), str(target_dir / new_name))
                    print(f"✅ Moved: {file_path.name} → {folder}/")
                    organized_count += 1
                    moved = True
                    break
            
            if not moved:
                other_dir = path / "Others"
                other_dir.mkdir(exist_ok=True)
                shutil.move(str(file_path), str(other_dir / file_path.name))
                print(f"📦 Moved: {file_path.name} → Others/")
                organized_count += 1
    
    print("=" * 50)
    print(f"🎉 Organization complete! Moved {organized_count} files.")

# ================================
# SYSTEM INFO CHECKER
# ================================

def get_size(bytes, suffix="B"):
    """Scale bytes to its proper format"""
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def system_info():
    """Display comprehensive system information"""
    
    print("🖥️  SYSTEM INFORMATION")
    print("=" * 60)
    
    # System Information
    print("\n💻 SYSTEM")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Version: {platform.version()}")
    print(f"  Architecture: {platform.architecture()[0]}")
    print(f"  Hostname: {socket.gethostname()}")
    
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"  Local IP: {local_ip}")
    except:
        print(f"  Local IP: Unable to determine")
    
    # Boot Time
    boot_time = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time)
    print(f"  Boot Time: {bt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # CPU Information
    print("\n⚡ CPU")
    print(f"  Processor: {platform.processor() or 'Unknown'}")
    print(f"  Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    print(f"  Usage: {psutil.cpu_percent(interval=1)}%")
    
    # Memory Information
    print("\n🧠 MEMORY")
    mem = psutil.virtual_memory()
    print(f"  Total: {get_size(mem.total)}")
    print(f"  Used: {get_size(mem.used)} ({mem.percent}%)")
    print(f"  Available: {get_size(mem.available)}")
    
    # Disk Information
    print("\n💾 DISK")
    partitions = psutil.disk_partitions()
    for partition in partitions[:3]:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            print(f"  {partition.device} ({partition.mountpoint})")
            print(f"    Total: {get_size(usage.total)}")
            print(f"    Used: {get_size(usage.used)} ({usage.percent}%)")
            print(f"    Free: {get_size(usage.free)}")
        except (PermissionError, FileNotFoundError):
            continue
    
    # Network Information
    print("\n🌐 NETWORK")
    net_io = psutil.net_io_counters()
    print(f"  Bytes Sent: {get_size(net_io.bytes_sent)}")
    print(f"  Bytes Received: {get_size(net_io.bytes_recv)}")
    
    # Current User
    print("\n👤 USER")
    try:
        print(f"  Username: {os.getlogin()}")
    except:
        print(f"  Username: Unknown")
    print(f"  Current Directory: {os.getcwd()}")

# ================================
# COUNTDOWN TIMER
# ================================

def beep():
    """Play system beep sound"""
    print('\a', end='', flush=True)

def clear_line():
    """Clear current line in terminal"""
    print('\r' + ' ' * 50, end='\r', flush=True)

def countdown_timer(seconds, message="Time's up!"):
    """Countdown timer with visual progress"""
    
    try:
        seconds = int(seconds)
        if seconds <= 0:
            print("❌ Please enter a positive number of seconds")
            return
        
        original_seconds = seconds
        print(f"⏰ Countdown: {seconds} seconds")
        print("Press Ctrl+C to stop the timer")
        print("-" * 30)
        
        start_time = time.time()
        
        while seconds > 0:
            try:
                mins, secs = divmod(seconds, 60)
                hours, mins = divmod(mins, 60)
                
                progress = (original_seconds - seconds) / original_seconds
                bar_length = 30
                filled = int(bar_length * progress)
                bar = '█' * filled + '░' * (bar_length - filled)
                
                if hours > 0:
                    time_format = f"{hours:02d}:{mins:02d}:{secs:02d}"
                else:
                    time_format = f"{mins:02d}:{secs:02d}"
                
                print(f"⏳ {time_format} [{bar}] {progress*100:.1f}%", end='\r', flush=True)
                
                time.sleep(1)
                seconds -= 1
                
            except KeyboardInterrupt:
                clear_line()
                elapsed = time.time() - start_time
                print(f"⏹️  Timer stopped after {int(elapsed)} seconds")
                return
        
        clear_line()
        print(f"🎉 {message}")
        
        for _ in range(3):
            beep()
            time.sleep(0.5)
            
    except ValueError:
        print("❌ Please enter a valid number of seconds")

def pomodoro_timer(work_minutes=25, break_minutes=5):
    """Pomodoro technique timer"""
    
    cycles = 0
    try:
        while True:
            cycles += 1
            print(f"\n🍅 Pomodoro Cycle {cycles}")
            print("=" * 30)
            
            print(f"💻 Work session: {work_minutes} minutes")
            countdown_timer(work_minutes * 60, "Work session complete! Time for a break.")
            
            print(f"\n☕ Break session: {break_minutes} minutes")
            countdown_timer(break_minutes * 60, "Break over! Back to work.")
            
            print(f"\n✅ Completed cycle {cycles}. Continue? (y/n): ", end='')
            choice = input().lower()
            if choice != 'y':
                print("👋 Pomodoro session ended!")
                break
                
    except KeyboardInterrupt:
        print("\n👋 Pomodoro session interrupted!")

# ================================
# MAIN PROGRAM
# ================================

def main():
    parser = argparse.ArgumentParser(description='Multi-Tool Terminal Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # File Organizer command
    org_parser = subparsers.add_parser('organize', help='Organize files by type')
    org_parser.add_argument('directory', nargs='?', default='.', 
                           help='Directory to organize (default: current)')
    
    # System Info command
    subparsers.add_parser('systeminfo', help='Display system information')
    
    # Timer commands
    timer_parser = subparsers.add_parser('timer', help='Start a countdown timer')
    timer_parser.add_argument('seconds', type=int, help='Seconds to count down')
    timer_parser.add_argument('--message', '-m', default="Time's up!", 
                            help='Custom message when timer ends')
    
    # Pomodoro command
    pomodoro_parser = subparsers.add_parser('pomodoro', help='Start Pomodoro timer')
    pomodoro_parser.add_argument('--work', '-w', type=int, default=25,
                               help='Work minutes (default: 25)')
    pomodoro_parser.add_argument('--break', '-b', type=int, default=5,
                               help='Break minutes (default: 5)', dest='break_minutes')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'organize':
            if not Path(args.directory).exists():
                print(f"❌ Error: Directory '{args.directory}' not found!")
            else:
                organize_files(args.directory)
                
        elif args.command == 'systeminfo':
            system_info()
            
        elif args.command == 'timer':
            countdown_timer(args.seconds, args.message)
            
        elif args.command == 'pomodoro':
            pomodoro_timer(args.work, args.break_minutes)
            
    except KeyboardInterrupt:
        print("\n👋 Program interrupted by user!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    # Check if psutil is installed for systeminfo
    try:
        import psutil
    except ImportError:
        print("❌ 'psutil' package required for system info. Install with: pip install psutil")
        exit(1)
    
    main()
