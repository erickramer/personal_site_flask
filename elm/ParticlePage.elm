module ParticlePage exposing (Model, Msg(..), WindowSize, initModel, init, update, randomVelocity, randomPosition, randomAcceleration, randomMass, newParticle, newParticles, svg, svgAttributes, subscriptions)

import Box exposing (Box, updateBox)
import Browser.Events
import Html exposing (Html, div)
import Html.Attributes exposing (style)
import Particle exposing (Particle)
import Random
import Svg exposing (Svg)
import Svg.Attributes
import Vector


-- MODEL

type alias Model =
    { box : Box
    , particles : List Particle
    , g : Float
    }

type alias WindowSize =
    { width : Float
    , height : Float
    }

type Msg
    = OnAnimate Float
    | NewParticles (List Particle)
    | ResetParticles Int
    | NewWindowSize WindowSize


-- INITIALIZATION

initModel : Model
initModel =
    Model (Box ( 0, 100 ) ( 0, 100 )) [] -0.005

init : () -> ( Model, Cmd Msg )
init _ =
    ( initModel, Cmd.none )


-- UPDATE

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
            ( { model | particles = particles }, Cmd.none )

        NewWindowSize windowSize ->
            let
                updated =
                    { model | box = updateBox model.box ( windowSize.height, windowSize.width ), particles = [] }
            in
            ( updated
            , Random.generate NewParticles (newParticles updated 40)
            )


-- SUBSCRIPTIONS

subscriptions : ((WindowSize -> Msg) -> Sub Msg) -> Model -> Sub Msg
subscriptions windowSizePort model =
    Sub.batch
        [ Browser.Events.onAnimationFrameDelta OnAnimate
        , windowSizePort NewWindowSize
        ]


-- SVG HELPERS

svg : Model -> List (Svg Msg) -> Svg Msg
svg model elements =
    Svg.svg (svgAttributes model) elements

svgAttributes : Model -> List (Svg.Attribute msg)
svgAttributes model =
    [ Svg.Attributes.id "mysvg"
    , Svg.Attributes.pointerEvents "all"
    , style "width" (String.fromFloat (Box.max model.box.width))
    , style "height" (String.fromFloat (Box.max model.box.height))
    , style "background" "white"
    ]


-- PARTICLE GENERATION

randomVelocity : Model -> Random.Generator Vector.Vector
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

randomPosition : Model -> Random.Generator Vector.Vector
randomPosition model =
    Random.map2
        Vector.vector
        (Random.float (Box.max model.box.width * 0) (Box.max model.box.width * 1))
        (Random.float (Box.max model.box.height * 0) (Box.max model.box.height * 1))

randomAcceleration : Random.Generator Vector.Vector
randomAcceleration =
    Random.map2 Vector.vector (Random.float 0 0) (Random.float 0 0)

randomMass : Box -> Random.Generator Float
randomMass box =
    Random.map (\x -> x ^ 2) (Random.float 2 ((Box.max box.width) / 100))

newParticle : Model -> Random.Generator Particle
newParticle model =
    Particle.randomParticle
        (randomPosition model)
        (randomVelocity model)
        randomAcceleration
        (randomMass model.box)

newParticles : Model -> Int -> Random.Generator (List Particle)
newParticles model n =
    Random.list n (newParticle model)


