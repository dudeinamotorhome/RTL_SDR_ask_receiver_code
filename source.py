# RTL_SDR_ask_receiver_code
contains receiver schematic for receiving ask data @433 mhz


#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Sun Apr  2 19:17:11 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.centfreq = centfreq = 433.903e6

        ##################################################
        # Blocks
        ##################################################
        _centfreq_sizer = wx.BoxSizer(wx.VERTICAL)
        self._centfreq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_centfreq_sizer,
        	value=self.centfreq,
        	callback=self.set_centfreq,
        	label='centrefreq',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._centfreq_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_centfreq_sizer,
        	value=self.centfreq,
        	callback=self.set_centfreq,
        	minimum=433.780e6,
        	maximum=433.936e6,
        	num_steps=500,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_centfreq_sizer)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_f(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=4e3,
        	v_scale=0.5,
        	v_offset=0,
        	t_scale=0.05,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_FREE,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.rtlsdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.rtlsdr_source_0.set_sample_rate(2e6)
        self.rtlsdr_source_0.set_center_freq(centfreq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(2, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(2, 0)
        self.rtlsdr_source_0.set_gain_mode(False, 0)
        self.rtlsdr_source_0.set_gain(45, 0)
        self.rtlsdr_source_0.set_if_gain(10, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(2000e3, 0)
          
        self.low_pass_filter_1 = filter.fir_filter_fff(5, firdes.low_pass(
        	1, 40e3, 6e2, 2e2, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(50, firdes.low_pass(
        	1, 2e6, 19.5e3, 500, firdes.WIN_HAMMING, 6.76))
        self.digital_clock_recovery_mm_xx_0 = digital.clock_recovery_mm_ff(32*(1+0.0), 0.25*0.175*0.175, 0.5, 0.175, 0.005)
        self.digital_binary_slicer_fb_0 = digital.binary_slicer_fb()
        self.blocks_udp_sink_0 = blocks.udp_sink(gr.sizeof_char*1, '127.0.0.1', 5267, 30, True)
        self.blocks_short_to_char_0 = blocks.short_to_char(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((5, ))
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_short_0 = blocks.char_to_short(1)
        self.blocks_add_const_vxx_1 = blocks.add_const_vss((19455, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-1.9, ))

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_add_const_vxx_0, 0), (self.digital_clock_recovery_mm_xx_0, 0))    
        self.connect((self.blocks_add_const_vxx_0, 0), (self.wxgui_scopesink2_0, 0))    
        self.connect((self.blocks_add_const_vxx_1, 0), (self.blocks_short_to_char_0, 0))    
        self.connect((self.blocks_char_to_short_0, 0), (self.blocks_add_const_vxx_1, 0))    
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.low_pass_filter_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))    
        self.connect((self.blocks_short_to_char_0, 0), (self.blocks_udp_sink_0, 0))    
        self.connect((self.digital_binary_slicer_fb_0, 0), (self.blocks_char_to_short_0, 0))    
        self.connect((self.digital_clock_recovery_mm_xx_0, 0), (self.digital_binary_slicer_fb_0, 0))    
        self.connect((self.low_pass_filter_0, 0), (self.blocks_complex_to_mag_squared_0, 0))    
        self.connect((self.low_pass_filter_1, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.rtlsdr_source_0, 0), (self.low_pass_filter_0, 0))    

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_centfreq(self):
        return self.centfreq

    def set_centfreq(self, centfreq):
        self.centfreq = centfreq
        self._centfreq_slider.set_value(self.centfreq)
        self._centfreq_text_box.set_value(self.centfreq)
        self.rtlsdr_source_0.set_center_freq(self.centfreq, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
