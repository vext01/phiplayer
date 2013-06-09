import subprocess, sys, re, os
import urwid
import broadcast

GET_IPLAYER="get_iplayer"
class PhiPlayerError(Exception): pass

def item_chosen(button, udata):
    stream(udata.pid)

# XXX make menu items prettier
def mk_menu(title, items):
    body = [urwid.Text(title), urwid.Divider()]

    for item in items:
        item_str = str(item)
        button = urwid.Button(item_str)
        urwid.connect_signal(button, 'click', item_chosen, item)
        button._w = urwid.AttrMap(urwid.SelectableIcon(item_str, 1),
                None, focus_map='reversed')
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

# XXX asumes mplayer for now
def stream(pid):
    #raise urwid.ExitMainLoop
    screen.stop()
    os.system("%s --stream --player='mplayer -' %s" % (GET_IPLAYER, pid))
    screen.start()

def get_broadcast_list():
    pipe = subprocess.Popen(GET_IPLAYER,
            shell=True, stdout=subprocess.PIPE).stdout

    bcasts = []
    for line in pipe:
        if not re.match("^[0-9]*:", line): continue
        bcasts.append(broadcast.Broadcast.from_line(line))

    pipe.close()
    return bcasts

def broadcast_menu_str(bcast):
    cats = ", ".join(bcast.categs)
    return "%s: %s - %s. %s" % \
            (bcast.pid, bcast.title, bcast.descr, cats)

if __name__ == "__main__":
    bcasts = get_broadcast_list()

    if not bcasts: raise PhiPlayerError("Could not find any broadcasts")

    # build a simple menu
    main = urwid.Padding(mk_menu("Broadcasts", bcasts), left=0, right=0)

    # build the toplevel ui
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 100),
            valign='middle', height=('relative', 100))

    # let's go
    screen = urwid.raw_display.Screen()
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')], screen=screen).run()
