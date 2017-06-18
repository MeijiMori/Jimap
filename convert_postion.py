#!
# -*- coding: utf-8 -*-
import math
import pdb

L = 85.05112878
PAI = math.pi

def convert_longlati_topixcel(latitude, longitude, z):
    px,py = 0,0
    px = math.pow(2, z + 7) * (longitude / 180 + 1)
    py = (math.pow(2, z + 7) / PAI) \
            * (-1 * math.atanh(math.sin((PAI / 180) * latitude)) \
            + math.atanh(math.sin((PAI / 180) * L)))
    return px, py

def convert_pixcel_tolonglati(pixel_x, pixel_y, z):
    Longitude,Latitude = 0,0
    Longitude = 180 * (pixel_x / math.pow(2, z + 7) - 1)
    Latitude = 180 / PAI \
            * (math.asin(math.tanh(-1 * (PAI / math.pow(2, z + 7) * pixel_y) \
            + math.atanh(math.sin((PAI / 180) * L)))))

    return Latitude, Longitude

def long2_tile(longitude, zoom):
    return (math.floor((longitude + 180) / 360 * math.pow(2, zoom)))

def lat2_tile(longitude, zoom):
    return (math.floor((1 - math.log(math.tan(latitude * PAI / 180) + 1 \
            / math.cos(latitude * PAI / 180)) / PAI) / 2 * math.pow(2, zoom)))

def tile2_long(x, zoom):
    return (x / math.pow(2, zoom) * 360 - 180)

def tile2_lat(y, zoom):
    n = PAI - 2 * PAI * y / math.pow(2, zoom)
    return (180 / PAI * math.atan(0.5 * (math.exp(n) - math.exp(-n))))

if __name__ == '__main__':
    #latitude  = 35.43134  # ido
    #longitude = 139.26086 # kdo
    #z = 5                # zoom level
    #yt = math.pow(2, z + 7) / pai
    #print "yt : {0}".format(yt)

    #x,y = convert_longlati_topixcel(latitude, longitude, z)
    #Latitude, Longitude = convert_pixcel_tolonglati(x, y, z)
    #print "zoom level : {0}".format(z)
    #print "pixel_x : {0} / pixel_y : {1}".format(x,y)
    #print "tile_x : {0} / tile_y : {1}".format(x / 256, y / 256)
    #print "tile_x of position x : {0} / tile_y of position y : {1}".format(x % 256, y % 256)
    #print "latitude : {0} / longitude : {1}".format(Latitude, Longitude)
    #tile_x = 127
    #tile_y = 83
    #latitude, longitude = convert_pixcel_tolonglati(tile_x, tile_y, 8)
    zoom = 5
    latitude = 46.848355
    longitude = 128.142854

    pic_x, pic_y = convert_longlati_topixcel(latitude, longitude, zoom)
    Latitude, Longitude = convert_pixcel_tolonglati(pic_x, pic_y, zoom)

    pic_x2 = long2_tile(longitude, zoom)
    pic_y2 = lat2_tile(latitude, zoom)
    Latitude2 = tile2_lat(pic_y2, zoom)
    Longitude2 = tile2_long(pic_x2, zoom)
    print "tile_x : {0} / tile_y : {1}".format(pic_x/ 256, pic_y/ 256)
    print "latitude : {0} / longitude : {1}".format(Latitude, Longitude)
    print "tile_x2 : {0} / tile_y2 : {1}".format(pic_x2, pic_y2)
    print "latitude2 : {0} / longitude2 : {1}".format(Latitude2, Longitude2)
    #pdb.set_trace()
