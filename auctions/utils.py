def get_max_bid(objs):
    """returns maximum bid amount """
    max_bid = 0
    for obj in objs:
        if obj.bid_amount > max_bid:
            max_bid = obj.bid_amount
    return max_bid