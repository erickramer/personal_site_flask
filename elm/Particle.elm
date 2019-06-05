module Particle exposing (Particle, collide, collide_, collisionDeltaTime, collisionFilter, cr, distance, isCollision, mergeCollisions, momentum, radius, randomParticle, resolveCollisions, toCircle, update, updateAcceleration, updatePosition, updateVelocity)

import Opt
import Random
import Svg exposing (circle)
import Svg.Attributes exposing (cx, cy, fill, r)
import Vector exposing (Vector, x, y)


type alias Particle =
    { position : Vector
    , velocity : Vector
    , acceleration : Vector
    , mass : Float
    }


cr =
    0


collisionEpsilon =
    0.000001


distance : Particle -> Particle -> Float
distance p q =
    Vector.distance p.position q.position


radius : Particle -> Float
radius p =
    sqrt p.mass


momentum : Particle -> Vector
momentum p =
    Vector.multiply p.mass p.velocity

-- collision

isCollision : Particle -> Particle -> Bool
isCollision p q =
    distance p q < radius p + radius q - collisionEpsilon


anyCollision : List Particle -> Bool
anyCollision particles =
    case particles of
        p :: ps ->
            let
                priorCollision =
                    anyCollision ps
            in
            if priorCollision then
                True

            else
                List.any (isCollision p) ps

        [] ->
            False


collisionDeltaTime : Particle -> Particle -> Float
collisionDeltaTime p q =
    let
        f dt =
            let
                po =
                    updatePosition dt p

                qo =
                    updatePosition dt q

                d =
                    distance po qo
            in
            abs (d - radius po - radius qo)
    in
    Opt.minimize f -0.5 0.1


collide_ : Particle -> Particle -> ( Particle, Particle )
collide_ p q =
    let
        totalMomentum =
            Vector.add (momentum p) (momentum q)

        pElasticity =
            Vector.subtract q.velocity p.velocity
                |> Vector.multiply q.mass
                |> Vector.multiply cr

        qElasticity =
            Vector.subtract p.velocity q.velocity
                |> Vector.multiply p.mass
                |> Vector.multiply cr

        pVelocity =
            totalMomentum
                |> Vector.add pElasticity
                |> Vector.divide (p.mass + q.mass)

        qVelocity =
            totalMomentum
                |> Vector.add qElasticity
                |> Vector.divide (p.mass + q.mass)
    in
    ( { p | velocity = pVelocity }, { q | velocity = qVelocity } )


collide : Particle -> Particle -> ( Particle, Particle )
collide p q =
    if isCollision p q then
        let
            dt =
                collisionDeltaTime p q

            -- initial particles are moment of collision
            po =
                updatePosition dt p

            qo =
                updatePosition dt q

            -- updated velocities immediately post collision
            ( pc, qc ) =
                collide_ po qo

            -- stepping forward in time
            pf =
                updatePosition -dt pc

            qf =
                updatePosition -dt qc
        in
        ( pf, qf )

    else
        ( p, q )


collisionFilter : Particle -> List Particle -> ( List Particle, List Particle )
collisionFilter p qs =
    let
        reducer q ( collisions, notCollisions ) =
            if isCollision p q then
                if sigCollision p q then
                    ( q :: collisions, notCollisions )

                else
                    ( collisions, q :: notCollisions )

            else
                ( collisions, q :: notCollisions )
    in
    List.foldl reducer ( [], [] ) qs


mergeCollisions : List Particle -> List Particle
mergeCollisions particles =
    case particles of
        p :: ps ->
            let
                newParticles =
                    mergeCollisions ps

                ( collisions, notCollisions ) =
                    collisionFilter p newParticles

                newP =
                    List.foldl merge p collisions
            in
            newP :: notCollisions

        [] ->
            []


resolveCollisions : List Particle -> List Particle
resolveCollisions particles =
    case particles of
        p :: ps ->
            let
                newParticles =
                    resolveCollisions ps

                ( collisions, notCollisions ) =
                    collisionFilter p newParticles

                collisionsSorted =
                    List.sortBy (collisionDeltaTime p) collisions
            in
            if isSignificantCollision p collisionsSorted then
                case collisionsSorted of
                    q :: qs ->
                        let
                            y =
                                Debug.log "Collisions of size" (2 + List.length qs)

                            ( newP, newQ ) =
                                collide p q
                        in
                        resolveCollisions [ newP, newQ ] ++ qs ++ notCollisions

                    [] ->
                        p :: notCollisions

            else
                p :: collisionsSorted ++ notCollisions

        [] ->
            []


areTouching : Particle -> Particle -> Bool
areTouching p q =
    let
        collision =
            isCollision p q

        sameVelocity =
            Vector.magnitude (Vector.subtract p.velocity q.velocity) < 0.0001
    in
    collision && sameVelocity


sigCollision p q =
    let
        ( newP, newQ ) =
            collide_ p q
    in
    if Vector.equivalent p.velocity newP.velocity then
        False

    else
        True


isSignificantCollision : Particle -> List Particle -> Bool
isSignificantCollision p qs =
    let
        collideOne b a =
            let
                ( newA, newB ) =
                    collide_ a b
            in
            newA

        pFinal =
            List.foldr collideOne p qs
    in
    not (Vector.equivalent p.velocity pFinal.velocity)


merge : Particle -> Particle -> Particle
merge p q =
    let
        newMass =
            p.mass + q.mass

        newVelocity =
            Vector.add (momentum p) (momentum q)
                |> Vector.divide newMass

        newPosition =
            Vector.add
                (Vector.multiply p.mass p.position)
                (Vector.multiply q.mass q.position)
                |> Vector.divide newMass
    in
    Particle newPosition newVelocity (Vector.vector 0 0) newMass



-- update


updatePosition : Float -> Particle -> Particle
updatePosition dt p =
    { p | position = Vector.add p.position (Vector.multiply dt p.velocity) }


updateVelocity : Float -> Particle -> Particle
updateVelocity dt p =
    { p | velocity = Vector.add p.velocity (Vector.multiply dt p.acceleration) }


updateAcceleration : Float -> List Particle -> List Particle
updateAcceleration g particles =
    let
        acceleration p q =
            let
                r =
                    Vector.subtract q.position p.position
                        |> Vector.normalize

                dist =
                    max (distance p q) (radius p + radius q)

                k =
                    g * q.mass / dist ^ 2
            in
            if distance p q < 1.0e-4 then
                Nothing

            else
                Maybe.Just (Vector.multiply k r)

        totalAcceleration particle =
            List.filterMap (acceleration particle) particles
                |> List.foldl Vector.add (Vector.vector 0 0)
    in
    particles
        |> List.map (\p -> { p | acceleration = totalAcceleration p })


update : Particle -> Float -> Particle
update p time =
    p |> updateVelocity time |> updatePosition time



-- random Vector


randomParticle :
    Random.Generator Vector
    -> Random.Generator Vector
    -> Random.Generator Vector
    -> Random.Generator Float
    -> Random.Generator Particle
randomParticle position velocity acceleration mass =
    Random.map4
        Particle
        position
        velocity
        acceleration
        mass



-- drawing


toCircle fillColor particle =
    Svg.circle
        [ cx (String.fromFloat (x particle.position))
        , cy (String.fromFloat (y particle.position))
        , r (String.fromFloat (radius particle))
        , fill fillColor
        ]
        []
