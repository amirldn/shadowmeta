import wx
import os
import time
import datetime

# Constants
default_path = "D:\Videos\Shadowplay"

class wxbutton(wx.Frame):

    def __init__(self, *args, **kw):
        super(wxbutton, self).__init__(*args, **kw)

        self.InitUI()

    def InitUI(self):

        pnl = wx.Panel(self)
        rename_button = wx.Button(pnl, label='Rename', pos=(20, 20))
        trim_button = wx.Button(pnl, label='Trim', pos=(20, 40))
        delete_button = wx.Button(pnl, label='Delete', pos=(20, 60))
        quit_button = wx.Button(pnl, label='Quit', pos=(20, 100))

        quit_button.Bind(wx.EVT_BUTTON, self.OnClose)

        self.SetSize((350, 250))
        self.SetTitle('shadowmeta')
        self.Centre()

    def OnClose(self, e):

        self.Close(True)


def main():
    # maybe dont use this way of doing it ------------
    # #when WMI gives the call that a game has opened
    # game_open_time = datetime.datetime.now()
    # print(game_open_time)

    # Better way?
    # Monitor shadowplay directory for changes

    shadowplay_folder_path = input("Shadowplay Path: ")
    print(default_path)
    if shadowplay_folder_path == '':
        shadowplay_folder_path = default_path
    before = dict([(f, None) for f in os.listdir(shadowplay_folder_path)])
    while 1:
        print("loop")
        time.sleep(2)
        after = dict([(f, None) for f in os.listdir(shadowplay_folder_path)])
        added = [f for f in after if not f in before]
        removed = [f for f in before if not f in after]
        if added: print
        "Added: ", ", ".join(added)
        if removed: print
        "Removed: ", ", ".join(removed)
        before = after

    app = wx.App()
    ex = wxbutton(None)
    ex.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()





# when game opens, note the time
# when fullscreen app closes, list all files in shadowplay directory that was created after game open time
# display a box with all the shadowplays made for that session
# lets you either play in VLC or rename
# display a box that has the name of the file and lets you rename it
