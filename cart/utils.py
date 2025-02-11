def calculate_cart_total(cart, movies):
    total = 0
    for movie in movies:
        quantity = cart.get(str(movie.id), 0)
        total += movie.price * int(quantity)
    return total
