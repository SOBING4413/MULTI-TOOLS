"""
MULTI TOOL By.Sobing4413 (Python) v1.0
All-in-one utility to simplify your digital life

How to run:
    Double-click RUN.bat
    or
    python multitool.py
"""

import sys
import time
import random
import datetime

try:
    from colorama import Fore, Style
except ImportError:
    print("[!] Dependencies not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import psutil
except ImportError:
    print("[!] psutil not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

# Import utils
from utils.ui import (
    clear_screen, get_color, get_accent, get_input, print_error, SETTINGS, THEME_COLORS,
    print_header, print_success, pause, print_menu_category, print_menu_item,
    print_menu_end, print_box, print_fancy_box, BOX, UI_WIDTH,
    splash_screen, print_system_status_bar, get_greeting, get_random_tip,
    type_text, animate_line, print_gradient_text, loading_spinner,
    print_divider, print_info,
)
from utils.helpers import is_admin

# Import language module
from utils.language import (
    lang, set_language, get_current_language, get_current_language_name,
    get_available_languages, get_tips, get_greeting_text, LANGUAGES,
)

# Import modules - Power
from modules.power import shutdown_timer, restart_timer, cancel_schedule, lock_pc, sleep_timer

# Import modules - System Info
from modules.sysinfo import (
    system_info, disk_space, battery_status, check_uptime, realtime_monitor,
    gpu_info, user_info_detail, hardware_summary,
)

# Import modules - Network
from modules.network import (
    check_ip, ip_real_detail, traceroute, flush_dns, ping_test,
    network_info, wifi_toggle, wifi_passwords, speed_test, dns_lookup,
)

# Import modules - Cleanup
from modules.cleanup import clean_temp, clean_recycle_bin, disk_benchmark

# Import modules - Processes
from modules.processes import running_programs, kill_process, startup_manager

# Import modules - Security
from modules.security import (
    check_firewall, check_open_ports, check_antivirus, suspicious_connections,
    check_user_accounts, privacy_cleaner, security_overview,
)

# Import modules - Shortcuts
from modules.shortcuts import app_launcher, take_screenshot, quick_settings, system_shortcuts

# ============================================================
# INFO
# ============================================================
VERSION = "v1.0"
AUTHOR = "Sobing4413"
GITHUB_URL = "https://github.com/Sobing4413"
DISCORD_URL = "https://discord.gg/9nsub2yx4V"


def change_language():
    """Change the application language."""
    print_header("  " + lang("menu_language"))

    languages = get_available_languages()
    c = get_color()
    a = get_accent()

    print(f"  {a}  {lang('select_language')}:{Style.RESET_ALL}")
    print()

    lang_list = list(languages.items())
    for i, (code, info) in enumerate(lang_list, 1):
        flag = info["flag"]
        native = info["native"]
        name = info["name"]
        marker = ""
        if code == get_current_language():
            marker = f" {Fore.LIGHTYELLOW_EX}<< active{Style.RESET_ALL}"
        print(f"    {c}  [{i:>2}] {flag} {native} ({name}){marker}{Style.RESET_ALL}")

    print()
    current_name = get_current_language_name()
    print(f"  {c}  {lang('current_language')}: {Fore.LIGHTYELLOW_EX}{current_name}{Style.RESET_ALL}")
    print()

    choice = get_input(f"{lang('select_menu')} [1-{len(lang_list)}]: ")

    try:
        idx = int(choice) - 1
        if 0 <= idx < len(lang_list):
            code = lang_list[idx][0]
            set_language(code)
            print()
            print_success(f"{lang('language_changed')} {get_current_language_name()}")
        else:
            print_error(lang("invalid_choice"))
    except ValueError:
        print_error(lang("invalid_choice"))

    pause()


def settings_menu():
    """Change color theme and animation settings."""
    print_header("  " + lang("menu_settings"))

    themes = [
        ("1", "green", "Green (Default - Hacker Style)"),
        ("2", "cyan", "Cyan (Cool Blue)"),
        ("3", "yellow", "Yellow (Warning Style)"),
        ("4", "red", "Red (Red Alert)"),
        ("5", "magenta", "Magenta (Purple)"),
        ("6", "white", "White (Classic)"),
    ]

    c = get_color()
    a = get_accent()
    print(f"  {a}  Select Theme Color:{Style.RESET_ALL}")
    print()
    for num, theme_key, desc in themes:
        color = THEME_COLORS.get(theme_key, Fore.WHITE)
        marker = ""
        if SETTINGS["theme"] == theme_key:
            marker = f" {Fore.LIGHTYELLOW_EX}<< active{Style.RESET_ALL}"
        print(f"    {color}  [{num}] {desc}{marker}{Style.RESET_ALL}")

    print()
    print(f"  {c}  Current theme: {Fore.LIGHTYELLOW_EX}{SETTINGS['theme']}{Style.RESET_ALL}")
    print()

    # Toggle animations
    anim_on = SETTINGS.get("animations", True)
    anim_status = "ON" if anim_on else "OFF"
    print(f"    {c}  [7] Toggle Animation ({anim_status}){Style.RESET_ALL}")
    print()

    choice = get_input("Select [1-7]: ")

    if choice == "7":
        SETTINGS["animations"] = not SETTINGS.get("animations", True)
        status = "ON" if SETTINGS["animations"] else "OFF"
        print()
        print_success(f"Animation: {status}")
    else:
        for num, theme_name, _ in themes:
            if choice == num:
                SETTINGS["theme"] = theme_name
                print()
                print_success(f"Theme changed to: {theme_name}")
                break
        else:
            print_error(lang("invalid_choice"))

    pause()


def _print_main_header():
    """Print the professional main menu header."""
    c = get_color()
    a = get_accent()
    dim = Style.DIM
    w = UI_WIDTH
    h = BOX['h']
    v = BOX['v']
    tl = BOX['tl']
    tr = BOX['tr']
    bl = BOX['bl']
    br = BOX['br']
    lt = BOX['lt']
    rt = BOX['rt']

    # Status bar
    print_system_status_bar()
    print()

    # Top border
    print(f"  {c}{tl}{h * w}{tr}{Style.RESET_ALL}")

    # ASCII Art Header
    if pyfiglet:
        ascii_art = pyfiglet.figlet_format("MultiTool", font="slant")
        art_lines = [line for line in ascii_art.split("\n") if line.strip()]
        for line in art_lines:
            if len(line) > w - 2:
                line = line[:w - 2]
            pad_l = (w - len(line)) // 2
            pad_r = w - len(line) - pad_l
            print(f"  {c}{v}{' ' * pad_l}{a}{line}{c}{' ' * pad_r}{v}{Style.RESET_ALL}")
    else:
        title_text = f"MULTI TOOL By.{AUTHOR} {VERSION}"
        pad_l = (w - len(title_text)) // 2
        pad_r = w - len(title_text) - pad_l
        print(f"  {c}{v}{' ' * pad_l}{a}{title_text}{c}{' ' * pad_r}{v}{Style.RESET_ALL}")

    # Separator
    print(f"  {c}{lt}{h * w}{rt}{Style.RESET_ALL}")

    # Greeting and description
    greeting = get_greeting_text()
    welcome_text = lang("welcome")
    greeting_line = f"  {greeting}! {welcome_text}"
    g_pad = w - len(greeting_line) - 2
    print(f"  {c}{v} {a}{greeting_line}{c}{' ' * max(0, g_pad)} {v}{Style.RESET_ALL}")

    desc_text = lang("description")
    d_pad = w - len(desc_text) - 4
    print(f"  {c}{v}  {dim}{desc_text}{Style.RESET_ALL}{c}{' ' * max(0, d_pad)}  {v}{Style.RESET_ALL}")

    # Status
    if is_admin():
        status_label = lang("status_admin")
        status_color = Fore.GREEN
        status_icon = "ADMIN"
    else:
        status_label = lang("status_user")
        status_color = Fore.YELLOW
        status_icon = "USER"

    status_line = f"  {lang('status')}: {status_label}"
    s_pad = w - len(status_line) - 4
    print(f"  {c}{v}  {status_color}{status_line}{c}{' ' * max(0, s_pad)}  {v}{Style.RESET_ALL}")

    # Language indicator
    lang_name = get_current_language_name()
    lang_line = f"  Language: {lang_name}"
    l_pad = w - len(lang_line) - 4
    print(f"  {c}{v}  {Fore.CYAN}{lang_line}{c}{' ' * max(0, l_pad)}  {v}{Style.RESET_ALL}")

    # Credits separator
    print(f"  {c}{lt}{h * w}{rt}{Style.RESET_ALL}")

    # Credits
    credit_text = f"By {AUTHOR} | {VERSION}"
    cr_pad_l = (w - len(credit_text)) // 2
    cr_pad_r = w - len(credit_text) - cr_pad_l
    print(f"  {c}{v}{' ' * cr_pad_l}{a}{credit_text}{c}{' ' * cr_pad_r}{v}{Style.RESET_ALL}")

    github_text = f"GitHub  : {GITHUB_URL}"
    gh_pad = w - len(github_text) - 4
    print(f"  {c}{v}  {dim}{a}{github_text}{Style.RESET_ALL}{c}{' ' * max(0, gh_pad)}  {v}{Style.RESET_ALL}")

    discord_text = f"Discord : {DISCORD_URL}"
    dc_pad = w - len(discord_text) - 4
    print(f"  {c}{v}  {dim}{a}{discord_text}{Style.RESET_ALL}{c}{' ' * max(0, dc_pad)}  {v}{Style.RESET_ALL}")

    # Bottom border
    print(f"  {c}{bl}{h * w}{br}{Style.RESET_ALL}")


def _print_menu():
    """Print the main menu with translated labels."""
    c = get_color()
    a = get_accent()

    # Category 1: Power
    print_menu_category(lang("cat_power"))
    print_menu_item("1", lang("menu_shutdown"))
    print_menu_item("2", lang("menu_restart"))
    print_menu_item("3", lang("menu_cancel_schedule"))
    print_menu_item("4", lang("menu_lock"))
    print_menu_item("5", lang("menu_sleep"))
    print_menu_end()
    print()

    # Category 2: Info
    print_menu_category(lang("cat_info"))
    print_menu_item("6", lang("menu_sysinfo"))
    print_menu_item("7", lang("menu_disk"))
    print_menu_item("8", lang("menu_battery"))
    print_menu_item("9", lang("menu_uptime"))
    print_menu_item("10", lang("menu_monitor"))
    print_menu_item("11", lang("menu_gpu"))
    print_menu_item("12", lang("menu_userinfo"))
    print_menu_item("13", lang("menu_hardware"))
    print_menu_end()
    print()

    # Category 3: Network
    print_menu_category(lang("cat_network"))
    print_menu_item("14", lang("menu_checkip"))
    print_menu_item("15", lang("menu_ipdetail"))
    print_menu_item("16", lang("menu_flushdns"))
    print_menu_item("17", lang("menu_ping"))
    print_menu_item("18", lang("menu_traceroute"))
    print_menu_item("19", lang("menu_dnslookup"))
    print_menu_item("20", lang("menu_netinfo"))
    print_menu_item("21", lang("menu_wifi_toggle"))
    print_menu_item("22", lang("menu_wifi_pass"))
    print_menu_item("23", lang("menu_speedtest"))
    print_menu_end()
    print()

    # Category 4: Cleanup
    print_menu_category(lang("cat_cleanup"))
    print_menu_item("24", lang("menu_cleantemp"))
    print_menu_item("25", lang("menu_cleanbin"))
    print_menu_item("26", lang("menu_benchmark"))
    print_menu_end()
    print()

    # Category 5: Processes
    print_menu_category(lang("cat_process"))
    print_menu_item("27", lang("menu_running"))
    print_menu_item("28", lang("menu_killproc"))
    print_menu_item("29", lang("menu_startup"))
    print_menu_end()
    print()

    # Category 6: Security
    print_menu_category(lang("cat_security"))
    print_menu_item("30", lang("menu_secoverview"))
    print_menu_item("31", lang("menu_firewall"))
    print_menu_item("32", lang("menu_ports"))
    print_menu_item("33", lang("menu_antivirus"))
    print_menu_item("34", lang("menu_suspicious"))
    print_menu_item("35", lang("menu_useraccount"))
    print_menu_item("36", lang("menu_privacy"))
    print_menu_end()
    print()

    # Category 7: Shortcuts
    print_menu_category(lang("cat_shortcuts"))
    print_menu_item("37", lang("menu_applauncher"))
    print_menu_item("38", lang("menu_screenshot"))
    print_menu_item("39", lang("menu_quicksettings"))
    print_menu_item("40", lang("menu_sysshortcuts"))
    print_menu_end()
    print()

    # Category 8: Other
    print_menu_category(lang("cat_other"))
    print_menu_item("41", lang("menu_settings"))
    print_menu_item("42", lang("menu_language"))
    print_menu_item("0", lang("menu_exit"))
    print_menu_end()
    print()


def _print_tip():
    """Print a random translated tip."""
    tips = get_tips()
    if tips:
        tip = random.choice(tips)
        c = get_color()
        a = get_accent()
        print(f"  {a}{tip}{Style.RESET_ALL}")
        print()


def _exit_animation():
    """Show exit animation."""
    c = get_color()
    a = get_accent()
    dim = Style.DIM

    clear_screen()
    print()

    loading_spinner(lang("closing_app"), 1.0)
    print()

    # Goodbye box
    lines = [
        f"{lang('goodbye_thanks')} MultiTool!",
        f"{lang('goodbye_star')}",
        "",
        f"GitHub  : {GITHUB_URL}",
        f"Discord : {DISCORD_URL}",
        "",
        f"{lang('goodbye_see_you')} ",
    ]
    print_fancy_box(lines, title=f" MultiTool {VERSION} ")
    print()

    time.sleep(1)


def main():
    """Main entry point."""
    # Show splash screen on first run
    if SETTINGS.get("animations", True):
        splash_screen()
        time.sleep(0.5)

    # Main loop
    while True:
        clear_screen()
        print()

        _print_main_header()
        print()

        _print_menu()

        _print_tip()

        choice = get_input(f"{lang('select_menu')} [0-42]: ")

        # Menu dispatch table
        menu_actions = {
            # Power
            "1": shutdown_timer,
            "2": restart_timer,
            "3": cancel_schedule,
            "4": lock_pc,
            "5": sleep_timer,
            # Info
            "6": system_info,
            "7": disk_space,
            "8": battery_status,
            "9": check_uptime,
            "10": realtime_monitor,
            "11": gpu_info,
            "12": user_info_detail,
            "13": hardware_summary,
            # Network
            "14": check_ip,
            "15": ip_real_detail,
            "16": flush_dns,
            "17": ping_test,
            "18": traceroute,
            "19": dns_lookup,
            "20": network_info,
            "21": wifi_toggle,
            "22": wifi_passwords,
            "23": speed_test,
            # Cleanup
            "24": clean_temp,
            "25": clean_recycle_bin,
            "26": disk_benchmark,
            # Processes
            "27": running_programs,
            "28": kill_process,
            "29": startup_manager,
            # Security
            "30": security_overview,
            "31": check_firewall,
            "32": check_open_ports,
            "33": check_antivirus,
            "34": suspicious_connections,
            "35": check_user_accounts,
            "36": privacy_cleaner,
            # Shortcuts
            "37": app_launcher,
            "38": take_screenshot,
            "39": quick_settings,
            "40": system_shortcuts,
            # Other
            "41": settings_menu,
            "42": change_language,
        }

        if choice == "0":
            _exit_animation()
            break
        elif choice in menu_actions:
            try:
                menu_actions[choice]()
            except KeyboardInterrupt:
                print()
                print_info("Operation cancelled.")
                pause()
            except Exception as e:
                print()
                print_error(f"Error: {e}")
                pause()
        else:
            print_error(lang("invalid_choice"))
            pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print(f"\n  {Fore.YELLOW}{lang('stopped_by_user')}{Style.RESET_ALL}")
        print()