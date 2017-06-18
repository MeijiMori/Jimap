#!
# -*- coding: utf-8 -*-

import urllib2
import os
import glob
import math
import re
import csv

from Tkinter import *
import ttk
from ScrolledText import *
from PIL import Image, ImageTk
import tkFont

from convert_postion import convert_longlati_topixcel, convert_pixcel_tolonglati
from get_position_info import get_place_candidate

# Variables
# data_dir
DATA_DIR = "./jimapn_data"

# Functions
# Make Data directory
def make_data_dir():
    if not(os.path.exists(DATA_DIR)):
        # make data dir
        os.makedirs(DATA_DIR)

    # level map dir
    for i in xrange(Jimapn.MIN_ZOOM_LEVEL, Jimapn.MAX_ZOOM_LEVEL + 1):
        level_map_dir = DATA_DIR + "/map_tile/" + str(i)
        if not(os.path.exists(level_map_dir)):
                # make zoom dir
                os.mkdir(level_map_dir)


# edit window
class edit_window():

    def __init__(self, parent, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        frame = Toplevel(parent)
        frame.title("場所の編集:{0},{1}".format(latitude, longitude))

        first_line = Frame(frame)
        first_line.grid(row=0, column=0)
        la_mean = Label(first_line)
        la_mean.configure(
                text=u"緯度",
                )
        la_mean.grid(row=0, column=0)
        la_text = Entry(first_line)
        self.lat = StringVar()
        la_text.configure(
                textvariable=self.lat,
                )
        la_text.grid(row=1, column=0)
        lo_mean = Label(first_line)
        lo_mean.configure(
                text=u"経度",
                )
        lo_mean.grid(row=0, column=1)
        lo_text = Entry(first_line)
        self.lon = StringVar()
        lo_text.configure(
                textvariable=self.lon,
                )
        lo_text.grid(row=1, column=1)

        second_line = Frame(frame)
        second_line.grid(row=1, column=0)
        pnk_mean = Label(second_line)
        pnk_mean.configure(
                text=u"よみ",
                )
        pnk_mean.grid(row=0, column=0)
        self.pnk = StringVar()
        place_name_kana = Entry(second_line)
        place_name_kana.configure(
                textvariable=self.pnk
                )
        place_name_kana.grid(row=1, column=0)
        pn_mean = Label(second_line)
        pn_mean.configure(
                text=u"場所名",
                )
        pn_mean.grid(row=2, column=0)
        self.pn = StringVar()
        place_name = Entry(second_line)
        place_name.configure(
                textvariable=self.pn
                )
        place_name.grid(row=3, column=0)

        third_line = Frame(frame)
        third_line.grid(row=2, column=0)
        layer_mean = Label(third_line)
        layer_mean.configure(
                text=u"レイヤー",
                )
        layer_mean.grid(row=0, column=0)
        self.layer_selecter = ttk.Combobox(third_line)
        self.layer_selecter.configure(
                values=("default"),
                )
        self.layer_selecter.grid(row=1, column=0)
        kind_mean = Label(third_line)
        kind_mean.configure(
                text=u"種類",
                )
        kind_mean.grid(row=0, column=1)
        self.kind_selecter = ttk.Combobox(third_line)
        self.kind_selecter.configure(
                values=("default"),
                )
        self.kind_selecter.grid(row=1, column=1)

        fourth_line = Frame(frame)
        fourth_line.grid(row=3, column=0)
        self.memo = Text(fourth_line)
        self.memo.configure(
                height=8,
                width=50,
                )
        self.memo.grid(row=0, column=0)

        fifth_line = Frame(frame)
        fifth_line.grid(row=4, column=0)
        ok_button = Button(fifth_line)
        ok_button.configure(
                text="OK",
                command=self.recode_place
                )
        ok_button.grid(row=0, column=0)
        cancel_button = Button(fifth_line)
        cancel_button.configure(
                text=u"CANCEL",
                )
        cancel_button.grid(row=0, column=1)

    def show(self, event):
        pass

    def get_place_info(self):
        pass

    def setter(self):
        self.lat.set(self.latitude)
        self.lon.set(self.longitude)

    def save_place(self):
        place_name = self.pn.get().encode('utf-8')
        place_name_kana = self.pnk.get().encode('utf-8')
        layer = self.layer_selecter.get()
        kind = self.kind_selecter.get()
        latitude = self.lat.get()
        longitude = self.lon.get()
        memo = self.memo.get('1.0 linestart', 'end').encode('utf-8')

        recode_dir = DATA_DIR + "/" + "place_data" + "/" + str(layer) + "/" + str(kind)
        if not(os.path.exists(recode_dir)):
            os.makedirs(recode_dir)
        recode_file = recode_dir + "/" + "recode_file.csv"
        with open(recode_file, "ab") as csv_file:
            csv_file.seek(os.SEEK_END)
            writer = csv.writer(csv_file)
            writer.writerow([place_name, place_name_kana, layer,
                kind, latitude, longitude, memo])

    def load_place(self, latitude, longitude):
        recode_dir = DATA_DIR + "/" + "place_data" + "/" + str(layer) + "/" + str(kind)
        if not(os.path.exists(recode_dir)):
            os.makedirs(recode_dir)
        recode_file = recode_dir + "/" + "recode_file.csv"
        with open(recode_file, "ab") as csv_file:
            csv_file.seek(os.SEEK_END)
            writer = csv.writer(csv_file)
            writer.writerow([place_name, place_name_kana, layer,
                kind, latitude, longitude, memo])

        place_name = self.pn.get().encode('utf-8')
        place_name_kana = self.pnk.get().encode('utf-8')
        layer = self.layer_selecter.get()
        kind = self.kind_selecter.get()
        latitude = self.lat.get()
        longitude = self.lon.get()
        memo = self.memo.get('1.0 linestart', 'end').encode('utf-8')


# Main window
class Jimapn(Frame):

    # Max zoom level
    MAX_ZOOM_LEVEL = 18
    # Min zoom level
    MIN_ZOOM_LEVEL = 5
    # Tile size
    TILE_HEIGHT = 256
    TILE_WIDTH = 256
    # Canvas size
    CANVAS_HEIGHT = 768
    CANVAS_WIDTH = 768
    # Display canvas size
    DISPLAY_CANVAS_HEIGHT = 480
    DISPLAY_CANVAS_WIDTH = 500
    # Canvas TILE
    CANVAS_X = 5
    CANVAS_Y = 5
    CANVAS_XY = CANVAS_X * CANVAS_Y

    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.master.title("[JIMAP]")
        self.master.minsize(300, 300)
        self.master.maxsize(2000, 2000)
        self.master.geometry("1000x600")  # window size
        self.mode = "{0}".format("Select")
        self.zoom_level = Jimapn.MIN_ZOOM_LEVEL
        self.latitude = 35.43134
        self.longitude = 139.26086
        self.aaom_x = 0
        self.aaom_y = 0
        self.map_area = [[ '' for i in xrange(Jimapn.CANVAS_X)] for j in xrange(Jimapn.CANVAS_Y)]
        # self.print_map = [[ '' for i in xrange(Jimapn.CANVAS_X)] for j in xrange(Jimapn.CANVAS_Y)]
        self.cid = [[ '' for i in xrange(Jimapn.CANVAS_X)] for j in xrange(Jimapn.CANVAS_Y)]
        for i in xrange(Jimapn.CANVAS_X):
            for j in xrange(Jimapn.CANVAS_Y):
                self.map_area[i][j] = {
                        "img_file_path" : "",
                        "img_file"      : "",
                        }
        # ## Layout
        # Menu
        menubar = Menu(self)
        files = Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Files", underline=0, menu=files)
        exit = Menu(menubar, tearoff=False)
        menubar.add_cascade(label="Exit", underline=0, menu=exit)
        exit.add_command(label="Exit", underline=0, command=sys.exit)
        self.master.configure(menu=menubar)

        # # Left side
        left_side_frame = LabelFrame(self)
        left_side_frame.configure(
                labelanchor="nw",
                text="layer",
                relief="groove"
                )
        left_side_frame.grid(
                row=0, column=0,
                padx=1, pady=1,
                sticky="W"
                )
        # display my place point
        myplace_display = ScrolledText(left_side_frame)
        myplace_display.configure(
                height=4,
                width=20,
                )
        myplace_display.grid(row=0, column=0,
                padx=1, pady=5)

        # # Center
        center_frame = Frame(self)
        center_frame.configure(
                relief="raised"
                )
        center_frame.grid(row=0, column=1, sticky="W" + "E" + "N" + "S")

        # Top
        # # search place input
        self.search_place_text = StringVar()
        self.search_place = Entry(center_frame)
        self.bind_search_place()
        self.search_place.configure(
                width=50,
                relief="sunken",
                textvariable=self.search_place_text
                )
        self.search_place.grid(row=0, column=0, padx=5, pady=5)
        # search button
        self.search_button = Button(center_frame)
        self.search_button.configure(
                foreground="#3f3f3f",
                background="#cfcfcf",
                text="Search",
                cursor="arrow",
                command=self.search_place_start,
                 )
        self.search_button.grid(row=0, column=1, padx=5, pady=5)

        # Draw maps
        self.print_map = Canvas(center_frame)
        self.bind_canvas()
        self.print_map.configure(
            height=Jimapn.DISPLAY_CANVAS_HEIGHT,
            width=Jimapn.DISPLAY_CANVAS_WIDTH,
            scrollregion=("0", "0", Jimapn.CANVAS_WIDTH, Jimapn.CANVAS_HEIGHT)
            )
        self.print_map.grid(row=1, column=0, sticky="W" + "E" + "N" + "S")

        self.xscroll = Scrollbar(center_frame)
        self.xscroll.configure(
                orient="horizontal",
                background="#0f0f0f",
                activebackground="#0f0f0f",
                highlightbackground="#0f0f0f",
                troughcolor="#2f8fff",
                relief="groove",
                activerelief="flat",
                width=10,
                command=self.print_map.xview,
                )
        self.xscroll.grid(row=2, column=0, sticky="E" + "W")

        self.yscroll = Scrollbar(center_frame)
        self.yscroll.configure(
                orient="vertical",
                command=self.print_map.yview,
                )
        self.yscroll.grid(row=1, column=1, sticky='N' + 'S')

        self.print_map.config(xscrollcommand=self.xscroll.set,
                yscrollcommand=self.yscroll.set)
        center_frame.grid_rowconfigure(0, weight=1, minsize=0)
        center_frame.grid_columnconfigure(0, weight=1, minsize=0)

        # # Right side
        right_side_frame = LabelFrame(self)
        right_side_frame.configure(
                labelanchor="nw",
                text="tools",
                relief="groove"
                )
        right_side_frame.grid(row=0, column=2)

        # select button
        select_button = Button(right_side_frame)
        select_button.configure(
                foreground="#3f3f3f",
                background="#cfcfcf",
                text="➩",
                cursor="man"
                 )
        select_button.grid(row=0, column=0, padx=5, pady=5)
        # draw button
        draw_button = Button(right_side_frame)
        draw_button.configure(
                foreground="#3f3f3f",
                background="#cfcfcf",
                text="✎",
                cursor="pencil"
                 )
        draw_button.grid(row=0, column=1, padx=5, pady=5)
        # Map zoom
        zoom_in_button = Button(right_side_frame)
        zoom_in_button.configure(
            foreground="#5f5f5f",
                background="#ffffff",
                text="+",
                relief="groove",
                command=lambda : self.scale_change(1)
                )
        zoom_in_button.grid(row=10, column=0, padx=5, pady=5)

        print_zoom_level = Label(right_side_frame)
        self.zoom_level_label = StringVar()
        self.zoom_level_label.set(self.zoom_level)
        print_zoom_level.configure(
            width=2,
            textvariable=self.zoom_level_label,
            foreground="#cfcfcf",
            background="#0f0f0f",
            relief="groove"
            )
        print_zoom_level.grid(row=11, column=0, padx=5, pady=5)

        zoom_out_button = Button(right_side_frame)
        zoom_out_button.configure(
            foreground="#5f5f5f",
                background="#ffffff",
                text="-",
                relief="groove",
                command=lambda : self.scale_change(-1)
                )
        zoom_out_button.grid(row=12, column=0, padx=5, pady=5)


        # # Bottom
        bottom_frame = LabelFrame(self)
        bottom_frame.configure(
                bg="#efefef",
                labelanchor="nw",
                text="debug space",
                relief="ridge"
                )
        bottom_frame.grid(row=1, column=1, padx=10, pady=10)

        # print mode
        self.mode_print = Label(bottom_frame)
        self.mode_print.configure(
                foreground="#5f5f5f",
                background="#dfdfdf",
                height=1,
                width=10,
                relief="groove",
                text="{0}".format(self.mode)
                )
        self.mode_print.grid(row=1, column=0, padx=5, pady=5)

        # print mouse cursor postion
        self.print_xy = Label(bottom_frame)
        self.print_xy.configure(
                foreground="#5f5f5f",
                background="#dfdfdf",
                height=1,
                width=25,
                relief="groove"
                )
        self.print_xy.grid(row=1, column=1, padx=5, pady=5)

        # print log
        # # log print space
        font = tkFont.Font(family="Consolas", size=10)
        self.log_place = ScrolledText(bottom_frame)
        self.log_place.configure(
                foreground="#5f5f5f",
                background="#dfdfdf",
                selectforeground="#cfcfcf",
                selectbackground="#2f2f8f",
                height=5,
                width=50,
                relief="sunken",
                font=font,
                )
        self.log_place.grid(row=0, column=1, padx=5, pady=5)
        self.log_place.insert("end", "zoom_level : {0}\n".format(self.zoom_level))
        self.log_place.see("end")
        self.map_draw(latitude=self.latitude, longitude=self.longitude)
        self.show_place()

        # right click menu
        self.right_click_menu = Menu(self.print_map, tearoff=False)
        place_recode = Menu(self.right_click_menu)
        self.right_click_menu.add_cascade(label=u"場所", menu=place_recode, under=2)
        place_recode.add_command(label=u"この場所を登録", underline=1, command=self.recode_place)
        exit_menu = Menu(self.right_click_menu)
        self.right_click_menu.add_cascade(label=u"終了", underline=0, menu=exit_menu)
        exit_menu.add_command(label=u"終了", underline=1, command=sys.exit)
        # place_recode.add_cascade(label = "Recode place", underline = 0, menu = place_recode)


    def map_draw(self, **args):
        if "latitude" in args or "longitude" in args:
            x, y = convert_longlati_topixcel(args["latitude"], args["longitude"], self.zoom_level)
            self.offset_x = int(math.floor(x))
            self.offset_y = int(math.floor(y))
        else:
            self.offset_x = args["offset_x"]
            self.offset_y = args["offset_y"]

        tile_x, position_in_tile_x = divmod(self.offset_x, Jimapn.TILE_WIDTH)
        tile_y, position_in_tile_y = divmod(self.offset_y, Jimapn.TILE_WIDTH)

        # 必要なタイル数
        rows = Jimapn.CANVAS_HEIGHT / Jimapn.TILE_HEIGHT
        columns = Jimapn.CANVAS_WIDTH / Jimapn.TILE_WIDTH

        if position_in_tile_x != 0:
            columns += 1
        if position_in_tile_y != 0:
            rows += 1

        for i in xrange(rows):
            for j in xrange(columns):
                self.log_place.insert("end", "i : {0} / j : {1}\n".format(i, j))
                self.log_place.see("end")
                self.map_area[i][j]["img_path"] = self.set_img_path(tile_x + j, tile_y + i)
                # print "img_path : {0}".format(img_path)
                if self.map_area[i][j]["img_path"]:
                    image = Image.open(self.map_area[i][j]["img_path"])
                    self.map_area[i][j]["img_file"] = ImageTk.PhotoImage(image)
                    padding_x = j * Jimapn.TILE_WIDTH + (Jimapn.TILE_WIDTH / 2) - position_in_tile_x
                    padding_y = i * Jimapn.TILE_HEIGHT + (Jimapn.TILE_HEIGHT / 2) - position_in_tile_y

                    # padding_x = (j-1) * Jimapn.TILE_WIDTH + (Jimapn.TILE_WIDTH / 2)
                    # padding_y = (i-1) * Jimapn.TILE_HEIGHT + (Jimapn.TILE_HEIGHT / 2)
                    # self.cid[i][j] = self.print_map.create_image(padding_x, padding_y, image =
                            # self.map_area[i][j]["img_file"])
                    self.cid[i][j] = self.print_map.create_image(padding_x, padding_y, image=
                            self.map_area[i][j]["img_file"], tags="map_tile")
#                     map_tile(padding_x, padding_y, self.map_area[i][j]["img_file"])
                    self.log_place.insert("end", "Canvas id : {0} \n".format(self.cid[i][j]))
                    self.log_place.insert("end", "Canvas_row : {0:d} \n".format(rows))
                    self.log_place.insert("end", "canvas_column : {0:d}\n".format(columns))
                    self.log_place.insert("end", "map_tile-{0}-{1} : {2}\n".format(i, j,
                        self.map_area[i][j]["img_file"]))
                    self.log_place.see("end")

        # draw line that tile size
#         for i in xrange(3):
#             line_padding_x = (i + 1) * Jimapn.TILE_WIDTH
#             line_padding_y = (i + 1) * Jimapn.TILE_HEIGHT
#             self.log_place.insert("end", "line_padding_x : {0:d}\n".format(line_padding_x))
#             self.log_place.insert("end", "line_padding_y : {0:d}\n".format(line_padding_y))
#             self.log_place.see("end")
#             self.print_map.create_line(line_padding_x, 0, line_padding_x, Jimapn.CANVAS_HEIGHT)
#             self.print_map.create_line(0, line_padding_y, Jimapn.CANVAS_WIDTH, line_padding_y)

        # draw center mark
        self.print_map.create_rectangle(Jimapn.CANVAS_HEIGHT / 2 - 8,
                                        Jimapn.CANVAS_WIDTH / 2 - 8,
                                        Jimapn.CANVAS_HEIGHT / 2 + 8,
                                        Jimapn.CANVAS_WIDTH / 2 + 8,
                                        fill="#0f0f3f")
        # draw copyright
        copyright = u"©地理図院地図"
        ctx = Jimapn.DISPLAY_CANVAS_HEIGHT - 50
        cty = Jimapn.DISPLAY_CANVAS_WIDTH - 50
        self.print_map.create_text(ctx, cty, text=copyright)



    def loop_range(self):
        """ get loop range """
        start_x = 1
        start_y = 1
        if self.aaom_x % Jimapn.TILE_WIDTH == 0 or self.aaom_x == 0:
            start_x = 1
        elif self.aaom_x > 0:
            start_x = 0
        elif self.aaom_x < 0:
            start_x = 2
        if self.aaom_y % Jimapn.TILE_WIDTH == 0 or self.aaom_y == 0:
            start_y = 1
        elif self.aaom_y > 0:
            start_y = 0
        elif self.aaom_y < 0:
            start_y = 2
        end_x = start_x + 3
        end_y = start_y + 3

        return start_x, start_y, end_x, end_y

    def set_img_path(self, lat, lon):
        """ return maptile file path """
        x = lat
        y = lon
        data_id = "std"
        ext = "png"

        map_tile_file = "{0}/map_tile/{1}/{2}-{3}.{4}".format(
                DATA_DIR, self.zoom_level, x, y, ext)
        if not(os.path.exists(map_tile_file)):
            # map tile file download
            try:
                request_url = "http://cyberjapandata.gsi.go.jp/xyz/" + \
                        "{0}/{1}/{2}/{3}.{4}".format(
                        data_id, self.zoom_level,
                        x, y, ext)
                request = urllib2.urlopen(request_url)
                with open(map_tile_file, "wb") as picf:
                    picf.write(request.read())
            except urllib2.URLError:
                # Request file not exists ...
                map_tile_file = DATA_DIR + "/No_Image/No_Image.png"

        return map_tile_file


    def scale_change(self, n):
        old_level = self.zoom_level
        self.zoom_level += n
        if self.zoom_level < Jimapn.MIN_ZOOM_LEVEL:
            self.zoom_level = Jimapn.MIN_ZOOM_LEVEL
            return self.zoom_level
        elif self.zoom_level > Jimapn.MAX_ZOOM_LEVEL:
            self.zoom_level = Jimapn.MAX_ZOOM_LEVEL
            return self.zoom_level

        self.zoom_level_label.set(self.zoom_level)
        self.log_place.insert("end", "*** zoom change : {0}->{1} <{2}> ***\n".format(
            old_level, self.zoom_level, n))
        self.log_place.see("end")
        self.offset_x = int(self.offset_x * math.pow(2, n))
        self.offset_y = int(self.offset_y * math.pow(2, n))

        if n > 0:
            ajust_x = Jimapn.TILE_WIDTH
            ajust_y = Jimapn.TILE_HEIGHT
        else:
            ajust_x = -Jimapn.TILE_WIDTH
            ajust_y = -Jimapn.TILE_HEIGHT

        self.map_draw(offset_x=self.offset_x + ajust_x, offset_y=self.offset_y + ajust_y)


    def recode_place_draw(self):
        pass


    # Canvas event
    def bind_canvas(self):
        self.print_map.bind("<Motion>", self.get_canvas_postion)
        self.print_map.bind("<Button-1>", self.drag_start)
        self.print_map.bind("<ButtonRelease-1>", self.move_map)
        self.print_map.bind("<Button-3>", self.show_right_menu)


    # Search event
    def bind_search_place(self):
        self.search_place.bind("<Return>", self.call_search_place_start)


    # display candidate list event
    def bind_display_candidate(self):
        self.candidate_box.bind("<Button-1>", self.select_position)


    def select_position(self, event):
        selection = self.candidate_box.selection()
        if selection:
            item = self.candidate_box.item(selection)
            latitude = item["values"][1]
            longitude = item["values"][2]
            print "latitude : {0}".format(latitude)
            print "longitude : {0}".format(longitude)
            self.map_draw(latitude=float(latitude), longitude=float(longitude))
        # print select


    def call_search_place_start(self, event):
        self.search_place_start()


    def search_place_start(self):
        print " start search place"
        search_place_string = self.search_place_text.get()
        if search_place_string == "" :
            print "None input"
            return False
        self.log_place.insert("end", "search : {0}\n".format(search_place_string.encode('utf-8')))
        # latitude, longitude
        match = re.match(r"(\d+\.*\d*[,\s]+\d+\.*\d*)", search_place_string)
        # Zenkaku
        match2 = re.match(r"([^\x01-\x7E])", search_place_string)
        if match:
            print "search case latitude, longitude"
            position = re.split(r"([,\s])+", search_place_string)
            # self.log_place.insert("end", "search : {0}\n".format(match))
            latitude = position[0]
            longitude = position[2]
            self.log_place.see("end")
            self.map_draw(latitude=float(latitude), longitude=float(longitude))
            return True
        elif match2:
            print "search case place name"
            candidate = get_place_candidate(search_place_string)
            if candidate:
                candi_win = Toplevel(self)
                candi_win.title("Candidate List")
                candi_win.configure(
                        background="#0f0f0f",
                        highlightcolor="#2faf2f",
                        highlightbackground="#0f0faf",
                        relief="groove",
                        )
                cwf = Frame(candi_win)
                cwf.pack(fill="both", expand=1)
                style = ttk.Style()
                style.configure(
                        'Treeview',
                        width=50,
                        height=30,
                        foreground="#5f5f5f",
                        background="#ffefef",
                        highlightcolor="#2faf2f",
                        highlightbackground="#0f0faf",
                        scrollregion=("0", "0", 200, 200)
                        )
                self.candidate_box = ttk.Treeview(cwf)
                self.candidate_box.configure(
                        columns=('place_name', 'latitude', 'longitude'),
                        )
                self.cbxscroll = Scrollbar(cwf, orient="horizontal",
                        command=self.candidate_box.xview)
                self.cbyscroll = Scrollbar(cwf, orient="vertical",
                        command=self.candidate_box.yview)
                self.candidate_box.configure(
                        selectmode="browse",
                        xscroll=self.cbxscroll.set,
                        yscroll=self.cbyscroll.set,
                        )
                # self.candidate_box.pack()
                # self.cbyscroll.pack()
                self.candidate_box.grid(row=0, column=0, sticky='W' + 'E' + 'N' + 'S')
                self.cbxscroll.grid(row=1, column=0, sticky='W' + 'E')
                self.cbyscroll.grid(row=0, column=1, sticky='N' + 'S')

                self.candidate_box.column("#0", width=0)
                self.candidate_box.heading("place_name", text=u"地名")
                self.candidate_box.heading("latitude", text=u"緯度")
                self.candidate_box.heading("longitude", text=u"経度")
                for i in xrange(len(candidate)):
                    # print "place_name : {0}".format(candidate[i]["place_name"])
                    # print "latitude : {0}".format(candidate[i]["latitude"])
                    # print "longitude : {0}".format(candidate[i]["longitude"])
                    self.candidate_box.insert("", "end",
                            values=(
                                candidate[i]["place_name"].decode('shift-jis'),
                                candidate[i]["latitude"],
                                candidate[i]["longitude"])
                            )
                #    candidate_box.insert("end", "{0} | {1} | {2}".format( \
                #            candidate[i]["place_name"].decode('shift-jis'),\
                #            candidate[i]["latitude"], \
                #            candidate[i]["longitude"],
                #            ))
                    pass
                self.bind_display_candidate()
                # print candidate
            else:
                print "Not found ..."
        else:
            print "Sorry Not found ..."
            pass


    def get_canvas_postion(self, event):
        pos_x = event.x
        pos_y = event.y
        # self.master.title("[JIMAP] x:{0} / y:{1}".format(str(pos_x),str(pos_y)))
        latitude, longitude = self.oncursor_position(pos_x, pos_y)
        # print "x : {0} / y : {1}".format(pos_x, pos_y)
        self.print_xy.configure(
                text="x : {0:4d} / y : {1:4d}".format(pos_x, pos_y)
                )


    def oncursor_position(self, x, y):
        scroll_x1, _ = self.xscroll.get()
        scroll_y1, _ = self.yscroll.get()
        pad_x = scroll_x1 * Jimapn.CANVAS_WIDTH
        pad_y = scroll_y1 * Jimapn.CANVAS_HEIGHT
        # print "xscroll : {0}".format(pad_x)
        # print "yscroll : {0}".format(pad_y)
        # cursor_tile_x = x / Jimapn.TILE_WIDTH
        # cursor_tile_y = y / Jimapn.TILE_HEIGHT
        cursor_position_x = (self.offset_x + x + pad_x)
        cursor_position_y = (self.offset_y + y + pad_y)
        self.log_place.insert("end", "cursor tile x : {0}\n".format(cursor_position_x))
        self.log_place.insert("end", "cursor tile y : {0}\n".format(cursor_position_y))
        self.latitude, self.longitude = convert_pixcel_tolonglati(cursor_position_x, cursor_position_y, self.zoom_level)
        self.log_place.insert("end", "zoom level : {0}\n".format(self.zoom_level))
        self.log_place.insert("end", "latitude : {0}\n".format(self.latitude))
        self.log_place.insert("end", "longitude : {0}\n".format(self.longitude))
        # self.log_place.see("end")
        self.master.title("[JIMAP] x:{0} / y:{1}".format(str(self.latitude), str(self.longitude)))
        return self.latitude, self.longitude

    def drag_start(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.print_map.configure(
                cursor="hand2"
                )
        self.log_place.insert("end", "x : {0} / y : {1}\n".format(
            self.drag_start_x,
            self.drag_start_y))


    def move_map(self, event):
        x = event.x
        y = event.y
        aom_x = x - self.drag_start_x
        aom_y = y - self.drag_start_y
        self.offset_x -= aom_x
        self.offset_y -= aom_y
        # self.print_map.move("map_tile", aom_x, aom_y)
        self.map_draw(offset_x=self.offset_x, offset_y=self.offset_y)


    def show_right_menu(self, event):
        self.right_click_menu.post(event.x_root, event.y_root)

    def recode_place(self):
        win = edit_window(self, self.latitude, self.longitude)
        win.setter()

    def show_place(self):
        # recode place exists?
        place = {}
        recode_dir = DATA_DIR + "/" + "place_data"
        # layer directory
        for layer in glob.glob(recode_dir + "/*"):
            if os.path.isdir(layer):
                # kind directory
                for kind in glob.glob(layer + "/*"):
                    if os.path.isdir(kind):
                        # recode file
                        for place_file in glob.glob(kind + "/*"):
                            if os.path.isdir(place_file):
                                print "Not found ..."
                                pass
                            else:
                                print "Found : {0}".format(place_file)
                                with open(place_file, "rb") as pf:
                                    reader = csv.reader(pf)
                                    for row in reader:
                                        place = {
                                                layer : {
                                                    kind : {
                                                        "place_name" :
                                                        row[0].decode('utf-8'),
                                                        "place_name_kana" :
                                                        row[1].decode('utf-8'),
                                                        "layer" : row[2],
                                                        "kind" : row[3],
                                                        "latitude" : row[4],
                                                        "longitude" : row[5],
                                                        "memo" :
                                                        row[6].decode('utf-8'),
                                                        }
                                                    }
                                                }


                    else:
                        pass
            else:
                pass
            print place


def main():
    make_data_dir()
    app = Jimapn()
    app.pack()
    app.mainloop()


if __name__ == '__main__':
    main()

# vim: ft=python
# vim: fen:fdm=marker
