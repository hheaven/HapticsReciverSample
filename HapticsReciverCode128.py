# from PIL import Image
from pyzbar.pyzbar import decode

#
class HapticsReciverCode128:

    #
    def __init__( self, area = ( 1, 8 ), one_block = ( 256, 4 ) ):
        self.block_area     = area
        self.one_block      = one_block
        
        # self.value[y][x]
        self.value      = [ [ 0.0 ] * self.block_area[ 0 ] for i in range( self.block_area[ 1 ] ) ]

    #
    def rect( self, client_rect = None ):
        return  (
            self.block_area[ 0 ] * self.one_block[ 0 ],
            self.block_area[ 1 ] * self.one_block[ 1 ]
        )

    #
    def update( self, img ):

        # BGRA並びなのでBを指定してRを取り出し
        img = img.getchannel( 'B' )

        for y in range( self.block_area[ 1 ] ):
            for x in range( self.block_area[ 0 ] ):

                # 1block分切り抜き
                # 上下をトリミング
                px  = x * self.one_block[ 0 ]
                py  = y * self.one_block[ 1 ] + int( self.one_block[ 1 ] / 3 )

                block_img   = img.crop( ( px, py, px + self.one_block[ 0 ], py + int( self.one_block[ 1 ] / 3 ) + 1 ) )

                data    = decode( block_img )

                if data:
                    # 6文字中下位3文字に'000'-'255'が入ってるバーコード
                    self.value[ y ][ x ]    = int( data[ 0 ][ 0 ].decode()[ -3: ] ) / 255

