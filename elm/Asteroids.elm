port module Main exposing (KeyPoint, Model, Msg(..), Particle, Pose, Position, Space, SpaceShip, Span, Vector, asteroidToCircle, canvasSpace, collideAsteroid, collideAsteroids, collideMissile, collideMissiles, createMissile, diagonal, filterParticles, gameSpace, inSpace, init, isCollision, main, missileToCircle, moveParticle, moveSpaceship, newMissile, newPose, particleScale, randomAsteroid, randomPosition, scalarScale, scaleCanvasToGameVector, scaleGameToSvgParticle, scaleGameToSvgVector, spaceShipToImg, subscriptions, svgHeight, svgSpace, svgWidth, toCircle, update, vectorScale, view)

import Array
import Browser
import Html exposing (Html, button, div, h1, p, text)
import Html.Events exposing (onClick)
import Html.Attributes exposing (class)
import Json.Decode exposing (Decoder, field, float, int, map2, map3, string)
import Random
import Svg
import Svg.Attributes exposing (..)
import Time
import Browser.Events


svgWidth =
    600.0


svgHeight =
    600.0



-- types


type alias KeyPoint =
    { score : Float
    , part : String
    , position : Position
    }


type alias Position =
    { x : Float
    , y : Float
    }


type alias Pose =
    List KeyPoint


type alias Particle =
    { position : Vector
    , velocity : Vector
    , radius : Float
    }


type alias Span =
    { min : Float
    , max : Float
    }


type alias Space =
    { x : Span
    , y : Span
    }


type alias Vector =
    { x : Float
    , y : Float
    }


type alias Model =
    { spaceship : SpaceShip
    , asteroids : List Particle
    , missiles : List Particle
    , score : Int
    , alive : Bool
    }


type alias SpaceShip =
    { position : Vector
    , dimension : Vector
    }


type Msg
    = Tock Time.Posix
    | NewAsteroid Particle
    | NewPose Pose
    | NewMissile Bool
    | OnAnimate Float



-- mapping functions


diagonal : Space -> Float
diagonal space =
    let
        x =
            space.x.max - space.x.min

        y =
            space.y.max - space.y.min
    in
    sqrt ((x ^ 2) + (y ^ 2))


gameSpace =
    Space
        (Span -100 100)
        (Span -100 100)


svgSpace =
    Space
        (Span 0 svgWidth)
        (Span 0 svgHeight)


canvasSpace =
    Space
        (Span 0 300)
        (Span 0 300)



-- scaling functions


scalarScale : Span -> Span -> Float -> Float
scalarScale domain range input =
    let
        domainLength =
            domain.max - domain.min

        rangeLength =
            range.max - range.min
    in
    ((input - domain.min) / domainLength) * rangeLength + range.min


vectorScale : Space -> Space -> Vector -> Vector
vectorScale domain range input =
    let
        xOut =
            scalarScale domain.x range.x input.x

        yOut =
            scalarScale domain.y range.y input.y
    in
    Vector xOut yOut


particleScale : Space -> Space -> Particle -> Particle
particleScale domain range input =
    let
        positionOut =
            vectorScale domain range input.position

        velocityOut =
            vectorScale domain range input.velocity

        radiusOut =
            scalarScale
                (Span 0 (diagonal domain))
                (Span 0 (diagonal range))
                input.radius
    in
    Particle positionOut velocityOut radiusOut


inSpace : Space -> Particle -> Bool
inSpace space particle =
    particle.position.x
        > space.x.min
        && particle.position.x
        < space.x.max
        && particle.position.y
        > space.y.min
        && particle.position.y
        < space.y.max


scaleGameToSvgParticle : Particle -> Particle
scaleGameToSvgParticle =
    particleScale gameSpace svgSpace


scaleGameToSvgVector : Vector -> Vector
scaleGameToSvgVector =
    vectorScale gameSpace svgSpace


scaleCanvasToGameVector : Vector -> Vector
scaleCanvasToGameVector =
    vectorScale canvasSpace gameSpace



-- updates


isCollision : Particle -> Particle -> Bool
isCollision a b =
    let
        d =
            (a.position.x - b.position.x) ^ 2 + (a.position.y - b.position.y) ^ 2
    in
    sqrt d < (a.radius + b.radius)


moveParticle : Float -> Particle -> Particle
moveParticle dt particle =
    let
        newPosition =
            Vector
                (particle.position.x + dt * particle.velocity.x)
                (particle.position.y + dt * particle.velocity.y)
    in
    { particle | position = newPosition }


moveSpaceship : SpaceShip -> Pose -> SpaceShip
moveSpaceship spaceship pose =
    let
        nose =
            pose
                |> List.filter (\x -> x.part == "nose")
                |> List.head
    in
    case nose of
        Just keypoint ->
            let
                newPosition =
                    scaleCanvasToGameVector
                        (Vector keypoint.position.x keypoint.position.y)
            in
            { spaceship | position = newPosition }

        Nothing ->
            spaceship


filterParticles : Space -> List Particle -> ( Int, List Particle )
filterParticles space particles =
    let
        notInSpace =
            \particle ->
                particle
                    |> inSpace space
                    |> not
    in
    ( particles
        |> List.map (inSpace space)
        |> List.map
            (\x ->
                if x then
                    1

                else
                    0
            )
        |> List.sum
    , List.filter notInSpace particles
    )


collideMissile : List Particle -> Particle -> Maybe Particle
collideMissile asteroids missile =
    let
        collisions =
            List.map (isCollision missile) asteroids
    in
    if List.any identity collisions then
        Nothing

    else
        Just missile


