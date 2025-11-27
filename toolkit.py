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
# TERMINAL STYLING
# ================================
from colorama import Fore, Style, init
init(autoreset=True)

def user_input(prompt):
    """Prompt input user dengan warna hijau"""
    return input(f"{Fore.GREEN}{prompt}{Style.RESET_ALL}")

def bot_thinking(message):
    """Pesan proses / thinking dengan warna kuning"""
    print(f"{Fore.YELLOW}{message}{Style.RESET_ALL}")

def bot_output(message):
    """Output agent dengan warna cyan"""
    print(f"{Fore.CYAN}{message}{Style.RESET_ALL}")

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
    
    bot_output(f"📁 Organizing files in: {path.absolute()}")
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
                    
                    bot_thinking(f"Moving {file_path.name} → {folder}/")
                    shutil.move(str(file_path), str(target_dir / new_name))
                    organized_count += 1
                    moved = True
                    break
            
            if not moved:
                other_dir = path / "Others"
                other_dir.mkdir(exist_ok=True)
                bot_thinking(f"Moving {file_path.name} → Others/")
                shutil.move(str(file_path), str(other_dir / file_path.name))
                organized_count += 1
    
    print("=" * 50)
    bot_output(f"🎉 Organization complete! Moved {organized_count} files.")

# ================================
# SYSTEM INFO CHECKER
# ================================
def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f} {unit}{suffix}"
        bytes /= factor

def system_info():
    bot_output("🖥️  SYSTEM INFORMATION")
    print("=" * 60)
    
    # System Information
    print("\n💻 SYSTEM")
    bot_output(f"  OS: {platform.system()} {platform.release()}")
    bot_output(f"  Version: {platform.version()}")
    bot_output(f"  Architecture: {platform.architecture()[0]}")
    bot_output(f"  Hostname: {socket.gethostname()}")
    
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        bot_output(f"  Local IP: {local_ip}")
    except:
        bot_output("  Local IP: Unable to determine")
    
    # Boot Time
    boot_time = psutil.boot_time()
    bt = datetime.datetime.fromtimestamp(boot_time)
    bot_output(f"  Boot Time: {bt.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # CPU Information
    print("\n⚡ CPU")
    bot_output(f"  Processor: {platform.processor() or 'Unknown'}")
    bot_output(f"  Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical")
    bot_output(f"  Usage: {psutil.cpu_percent(interval=1)}%")
    
    # Memory Information
    print("\n🧠 MEMORY")
    mem = psutil.virtual_memory()
    bot_output(f"  Total: {get_size(mem.total)}")
    bot_output(f"  Used: {get_size(mem.used)} ({mem.percent}%)")
    bot_output(f"  Available: {get_size(mem.available)}")
    
    # Disk Information
    print("\n💾 DISK")
    partitions = psutil.disk_partitions()
    for partition in partitions[:3]:
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            bot_output(f"  {partition.device} ({partition.mountpoint})")
            bot_output(f"    Total: {get_size(usage.total)}")
            bot_output(f"    Used: {get_size(usage.used)} ({usage.percent}%)")
            bot_output(f"    Free: {get_size(usage.free)}")
        except (PermissionError, FileNotFoundError):
            continue
    
    # Network Information
    print("\n🌐 NETWORK")
    net_io = psutil.net_io_counters()
    bot_output(f"  Bytes Sent: {get_size(net_io.bytes_sent)}")
    bot_output(f"  Bytes Received: {get_size(net_io.bytes_recv)}")
    
    # Current User
    print("\n👤 USER")
    try:
        bot_output(f"  Username: {os.getlogin()}")
    except:
        bot_output("  Username: Unknown")
    bot_output(f"  Current Directory: {os.getcwd()}")

# ================================
# COUNTDOWN TIMER
# ================================
def beep():
    print('\a', end='', flush=True)

def clear_line():
    print('\r' + ' ' * 50, end='\r', flush=True)

def countdown_timer(seconds, message="Time's up!"):
    try:
        seconds = int(seconds)
        if seconds <= 0:
            bot_output("❌ Please enter a positive number of seconds")
            return
        
        original_seconds = seconds
        bot_output(f"⏰ Countdown: {seconds} seconds")
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
                
                bot_thinking(f"⏳ {time_format} [{bar}] {progress*100:.1f}%")
                time.sleep(1)
                seconds -= 1
                
            except KeyboardInterrupt:
                clear_line()
                bot_output("⏹️  Timer stopped by user")
                return
        
        clear_line()
        bot_output(f"🎉 {message}")
        
        for _ in range(3):
            beep()
            time.sleep(0.5)
            
    except ValueError:
        bot_output("❌ Please enter a valid number of seconds")

def pomodoro_timer(work_minutes=25, break_minutes=5):
    cycles = 0
    try:
        while True:
            cycles += 1
            print(f"\n🍅 Pomodoro Cycle {cycles}")
            print("=" * 30)
            
            bot_output(f"💻 Work session: {work_minutes} minutes")
            countdown_timer(work_minutes * 60, "Work session complete! Time for a break.")
            
            bot_output(f"\n☕ Break session: {break_minutes} minutes")
            countdown_timer(break_minutes * 60, "Break over! Back to work.")
            
            choice = user_input("\nContinue? (y/n): ").lower()
            if choice != 'y':
                bot_output("👋 Pomodoro session ended!")
                break
                
    except KeyboardInterrupt:
        bot_output("\n👋 Pomodoro session interrupted!")

# ================================
# MAIN PROGRAM
# ================================
def main():
    parser = argparse.ArgumentParser(description='Multi-Tool Terminal Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # File Organizer
    org_parser = subparsers.add_parser('organize', help='Organize files by type')
    org_parser.add_argument('directory', nargs='?', default='.', help='Directory to organize (default: current)')
    
    # System Info
    subparsers.add_parser('systeminfo', help='Display system information')
    
    # Timer
    timer_parser = subparsers.add_parser('timer', help='Start a countdown timer')
    timer_parser.add_argument('seconds', type=int)
    timer_parser.add_argument('--message', '-m', default="Time's up!")
    
    # Pomodoro
    pomodoro_parser = subparsers.add_parser('pomodoro', help='Start Pomodoro timer')
    pomodoro_parser.add_argument('--work', '-w', type=int, default=25)
    pomodoro_parser.add_argument('--break', '-b', type=int, default=5, dest='break_minutes')
    
    args = parser.parse_args()
    
    if not args.command:
        bot_output(parser.format_help())
        return
    
    try:
        if args.command == 'organize':
            if not Path(args.directory).exists():
                bot_output(f"❌ Error: Directory '{args.directory}' not found!")
            else:
                organize_files(args.directory)
                
        elif args.command == 'systeminfo':
            system_info()
            
        elif args.command == 'timer':
            countdown_timer(args.seconds, args.message)
            
        elif args.command == 'pomodoro':
            pomodoro_timer(args.work, args.break_minutes)
            
    except KeyboardInterrupt:
        bot_output("👋 Program interrupted by user!")
    except Exception as e:
        bot_output(f"❌ Error: {e}")

if __name__ == "__main__":
    try:
        import psutil
    except ImportError:
        bot_output("❌ 'psutil' package required for system info. Install with: pip install psutil")
        exit(1)
    
    main()
