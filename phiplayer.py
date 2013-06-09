import subprocess, sys, re
import urwid
import broadcast

GET_IPLAYER="get_iplayer"
class PhiPlayerError(Exception): pass

def item_chosen(button, choice):
    print("Chose: %s" % choice)


def mk_menu(title, items):
    body = [urwid.Text(title), urwid.Divider()]

    for c in items:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def get_broadcast_list():
    pipe = subprocess.Popen(GET_IPLAYER,
            shell=True, stdout=subprocess.PIPE).stdout

    """
    for line in pipe:
        if line.strip() == "Matches:": break
    else:
        raise PhiPlayerError("Couldn't find matches marker")
    """

    bcasts = []
    for line in pipe:
        if not re.match("^[0-9]*:", line): continue
        bcasts.append(broadcast.Broadcast.from_line(line))

    for i in bcasts:
        print(i)

if __name__ == "__main__":
    get_broadcast_list()


    """
    items = [ "test%s" % str(x) for x in range(10) ]
    main = urwid.Padding(mk_menu("THIS IS A TEST", items), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
    """
