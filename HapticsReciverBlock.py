BLOCK_SIZE  = 3

#
class HapticsReciverBlock:

    #
    def __init__( self, area = ( 8, 1 ), scale = ( 0.01, 0.02 ), threshold = 8 ):
        self.block_area     = area
        self.block_sacle    = scale
        self.threshold      = threshold

        # self.value[y][x]
        self.value      = [ [ 0.0 ] * self.block_area[ 0 ] for i in range( self.block_area[ 1 ] ) ]
 

    #
    def rect( self, client_rect ):
        return  ( 
            int( ( self.block_area[ 0 ] * self.block_sacle[ 0 ] ) * client_rect[ 2 ] ),
            int( ( self.block_area[ 1 ] * self.block_sacle[ 1 ] ) * client_rect[ 3 ] ) )


    #
    def update( self, imgdata ):

        for y in range( self.block_area[ 1 ] ):
            for x in range( self.block_area[ 0 ] ):

                av  = 0.0
                for yy in range( BLOCK_SIZE ):
                    for xx in range( BLOCK_SIZE ):
                        idx = ( x * BLOCK_SIZE + xx ) + ( y * BLOCK_SIZE + yy ) * self.block_area[ 0 ] * BLOCK_SIZE

                        bgra    = imgdata[ idx ]

                        # BGRA
                        r   = bgra[ 2 ]
                        g   = bgra[ 1 ]
                        b   = bgra[ 0 ]

                        if b > self.threshold or g > self.threshold:
                            r   = 0

                        av  += r
                
                self.value[ y ][ x ]    = av / ( BLOCK_SIZE * BLOCK_SIZE * 255 )

