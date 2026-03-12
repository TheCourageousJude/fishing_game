#!/usr/bin/env python3
"""
Junior's Fishing Adventure — Python/Tkinter Port
Faithfully ported from the Java Swing original.
Run with: python fishing_game.py
"""

import tkinter as tk
from tkinter import messagebox
import random
import math
import time

# ============================================================
# CONSTANTS
# ============================================================
WIN_W, WIN_H = 900, 700
TIMER_MS = 10
UP_ACCEL = 0.3
GRAVITY = 0.3
MAX_BAR_SPEED = 20.0
PROGRESS_FILL_RATE = 2.0
PROGRESS_DECAY_RATE = -3.0
SEARCH_CHECK_MS = 1000
BITE_WINDOW_MS = 2000
BG_PIXEL_SIZE = 25
MAX_STAGES = 5
STAGE_TARGET = 500
BAR_HEIGHT = 500
BAR_WIDTH = 40
BAR_X = 720
BAR_Y = 80
PROG_X = 675
PROG_Y = 80
PROG_W = 25

STAGE_DIFFICULTY  = [[1,20],[10,30],[18,45],[28,55],[48,93]]
STAGE_BASE_VALUES = [[150,250],[300,500],[450,750],[600,1000],[750,1250]]
FISH_BONUS        = [1.0, 1.2, 1.2, 1.5]
CAPTAIN_FEES      = [500, 1000, 1500, 2500, 5000]

COLOR_IDLE       = "#FFFFC8"
COLOR_SEARCHING  = "#C8E6FF"
COLOR_BITE       = "#C8FFC8"

def _hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

# ============================================================
# PIXEL ART PALETTES & DATA
# ============================================================

VICTORY_PALETTE = [
    _hex(255,238,0), _hex(20,110,160), _hex(30,140,200), _hex(85,170,229),
    _hex(180,180,180), _hex(150,230,60), _hex(70,150,0), _hex(230,0,0),
    _hex(180,0,0), _hex(230,210,150), _hex(190,240,240), _hex(0,0,0),
    _hex(120,120,120), _hex(200,200,200), _hex(230,235,225), _hex(0,120,40),
    _hex(160,160,160),
]

VICTORY_BG = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,4,4,4,4],
    [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,4,4,1],
    [1,1,4,4,4,1,1,1,1,1,1,1,1,4,4,4,4,4,4,1,1,1,1,1,1,1,1,1],
    [2,4,4,4,4,4,2,2,2,2,2,2,2,2,4,2,4,2,2,2,2,14,14,14,14,14,2,2],
    [2,2,4,4,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,14,14,11,14,11,14,14,2],
    [2,2,2,2,2,8,8,8,8,8,8,8,8,2,2,2,2,2,2,2,14,14,14,14,14,14,14,2],
    [2,2,2,2,8,8,7,7,7,7,7,8,8,8,2,2,2,2,2,2,14,11,14,14,14,11,14,2],
    [2,2,2,8,8,7,7,7,7,7,8,8,7,8,8,2,2,2,2,2,14,14,11,11,11,14,14,2],
    [2,2,8,8,7,7,7,7,7,8,8,7,7,7,8,8,2,2,2,2,2,14,14,14,14,14,2,2],
    [3,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,3,3,11,11,3,14,3,3,3,3,3],
    [3,3,3,6,6,6,6,6,6,6,6,6,6,6,6,3,3,3,11,11,11,11,3,3,3,3,3,3],
    [3,3,3,6,10,11,10,5,10,11,10,6,5,5,6,3,3,3,11,11,11,11,13,13,13,13,3,3],
    [3,3,3,6,11,11,11,5,11,11,11,6,9,9,6,3,11,3,3,11,11,13,10,11,10,13,10,3],
    [3,3,3,6,10,11,10,5,10,11,10,6,9,9,6,3,11,3,11,11,11,11,13,11,13,13,13,13],
    [3,3,3,6,5,5,5,5,5,5,5,6,9,9,6,3,3,11,11,11,11,11,11,13,13,13,13,13],
    [3,3,3,6,5,5,5,5,5,5,5,6,9,9,6,3,3,3,11,11,11,11,3,12,3,3,12,3],
    [16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,11,16,16,11,16,16,16,16,16,16],
    [15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
]

MARKET_PALETTE = [
    _hex(210,170,120), _hex(245,167,58), _hex(0,0,0), _hex(144,84,0),
    _hex(124,77,0), _hex(255,255,255), _hex(200,129,12), _hex(152,94,0),
    _hex(240,97,0), _hex(139,118,7), _hex(204,245,247), _hex(0,76,199),
    _hex(255,238,0), _hex(211,211,211), _hex(64,64,64),
]

MARKET_BG = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,2,5,5,5,5,5,5,5,5,5,5,5,5,5,2,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,2,5,5,5,5,5,5,5,5,5,5,5,5,5,2,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,2,5,5,5,5,5,5,5,5,5,5,5,5,5,2,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,2,5,5,5,5,5,5,5,5,5,5,5,5,5,2,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,2,5,5,5,5,5,5,5,5,5,5,5,5,5,2,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,0,2,2,2,2,2,2,2,2,2,2,2,5,2,0,0,0,0,6,3,3,3,3,3,3,3,3,3,3,3,3,6,0,0],
    [0,0,0,0,2,9,9,9,9,9,9,9,2,2,5,2,0,0,0,0,6,6,6,6,6,6,6,6,6,6,6,6,6,6,0,0],
    [0,0,0,2,2,9,9,9,9,9,9,2,2,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0],
    [0,0,2,9,9,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
    [0,0,0,2,2,4,4,4,4,4,4,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0],
    [0,0,0,0,2,2,2,4,4,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,2,0,0,0,0,4,0],
    [0,0,0,0,2,4,2,4,4,4,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,12,12,6,2,0,0,0,0],
    [0,0,0,0,2,4,4,4,4,4,4,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,10,2,12,12,6,6,6,0,0,0],
    [0,0,0,0,2,2,2,2,2,2,2,4,2,0,0,0,0,0,0,0,0,0,0,0,0,0,10,10,10,10,6,13,2,13,0,0],
    [0,0,0,0,2,4,4,4,4,4,4,4,2,0,2,2,2,2,2,0,0,0,0,0,0,0,4,10,10,10,13,13,13,4,0,0],
    [0,0,0,2,2,2,2,4,4,2,2,2,2,2,11,2,4,4,2,0,0,0,0,0,0,0,4,4,4,4,4,4,4,4,0,0],
    [0,0,2,11,11,2,10,2,2,10,2,11,11,11,11,2,2,2,0,0,0,0,0,0,0,0,4,7,7,7,7,7,7,4,0,0],
    [7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,4,14,14,14,14,14,14,4,7,7],
    [1,1,7,1,1,1,7,1,1,1,1,7,1,1,1,7,1,1,1,1,7,1,1,1,7,1,4,13,13,13,13,13,13,4,1,1],
    [1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,4,7,7,7,7,7,7,4,1,1],
    [1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,4,7,7,7,7,7,7,4,1,1],
    [1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,4,14,14,14,14,14,14,4,1,1],
    [1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,4,13,13,13,13,13,13,4,1,1],
    [1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,1,1,1,7,1,7,1,7,1,4,7,7,7,7,7,7,4,1,1],
]

MENU_PALETTE = [
    _hex(0,0,0), _hex(139,69,19), _hex(255,165,0), _hex(0,0,139),
    _hex(0,100,0), _hex(255,224,189), _hex(255,255,255), _hex(0,140,255),
    _hex(0,70,255), _hex(0,30,255), _hex(101,67,33), _hex(34,139,34),
    _hex(0,85,0), _hex(139,0,0),
]