collideMissiles : List Particle -> List Particle -> List Particle
collideMissiles missiles asteroids =
    List.filterMap (collideMissile asteroids) missiles


collideAsteroid : List Particle -> Particle -> Maybe Particle
collideAsteroid missiles asteroid =
    let
        counts =
            missiles
                |> List.map (isCollision asteroid)
                |> List.map
                    (\x ->
                        if x then
                            1

                        else
                            0
                    )
                |> List.sum

        newRadius =
            asteroid.radius / (2 ^ counts)
    in
    if newRadius > 0.75 then
        Just { asteroid | radius = newRadius }

    else
        Nothing


collideAsteroids : List Particle -> List Particle -> (List Particle, Int)
collideAsteroids missiles asteroids =
    let 
        newAsteroids = 
            List.filterMap (collideAsteroid missiles) asteroids
        
        collisions =
            List.map (\missile -> 
                        List.map (\asteroid -> isCollision missile asteroid) asteroids) missiles

        trueCollisions = 
            List.map (\a -> List.filter (\x -> x) a) collisions

        nCollisions =
            List.sum (List.map List.length trueCollisions)
    in
    (newAsteroids, nCollisions)
        



randomPosition : Random.Generator Vector
randomPosition =
    Random.map (\x -> Vector x -100) (Random.float -100 100)


randomAsteroid : Random.Generator Particle
randomAsteroid =
    let
        position =
            randomPosition

        velocity =
            Vector 0 0.01

        radius =
            Random.float 2 7
    in
    Random.map2 (\p r -> Particle p velocity r)
        position
        radius


createMissile : SpaceShip -> Particle
createMissile spaceship =
    let
        velocity =
            Vector 0 -0.05

        radius =
            0.75

        position = 
            Vector (spaceship.position.x + 10) spaceship.position.y
    in
    Particle position velocity radius



-- drawing functions


toCircle : Particle -> String -> Svg.Svg msg
toCircle particle fillColor =
    let
        newParticle =
            scaleGameToSvgParticle particle
    in
    Svg.circle
        [ cx (String.fromFloat newParticle.position.x)
        , cy (String.fromFloat newParticle.position.y)
        , r (String.fromFloat newParticle.radius)
        , fill fillColor
        ]
        []


asteroidToCircle particle =
    toCircle particle "black"


missileToCircle particle =
    toCircle particle "red"


spaceShipToImg spaceship =
    let
        position =
            scaleGameToSvgVector spaceship.position
    in
    Svg.image
        [ width (String.fromFloat spaceship.dimension.x)
        , height (String.fromFloat spaceship.dimension.y)
        , x (String.fromFloat position.x)
        , y (String.fromFloat position.y)
        , xlinkHref "/static/images/spaceship.svg"
        ]
        []


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- JSON types


init : () -> ( Model, Cmd Msg )
init _ =
    let
        spaceship =
            SpaceShip (Vector 0 0) (Vector 50 50)

        asteroids =
            []

        missiles =
            []

        score =
            0

        alive =
            True
    in
    ( Model spaceship asteroids missiles score alive, Cmd.none )


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        -- Tick time ->
        --     let
        --         (newAsteroids, nCollisions) =
        --             collideAsteroids model.missiles model.asteroids

        --         newMissiles =
        --             collideMissiles model.missiles model.asteroids
        --     in
        --     ( { model
        --         | asteroids = List.map moveParticle newAsteroids
        --         , missiles = List.map moveParticle model.missiles
        --         , score = model.score + nCollisions
        --       }
        --     , Cmd.none
        --     )
        
        OnAnimate dt ->
            let
                (newAsteroids, nCollisions) =
                    collideAsteroids model.missiles model.asteroids

                newMissiles =
                    collideMissiles model.missiles model.asteroids
            in
            ( { model
                | asteroids = List.map (moveParticle dt) newAsteroids
                , missiles = List.map (moveParticle dt) model.missiles
                , score = model.score + nCollisions
              }
            , Cmd.none
            )

        Tock time ->
            ( model
            , Random.generate NewAsteroid randomAsteroid
            )

        NewAsteroid asteroid ->
            ( { model | asteroids = asteroid :: model.asteroids }
            , Cmd.none
            )

        NewPose pose ->
            ( { model | spaceship = moveSpaceship model.spaceship pose }, Cmd.none )

        NewMissile bool ->
            let
                missile =
                    createMissile model.spaceship
            in
            ( { model | missiles = missile :: model.missiles }, Cmd.none )



-- subscriptions


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.batch
        [ --Time.every 100 Tick
          Time.every 1000 Tock
        , newPose NewPose
        , newMissile NewMissile
        , Browser.Events.onAnimationFrameDelta OnAnimate
        ]


view : Model -> Html Msg
view model =
    div [ Html.Attributes.class "container" ]
        [   div [ Html.Attributes.class "row" ] []
            [Html.h3 [] [ text ("Score: " ++ String.fromInt model.score) ]
        , div []
            [ Svg.svg
                [ width (String.fromFloat svgWidth)
                , height (String.fromFloat svgHeight)
                , viewBox "0 0 600 600"
                ]
                (spaceShipToImg model.spaceship
                    :: (List.map asteroidToCircle model.asteroids
                            ++ List.map missileToCircle model.missiles
                       )
                )
            ]
        ]



-- ports


port newPose : (Pose -> msg) -> Sub msg


port newMissile : (Bool -> msg) -> Sub msg
