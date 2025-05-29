port module About exposing (Model, Msg(..), SvgSize, init, initModel, main, newParticle, newParticles, randomAcceleration, randomMass, randomPosition, randomVelocity, subscriptions, svg, svgAttributes, svgElements, update, view, storeParticles, loadParticles)

import Box exposing (Box, updateBox)
import Browser
import Browser.Events
import Html exposing (Html, div, h2, p, a, text)
import Html.Attributes exposing (style, class, href)
import Particle exposing (Particle)
import Random
import Svg
import Svg.Attributes
import Vector


type alias Model =
    { box : Box
    , particles : List Particle
    , g : Float
    }


type alias SvgSize =
    { width : Float
    , height : Float
    }


type Msg
    = OnAnimate Float
    | NewParticles (List Particle)
    | ResetParticles Int
    | NewWindowSize WindowSize
    | ParticlesLoaded (List Particle)


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }


initModel =
    Model (Box ( 0, 100 ) ( 0, 100 )) [] -0.005


init : () -> ( Model, Cmd Msg )
init _ =
    ( initModel
    , Cmd.none
    )


view model =
    div [] [svg model]


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        OnAnimate dt ->
            let
                collisionHandler =
                    if model.g > 0 then
                        Particle.mergeCollisions

                    else
                        Particle.resolveCollisions

                particles =
                    if dt < 150 then
                        model.particles
                            |> List.map (Particle.updatePosition dt)
                            |> List.map (Box.bounce model.box)
                            |> collisionHandler
                            |> Particle.updateAcceleration model.g
                            |> List.map (Particle.updateVelocity dt)
                    else
                        model.particles
            in
            ( { model | particles = particles }, storeParticles particles )

        ResetParticles n ->
            ( model, Random.generate NewParticles (newParticles model n) )

        NewParticles particles ->
            ( { model | particles = particles }
            , storeParticles particles
            )

        NewWindowSize windowSize  ->
            let
                newBox = updateBox model.box (windowSize.height, windowSize.width)
            in
            if List.isEmpty model.particles then
                ( { model | box = newBox }
                , Random.generate NewParticles (newParticles { model | box = newBox } 40)
                )
            else
                ( { model | box = newBox }, Cmd.none )

        ParticlesLoaded particles ->
            ( { model | particles = particles }, Cmd.none )


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Browser.Events.onAnimationFrameDelta OnAnimate
        , newWindowSize NewWindowSize
        , loadParticles ParticlesLoaded
        ]


svg model =
    Svg.svg (svgAttributes model) (svgElements model)


svgAttributes model =
    [ -- Svg.Attributes.height (String.fromFloat (Box.max model.box.height))
      --, Svg.Attributes.width (String.fromFloat (Box.max model.box.width))
      Svg.Attributes.id "mysvg"
    , Svg.Attributes.pointerEvents "all"
    , style "width" (String.fromFloat (Box.max model.box.width))
    , style "height" (String.fromFloat (Box.max model.box.height))
    , style "background" "white"
    ]


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
                        [ div [ class "one-half column" ]
                            [ h2 [] [ text "About" ] ]
                        ]
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
    ( List.map (Particle.toCircle fillColor) model.particles ) ++ [ aboutText ]


randomVelocity model =
    let
        vx =
            2.0e-5 * Box.max model.box.width

        vy =
            2.0e-5 * Box.max model.box.height
    in
    Random.map2
        Vector.vector
        (Random.float -vx vx)
        (Random.float -vy vy)


randomPosition model =
    Random.map2
        Vector.vector
        (Random.float (Box.max model.box.width * 0) (Box.max model.box.width * 1))
        (Random.float (Box.max model.box.height * 0) (Box.max model.box.height * 1))


randomAcceleration =
    Random.map2 Vector.vector (Random.float 0 0) (Random.float 0 0)


randomMass : Box -> Random.Generator Float
randomMass box =
    Random.map (\x -> x ^ 2) (Random.float 2 ((Box.max box.width) / 100) )


newParticle model =
    Particle.randomParticle
        (randomPosition model)
        (randomVelocity model)
        randomAcceleration
        (randomMass model.box)


newParticles model n =
    Random.list n (newParticle model)

-- window size updates

type alias WindowSize = {
        width: Float
      , height: Float
    }

port newWindowSize : ( WindowSize -> msg) -> Sub msg

port storeParticles : List Particle -> Cmd msg

port loadParticles : (List Particle -> msg) -> Sub msg

