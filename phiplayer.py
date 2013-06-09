import subprocess, sys, re
import urwid
import broadcast

GET_IPLAYER="get_iplayer"
class PhiPlayerError(Exception): pass

def item_chosen(button):
    print(button.label)

# XXX make menu items prettier
def mk_menu(title, items):
    body = [urwid.Text(title), urwid.Divider()]

    for c in items:
        button = urwid.Button(c, on_press=item_chosen)
        button._w = urwid.AttrMap(urwid.SelectableIcon(c, 1),
                None, focus_map='reversed')
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

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
    items = [ broadcast_menu_str(x) for x in bcasts ]
    main = urwid.Padding(mk_menu("Broadcasts", items), left=0, right=0)

    # build the toplevel ui
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 100),
            valign='middle', height=('relative', 100))

    # let's go
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
