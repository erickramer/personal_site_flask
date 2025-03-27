port module Home exposing (Model, Msg(..), SvgSize, init, initModel, main, newParticle, newParticles, randomAcceleration, randomMass, randomPosition, randomVelocity, subscriptions, svg, svgAttributes, svgElements, update, view)

import Box exposing (Box, updateBox)
import Browser
import Browser.Dom exposing (Viewport)
import Browser.Events
import Html exposing (Html, button, div, h1, text)
import Html.Attributes exposing (style)
import Html.Events exposing (onClick)
import Particle exposing (Particle)
import Random
import Svg
import Svg.Attributes
import Task
import Time
import Vector
import Link


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

links = ["about", "demos", "resume", "contact"]

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
            ( { model | particles = particles }, Cmd.none )

        ResetParticles n ->
            ( model, Random.generate NewParticles (newParticles model n) )

        NewParticles particles ->
            ( { model | particles = particles }
            , Cmd.none
            )

        NewWindowSize windowSize  ->
            ( { model | box = updateBox model.box (windowSize.height, windowSize.width), particles = [] } , 
                Random.generate 
                    NewParticles 
                    (newParticles { model | box = updateBox model.box (windowSize.height, windowSize.width), particles = [] }  40))


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ Browser.Events.onAnimationFrameDelta OnAnimate, newWindowSize NewWindowSize ]


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
    in
    ( List.map (Particle.toCircle fillColor) model.particles ) ++
    Link.toTexts model.box links


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

