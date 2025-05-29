port module Home exposing (main)

import Browser
import Html exposing (Html, div)
import Link
import ParticlePage exposing (Model, Msg(..), init, update, subscriptions, svg)
import Particle exposing (Particle)
import Svg exposing (Svg)

-- record used with the window size port
type alias WindowSize =
    { width : Float
    , height : Float
    }


links = [ "about", "demos", "resume", "contact" ]

view : Model -> Html Msg
view model =
    div [] [ svg model (svgElements model) ]

svgElements : Model -> List (Svg Msg)
svgElements model =
    let
        fillColor = "black"
    in
    (List.map (Particle.toCircle fillColor) model.particles)
        ++ Link.toTexts model.box links

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions newWindowSize
        , view = view
        }

port newWindowSize : ({ width : Float, height : Float } -> msg) -> Sub msg
