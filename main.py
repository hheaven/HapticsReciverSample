import sys
import time

from PIL import Image

import PrintWindow
import HapticsReciverBlock
import HapticsReciverCode128



#
def main():
    #
    reciver = HapticsReciverBlock.HapticsReciverBlock( area = ( 8, 1 ), threshold = 8 )
    # reciver = HapticsReciverCode128.HapticsReciverCode128( area = ( 1, 8 ), one_block = ( 256, 4 ) )

    print( type( reciver ) )

    #
    window_name = "VRChat"

    hwnd    = PrintWindow.findHwnd( window_name )
    while True:
        #
        if not hwnd:
            time.sleep( 10 )
            hwnd    = PrintWindow.findHwnd( window_name )

            if not hwnd:
                continue

        #
        try:
            client_rect     = PrintWindow.getClientRect( hwnd )
        except Exception as e:
            print( e )
            hwnd    = None
            continue

        capture_rect    = reciver.rect( client_rect )

        #
        bmp = PrintWindow.printWindow( hwnd, capture_rect )

        #
        info    = bmp[ 0 ]
        bits    = bmp[ 1 ]
        margin  = bmp[ 2 ]

        # print( info )

        w   = info[ "bmWidth" ]
        h   = info[ "bmHeight" ]

        # bitsのデータはBGRAの並びになってるけど気にしない
        img = Image.frombytes( 'RGBA', ( w, h ), bits, 'raw' )

        # ウィンドウフレーム分を切り抜き
        img = img.crop( ( margin[ 0 ], margin[ 1 ], w, h ) )
        # img.save( "test1.bmp" )


        if type( reciver ) == HapticsReciverBlock.HapticsReciverBlock:
            # 処理サイズに拡大縮小
            img = img.resize( ( reciver.block_area[ 0 ] * HapticsReciverBlock.BLOCK_SIZE, reciver.block_area[ 1 ] * HapticsReciverBlock.BLOCK_SIZE ), Image.NEAREST )
            # img.save( "test2.bmp" )


            # 画像データから値を更新
            reciver.update( img.getdata() )

        else:
            # 画像データから値を更新
            reciver.update( img )


        #
        print( reciver.value )

        time.sleep( 0.1 )

    return  0


if __name__ == "__main__":
    sys.exit( main() )
