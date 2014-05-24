import gtk.gdk as gg
import cv2
import os

def get_screenshot(x=0, y=0, w=None, h=None):
    window = gg.get_default_root_window()
    if not (w and h):
        w, h = window.get_size()
    pixbuf = gg.Pixbuf(gg.COLORSPACE_RGB, False, 8, w, h)
    pixbuf = pixbuf.get_from_drawable(window, window.get_colormap(),x,y,0,0,w,h)
    pixbuf.save('sc.png', 'png')
    img = cv2.imread('sc.png',0)
    os.remove('sc.png')
    return img

