import urwid

def item_chosen(button, choice):
    print("Chose: %s" % choice)


def mk_menu(title, items):
    body = [urwid.Text(title), urwid.Divider()]

    for c in items:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

if __name__ == "__main__":
    items = [ "test%s" % str(x) for x in range(10) ]
    main = urwid.Padding(mk_menu("THIS IS A TEST", items), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
