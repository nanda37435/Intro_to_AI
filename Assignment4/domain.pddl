(define (domain sokorobotto)
    (:requirements :typing)
    (:types  
    	order location saleitem shipment - object
    	robot pallette - robo
    )
    (:predicates 
    	(includes ?x - shipment ?y - saleitem)
    	(ships ?x - shipment ?y - order)
    	(unstarted ?x - shipment)
    	(orders ?x - order ?y - saleitem)
    	(packing-location ?x - location)
    	(available ?x - location)
    	(contains ?x - pallette ?y - saleitem)
    	(free ?x - robot)
    	(connected ?x - location ?y - location)
    	(at ?x - robo ?y - location)
    	(no-robot ?x - location)
    	(no-pallette ?x - location)
    )
    (:action carry
    :parameters
        (
            ?loc ?pack - location
            ?pal - pallette
            ?order_name - order
            ?item_name - saleitem
        )
    :precondition
        (
            and
            (at ?pal ?loc)
            (connected ?loc ?pack)
            (no-pallette ?pack)
            (orders ?order_name ?item_name)
            (available ?pack)
            (packing-location ?pack)
            (connected ?loc ?pack)
            (connected ?pack ?loc)
        )
    :effect
        (
            and
            (not(no-pallette ?pack))
            (contains ?pal ?item_name)
        )
    )
    (:action move
    :parameters
        (
            ?robot_var - robot
            ?loc1 ?loc2 ?pack - location
            ?pal - pallette
            ?shipment_name - shipment
            ?order_name - order
            ?item_name - saleitem
        )
    :precondition
        (
            and
            (free ?robot_var)
            (at ?robot_var ?loc1)
            (at ?pal ?loc1)
            (unstarted ?shipment_name)
            (ships ?shipment_name ?order_name)
            (contains ?pal ?item_name)
            (not(no-pallette ?pack))
            (no-robot ?pack)
        )
    :effect
        (
            and
            (not(at ?robot_var ?loc1))
            (not(free ?robot_var))
            (not(no-robot ?pack))
            (not(no-robot ?loc2))
            (not(unstarted ?shipment_name))
            (includes ?shipment_name ?item_name)
        )
    )
    (:action complete
    :parameters
        (
            ?robot_var - robot
            ?pack ?loc2 - location
            ?shipment_name - shipment
            ?item_name - saleitem
        )
    :precondition
        (
            and
            (not(free ?robot_var))
            (not(no-pallette ?pack))
            (not(unstarted ?shipment_name))
            (includes ?shipment_name ?item_name)
        )
    :effect
        (
            and
            (no-pallette ?pack)
            (free ?robot_var)
            (no-robot ?pack)
            (unstarted ?shipment_name)
        )
    )
)











