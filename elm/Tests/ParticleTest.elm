module Tests.ParticleTest exposing (tests)

import Test exposing (..)
import Expect
import Particle
import Array
import Vector

p : Particle.Particle
p =
    { position = Vector.vector 0 0
    , velocity = Vector.vector 1 0
    , acceleration = Vector.vector 0 0
    , mass = 1
    }

q : Particle.Particle
q =
    { position = Vector.vector 0.5 0
    , velocity = Vector.vector -1 0
    , acceleration = Vector.vector 0 0
    , mass = 1
    }

far : Particle.Particle
far =
    { position = Vector.vector 3 0
    , velocity = Vector.vector 0 0
    , acceleration = Vector.vector 0 0
    , mass = 1
    }

tests : Test
tests =
    describe "Particle collision functions"
        [ test "collisionFilter detects collision" <|
            \_ ->
                let
                    ( collisions, notCollisions ) =
                        Particle.collisionFilter p (Array.fromList [ q ])
                in
                Expect.equal 1 (Array.length collisions)
        , test "resolveCollisions with no collision preserves velocities" <|
            \_ ->
                let
                    arr = Array.fromList [ p, far ]
                    result = Particle.resolveCollisions arr
                    v0 = Array.get 0 result |> Maybe.map .velocity
                    v1 = Array.get 1 result |> Maybe.map .velocity
                in
                Expect.true "velocities preserved"
                    ((v0 == Just p.velocity && v1 == Just far.velocity)
                        || (v0 == Just far.velocity && v1 == Just p.velocity))
        , test "resolveCollisions updates velocities on collision" <|
            \_ ->
                let
                    arr = Array.fromList [ p, q ]
                    result = Particle.resolveCollisions arr
                    p1 = Array.get 0 result |> Maybe.withDefault p
                in
                Expect.notEqual p.velocity p1.velocity
        ]
