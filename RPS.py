def player(prev_play, opponent_history=[], my_history=[], counter={"count": 0}):
    beats = {"R": "P", "P": "S", "S": "R"}

    # New match detection (empty string signals start of a new match)
    if prev_play == "":
        opponent_history.clear()
        my_history.clear()
        counter["count"] = 0

    if prev_play != "":
        opponent_history.append(prev_play)

    counter["count"] += 1

    # --- Detect Quincy: fixed cycle R, P, S, P ---
    quincy_pattern = ["R", "P", "S", "P"]
    is_quincy = len(opponent_history) >= 8 and all(
        opponent_history[i] == quincy_pattern[i % 4] for i in range(len(opponent_history))
    )

    # --- Detect Kris: always counters your previous move ---
    is_kris = False
    if len(my_history) >= 3:
        is_kris = all(
            opponent_history[i] == beats[my_history[i]]
            for i in range(1, len(my_history))
        )

    guess = "R"

    if is_quincy:
        next_idx = len(opponent_history) % 4
        guess = beats[quincy_pattern[next_idx]]

    elif is_kris:
        last_my = my_history[-1] if my_history else "R"
        guess = beats[beats[last_my]]

    else:
        # General strategy: counter the opponent's most frequent recent move
        # (handles Mrugesh and provides a strong baseline against Abbey)
        if len(opponent_history) >= 3:
            last_ten = opponent_history[-10:]
            freq = {"R": last_ten.count("R"), "P": last_ten.count("P"), "S": last_ten.count("S")}
            most_common = max(freq, key=freq.get)
            guess = beats[most_common]
        else:
            guess = "P"

    my_history.append(guess)
    return guess
  
