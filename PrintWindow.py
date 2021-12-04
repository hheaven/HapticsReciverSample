import win32gui
import win32ui
from ctypes import windll


#
def findHwnd( window_name ):
    def enumWindowsCallback( hwnd, args ):
        if win32gui.IsWindowVisible( hwnd ) and win32gui.IsWindowEnabled( hwnd ):
            txt = win32gui.GetWindowText( hwnd )

            if txt.find( args[ 1 ] ) != -1:
                print( txt, args[ 1 ] )

            if txt == args[ 1 ]:
                print( txt )
                args[ 0 ].append( hwnd )

    hwnds   = []
    win32gui.EnumWindows( enumWindowsCallback, ( hwnds, window_name ) )

    if len( hwnds ) == 0:
        print( "Window Name Not Found!!", window_name )
        return  None

    return  hwnds[ 0 ]


#
def getClientRect( hwnd ):
    return  win32gui.GetClientRect( hwnd )


#
def printWindow( hwnd, capture_rect = None ):
    PW_CLIENTONLY           = 1
    PW_RENDERFULLCONTENT    = 2

    left, top, right, bot   = win32gui.GetWindowRect( hwnd )
    wndrect = win32gui.GetClientRect( hwnd )

    w   = right - left
    h   = bot - top

    # WinodwRect - ClientRect からウィンドウフレーム部分を推定
    side    = int( ( w - wndrect[ 2 ] ) / 2 )
    margin  = ( side, h - wndrect[ 3 ] - side, side, side )

    # 
    if capture_rect:
        w   = capture_rect[ 0 ] + margin[ 0 ]
        h   = capture_rect[ 1 ] + margin[ 1 ]
    else:
        w   = wndrect[ 2 ] + margin[ 0 ]
        h   = wndrect[ 3 ] + margin[ 1 ]


    #
    hwndDC = win32gui.GetWindowDC( hwnd )
    mfcDC  = win32ui.CreateDCFromHandle( hwndDC )
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap( mfcDC, w, h )

    saveDC.SelectObject( saveBitMap )

    windll.user32.PrintWindow( hwnd, saveDC.GetSafeHdc(), PW_RENDERFULLCONTENT )

    bmpinfo = saveBitMap.GetInfo()
    bmpbits = saveBitMap.GetBitmapBits( True )

    #
    win32gui.DeleteObject( saveBitMap.GetHandle() )
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC( hwnd, hwndDC )


    return  ( bmpinfo, bmpbits, margin )
