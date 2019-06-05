module Opt exposing (minimize)


absTolerance =
    1.0e-15


relTolerance =
    1.0e-15


maxIter =
    1.0e3



-- wrapper to set defaults
-- change to output minimum value


minimize : (Float -> Float) -> Float -> Float -> Float
minimize f x dx =
    minimize_ f x dx (f x) 0



-- change to output minimum value


minimize_ : (Float -> Float) -> Float -> Float -> Float -> Float -> Float
minimize_ f x dx yi iter =
    let
        xo =
            x + dx

        --Debug.log "xo" (x + dx)
        yo =
            f (x + dx)

        --Debug.log "yo" (f (x + dx))
        absDiff =
            abs (yi - yo)

        relDiff =
            absDiff / abs yi

        minimized =
            absDiff < absTolerance || relDiff < relTolerance
    in
    if x > 0 then
        minimize_ f 0 (-(abs dx) / 3) yo (iter + 1)

    else if minimized then
        x + dx

    else if iter > maxIter then
        Debug.log "Reached maximum iterations: " (x + dx)

    else if yo > yi then
        minimize_ f (x + dx) (-dx / 3) yo (iter + 1)

    else
        minimize_ f (x + dx) dx yo (iter + 1)
