port module About exposing (main)

import Browser
import Html exposing (Html, div, h2, p, a, text)
import Html.Attributes exposing (class, href, style)
import Box
import ParticlePage exposing (Model, Msg(..), init, update, subscriptions, svg)
import Particle exposing (Particle)
import Svg exposing (Svg)
import Svg.Attributes

-- record used with the window size port
type alias WindowSize =
    { width : Float
    , height : Float
    }

view : Model -> Html Msg
view model =
    div [] [ svg model (svgElements model) ]

svgElements : Model -> List (Svg Msg)
svgElements model =
    let
        fillColor = "black"
        aboutText =
            Svg.foreignObject
                [ Svg.Attributes.x "0"
                , Svg.Attributes.y "0"
                , Svg.Attributes.width (String.fromFloat (Box.max model.box.width))
                , Svg.Attributes.height (String.fromFloat (Box.max model.box.height))
                ]
                [ div [ class "container" ]
                    [ div [ class "row", style "margin-top" "15%" ]
                        [ div [ class "one-half column" ] [ h2 [] [ text "About" ] ] ]
                    , div [ class "row" ]
                        [ div [ class "one-half column" ]
                            [ p []
                                [ text "I'm Eric Kramer. I currently work at "
                                , a [ href "https://openai.com" ] [ text "OpenAI" ]
                                , text ", and I used to work at "
                                , a [ href "https://stripe.com" ] [ text "Stripe" ]
                                , text " and "
                                , a [ href "https://dataiku.com" ] [ text "Dataiku" ]
                                , text ". A long time ago, I was an MD/PhD student at UC San Diego."
                                ]
                            , p []
                                [ text "I live in Noe Valley, San Francisco, CA with my wife "
                                , a [ href "https://pagepiccinini.com" ] [ text "Page Piccinini" ]
                                , text ", our two cats and two sons. Get in touch if you want to talk more about data science or medicine."
                                ]
                            ]
                        ]
                    ]
                ]
    in
    (List.map (Particle.toCircle fillColor) model.particles) ++ [ aboutText ]

main : Program () Model Msg
main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions newWindowSize
        , view = view
        }

port newWindowSize : ( WindowSize -> msg ) -> Sub msg
