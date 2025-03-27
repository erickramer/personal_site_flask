module Link exposing (toTexts)

import Svg
import Svg.Attributes exposing (x, y)
import Box

toTexts box links =
    let
        textX = (Box.max box.width) / 5
        range = Box.max box.height
        offsetY = range * 0.1
        n =  List.length links
        textYs = List.map 
            (\i ->  range / (toFloat (n)) * (toFloat i - 0.5))
            (List.range 1 n)
    in
    List.map2 (toText textX) textYs links

toText textX textY link =
    Svg.a 
        [Svg.Attributes.xlinkHref ("/" ++ link)]
        [Svg.text_ 
                [
                 x (String.fromFloat textX), 
                 y (String.fromFloat textY),
                 Svg.Attributes.fontSize "4.5rem",
                 Svg.Attributes.fontFamily "Raleway, Helvetica, sans-serif"
                ] 

                [Svg.text link]
        ]