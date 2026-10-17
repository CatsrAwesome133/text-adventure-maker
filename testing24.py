all_decisions[first_option].show()

next = all_decisions[first_option].make()
playing = True
while playing:
    all_decisions[next].show()
    print()
    next = all_decisions[next].make()
    if next == last_option:
        playing = False