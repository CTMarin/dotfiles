from typing import List  # noqa: F401

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import battery


import os
import re
import subprocess
import psutil
import time

mod = "mod4"
terminal = "kitty"

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(),
        desc="Move window focus to other window"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "p", lazy.spawn("rofi -show run"), desc="Launch rofi"),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),

    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),
    
    # Screenshots
    Key([mod], "s", lazy.spawn("maim -s -u /home/carlos/screenshots/" + str(round(time.time() * 1000)) + "sc.png"), desc="Screenshot of a selection"),

    # Audio Control (Pulseaudio)
    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness Control (Brightnessctl)
    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),


]

groups = [Group(i) for i in [
    "   ", "   ", "   ","   ", "   ",
]]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        # Switch to workspace N
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        # Send window to workspace N
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

layout_conf = {
    'margin': 10,
    'border_width': 1,
    #'border_focus': '#eb64fa'
    'border_focus': '#3B7294'
}

layouts = [
    # layout.Columns(border_focus_stack='#d75f5f'),
    layout.MonadTall(**layout_conf),
    layout.Max(**layout_conf),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]


# --------------- Widgets ---------------
widget_defaults = dict(
    font='Mononoki Nerd Font Bold',
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

bar_config = {
    'background': '#141414',
    'margin': 10,
    'opacity': 1
}


def separator():
    return widget.Sep(linewidth=0, padding=0)

def icon(fontsize=16, text="?"):
    return widget.TextBox(
        fonstsize=fontsize,
        text=text,
        padding=3
    )

def powerline():
    return widget.TextBox(
        text="",
        fontsize=37,
        padding=-2
    )


def workspaces(): 
    return [
        separator(),
        widget.GroupBox(
            font='Mononoki Nerd Font',
            fontsize=16,
            margin_y=3,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=1,
            #background=['C71414'],
            rounded=False,
            highlight_method='line',
            highlight_color=['111111'],
            block_highlight_text_color=['1482C7'],
            urgent_alert_method='block',
            disable_drag=True
        ),
        separator(),
        widget.WindowName(fontsize=14, padding=10, max_chars=25),
        separator()
    ]

colors = [  ['#eb64fa'], # 0: first widget
            ['#cb07e0'], # 1: second widget
            ['#9f05b0'], # 2: third widget
            ['#711d7a'], # 3: fourth widget
            ['#5e0369'], # 4: fifth widget
            ['#111111'], # 5: bar background
            ['#ffffff']] # 6: font color

colors2 = [ ['#1482C7'], # 0: first widget
            ['#3B7294'], # 1: second widget
            ['#01FAD5'], # 2: third widget
            ['#FB5A3F'], # 3: fourth widget
            ['#C71414'], # 4: fifth widget
            ['#111111'], # 5: bar background
            ['#111111']] # 6: font color

widgets = [
            
        ]

screens = [
    Screen(
        top=bar.Bar(
            [
                *workspaces(),

                # CPU
                widget.TextBox(
                        text = "",
                        background = colors2[5],
                        foreground = colors2[0],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.CPU(
                        format = " {freq_current}GHz {load_percent}% ",
                        foreground = colors2[6],
                        background = colors2[0],
                        ),
                
                # Battery
                widget.TextBox(
                    text = '',
                        background = colors2[0],
                        foreground = colors2[1],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.Battery(
                        charge_char = "",
                        discharge_char = "",
                        empty_char = "",
                        full_char = "",
                        format = "{char} {percent:2.0%} {hour:d}:{min:02d}",
                        update_interval = 2,
                        foreground = colors2[6],
                        background = colors2[1],
                        padding = 5
                        ),
                
                # Date and Clock
                widget.TextBox(
                        text = "",
                        background = colors2[1],
                        foreground = colors2[2],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.Clock(
                        foreground = colors2[6],
                        background = colors2[2],
                        format = "%d/%m/%Y - %H:%M "
                        ), 

                # Volume and brightness
                widget.TextBox(
                        text = '',
                        background = colors2[2],
                        foreground = colors2[3],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.TextBox(
                        text = '墳',
                        background = colors2[3],
                        foreground = colors2[6],
                        ),
                widget.PulseVolume(
                        limit_max_volume = True,
                        step = 1,
                        foreground = colors2[6],
                        background = colors2[3],
                        padding = 5
                        ),
                
                # Shutdown
                widget.TextBox(
                        text = "",
                        background = colors2[3],
                        foreground = colors2[4],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.QuickExit(
                        default_text = "襤 Shutdown ",
                        countdown_format = "    羽 {}    ",
                        foreground = colors2[6], 
                        background = colors2[4]
                        ) 
            ],
            25, **bar_config
        ),
    ),
    
    Screen(
        top=bar.Bar(
            [
                *workspaces(),

                # CPU
                widget.TextBox(
                        text = "",
                        background = colors[5],
                        foreground = colors[0],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.CPU(
                        format = " {freq_current}GHz {load_percent}% ",
                        foreground = colors[6],
                        background = colors[0],
                        ),
                
                # Battery
                widget.TextBox(
                    text = '',
                        background = colors[0],
                        foreground = colors[1],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.Battery(
                        charge_char = "",
                        discharge_char = "",
                        empty_char = "",
                        full_char = "",
                        format = "{char} {percent:2.0%} {hour:d}:{min:02d}",
                        update_interval = 2,
                        foreground = colors[6],
                        background = colors[1],
                        padding = 5
                        ),
                
                # Date and Clock
                widget.TextBox(
                        text = "",
                        background = colors[1],
                        foreground = colors[2],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.Clock(
                        foreground = colors[6],
                        background = colors[2],
                        format = "%d/%m/%Y - %H:%M "
                        ), 

                # Volume and brightness
                widget.TextBox(
                        text = '',
                        background = colors[2],
                        foreground = colors[3],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.TextBox(
                        text = '墳',
                        background = colors[3],
                        foreground = colors[6],
                        ),
                widget.PulseVolume(
                        limit_max_volume = True,
                        step = 1,
                        foreground = colors[6],
                        background = colors[3],
                        padding = 5
                        ),
                
                # Shutdown
                widget.TextBox(
                        text = "",
                        background = colors[3],
                        foreground = colors[4],
                        padding = -4,
                        fontsize = 37
                        ),
                widget.QuickExit(
                        default_text = "襤 Shutdown ",
                        countdown_format = "    羽 {}    ",
                        foreground = colors[6], 
                        background = colors[4]
                        ) 
            ],
            25, **bar_config
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

@hook.subscribe.startup_once
def autostart():
    processes = [
        ['nitrogen', '--head=0', '--set-zoom-fill', '--random'],
        ['nitrogen', '--head=1', '--set-zoom-fill', '--random'],
        ['picom']
    ]

    for p in processes:
        subprocess.Popen(p)
    #home = os.path.expanduser('~')
    #subprocess.Popen([home + '/.config/qtile/autostart.sh'])


# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"