MENU_BG = [
    [4,11,11,4,4,4,11,11,11,4,4,11,11,4,4,4,4,11,11,11,4,4,11],
    [11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11],
    [11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11],
    [11,11,11,11,11,11,4,4,11,11,11,11,11,11,11,11,11,4,4,4,11,11,11],
    [4,4,11,11,4,4,3,12,4,4,4,11,4,4,11,4,4,12,12,10,4,4,4],
    [12,12,4,4,12,3,3,3,12,10,10,4,12,12,4,10,1,12,12,10,10,12,12],
    [12,12,10,10,12,3,5,5,12,10,10,12,12,12,1,1,6,12,12,10,10,12,12],
    [12,12,10,10,12,5,5,5,12,10,10,12,1,1,10,10,6,12,12,10,10,12,12],
    [12,12,10,10,12,3,13,13,12,10,10,1,12,12,10,10,6,12,12,10,10,12,12],
    [12,12,10,10,12,3,13,13,13,13,5,12,12,12,10,6,12,12,12,10,10,12,12],
    [12,12,10,10,12,12,3,3,3,3,10,12,12,12,10,6,12,12,12,10,10,12,12],
    [1,1,1,1,1,1,3,13,13,10,10,12,12,12,10,6,12,12,12,10,10,12,12],
    [2,1,2,2,1,2,3,13,13,13,10,12,12,12,10,6,12,12,12,10,10,12,12],
    [2,2,1,2,2,1,2,3,3,13,7,7,7,7,9,9,9,7,7,7,7,7,7],
    [1,1,1,1,1,1,1,1,1,3,7,7,7,7,7,7,7,7,7,7,7,7,7],
    [8,1,8,8,8,1,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
    [9,1,9,9,9,1,8,8,9,9,9,9,8,8,8,9,9,8,9,9,9,8,8],
]

STAGE_PALETTES = [
    [_hex(135,206,250),_hex(220,220,220),_hex(60,170,60),_hex(120,200,120),
     _hex(139,69,19),_hex(90,55,30),_hex(90,90,90),_hex(110,110,110),_hex(0,200,220)],
    [_hex(180,230,255),_hex(150,210,240),_hex(60,130,115),_hex(40,110,95),
     _hex(25,75,65),_hex(110,85,0),_hex(85,65,0),_hex(50,120,60),_hex(35,95,45),
     _hex(200,200,200),_hex(120,120,120)],
    [_hex(95,183,0),_hex(70,145,0),_hex(182,131,0),_hex(115,83,0),
     _hex(30,224,185),_hex(16,149,117)],
    [_hex(253,254,254),_hex(157,254,247),_hex(221,192,147),_hex(211,163,89),
     _hex(178,108,0),_hex(43,124,0),_hex(108,227,1),_hex(100,148,21),
     _hex(0,208,129),_hex(216,178,118)],
    [_hex(220,220,220),_hex(128,178,214),_hex(84,91,97),_hex(18,94,151),
     _hex(25,131,203),_hex(28,141,220),_hex(229,172,0),_hex(150,86,0),_hex(0,0,0)],
]

STAGE_BACKGROUNDS = [
    # Stage 1: Rivers
    [[0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
     [0,0,1,1,1,1,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,1,1],
     [0,0,0,1,1,1,1,0,0,1,1,1,1,1,1,0,0,1,1,1,1,1,1,0,0,0],
     [0,0,0,0,1,1,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,2],
     [0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,2,3],
     [2,0,0,2,0,2,2,0,0,0,0,0,2,0,0,0,0,2,3,2,0,2,3,2,3,3],
     [3,2,2,3,2,3,3,2,0,2,0,2,3,2,0,0,2,3,3,3,2,3,3,3,2,3],
     [3,2,3,3,3,2,3,3,2,3,2,3,3,3,2,2,3,3,3,3,3,2,3,2,3,3],
     [3,3,2,3,2,3,3,2,3,3,3,2,3,3,2,3,2,3,3,3,2,3,3,3,2,3],
     [3,2,3,3,3,2,3,2,3,3,3,2,3,3,2,3,3,2,3,2,3,3,3,3,3,2],
     [2,2,2,2,2,2,2,3,3,3,3,3,2,2,3,3,3,3,2,3,3,3,3,3,3,3],
     [5,0,4,4,5,5,2,2,2,2,2,2,2,3,3,2,3,3,2,2,2,2,2,2,2,2],
     [5,4,4,4,5,5,0,0,4,4,5,5,0,2,2,2,2,2,2,5,5,4,4,0,5,5],
     [6,6,6,4,4,5,0,0,4,4,4,5,0,0,0,4,4,0,0,5,5,4,4,4,5,5],
     [7,7,7,6,6,5,0,4,4,4,4,5,0,0,4,4,4,4,5,5,5,4,4,4,5,5],
     [7,7,7,7,7,6,0,4,6,6,4,4,5,0,4,4,4,4,5,5,4,4,4,6,6,5],
     [7,7,7,7,7,7,6,6,7,7,6,4,6,6,6,4,4,4,6,6,6,4,6,7,7,6],
     [6,6,6,6,7,6,7,7,7,7,7,6,7,7,7,6,4,6,7,7,7,6,7,7,7,7],
     [8,8,8,8,6,7,7,7,7,7,7,7,6,7,7,7,6,7,7,7,7,7,7,7,6,6],
     [8,8,8,8,8,6,6,7,6,6,6,6,7,7,7,6,6,6,7,7,7,7,6,6,8,8],
     [8,8,8,8,6,8,8,6,8,8,8,8,6,6,6,8,8,8,6,6,6,6,8,8,8,8],
     [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,6,6,7,7,6,8,8,8,8,8],
     [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,6,7,7,7,7,7,6,8,8,8,8],
     [6,8,8,8,6,6,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8],
     [7,6,6,6,7,7,6,6,6,6,8,8,8,8,8,6,6,6,8,8,8,8,8,6,6,8],
     [6,7,7,7,7,6,7,7,7,7,6,8,6,6,6,7,7,7,6,8,8,6,6,7,7,6],
     [7,7,7,7,6,7,7,7,7,7,7,6,7,7,7,7,7,7,7,6,6,7,7,7,7,7]],
    # Stage 2: Swamp
    [[1,1,0,0,0,0,1,1,1,1,1,0,1,1,1,8,8,8,8,8,8,8,8,8,1,1],
     [1,1,1,0,0,1,1,1,1,0,0,0,1,8,8,8,8,8,8,8,8,8,8,8,8,0],
     [0,1,1,1,1,1,1,1,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,0],
     [0,1,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,5,8,8,8,8,1],
     [1,8,8,8,8,8,8,8,8,8,8,8,8,8,5,5,8,8,8,5,5,8,8,8,8,8],
     [8,8,8,8,8,8,8,8,8,8,8,8,8,5,5,5,5,8,8,5,8,8,5,5,8,8],
     [8,8,8,5,8,8,5,8,8,8,8,8,8,8,8,5,5,8,8,5,8,8,5,5,8,8],
     [8,8,8,5,8,8,5,8,8,8,5,8,5,8,8,8,5,5,5,5,5,5,5,8,8,8],
     [5,5,5,5,5,5,5,8,8,8,5,5,5,5,8,8,5,5,5,5,5,5,5,8,8,8],
     [8,8,5,5,5,5,8,8,8,8,8,5,5,5,5,8,8,5,5,5,5,5,8,8,8,8],
     [8,8,8,8,5,5,8,6,8,8,8,5,5,0,8,8,6,8,5,5,5,5,8,6,8,8],
     [8,6,8,8,5,5,8,6,8,8,0,5,5,0,0,0,6,8,5,5,5,5,8,6,8,8],
     [0,6,0,5,5,5,0,6,6,0,0,5,5,5,0,6,6,0,5,5,5,5,0,6,6,0],
     [6,6,0,5,5,5,0,6,6,0,0,5,5,5,6,6,6,0,0,5,5,5,0,6,6,0],
     [6,6,0,5,5,5,5,0,6,0,5,5,5,5,6,0,6,6,0,5,5,5,0,6,6,6],
     [3,3,5,5,5,5,5,3,3,5,5,3,5,3,5,4,4,4,4,5,5,5,6,6,3,6],
     [4,4,5,5,5,5,5,3,3,3,3,3,3,3,3,3,4,4,4,5,5,5,3,3,3,3],
     [7,4,5,5,5,5,5,4,4,4,3,3,3,3,3,3,7,3,3,5,5,5,3,3,7,4],
     [3,3,5,5,5,5,5,5,4,4,4,4,7,4,4,3,3,3,3,5,5,5,4,4,4,4],
     [3,5,5,4,5,5,3,5,5,4,4,4,4,4,4,4,4,3,3,5,5,5,5,4,4,3],
     [4,5,5,3,5,5,3,5,5,3,4,4,4,4,4,4,4,4,5,5,5,5,5,3,3,3],
     [4,5,5,3,5,5,3,5,4,4,7,3,3,3,3,4,4,5,5,5,5,5,5,5,3,3],
     [3,3,3,3,5,5,4,4,4,4,4,3,3,7,3,3,5,5,5,5,5,5,5,5,5,3],
     [3,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,5,5,3,5,5,5,3,5,5,5],
     [4,4,4,4,7,4,4,3,3,3,3,3,3,3,3,5,5,5,3,5,5,5,3,3,5,5],
     [4,7,4,4,3,3,3,7,3,3,4,4,4,3,3,5,5,5,4,5,5,5,5,3,5,5],
     [3,3,3,3,3,3,3,3,3,4,4,7,4,4,4,5,5,3,4,4,5,5,5,4,4,4]],
    # Stage 3: Springs
    [[0,0,0,0,0,1,1,0,1,1,1,1,1,1,0,0,0,0,0,0,0,1,1,1,1,1],
     [0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,3,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,3,3,2,0],
     [0,0,0,0,0,0,1,1,0,1,1,1,1,1,3,1,1,0,0,0,1,3,3,3,2,2],
     [0,0,0,0,1,1,1,1,1,1,1,1,2,1,3,1,0,0,2,0,0,3,3,3,2,2],
     [0,0,0,1,1,1,0,0,1,1,1,1,2,1,3,3,0,0,2,2,0,3,3,3,3,2],
     [0,1,1,1,1,0,0,0,0,1,1,2,2,1,3,3,1,0,2,2,0,3,3,3,3,2],
     [1,1,1,0,0,0,2,0,0,0,1,2,2,2,3,3,0,2,2,2,0,3,3,3,3,2],
     [1,1,1,0,0,0,2,2,0,0,0,2,2,2,3,3,0,2,2,2,1,3,3,3,3,2],
     [1,1,1,1,0,0,2,2,0,0,0,2,2,2,3,3,3,2,2,2,3,3,3,3,3,3],
     [1,2,2,1,0,2,2,2,0,0,1,2,2,2,3,3,3,2,2,2,3,3,3,3,3,3],
     [0,2,2,0,0,2,2,2,1,1,1,2,2,3,3,3,3,2,2,2,3,3,3,3,3,3],
     [0,2,2,3,1,2,2,2,2,1,2,2,2,3,3,3,3,2,2,3,3,3,3,3,3,3],
     [2,2,3,3,1,2,2,2,2,1,2,2,2,3,3,3,3,3,2,3,5,5,5,5,5,5],
     [2,2,3,3,3,2,2,3,3,3,2,2,3,3,5,5,5,5,5,5,5,5,5,5,5,5],
     [2,2,3,3,3,2,3,3,3,3,3,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
     [2,2,3,3,3,2,3,3,3,3,3,3,3,5,5,5,5,4,4,4,4,4,4,4,4,4],
     [2,3,3,3,5,5,5,5,3,3,3,3,3,3,3,4,4,4,3,3,5,4,4,4,4,4],
     [5,5,5,5,5,5,5,5,5,5,5,3,3,3,3,3,4,3,3,5,5,4,4,4,4,4],
     [5,5,5,5,5,4,4,4,4,5,5,5,5,3,3,3,3,3,5,5,4,4,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,3,3,3,3,3,4,4,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,4,4,4,5,3,3,5,5,3,3,3,3,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,4,4,5,3,3,5,5,5,5,5,3,3,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,4,5,5,5,5,5,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,4,4,4,4,5,5,4,4,4,4,4],
     [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]],
    # Stage 4: Oasis
    [[1,1,0,0,1,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1],
     [1,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,1,1,1,1,0,0,0,0,0,1],
     [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1],
     [1,0,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2],
     [1,1,1,2,2,2,2,2,2,2,1,1,1,2,2,2,1,6,6,1,1,1,9,9,2,2],
     [1,2,2,2,2,5,5,9,9,2,2,1,2,2,2,6,6,6,6,6,9,9,6,6,9,9],
     [2,2,2,5,5,5,5,9,9,9,2,2,2,2,2,2,6,6,6,6,6,6,6,6,6,9],
     [5,5,2,5,5,5,9,9,9,9,9,2,2,2,6,6,6,6,6,4,6,6,6,9,9,9],
     [5,5,5,5,5,5,5,5,5,9,9,9,9,2,9,6,6,6,9,4,4,6,6,6,9,9],
     [2,9,5,5,4,5,5,9,9,9,9,9,9,9,9,9,9,9,9,4,4,6,6,6,6,9],
     [5,5,5,4,4,9,9,9,9,9,9,9,6,6,6,9,9,9,4,4,4,9,9,6,9,9],
     [5,5,9,4,6,6,6,9,9,9,6,6,6,6,6,9,9,9,4,4,9,9,9,9,9,9],
     [3,3,9,9,4,6,6,6,6,3,6,6,6,9,7,9,7,4,4,4,3,7,3,9,3,3],
     [3,3,3,3,4,6,6,6,6,6,6,6,3,7,7,3,7,4,4,7,3,7,7,3,3,3],
     [3,7,3,4,4,4,6,6,6,6,6,6,6,7,3,7,4,4,4,7,3,3,7,3,3,3],
     [3,7,7,4,6,6,6,6,4,4,6,6,6,8,8,8,4,4,7,7,5,5,5,3,7,3],
     [3,3,7,6,6,6,8,4,4,4,8,6,6,6,8,8,8,8,8,5,5,5,5,7,7,3],
     [7,3,7,8,8,8,8,4,4,8,8,6,5,5,5,5,8,5,5,5,5,5,8,7,3,3],
     [7,7,8,8,8,8,8,4,4,8,8,8,8,5,5,5,5,5,5,5,5,8,8,5,5,3],
     [3,7,8,8,8,8,4,4,4,8,8,8,8,8,8,5,5,5,5,5,5,5,5,5,5,5],
     [7,8,8,8,8,8,4,4,8,8,8,8,5,5,5,5,5,4,4,4,5,5,5,5,3,3],
     [7,7,7,8,8,4,4,4,8,8,8,5,5,5,5,5,4,4,4,4,5,5,3,7,7,3],
     [3,7,3,7,7,4,4,4,8,7,7,8,8,8,7,7,4,4,4,5,5,5,5,7,3,3],
     [3,7,3,7,3,4,4,4,8,7,8,8,7,8,7,4,4,4,3,7,5,5,5,5,5,3],
     [3,3,3,7,4,4,4,4,7,7,8,7,7,8,7,4,4,4,3,7,7,3,7,3,3,3],
     [3,3,3,3,3,3,7,7,7,3,3,7,3,3,7,4,4,4,3,3,7,7,7,3,3,3],
     [3,3,3,3,3,3,3,3,7,3,3,3,3,3,4,4,4,3,3,3,3,7,3,3,3,3]],
    # Stage 5: Deep Ocean
    [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0],
     [1,1,1,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,1],
     [1,1,0,0,0,0,0,0,1,1,1,1,1,1,0,1,1,0,0,1,1,1,1,0,1,1],
     [1,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,1,1,1,1,1],
     [1,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1],
     [1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,0,0,1,0,1,1,1,1,0,0,0],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0],
     [0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1],
     [0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1],
     [1,1,1,1,2,2,1,1,1,1,1,1,1,1,2,2,2,1,1,1,1,1,1,1,1,1],
     [1,1,1,2,2,2,2,1,1,1,1,1,1,2,2,2,2,2,1,1,1,1,1,2,1,1],
     [1,1,2,2,2,2,2,2,1,1,1,1,2,2,2,2,2,2,2,1,1,1,2,2,2,1],
     [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4],
     [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5],
     [5,5,3,5,5,5,3,5,5,5,3,5,5,5,3,5,5,5,3,5,5,5,3,5,5,5],
     [4,3,3,3,4,3,3,3,4,3,3,3,4,3,3,3,4,3,3,3,4,3,3,3,4,3],
     [4,4,5,4,4,4,4,5,4,4,4,4,5,4,4,4,4,5,4,4,4,4,5,4,4,4],
     [4,5,5,5,4,4,5,5,5,4,4,5,5,5,4,4,5,5,5,4,4,5,5,5,4,4],
     [5,5,5,5,3,5,5,5,5,3,5,5,5,5,3,5,5,5,5,3,5,5,5,5,3,5],
     [6,5,5,3,3,3,5,5,3,3,3,5,5,3,3,3,5,5,3,3,3,5,5,3,3,6],
     [6,6,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,6,6],
     [7,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,7],
     [7,7,7,7,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,7,7,7,7],
     [7,7,7,7,6,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,7,6,7,7,7,7],
     [5,7,6,4,6,5,7,7,4,7,5,4,7,4,4,5,7,4,4,7,5,6,4,6,7,5],
     [5,5,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,6,5,5],
     [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]],
]

# ============================================================
# FISH AI
# ============================================================
class FishAI:
    SMOOTH = 0
    ACTIVE = 1
    HYPER  = 2
    GLIDER = 3

    def __init__(self, fish_type, initial_y, bar_height, fish_height, timer_ms, difficulty):
        self.type        = fish_type
        self.y           = float(initial_y)
        self.bar_height  = bar_height
        self.fish_height = fish_height
        self.timer_ms    = timer_ms
        self.rand        = random.Random()

        self.base_speed      = 0.0
        self.difficulty_factor = 0.0
        self.diff_curve      = 0.0
        self.speed           = 0.0
        self.target_y        = 0.0
        self.direction       = -1
        self.current_difficulty = difficulty

        # Hyper vars
        self.hyper_base_speed    = 0.0
        self.hyper_jitter_bias   = 0.0
        self.burst_cooldown_ms   = 0
        self.hyper_jitter_ms     = 0
        self.hyper_burst_anim_ms = 0
        self.hyper_burst_animating = False
        self.hyper_burst_start_y = 0.0
        self.hyper_burst_end_y   = 0.0

        # Glider vars
        self.direction_switch_ms = 0
        self.direction_timer_ms  = 0
        self.speed_timer_ms      = 0

        # Active vars
        self.active_target_y       = 0.0
        self.active_speed_px_per_ms = 0.0
        self.dash_multiplier       = 1.0
        self.active_travel_ms      = 0
        self.dash_ms_remaining     = 0

        # Smooth vars
        self.smooth_is_dashing     = False
        self.smooth_dash_cooldown_ms = 0
        self.smooth_dash_elapsed_ms  = 0
        self.smooth_dash_total_ms    = 0
        self.smooth_travel_ms        = 0
        self.smooth_dash_start_y     = 0.0
        self.smooth_dash_target_y    = 0.0
        self.smooth_target_y         = 0.0
        self.smooth_speed_px_per_ms  = 0.0

        self.set_difficulty(difficulty)
        self._init_for_type()

    def _rand_between(self, lo, hi):
        return self.rand.randint(lo, hi)

    def _roll_hyper_base_speed(self, d):
        if d <= 15:  px = self._rand_between(80, 120)
        elif d <= 30: px = self._rand_between(120, 180)
        elif d <= 50: px = self._rand_between(180, 260)
        elif d <= 70: px = self._rand_between(260, 360)
        elif d <= 90: px = self._rand_between(360, 480)
        else:         px = self._rand_between(480, 620)
        return px / 100.0

    def _get_hyper_burst_distance(self, d):
        if d <= 14: return self._rand_between(23, 38)
        if d <= 30: return self._rand_between(38, 56)
        if d <= 50: return self._rand_between(56, 94)
        if d <= 70: return self._rand_between(75, 131)
        if d <= 90: return self._rand_between(94, 169)
        return self._rand_between(101, 188)

    def _pick_hyper_new_target(self):
        bottom = self.bar_height - self.fish_height
        dist = self._get_smooth_subtle_distance(self.current_difficulty)
        if self.rand.random() < 0.5:
            self.target_y = min(bottom, self.y + dist)
        else:
            self.target_y = max(0, self.y - dist)
        return self.target_y

    def _roll_direction_switch_ms(self, d):
        if d <= 15: return self._rand_between(1500, 2000)
        if d <= 30: return self._rand_between(1250, 1490)
        if d <= 50: return self._rand_between(1000, 1240)
        if d <= 70: return self._rand_between(700, 900)
        if d <= 90: return self._rand_between(300, 600)
        return self._rand_between(1200, 2100)

    def _roll_glider_speed(self, d):
        if d <= 15:  lo, hi = 100, 200
        elif d <= 30: lo, hi = 150, 275
        elif d <= 50: lo, hi = 200, 350
        elif d <= 70: lo, hi = 250, 425
        elif d <= 90: lo, hi = 300, 500
        else:         lo, hi = 350, 600
        return (self._rand_between(lo, hi) / 100.0) * (1.0 + self.diff_curve * 0.35)

    def _get_distance_by_difficulty(self, d):
        if d <= 14: return self._rand_between(10, 25)
        if d <= 30: return self._rand_between(25, 55)
        return self._rand_between(35, 80)

    def _get_dash_chance(self, d):
        if d <= 14: return 5
        if d <= 30: return 10
        if d <= 50: return 18
        if d <= 70: return 30
        if d <= 90: return 45
        return 60

    def _get_time_by_difficulty(self, d):
        if d <= 14: return self._rand_between(300, 400)
        if d <= 30: return self._rand_between(275, 375)
        if d <= 50: return self._rand_between(250, 350)
        if d <= 70: return self._rand_between(225, 325)
        return self._rand_between(150, 325)

    def _get_smooth_dash_distance(self, d):
        if d <= 14: return self._rand_between(30, 50)
        if d <= 30: return self._rand_between(50, 75)
        if d <= 50: return self._rand_between(75, 125)
        if d <= 70: return self._rand_between(100, 175)
        return self._rand_between(125, 250)

    def _get_smooth_subtle_distance(self, d):
        if d <= 14: return self._rand_between(10, 20)
        if d <= 30: return self._rand_between(20, 40)
        if d <= 50: return self._rand_between(30, 60)
        if d <= 70: return self._rand_between(40, 80)
        return self._rand_between(45, 145)

    def _roll_smooth_dash(self, d):
        return self.rand.randint(0, 99) < (30 if d <= 50 else 55)

    def set_difficulty(self, difficulty):
        d = max(1, min(100, difficulty))
        self.diff_curve = math.pow(d / 100.0, 1.4)
        self.difficulty_factor = 0.35 + self.diff_curve * 1.05
        if self.type == FishAI.GLIDER:
            self.speed = self._roll_glider_speed(d)
            self.direction_switch_ms = self._roll_direction_switch_ms(d)
            self.direction_timer_ms = self.direction_switch_ms
        elif self.type == FishAI.HYPER:
            self.hyper_base_speed = self._roll_hyper_base_speed(d)
            self.speed = self.hyper_base_speed * self.difficulty_factor
            if not self.hyper_burst_animating:
                self._pick_hyper_new_target()

    def _init_for_type(self):
        if self.type == FishAI.SMOOTH:
            self._init_smooth_ai(self.current_difficulty)
        elif self.type == FishAI.ACTIVE:
            self._init_active_ai(self.current_difficulty)
        elif self.type == FishAI.HYPER:
            self.hyper_base_speed = self._roll_hyper_base_speed(self.current_difficulty)
            self.speed = self.hyper_base_speed * self.difficulty_factor
            self.target_y = self._pick_hyper_new_target()
            self.burst_cooldown_ms = self._rand_between(50, 100)
            self.hyper_jitter_ms = self._rand_between(50, 150)
        elif self.type == FishAI.GLIDER:
            self.speed = self._roll_glider_speed(self.current_difficulty)
            self.speed_timer_ms = 1500 + self.rand.randint(0, 1499)
            self.direction_switch_ms = self._roll_direction_switch_ms(self.current_difficulty)
            self.direction_timer_ms = self.direction_switch_ms
            self.direction = 1 if self.rand.random() < 0.5 else -1
        if self.type != FishAI.GLIDER:
            self.speed = self.base_speed * self.difficulty_factor

    def _init_smooth_ai(self, d):
        self.current_difficulty = d
        self.diff_curve = d / 100.0
        self.y = self.bar_height - self.fish_height
        self.smooth_is_dashing = False
        self.smooth_dash_cooldown_ms = self._rand_between(300, 600)
        self._pick_smooth_subtle_move(d)

    def _init_active_ai(self, d):
        self.current_difficulty = d
        self.diff_curve = d / 100.0
        if self.y <= 0:
            self.y = (self.bar_height - self.fish_height) / 2.0
        self._pick_active_target(d)
        self.dash_ms_remaining = 0
        self.dash_multiplier = 1.0

    def _pick_active_target(self, d):
        bottom = self.bar_height - self.fish_height
        dist = self._get_distance_by_difficulty(d)
        t = self._get_time_by_difficulty(d)
        down = self.rand.random() < 0.5
        self.active_target_y = max(0, min(bottom, self.y + dist if down else self.y - dist))
        if self.active_target_y == self.y:
            self.active_target_y = min(bottom, self.y + dist)
        self.active_speed_px_per_ms = abs(self.active_target_y - self.y) / t
        self.active_travel_ms = t
        if self.rand.randint(0, 99) < self._get_dash_chance(d):
            self.dash_ms_remaining = 500
            self.dash_multiplier = 2.8
        else:
            self.dash_ms_remaining = 0
            self.dash_multiplier = 1.0

    def _do_active_tick(self, tick_ms):
        if self.dash_ms_remaining > 0:
            self.dash_ms_remaining -= tick_ms
            if self.dash_ms_remaining <= 0:
                self.dash_multiplier = 1.0
        move = self.active_speed_px_per_ms * tick_ms * self.dash_multiplier
        diff = self.active_target_y - self.y
        if abs(diff) <= move or self.active_travel_ms <= 0:
            self.y = self.active_target_y
            self._pick_active_target(self.current_difficulty)
        else:
            self.y += math.copysign(move, diff)
            self.active_travel_ms -= tick_ms
        bottom = self.bar_height - self.fish_height
        self.y = max(0, min(bottom, self.y))

    def _do_hyper_tick(self, tick_ms):
        bottom = self.bar_height - self.fish_height
        self.hyper_jitter_ms -= tick_ms
        if self.hyper_jitter_ms <= 0:
            self.hyper_jitter_ms = self._rand_between(50, 150)
            self.hyper_jitter_bias = (self.rand.random() - 0.5) * 1.4
        if self.hyper_burst_animating:
            self.hyper_burst_anim_ms -= tick_ms
            if self.hyper_burst_anim_ms <= 0:
                self.y = self.hyper_burst_end_y
                self.hyper_burst_animating = False
                self.burst_cooldown_ms = self._rand_between(50, 100)
                self._pick_hyper_new_target()
            else:
                p = 1.0 - (self.hyper_burst_anim_ms / 150.0)
                e = 2*p*p if p < 0.5 else 1 - math.pow(-2*p+2, 2)/2
                self.y = self.hyper_burst_start_y + (self.hyper_burst_end_y - self.hyper_burst_start_y)*e + self.hyper_jitter_bias*0.2
        elif self.burst_cooldown_ms <= 0 and self.rand.randint(0,99) < 20 + int(self.diff_curve*25):
            self.hyper_burst_animating = True
            self.hyper_burst_anim_ms = 150
            self.hyper_burst_start_y = self.y
            dist = self._get_hyper_burst_distance(self.current_difficulty)
            sign = 1 if self.rand.random() < 0.5 else -1
            self.hyper_burst_end_y = max(0, min(bottom, self.y + sign * dist))
        else:
            if self.burst_cooldown_ms > 0:
                self.burst_cooldown_ms -= tick_ms
            diff = self.target_y - self.y
            if abs(diff) > 1.0:
                self.y += (self.hyper_base_speed * 1.25) * math.copysign(1, diff) + self.hyper_jitter_bias * 0.4
            if abs(self.target_y - self.y) < 2.0:
                self._pick_hyper_new_target()
        if self.y <= 0 or self.y >= bottom:
            self._pick_hyper_new_target()

    def _do_glider_tick(self, tick_ms):
        self.speed_timer_ms -= tick_ms
        if self.speed_timer_ms <= 0:
            self.speed = self._roll_glider_speed(self.current_difficulty)
            self.speed_timer_ms = 1500 + self.rand.randint(0, 1499)
        if self.rand.randint(0, 999) < 7 or self.direction_timer_ms <= 0:
            self.direction *= -1
            self.direction_timer_ms = self._roll_direction_switch_ms(self.current_difficulty)
        self.direction_timer_ms -= tick_ms
        self.y += self.direction * self.speed
        bottom = self.bar_height - self.fish_height
        if self.y <= 0:
            self.y = 0
            self.direction = 1
        elif self.y >= bottom:
            self.y = bottom
            self.direction = -1

    def _start_smooth_dash(self, d):
        bottom = self.bar_height - self.fish_height
        self.smooth_is_dashing = True
        self.smooth_dash_elapsed_ms = 0
        self.smooth_dash_cooldown_ms = 800
        self.smooth_dash_start_y = self.y
        dist = self._get_smooth_dash_distance(d)
        down = self.rand.random() < 0.5
        self.smooth_dash_target_y = min(bottom, self.y + dist) if down else max(0, self.y - dist)
        self.smooth_dash_total_ms = self._rand_between(260, 340) if d <= 50 else self._rand_between(220, 300)

    def _do_smooth_dash_tick(self, tick_ms):
        self.smooth_dash_elapsed_ms += tick_ms
        t = min(1.0, self.smooth_dash_elapsed_ms / float(self.smooth_dash_total_ms))
        curve = 1.0 - math.pow(1.0 - t, 3.2)
        self.y = self.smooth_dash_start_y + (self.smooth_dash_target_y - self.smooth_dash_start_y) * curve
        if t >= 1.0:
            self.y = self.smooth_dash_target_y
            self.smooth_is_dashing = False
            self._pick_smooth_subtle_move(self.current_difficulty)

    def _pick_smooth_subtle_move(self, d):
        bottom = self.bar_height - self.fish_height
        dist = self._get_smooth_subtle_distance(d)
        down = self.rand.random() < 0.5
        self.smooth_target_y = min(bottom, self.y + dist) if down else max(0, self.y - dist)
        self.smooth_travel_ms = self._rand_between(900, 1400)
        delta = abs(self.smooth_target_y - self.y)
        self.smooth_speed_px_per_ms = delta / self.smooth_travel_ms if self.smooth_travel_ms > 0 else 0

    def _do_smooth_tick(self, tick_ms, d):
        if self.smooth_dash_cooldown_ms > 0:
            self.smooth_dash_cooldown_ms -= tick_ms
        if self.smooth_is_dashing:
            self._do_smooth_dash_tick(tick_ms)
            return
        if self.smooth_dash_cooldown_ms <= 0 and self._roll_smooth_dash(d):
            self._start_smooth_dash(d)
            return
        move = self.smooth_speed_px_per_ms * tick_ms
        diff = self.smooth_target_y - self.y
        if abs(diff) <= move:
            self.y = self.smooth_target_y
            self._pick_smooth_subtle_move(d)
        else:
            self.y += math.copysign(move, diff)

    def update(self, tick_ms, difficulty):
        if difficulty != self.current_difficulty:
            self.current_difficulty = difficulty
            self.set_difficulty(difficulty)
        if self.type == FishAI.SMOOTH:
            self._do_smooth_tick(tick_ms, difficulty)
        elif self.type == FishAI.ACTIVE:
            self._do_active_tick(tick_ms)
        elif self.type == FishAI.HYPER:
            self._do_hyper_tick(tick_ms)
        elif self.type == FishAI.GLIDER:
            self._do_glider_tick(tick_ms)
        bottom = self.bar_height - self.fish_height
        self.y = max(0, min(bottom, self.y))
        return self.y


# ============================================================
# MAIN APPLICATION
# ============================================================
class FishingApp(tk.Tk):
    SCREEN_MENU    = "menu"
    SCREEN_GAME    = "game"
    SCREEN_MARKET  = "market"
    SCREEN_VICTORY = "victory"

    def __init__(self):
        super().__init__()
        self.title("Junior's Fishing Adventure")
        self.geometry(f"{WIN_W}x{WIN_H}")
        self.resizable(False, False)

        # ── game state ──────────────────────────────────────
        self.rand                = random.Random()
        self.current_stage       = 1
        self.current_bg_stage    = 0
        self.stage_score         = 0
        self.total_score         = 0
        self.time_remaining      = 90
        self.session_active      = False
        self.stage_ended         = False
        self.waiting_for_hook    = False
        self.rod_level           = 0
        self.green_height        = 100
        self.bobber_inventory    = [0]*5
        self.bobber_types        = [0]*5
        self.current_decay_rate  = PROGRESS_DECAY_RATE
        self.current_bite_chance = 0.50
        self.price_multiplier    = 1.0
        self.mod_menu_visible    = False

        # fishing state machine: "idle","searching","bite"
        self.fishing_state       = "idle"
        self.search_accumulator  = 0
        self.bite_start_time     = 0
        self.is_mini_game_active = False

        # mini game physics
        self.fish_y              = float(BAR_HEIGHT - 30)
        self.green_y             = BAR_HEIGHT - self.green_height
        self.bar_velocity        = 0.0
        self.green_progress_width = BAR_HEIGHT // 4
        self.space_pressed       = False
        self.new_round           = False
        self.tick_counter        = 0
        self.fish_ai             = None

        # difficulty / fish type (mod menu state)
        self.difficulty_var      = tk.StringVar(value="10")
        self.fish_type_var       = tk.StringVar(value="SMOOTH")

        # timer IDs
        self._game_timer_id      = None
        self._countdown_timer_id = None
        self._result_clear_id    = None

        # ── build UI ────────────────────────────────────────
        self._build_all_screens()
        self.show_screen(self.SCREEN_MENU)

    # ──────────────────────────────────────────────────────
    # SCREEN MANAGEMENT
    # ──────────────────────────────────────────────────────
    def _build_all_screens(self):
        self._build_menu_screen()
        self._build_game_screen()
        self._build_market_screen()
        self._build_victory_screen()

    def show_screen(self, name):
        for s in [self.menu_frame, self.game_frame, self.market_frame, self.victory_frame]:
            s.place_forget()
        if name == self.SCREEN_MENU:
            self.menu_frame.place(x=0, y=0, width=WIN_W, height=WIN_H)
        elif name == self.SCREEN_GAME:
            self.game_frame.place(x=0, y=0, width=WIN_W, height=WIN_H)
            self.game_frame.focus_set()
        elif name == self.SCREEN_MARKET:
            self._refresh_market_screen()
            self.market_frame.place(x=0, y=0, width=WIN_W, height=WIN_H)
        elif name == self.SCREEN_VICTORY:
            self.victory_frame.place(x=0, y=0, width=WIN_W, height=WIN_H)

    # ──────────────────────────────────────────────────────
    # MENU SCREEN
    # ──────────────────────────────────────────────────────
    def _build_menu_screen(self):
        self.menu_frame = tk.Frame(self, width=WIN_W, height=WIN_H, bg="#0A1E50")
        self.menu_frame.pack_propagate(False)

        c = tk.Canvas(self.menu_frame, width=WIN_W, height=WIN_H, bg="#0A1E50", highlightthickness=0)
        c.place(x=0, y=0)
        ps = 40
        for r, row in enumerate(MENU_BG):
            for col, idx in enumerate(row):
                if 0 <= idx < len(MENU_PALETTE):
                    c.create_rectangle(col*ps, r*ps, col*ps+ps, r*ps+ps,
                                       fill=MENU_PALETTE[idx], outline="")

        c.create_text(450, 85, text="Junior's Fishing Adventure",
                      font=("Georgia", 32, "bold"), fill="white", anchor="center")

        start_btn = tk.Button(self.menu_frame, text="START ADVENTURE!",
                              font=("Courier", 16, "bold"), bg="#4CAF50", fg="white",
                              relief="raised", bd=3, cursor="hand2",
                              command=self._start_new_game)
        start_btn.place(x=350, y=350, width=200, height=40)

        quit_btn = tk.Button(self.menu_frame, text="QUIT",
                             font=("Courier", 16, "bold"), bg="#D32F2F", fg="white",
                             relief="raised", bd=3, cursor="hand2",
                             command=self.destroy)
        quit_btn.place(x=350, y=420, width=200, height=40)

    # ──────────────────────────────────────────────────────
    # GAME SCREEN
    # ──────────────────────────────────────────────────────
    def _build_game_screen(self):
        self.game_frame = tk.Frame(self, width=WIN_W, height=WIN_H, bg="#0A1E50")
        self.game_frame.pack_propagate(False)

        # Background canvas (pixel art)
        self.bg_canvas = tk.Canvas(self.game_frame, width=WIN_W, height=WIN_H,
                                   bg="#0A1E50", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)
        self._draw_stage_bg(0)

        # Timer label
        self.timer_label = tk.Label(self.game_frame, text="1:30",
                                    font=("Courier", 34, "bold"), fg="white",
                                    bg="#0A1E50", anchor="e")
        self.timer_label.place(x=730, y=15, width=150, height=45)

        # Score label
        self.score_label = tk.Label(self.game_frame, text="Score: 0g",
                                    font=("Courier", 18), fg="#C8DCFF",
                                    bg="#0A1E50", anchor="e")
        self.score_label.place(x=730, y=60, width=150, height=28)

        # Stage label
        self.stage_label = tk.Label(self.game_frame, text="Stage: 1/5",
                                    font=("Courier", 16), fg="yellow",
                                    bg="#0A1E50", anchor="e")
        self.stage_label.place(x=730, y=88, width=150, height=25)

        # Status label
        self.status_label = tk.Label(self.game_frame, text="Click the button to fish!",
                                     font=("Courier", 12, "bold"), fg="yellow",
                                     bg="#0A1E50", anchor="center")
        self.status_label.place(x=630, y=580, width=280, height=30)

        # Result label
        self.result_label = tk.Label(self.game_frame, text="",
                                     font=("Courier", 11, "bold"), fg="white",
                                     bg="#0A1E50", anchor="center")
        self.result_label.place(x=630, y=610, width=280, height=25)

        # Control guide label
        self.control_guide_label = tk.Label(self.game_frame, text="",
                                            font=("Courier", 11), fg="white",
                                            bg="#0A1E50", anchor="center")
        self.control_guide_label.place(x=630, y=635, width=280, height=25)

        # Progress bar container
        self.prog_canvas = tk.Canvas(self.game_frame, width=PROG_W, height=BAR_HEIGHT,
                                     bg="red", highlightthickness=2,
                                     highlightbackground="black")
        self.prog_canvas.place(x=PROG_X, y=PROG_Y)
        init_gw = BAR_HEIGHT // 4
        self.prog_green = self.prog_canvas.create_rectangle(
            0, BAR_HEIGHT - init_gw, PROG_W, BAR_HEIGHT, fill="green", outline="")
        self.prog_red = self.prog_canvas.create_rectangle(
            0, 0, PROG_W, BAR_HEIGHT - init_gw, fill="red", outline="")

        # Bar container (fishing bar)
        self.bar_canvas = tk.Canvas(self.game_frame, width=BAR_WIDTH, height=BAR_HEIGHT,
                                    bg="#ADD8E6", highlightthickness=3,
                                    highlightbackground="black")
        self.bar_canvas.place(x=BAR_X, y=BAR_Y)

        # Green zone on bar
        self.green_zone_item = self.bar_canvas.create_rectangle(
            3, 0, BAR_WIDTH-3, self.green_height,
            fill="#00C800", stipple="", outline="black", width=2)

        # Fish indicator on bar
        self.fish_item = self.bar_canvas.create_oval(
            3, 0, BAR_WIDTH-5, 30, fill="yellow", outline="black", width=2)

        # Fishing overlay (semi-opaque gray over bar area)
        self.overlay_canvas = tk.Canvas(self.game_frame, width=95, height=BAR_HEIGHT,
                                        bg="#404040", highlightthickness=0)
        self.overlay_canvas.place(x=670, y=BAR_Y)
        # overlay visibility is managed in _update_hook_visuals via place/place_forget

        # Inventory slots
        self.inv_buttons = []
        for i in range(5):
            btn = tk.Button(self.game_frame, text="[  ]",
                            font=("Courier", 14, "bold"), bg="#B4B4B4",
                            relief="solid", bd=2, cursor="hand2",
                            command=lambda idx=i: None)
            btn.place(x=770, y=120 + i*65, width=100, height=60)
            self.inv_buttons.append(btn)

        # Hook button
        self.hook_btn = tk.Button(self.game_frame, text="Cast line",
                                  font=("Courier", 11, "bold"),
                                  bg=COLOR_IDLE, relief="raised", bd=3,
                                  cursor="hand2", command=self._handle_hook_click)
        self.hook_btn.place(x=770, y=450, width=100, height=100)

        # Mod menu widgets (initially hidden)
        self.mod_hide_btn = tk.Button(self.game_frame, text="HIDE MOD",
                                      font=("Courier", 9), command=self._toggle_mod_menu)
        self.mod_skip_btn = tk.Button(self.game_frame, text="SKIP LEVEL",
                                      font=("Courier", 9), command=self._skip_level)
        self.mod_diff_label = tk.Label(self.game_frame, text="Difficulty:",
                                       font=("Courier", 9), bg="#0A1E50", fg="white")
        self.mod_diff_entry = tk.Entry(self.game_frame, textvariable=self.difficulty_var,
                                       font=("Courier", 10), width=8)
        fish_types = ["SMOOTH", "ACTIVE", "HYPER", "GLIDER"]
        self.mod_type_combo = tk.OptionMenu(self.game_frame, self.fish_type_var, *fish_types)
        self.mod_new_fish_btn = tk.Button(self.game_frame, text="New Fish",
                                         font=("Courier", 9), command=self._restart_hook_random)

        # Key bindings
        self.game_frame.bind("<KeyPress-space>",   lambda e: self._set_space(True))
        self.game_frame.bind("<KeyRelease-space>", lambda e: self._set_space(False))
        self.game_frame.bind("<KeyPress-r>",       lambda e: self._restart_hook_random())
        self.game_frame.bind("<KeyPress-F7>",      lambda e: self._toggle_mod_menu())
        self.game_frame.bind("<KeyPress-f>",       lambda e: self._toggle_mod_menu())

    def _set_space(self, val):
        self.space_pressed = val

    def _draw_stage_bg(self, stage_idx):
        self.bg_canvas.delete("bg")
        bg   = STAGE_BACKGROUNDS[stage_idx]
        pal  = STAGE_PALETTES[stage_idx]
        ps   = BG_PIXEL_SIZE
        for r, row in enumerate(bg):
            for col, idx in enumerate(row):
                color = pal[idx] if 0 <= idx < len(pal) else pal[0]
                self.bg_canvas.create_rectangle(
                    col*ps, r*ps, col*ps+ps, r*ps+ps,
                    fill=color, outline="", tags="bg")

    # MARKET SCREEN
    def _build_market_screen(self):
        self.market_frame = tk.Frame(self, width=WIN_W, height=WIN_H, bg="#D2AA78")
        self.market_frame.pack_propagate(False)

        mc = tk.Canvas(self.market_frame, width=WIN_W, height=WIN_H,
                       bg="#D2AA78", highlightthickness=0)
        mc.place(x=0, y=0)
        ts = 25
        for r, row in enumerate(MARKET_BG):
            for col, idx in enumerate(row):
                if 0 <= idx < len(MARKET_PALETTE):
                    mc.create_rectangle(col*ts, r*ts, col*ts+ts, r*ts+ts,
                                        fill=MARKET_PALETTE[idx], outline="")

        # Dialogue text
        mc.create_text(95, 85,  text="Howdy! Name's Sam Marlin.", font=("Georgia",18,"bold"), fill="black", anchor="w")
        mc.create_text(95, 115, text="Welcome to my shop!", font=("Georgia",18,"bold"), fill="black", anchor="w")
        mc.create_text(95, 145, text="Fancy for some upgrades?", font=("Georgia",18,"bold"), fill="black", anchor="w")

        # Earnings & stage labels (dynamic — stored as canvas items)
        self.market_earnings_item = mc.create_text(
            120, 485, text="Earnings: 0g",
            font=("Courier", 16, "bold"), fill="#8B4513", anchor="center")
        self.market_stage_item = mc.create_text(
            120, 450, text="Stage: 1/5",
            font=("Courier", 16, "bold"), fill="black", anchor="center")
        self.market_canvas = mc

        # Inventory panel (static background)
        inv_bg = tk.Frame(self.market_frame, bg="#FFF8DC", bd=2, relief="solid")
        inv_bg.place(x=10, y=510, width=220, height=180)
        inv_title = tk.Label(inv_bg, text="INVENTORY", font=("Courier",12,"bold"),
                             bg="#FFF8DC")
        inv_title.pack(pady=(8,0))
        self.inv_labels = []
        for i in range(5):
            lbl = tk.Label(inv_bg, text=f"Slot {i+1}: Empty",
                           font=("Courier",10), bg="#FFF8DC", fg="gray")
            lbl.pack(anchor="w", padx=10)
            self.inv_labels.append(lbl)

        # Shop buttons
        rod_btn = tk.Button(self.market_frame,
                            text="Rod Upgrade\n250g-10000g",
                            font=("Courier",11), bg="#E8E8E8", cursor="hand2",
                            command=self._purchase_rod_upgrade)
        rod_btn.place(x=540, y=20, width=130, height=70)

        ease_btn = tk.Button(self.market_frame,
                             text="Ease Bobber\n500g (10 uses)",
                             font=("Courier",11), bg="#ADD8E6", cursor="hand2",
                             command=self._purchase_ease_bobber)
        ease_btn.place(x=680, y=20, width=130, height=70)

        chum_btn = tk.Button(self.market_frame,
                             text="Chum Bobber\n1000g (10 uses)",
                             font=("Courier",11), bg="#FFB6C1", cursor="hand2",
                             command=self._purchase_chum_bobber)
        chum_btn.place(x=540, y=150, width=130, height=70)

        gold_btn = tk.Button(self.market_frame,
                             text="Golden Bobber\n2000g (10 uses)",
                             font=("Courier",11), bg="#FFD700", cursor="hand2",
                             command=self._purchase_golden_bobber)
        gold_btn.place(x=680, y=150, width=130, height=70)

        continue_btn = tk.Button(self.market_frame, text="→ READY! ←",
                                 font=("Courier",16,"bold"), bg="#64B464", fg="white",
                                 cursor="hand2", command=self._advance_to_next_stage)
        continue_btn.place(x=320, y=530, width=250, height=50)

        menu_btn = tk.Button(self.market_frame, text="MAIN MENU",
                             font=("Courier",14), bg="#B4B4B4", cursor="hand2",
                             command=self._confirm_return_to_menu)
        menu_btn.place(x=350, y=600, width=200, height=40)

    def _refresh_market_screen(self):
        self.market_canvas.itemconfig(
            self.market_earnings_item, text=f"Earnings: {self.stage_score}g")
        self.market_canvas.itemconfig(
            self.market_stage_item, text=f"Stage: {self.current_stage}/5")

        rod_names = ["Poor","Basic","Fine","Sturdy","Reinforced","Carbon Fiber","Master"]
        rod_name = rod_names[self.rod_level] if self.rod_level < len(rod_names) else "Master"
        for i, lbl in enumerate(self.inv_labels):
            if i == 0:
                lbl.config(text=f"Rod: {rod_name} (Lv{self.rod_level})", fg="black")
            else:
                bi = i - 1
                if self.bobber_inventory[bi] > 0:
                    tn = {1:"Ease",2:"Chum",3:"Golden"}.get(self.bobber_types[bi],"?")
                    lbl.config(text=f"Slot {bi+1}: {tn} ({self.bobber_inventory[bi]}/10)", fg="black")
                else:
                    lbl.config(text=f"Slot {bi+1}: Empty", fg="gray")

    def _confirm_return_to_menu(self):
        if messagebox.askyesno("Leave session?",
                               "Are you sure you want to leave today's session?\nYour progress will be lost!"):
            self._cancel_timers()
            self.show_screen(self.SCREEN_MENU)

    # ──────────────────────────────────────────────────────
    # VICTORY SCREEN
    # ──────────────────────────────────────────────────────
    def _build_victory_screen(self):
        self.victory_frame = tk.Frame(self, width=WIN_W, height=WIN_H, bg="#FFD700")
        self.victory_frame.pack_propagate(False)

        vc = tk.Canvas(self.victory_frame, width=WIN_W, height=WIN_H,
                       bg="#FFD700", highlightthickness=0)
        vc.place(x=0, y=0)
        ts = 32
        for r, row in enumerate(VICTORY_BG):
            for col, idx in enumerate(row):
                if 0 <= idx < len(VICTORY_PALETTE):
                    vc.create_rectangle(col*ts, r*ts, col*ts+ts, r*ts+ts,
                                        fill=VICTORY_PALETTE[idx], outline="")

        vc.create_text(450, 50, text="CONGRATULATIONS!",
                       font=("Georgia",36,"bold"), fill="#8B4513", anchor="center")
        vc.create_text(450, 95, text="You went home safe and satisfied.",
                       font=("Courier",18), fill="#8B4513", anchor="center")
        vc.create_text(450, 125, text="The captain admires your fishing prowess.",
                       font=("Courier",18), fill="#8B4513", anchor="center")

        menu_btn = tk.Button(self.victory_frame, text="Back to Menu",
                             font=("Courier",16,"bold"), bg="#64B464", fg="white",
                             cursor="hand2", command=lambda: self.show_screen(self.SCREEN_MENU))
        menu_btn.place(x=350, y=145, width=200, height=50)

    # ──────────────────────────────────────────────────────
    # GAME START / RESET
    # ──────────────────────────────────────────────────────
    def _start_new_game(self):
        self.rod_level           = 0
        self.green_height        = 100
        self.bobber_inventory    = [0]*5
        self.bobber_types        = [0]*5
        self.current_decay_rate  = PROGRESS_DECAY_RATE
        self.current_bite_chance = 0.50
        self.price_multiplier    = 1.0
        self.total_score         = 0
        self.mod_menu_visible    = False
        self._hide_mod_menu()
        self._reset_to_stage1()
        self.show_screen(self.SCREEN_GAME)
        self.after(100, self._play_intro_dialogue)

    def _play_intro_dialogue(self):
        msgs = [
            "Hey kid, you've been chosen for the Junior Fishers Club trip today.",
            "Hope you've got the skills for your selected profession.",
            "If you don't, I'll send you back home.",
            "Now do me a favor and start fishing, okay?",
            "There's a fishmonger who buys our catch for trip money.",
            "This happens after the session. We've got no time to lose!",
            "I need 500g before we continue to our next trip.",
        ]
        for m in msgs:
            messagebox.showinfo("Captain", m)
        self.session_active = True
        self.is_mini_game_active = False
        self.stage_ended = False
        self.fishing_state = "idle"
        self._update_hook_visuals()
        self._reset_mini_game()
        self._start_countdown()
        self.game_frame.focus_set()

    def _reset_to_stage1(self):
        self.current_stage    = 1
        self.current_bg_stage = 0
        self.stage_ended      = False
        self.waiting_for_hook = False
        self._reset_score()
        self._reset_timer()
        self._update_stage_labels()
        self._draw_stage_bg(0)

    def _reset_score(self):
        self.stage_score = 0
        self.score_label.config(text="Score: 0g", fg="#C8DCFF")

    def _reset_timer(self):
        self.time_remaining = 90
        self.timer_label.config(text="1:30", fg="white")

    def _update_stage_labels(self):
        self.stage_label.config(text=f"Stage: {self.current_stage}/5")
        r = STAGE_DIFFICULTY[self.current_stage - 1]
        self.difficulty_var.set(str((r[0]+r[1])//2))

    def _reset_mini_game(self):
        self.space_pressed       = False
        self.new_round           = True
        self.tick_counter        = 0
        self.bar_velocity        = 0.0
        self.fish_y              = float(BAR_HEIGHT - 30)
        self.green_y             = BAR_HEIGHT - self.green_height
        self.green_progress_width = BAR_HEIGHT // 4

        t = self.fish_type_var.get()
        type_map = {"SMOOTH": FishAI.SMOOTH, "ACTIVE": FishAI.ACTIVE,
                    "HYPER": FishAI.HYPER,   "GLIDER": FishAI.GLIDER}
        ft = type_map.get(t, FishAI.SMOOTH)
        d  = self._parse_difficulty()
        self.fish_ai = FishAI(ft, self.fish_y, BAR_HEIGHT, 30, TIMER_MS, d)

        # Update canvas items
        self.bar_canvas.coords(self.green_zone_item,
                               3, self.green_y, BAR_WIDTH-3, self.green_y + self.green_height)
        self.bar_canvas.coords(self.fish_item, 3, 0, BAR_WIDTH-5, 30)
        self._update_progress_bar()

    def _parse_difficulty(self):
        try:
            return max(1, min(100, int(self.difficulty_var.get())))
        except ValueError:
            r = STAGE_DIFFICULTY[self.current_stage - 1]
            return self.rand.randint(r[0], r[1])

    # ──────────────────────────────────────────────────────
    # TIMERS
    # ──────────────────────────────────────────────────────
    def _cancel_timers(self):
        if self._game_timer_id:
            self.after_cancel(self._game_timer_id)
            self._game_timer_id = None
        if self._countdown_timer_id:
            self.after_cancel(self._countdown_timer_id)
            self._countdown_timer_id = None

    def _start_game_timer(self):
        if self._game_timer_id is None:
            self._game_timer_id = self.after(TIMER_MS, self._game_tick)

    def _start_countdown(self):
        if self._countdown_timer_id is None:
            self._countdown_timer_id = self.after(1000, self._update_countdown)

    def _update_countdown(self):
        self._countdown_timer_id = None
        if not self.session_active:
            return
        if self.time_remaining > 0:
            self.time_remaining -= 1
            m, s = divmod(self.time_remaining, 60)
            self.timer_label.config(text=f"{m}:{s:02d}",
                                    fg="red" if self.time_remaining <= 10 else "white")
            self._countdown_timer_id = self.after(1000, self._update_countdown)
        else:
            if self.is_mini_game_active:
                self.waiting_for_hook = True
                self.status_label.config(text="Time ran out. LAST FISH!", fg="red")
                self.control_guide_label.config(text="")
            else:
                self._evaluate_stage_progress()

    # ──────────────────────────────────────────────────────
    # FISHING STATE MACHINE
    # ──────────────────────────────────────────────────────
    def _show_overlay(self):
        if hasattr(self, 'overlay_canvas'):
            self.overlay_canvas.place(x=670, y=BAR_Y)

    def _hide_overlay(self):
        if hasattr(self, 'overlay_canvas'):
            self.overlay_canvas.place_forget()

    def _update_hook_visuals(self):
        if self.fishing_state == "idle":
            self.hook_btn.config(text="Cast line", bg=COLOR_IDLE,
                                 state="disabled" if self.stage_ended else "normal")
            self.status_label.config(text="Click the button to fish!", fg="yellow")
            self.control_guide_label.config(text="")
            self._show_overlay()
        elif self.fishing_state == "searching":
            self.hook_btn.config(text="Search...", bg=COLOR_SEARCHING,
                                 state="disabled" if self.stage_ended else "normal")
            self.status_label.config(text="Stay alert...", fg="yellow")
            self.control_guide_label.config(text="")
            self._show_overlay()
        elif self.fishing_state == "bite":
            self.hook_btn.config(text="HOOK!", bg=COLOR_BITE,
                                 state="disabled" if self.stage_ended else "normal")
            self.status_label.config(text="Press SPACE to control the hook.", fg="yellow")
            self.control_guide_label.config(text="(Hold SPACE to rise, release to fall)")
            self._hide_overlay()

    def _handle_hook_click(self):
        if self.is_mini_game_active or self.stage_ended:
            return
        if self.fishing_state == "idle":
            self.fishing_state = "searching"
            self.search_accumulator = 0
            self._update_hook_visuals()
            self._start_game_timer()
        elif self.fishing_state == "searching":
            self.fishing_state = "idle"
            self._update_hook_visuals()
        elif self.fishing_state == "bite":
            # Pick random difficulty & fish type for this catch
            r = STAGE_DIFFICULTY[self.current_stage - 1]
            d = self.rand.randint(r[0], r[1])
            self.difficulty_var.set(str(d))
            tc = self.rand.randint(0, 99)
            if self.current_stage <= 2:
                t = "SMOOTH" if tc < 50 else "ACTIVE" if tc < 85 else "HYPER" if tc < 95 else "GLIDER"
            elif self.current_stage <= 4:
                t = "SMOOTH" if tc < 35 else "ACTIVE" if tc < 70 else "HYPER" if tc < 90 else "GLIDER"
            else:
                t = "SMOOTH" if tc < 25 else "ACTIVE" if tc < 55 else "HYPER" if tc < 85 else "GLIDER"
            self.fish_type_var.set(t)
            self.fishing_state = "idle"
            self._update_hook_visuals()
            self._start_fishing_mini_game()

    def _update_fishing_state_machine(self):
        if self.is_mini_game_active or self.stage_ended:
            return
        if self.fishing_state == "searching":
            self.search_accumulator += TIMER_MS
            if self.search_accumulator >= SEARCH_CHECK_MS:
                self.search_accumulator = 0
                if self.rand.random() < self.current_bite_chance:
                    self.fishing_state = "bite"
                    self.bite_start_time = time.time()
                    self._update_hook_visuals()
        elif self.fishing_state == "bite":
            elapsed_ms = (time.time() - self.bite_start_time) * 1000
            if elapsed_ms > BITE_WINDOW_MS:
                self.fishing_state = "idle"
                self.status_label.config(
                    text="You hooked but there was no fish to hook!", fg="orange")
                self._update_hook_visuals()

    def _start_fishing_mini_game(self):
        self.is_mini_game_active = True
        self.hook_btn.config(state="disabled")
        self._hide_overlay()
        self._reset_mini_game()
        self._start_game_timer()

    def _end_fishing_session(self):
        self.is_mini_game_active = False
        self.fishing_state = "idle"
        self._update_hook_visuals()
        if self.waiting_for_hook:
            self.waiting_for_hook = False
            self._evaluate_stage_progress()

    # ──────────────────────────────────────────────────────
    # GAME TICK (10ms loop)
    # ──────────────────────────────────────────────────────
    def _game_tick(self):
        self._game_timer_id = None
        self.tick_counter += 1
        self._update_fishing_state_machine()

        if self.is_mini_game_active and not self.stage_ended:
            d = self._parse_difficulty()

            # Update green zone physics
            if self.new_round:
                self.bar_velocity += GRAVITY
                self.new_round = False
            else:
                self.bar_velocity += -UP_ACCEL if self.space_pressed else GRAVITY

            self.bar_velocity = max(-MAX_BAR_SPEED, min(MAX_BAR_SPEED, self.bar_velocity))
            self.green_y = int(self.green_y + self.bar_velocity)
            if self.green_y < 0:
                self.green_y = 0
                if self.bar_velocity < 0: self.bar_velocity = 0
            elif self.green_y + self.green_height > BAR_HEIGHT:
                self.green_y = BAR_HEIGHT - self.green_height
                if self.bar_velocity > 0: self.bar_velocity = 0

            # Update fish AI
            if self.fish_ai is None:
                self.fish_ai = FishAI(FishAI.SMOOTH, BAR_HEIGHT-30, BAR_HEIGHT, 30, TIMER_MS, d)
            self.fish_y = self.fish_ai.update(TIMER_MS, d)

            # Update canvas items
            gy = int(self.green_y)
            fy = int(self.fish_y)
            self.bar_canvas.coords(self.green_zone_item,
                                   3, gy, BAR_WIDTH-3, gy + self.green_height)
            self.bar_canvas.coords(self.fish_item, 3, fy, BAR_WIDTH-5, fy+30)

            # Progress
            in_green = (self.fish_y + 30 > self.green_y) and (self.fish_y < self.green_y + self.green_height)
            self.green_progress_width += PROGRESS_FILL_RATE if in_green else self.current_decay_rate
            self.green_progress_width = max(0, min(BAR_HEIGHT, self.green_progress_width))
            self._update_progress_bar()

            # Win / lose
            if self.green_progress_width >= BAR_HEIGHT:
                # CAUGHT
                self._game_timer_id = None  # don't reschedule
                pts = self._add_points_for_catch()
                self.result_label.config(text=f"Fish Caught! +{pts}g", fg="#64FF64")
                if self._result_clear_id:
                    self.after_cancel(self._result_clear_id)
                self._result_clear_id = self.after(2500, lambda: self.result_label.config(text=""))
                self._end_fishing_session()
                return
            elif self.green_progress_width <= 0 and self.tick_counter > 10:
                # ESCAPED
                self._game_timer_id = None
                self.result_label.config(text="Fish got away!", fg="red")
                if self._result_clear_id:
                    self.after_cancel(self._result_clear_id)
                self._result_clear_id = self.after(2500, lambda: self.result_label.config(text=""))
                self._end_fishing_session()
                return

        self._game_timer_id = self.after(TIMER_MS, self._game_tick)

    def _update_progress_bar(self):
        gw = int(self.green_progress_width)
        gt = BAR_HEIGHT - gw
        self.prog_canvas.coords(self.prog_green, 0, gt, PROG_W, BAR_HEIGHT)
        self.prog_canvas.coords(self.prog_red,   0, 0,  PROG_W, gt)

    # ──────────────────────────────────────────────────────
    # SCORING & STAGE EVALUATION
    # ──────────────────────────────────────────────────────
    def _add_points_for_catch(self):
        d = self._parse_difficulty()
        ft = self.fish_type_var.get()
        si = self.current_stage - 1
        is_hyper = (ft == "HYPER")
        base_val = STAGE_BASE_VALUES[si][1 if is_hyper else 0]
        type_idx = {"SMOOTH":0,"ACTIVE":1,"HYPER":2,"GLIDER":3}.get(ft, 0)
        bonus = FISH_BONUS[type_idx]
        pts = int(round(base_val * bonus * (0.5 + d/100.0) * self.price_multiplier))
        self.stage_score += pts
        self.total_score += pts
        self.score_label.config(text=f"Score: {self.stage_score}g", fg="yellow")
        self.after(200, lambda: self.score_label.config(fg="#C8DCFF"))
        self._use_bobber()
        return pts

    def _use_bobber(self):
        for i in range(5):
            if self.bobber_inventory[i] > 0:
                self.bobber_inventory[i] -= 1
                bt = self.bobber_types[i]
                if self.bobber_inventory[i] == 0:
                    self.bobber_types[i] = 0
                    if bt == 1: self.current_decay_rate = PROGRESS_DECAY_RATE
                    elif bt == 2: self.current_bite_chance = 0.50
                    elif bt == 3: self.price_multiplier = 1.0
                self._update_inv_buttons()
                break

    def _update_inv_buttons(self):
        for i, btn in enumerate(self.inv_buttons):
            if self.bobber_inventory[i] > 0:
                icons = {1:"[B]",2:"[C]",3:"[G]"}
                icon = icons.get(self.bobber_types[i], "[ ]")
                colors = {1:"#ADD8E6",2:"#FFB6C1",3:"#FFD700"}
                bg = colors.get(self.bobber_types[i], "#B4B4B4")
                btn.config(text=f"{icon} {self.bobber_inventory[i]}", bg=bg)
            else:
                btn.config(text="[  ]", bg="#B4B4B4")

    def _evaluate_stage_progress(self):
        self.session_active = False
        self.stage_ended    = True
        self.hook_btn.config(state="disabled")

        if self.stage_score >= STAGE_TARGET:
            if self.current_stage == MAX_STAGES:
                messagebox.showinfo("Final Stage Complete!",
                    f"Stage {self.current_stage} Complete!\n"
                    f"You earned {self.stage_score}g (Target: {STAGE_TARGET}g)\n"
                    "You've completed all stages!")
                self.show_screen(self.SCREEN_VICTORY)
            else:
                fee = CAPTAIN_FEES[self.current_stage - 1]
                if self.stage_score >= fee:
                    self.stage_score -= fee
                    messagebox.showinfo("Success!",
                        f"Stage {self.current_stage} Complete!\n"
                        f"Captain's Fee: {fee}g deducted!\n"
                        f"Remaining for shop: {self.stage_score}g\n"
                        "Visit the fishmonger to spend your gold!")
                    self.show_screen(self.SCREEN_MARKET)
                else:
                    messagebox.showwarning("GAME OVER",
                        f"Game Over!\nYou earned {self.stage_score + fee}g "
                        f"but couldn't pay the Captain's fee!\n"
                        f"Fee required: {fee}g")
                    self._do_reset_and_menu()
        else:
            messagebox.showwarning("GAME OVER",
                f"Game Over!\nYou only earned {self.stage_score}g\n"
                f"Target was {STAGE_TARGET}g")
            self._do_reset_and_menu()

    def _do_reset_and_menu(self):
        self.rod_level          = 0
        self.green_height       = 100
        self.bobber_inventory   = [0]*5
        self.bobber_types       = [0]*5
        self.current_decay_rate = PROGRESS_DECAY_RATE
        self.current_bite_chance = 0.50
        self.price_multiplier   = 1.0
        self.total_score        = 0
        self._update_inv_buttons()
        self.show_screen(self.SCREEN_MENU)

    # ──────────────────────────────────────────────────────
    # STAGE ADVANCEMENT (from market "READY" button)
    # ──────────────────────────────────────────────────────
    def _advance_to_next_stage(self):
        if self.current_stage <= MAX_STAGES:
            fee = CAPTAIN_FEES[self.current_stage - 1]
            if self.stage_score < fee:
                messagebox.showwarning("Sam Marlin",
                    f"Warning: Running low on money.\n"
                    f"Captain's fee coming up: {fee}g")
            else:
                self.stage_score -= fee

        self.current_stage += 1
        self.stage_ended       = False
        self.waiting_for_hook  = False

        if self.current_stage > MAX_STAGES:
            messagebox.showinfo("VICTORY!",
                f"CONGRATULATIONS!\nYou completed all 5 stages!\n"
                f"Total earnings: {self.total_score}g\n"
                "The Captain is proud of you, kid!")
            self._reset_to_stage1()
            self.show_screen(self.SCREEN_MENU)
        else:
            self._reset_score()
            self._reset_timer()
            self._update_stage_labels()
            self._update_hook_visuals()
            self._draw_stage_bg(self.current_stage - 1)
            self.current_bg_stage = self.current_stage - 1
            self.show_screen(self.SCREEN_GAME)
            self.game_frame.focus_set()

            captain_msgs = {
                2: "Not bad for a Junior Fisherman.\nI need 1,000g before our next trip.",
                3: "Feel the warmth?\nI need 1,500g before our next trip.",
                4: "Don't ask why.\nI need 2,500g before our next trip.",
                5: "Great job. Final stretch.\nI need 5,000g for a special surprise.",
            }
            msg = captain_msgs.get(self.current_stage,
                                   "I need 500g before we continue.")
            self.after(100, lambda: self._stage_transition_dialogue(msg))

    def _stage_transition_dialogue(self, msg):
        messagebox.showinfo("Captain", msg)
        self.session_active = True
        self._reset_mini_game()
        self._start_countdown()
        self.game_frame.focus_set()

    # ──────────────────────────────────────────────────────
    # PURCHASES
    # ──────────────────────────────────────────────────────
    def _purchase_rod_upgrade(self):
        prices = [250, 500, 1000, 2500, 5000, 10000]
        if self.rod_level >= len(prices):
            messagebox.showinfo("Max Level", "Rod already at max level!"); return
        cost = prices[self.rod_level]
        if self.stage_score >= cost:
            self.stage_score -= cost
            self.rod_level   += 1
            self.green_height += 10
            self.bar_canvas.coords(self.green_zone_item,
                                   3, self.green_y, BAR_WIDTH-3, self.green_y+self.green_height)
            self._refresh_market_screen()
            messagebox.showinfo("Upgrade Success",
                f"Rod upgraded to Level {self.rod_level}!\nGreen zone increased by 10px!")
        else:
            messagebox.showwarning("Insufficient Funds",
                f"Need {cost}g! You have: {self.stage_score}g")

    def _purchase_ease_bobber(self):
        self._purchase_bobber(1, 500, "Ease Bobber")

    def _purchase_chum_bobber(self):
        self._purchase_bobber(2, 1000, "Chum Bobber")

    def _purchase_golden_bobber(self):
        self._purchase_bobber(3, 2000, "Golden Bobber")

    def _purchase_bobber(self, btype, cost, name):
        slot = next((i for i in range(5) if self.bobber_inventory[i] == 0), -1)
        if slot == -1:
            messagebox.showwarning("Full", "Bobber inventory full! (5/5 slots)"); return
        if self.stage_score >= cost:
            self.stage_score -= cost
            self.bobber_inventory[slot] = 10
            self.bobber_types[slot]     = btype
            if btype == 1: self.current_decay_rate  = -2.0
            elif btype == 2: self.current_bite_chance = 0.80
            elif btype == 3: self.price_multiplier   = 2.0
            self._refresh_market_screen()
            self._update_inv_buttons()
            messagebox.showinfo("Purchase Success", f"{name} purchased!\nAdded to slot {slot+1}.")
        else:
            messagebox.showwarning("Insufficient Funds",
                f"Need {cost}g! You have: {self.stage_score}g")

    # ──────────────────────────────────────────────────────
    # MOD MENU
    # ──────────────────────────────────────────────────────
    def _toggle_mod_menu(self):
        self.mod_menu_visible = not self.mod_menu_visible
        if self.mod_menu_visible:
            self._show_mod_menu()
        else:
            self._hide_mod_menu()

    def _show_mod_menu(self):
        for btn in self.inv_buttons:
            btn.place_forget()
        self.mod_hide_btn.place(x=770, y=120, width=100, height=36)
        self.mod_skip_btn.place(x=770, y=170, width=100, height=36)
        self.mod_diff_label.place(x=770, y=220, width=120, height=25)
        self.mod_diff_entry.place(x=770, y=250, width=100, height=30)
        self.mod_type_combo.place(x=770, y=290, width=100, height=30)
        self.mod_new_fish_btn.place(x=770, y=360, width=100, height=36)

    def _hide_mod_menu(self):
        for w in [self.mod_hide_btn, self.mod_skip_btn, self.mod_diff_label,
                  self.mod_diff_entry, self.mod_type_combo, self.mod_new_fish_btn]:
            if hasattr(self, w.winfo_name() if hasattr(w,'winfo_name') else '__x__'):
                pass
            w.place_forget()
        for i, btn in enumerate(self.inv_buttons):
            btn.place(x=770, y=120+i*65, width=100, height=60)

    def _skip_level(self):
        self.stage_score = 5000
        messagebox.showinfo("Mod Menu", "SKIP LEVEL ACTIVATED!\nGranted 5000g.\nVisit the fishmonger!")
        self._evaluate_stage_progress()

    def _restart_hook_random(self):
        r = STAGE_DIFFICULTY[self.current_stage - 1]
        self.difficulty_var.set(str(self.rand.randint(r[0], r[1])))
        self._reset_mini_game()


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    app = FishingApp()
    app.mainloop()
