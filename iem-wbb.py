#!/usr/bin/python3


import sys
import cwiid
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from matplotlib.figure import Figure
from numpy import arange, pi, random, linspace
import os
import time as ptime
from math import sqrt
import matplotlib.pyplot as plt
import calculos as calc
from matplotlib.backends.backend_gtk3cairo import FigureCanvasGTK3Cairo as FigureCanvas

APs = []
MLs = []

class Iem_wbb:

    def on_window1_destroy(self, object, data=None):
        print("Quit with cancel")
        Gtk.main_quit()

    def on_gtk_quit_activate(self, menuitem, data=None):
        print("Quit from menu")
        Gtk.main_quit()

    def on_button1_clicked(self, widget):
        global APs, MLs

        balance = calc.readWBB()

        for (x,y) in balance:
            APs.append(x)
            MLs.append(y)

        max_absoluto_AP = calc.valorAbsoluto(min(APs), max(APs))
        max_absoluto_ML = calc.valorAbsoluto(min(MLs), max(MLs))

        max_absoluto_AP *= 1.25
        max_absoluto_ML *= 1.25

        print('max_absoluto_AP:',max_absoluto_AP,'max_absoluto_ML:',max_absoluto_ML)

        self.axis.clear()
        self.axis.set_ylabel('AP')
        self.axis.set_xlabel('MP')

        self.axis.set_xlim(-max_absoluto_ML, max_absoluto_ML)
        self.axis.set_ylim(-max_absoluto_AP, max_absoluto_AP)
        self.axis.plot(MLs, APs,'-',color='r')
        self.canvas.draw()

    def on_button2_clicked(self, widget):
        global APs, MLs
        APs, MLs = calc.geraAP_ML(APs, MLs)

        dis_resultante_total = calc.distanciaResultante(APs, MLs)
        dis_resultante_AP = calc.distanciaResultanteParcial(APs)
        dis_resultante_ML = calc.distanciaResultanteParcial(MLs)

        dis_media = calc.distanciaMedia(dis_resultante_total)

        dis_rms_total = calc.dist_RMS(dis_resultante_total)
        dis_rms_AP = calc.dist_RMS(dis_resultante_AP)
        dis_rms_ML = calc.dist_RMS(dis_resultante_ML)

        totex_total = calc.totex(APs, MLs)
        totex_AP = calc.totexParcial(APs)
        totex_ML = calc.totexParcial(MLs)

        mvelo_total = calc.mVelo(totex_total, 20)
        mvelo_AP = calc.mVelo(totex_AP, 20)
        mvelo_ML =  calc.mVelo(totex_ML, 20)

        self.entry_Mdist.set_text(str(dis_media))

        self.entry_Rdist_TOTAL.set_text(str(dis_rms_total))
        self.entry_Rdist_AP.set_text(str(dis_rms_AP))
        self.entry_Rdist_ML.set_text(str(dis_rms_ML))

        self.entry_TOTEX_TOTAL.set_text(str(totex_total))
        self.entry_TOTEX_AP.set_text(str(totex_AP))
        self.entry_TOTEX_ML.set_text(str(totex_ML))

        self.entry_MVELO_TOTAL.set_text(str(mvelo_total))
        self.entry_MVELO_AP.set_text(str(mvelo_AP))
        self.entry_MVELO_ML.set_text(str(mvelo_ML))

        max_absoluto_AP = calc.valorAbsoluto(min(APs), max(APs))
        max_absoluto_ML = calc.valorAbsoluto(min(MLs), max(MLs))

        max_absoluto_AP *=1.25
        max_absoluto_ML *=1.25

        print('max_absoluto_AP:', max_absoluto_AP, 'max_absoluto_ML:', max_absoluto_ML)
        self.axis.clear()

        self.axis.set_xlim(-max_absoluto_ML, max_absoluto_ML)
        self.axis.set_ylim(-max_absoluto_AP, max_absoluto_AP)

        self.axis.plot(MLs, APs,'-',color='g')
        self.axis.set_ylabel('AP')
        self.axis.set_xlabel('ML')
        self.canvas.draw()

    def __init__(self):
        self.gladeFile = "iem-wbb.glade"
        self.builder = Gtk.Builder()
        self.builder.add_from_file(self.gladeFile)

        self.builder.connect_signals(self)

        self.window = self.builder.get_object("window1")
        self.scrolledwindow = self.builder.get_object("scrolledwindow1")
        self.entry_Mdist = self.builder.get_object("mdist_")
        self.entry_Rdist_AP = self.builder.get_object("rdist_ap")
        self.entry_Rdist_ML = self.builder.get_object("rdist_ml")
        self.entry_Rdist_TOTAL = self.builder.get_object("rdist_t")
        self.entry_TOTEX_AP = self.builder.get_object("totex_ap")
        self.entry_TOTEX_ML = self.builder.get_object("totex_ml")
        self.entry_TOTEX_TOTAL = self.builder.get_object("totex_t")
        self.entry_MVELO_AP = self.builder.get_object("mvelo_ap")
        self.entry_MVELO_ML = self.builder.get_object("mvelo_ml")
        self.entry_MVELO_TOTAL = self.builder.get_object("mvelo_t")

        self.fig = plt.figure()

        self.axis = self.fig.add_subplot(111)
        self.axis.set_ylabel('AP')
        self.axis.set_xlabel('ML')
        self.canvas = FigureCanvas(self.fig)
        self.scrolledwindow.add_with_viewport(self.canvas)

        self.window.show_all()




if __name__ == "__main__":
    main = Iem_wbb()
    Gtk.main()

