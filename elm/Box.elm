module Box exposing (Box, area, bounce, max, min, size, svgAttributes, updateBox)

import Particle exposing (Particle)
import Svg
import Svg.Attributes exposing (height, width)
import Tuple
import Vector exposing (x, y)


type alias Box =
    { height : ( Float, Float )
    , width : ( Float, Float )
    }


min =
    Tuple.first


max =
    Tuple.second

area box =
    (max box.height - min box.width) * (max box.width - min box.width)

bounceX : Box -> Particle -> Particle
bounceX box particle =
    if x particle.position + Particle.radius particle > max box.width then
        let
            newPosition =
                ( max box.width - Particle.radius particle, y particle.position )

            newVelocity =
                ( -(abs <| x particle.velocity), y particle.velocity )
        in
        { particle | position = newPosition, velocity = newVelocity }

    else if x particle.position - Particle.radius particle < min box.width then
        let
            newPosition =
                ( min box.width + Particle.radius particle, y particle.position )

            newVelocity =
                ( abs <| x particle.velocity, y particle.velocity )
        in
        { particle | position = newPosition, velocity = newVelocity }

    else
        particle


bounceY : Box -> Particle -> Particle
bounceY box particle =
    if y particle.position + Particle.radius particle > max box.height then
        let
            newPosition =
                ( x particle.position, max box.height - Particle.radius particle )

            newVelocity =
                ( x particle.velocity, -(abs <| y particle.velocity) )
        in
        { particle | position = newPosition, velocity = newVelocity }

    else if y particle.position - Particle.radius particle < min box.height then
        let
            newPosition =
                ( x particle.position, min box.height + Particle.radius particle )

            newVelocity =
                ( x particle.velocity, abs <| y particle.velocity )
        in
        { particle | position = newPosition, velocity = newVelocity }

    else
        particle


bounce : Box -> Particle -> Particle
bounce box particle =
    particle
        |> bounceX box
        |> bounceY box


size : ( Float, Float ) -> Float
size ( x, y ) =
    y - x


svgAttributes box =
    [ height (String.fromFloat (max box.height))
    , width (String.fromFloat (max box.width))
    ]

updateBox : Box -> (Float, Float) -> Box
updateBox box (x, y) = 
    Box (min box.width, x) (min box.height, y)