import random

directions = ["UP", "RIGHT", "DOWN", "LEFT"]

# -----------------------------
# ENVIRONMENT SETUP
# -----------------------------

def setup_environment(n):
    grid = [["." for _ in range(n)] for _ in range(n)]
    cells = [(i, j) for i in range(n) for j in range(n)]
    cells.remove((0, 0))

    wumpus_pos = random.choice(cells); cells.remove(wumpus_pos)
    gold_pos = random.choice(cells); cells.remove(gold_pos)

    pit_count = max(1, int(0.2 * n * n))
    pit_positions = random.sample(cells, min(pit_count, len(cells)))

    grid[wumpus_pos[0]][wumpus_pos[1]] = "W"
    grid[gold_pos[0]][gold_pos[1]] = "G"
    for p in pit_positions:
        grid[p[0]][p[1]] = "P"

    return grid, wumpus_pos, gold_pos, pit_positions

# -----------------------------
# VIEW ENVIRONMENT
# -----------------------------

def view_environment(grid, agent_pos, visited, n, reveal=False):
    print("\n" + "=" * (n * 6 + 1))
    print("     " + "".join(f"  C{j} " for j in range(n)))
    print("     " + "+----" * n + "+")
    for i in range(n):
        row = ""
        for j in range(n):
            if (i, j) == agent_pos:  cell = "A"
            elif reveal:              cell = grid[i][j] if grid[i][j] != "." else " "
            elif (i, j) in visited:  cell = "V" if grid[i][j] == "." else grid[i][j]
            else:                    cell = "?"
            row += f"|{cell:^4}"
        print(f"  R{i} {row}|")
        print("     " + "+----" * n + "+")
    print("Legend: A=Agent  V=Visited  ?=Unknown  W=Wumpus  G=Gold  P=Pit\n")

# ← NEW: Print both maps side by side
def view_dual(grid, agent_pos, visited, n):
    header = f"{'AGENT VIEW (Explored)':^{n*6}}    {'FULL MAP (Revealed)':^{n*6}}"
    col_header = "     " + "".join(f"  C{j} " for j in range(n))
    divider = "     " + "+----" * n + "+"

    print("\n" + "=" * (n * 13 + 6))
    print(header)
    print(f"{col_header}    {col_header}")
    print(f"{divider}    {divider}")

    for i in range(n):
        left = right = ""
        for j in range(n):
            # Agent view (left)
            if (i, j) == agent_pos:  lc = "A"
            elif (i, j) in visited:  lc = "V" if grid[i][j] == "." else grid[i][j]
            else:                    lc = "?"
            left += f"|{lc:^4}"

            # Full reveal (right)
            rc = grid[i][j] if grid[i][j] != "." else " "
            if (i, j) == agent_pos: rc = "A"
            right += f"|{rc:^4}"

        print(f"  R{i} {left}|      R{i} {right}|")
        print(f"{divider}    {divider}")

    print("Legend: A=Agent  V=Visited  ?=Unknown  W=Wumpus  G=Gold  P=Pit\n")

# -----------------------------
# PERCEPTS
# -----------------------------

def get_percepts(pos, wumpus_pos, pits, gold_pos, n, bump=0, scream=0):
    i, j = pos
    adj = [(i+di, j+dj) for di, dj in [(-1,0),(1,0),(0,-1),(0,1)] if 0<=i+di<n and 0<=j+dj<n]

    stench  = 1 if wumpus_pos in adj else 0
    breeze  = 1 if any(p in adj for p in pits) else 0

    # Glitter: triggers when gold is at current pos OR adjacent
    glitter = 1 if gold_pos == pos else 0

    return [stench, breeze, glitter, bump, scream]

# -----------------------------
# ACTIONS
# -----------------------------

def move_forward(pos, direction, n):
    x, y = pos
    dx, dy = {"UP":(-1,0),"DOWN":(1,0),"LEFT":(0,-1),"RIGHT":(0,1)}[direction]
    nx, ny = x+dx, y+dy
    if 0 <= nx < n and 0 <= ny < n:
        return (nx, ny), False
    return pos, True  # bump (no print for auto mode)

def turn_left(d):  return directions[(directions.index(d) - 1) % 4]
def turn_right(d): return directions[(directions.index(d) + 1) % 4]

def shoot_arrow(pos, direction, wumpus_pos, arrow, score):
    if not arrow:
        return wumpus_pos, arrow, score, 0, "No arrow left!"
    arrow = False; score -= 10
    ax, ay = pos
    wx, wy = wumpus_pos if wumpus_pos else (-1, -1)
    hit = ((direction == "RIGHT" and ax == wx and ay < wy) or
           (direction == "LEFT"  and ax == wx and ay > wy) or
           (direction == "DOWN"  and ay == wy and ax < wx) or
           (direction == "UP"    and ay == wy and ax > wx))
    if hit:
        return None, arrow, score, 1, "Wumpus KILLED! You hear a scream!"
    return wumpus_pos, arrow, score, 0, "Arrow missed..."

def grab_gold(pos, gold_pos, score):
    if pos == gold_pos:
        return True, score + 1000, "GOLD GRABBED! You Win!"
    return False, score, "No gold here."

#def climb_out(pos, score, gold_grabbed):
 #   if pos != (0, 0):
  #      return False, score, "Can only climb out from (0,0)."
   # msg = "Escaped WITH the gold!" if gold_grabbed else "Escaped WITHOUT the gold."
    #return True, score, msg

# -----------------------------
# STATUS DISPLAY
# -----------------------------

def display_status(pos, direction, score, arrow, percepts):
    labels = ["Stench","Breeze","Glitter","Bump","Scream"]
    active = [labels[i] for i in range(5) if percepts[i]]
    print(f"\n  Pos:{pos}  Dir:{direction}  Score:{score}  Arrow:{'Yes' if arrow else 'No'}")
    print(f"  Percepts:{percepts}  Active:[{', '.join(active) if active else 'None'}]")

# -----------------------------
# GAME LOOP
# -----------------------------

def play_game(n, manual):
    grid, wumpus_pos, gold_pos, pits = setup_environment(n)
    pos, direction, score, arrow      = (0,0), "RIGHT", 100, True
    gold_grabbed, visited, wumpus_dead = False, {(0,0)}, False
    print("\n--- INITIAL ENVIRONMENT ---")
    view_environment(grid, pos, visited, n, reveal=True)
    print(f"  Wumpus:{wumpus_pos}  Gold:{gold_pos}  Pits:{pits}")

    step = 0
    percepts = get_percepts(pos, wumpus_pos, pits, None if gold_grabbed else gold_pos, n, scream=1 if wumpus_dead else 0)
    while True:
        step += 1

        if manual:
            print(f"\n=== STEP {step} ===")
            display_status(pos, direction, score, arrow, percepts)
            view_environment(grid, pos, visited, n)
            print("  W=Forward  A=Left  D=Right  G=Grab  S=Shoot V=View")
            action = input("  Action: ").strip().upper()
        else:
            # ← Auto mode: only show status, no map, no action result messages
            print(f"\n=== STEP {step} ===")
            display_status(pos, direction, score, arrow, percepts)
            action = random.choice(["W","A","D","G","S"])
            print(f"  Auto Action: {action}")

        score -= 1
        bump = False

        if action == "W":
            new_pos, bump = move_forward(pos, direction, n)
            if bump:
                percepts[3] = 1
                if manual: print("  >> BUMP! Hit the wall.")
            else:
                pos = new_pos; visited.add(pos)
                if manual: print(f"  >> Moved to {pos}")

        elif action == "A":
            direction = turn_left(direction)
            if manual: print(f"  >> Turned Left. Facing: {direction}")

        elif action == "D":
            direction = turn_right(direction)
            if manual: print(f"  >> Turned Right. Facing: {direction}")

        elif action == "G":
            gold_grabbed, score, msg = grab_gold(pos, gold_pos, score)
            if manual: print(f"  >> {msg}")
            if gold_grabbed: break

        elif action == "S":
            wumpus_pos, arrow, score, scream, msg = shoot_arrow(pos, direction, wumpus_pos, arrow, score)
            if scream: wumpus_dead = True
            if manual: print(f"  >> {msg}")

        #elif action == "C":
         #   done, score, msg = climb_out(pos, score, gold_grabbed)
          #  if manual: print(f"  >> {msg}")
           # if done: break

        elif action == "V" and manual:
            # ← Show agent view and full map side by side
            view_dual(grid, pos, visited, n)
            score += 1  # refund since not a game action

        else:
            if manual: print("  >> Invalid action.")
            score += 1  # refund

        # --- Hazard Checks ---
        if pos in pits:
            score -= 1000
            print(f"\n  You FELL into a PIT! Score:{score}"); break
        if wumpus_pos and pos == wumpus_pos:
            print(f"\n  EATEN by the Wumpus! Score:{score}"); break
        if score <= 0:
            print(f"\n  Score reached 0! Game Over."); break
        percepts = get_percepts(pos, wumpus_pos, pits, None if gold_grabbed else gold_pos, n, scream=1 if wumpus_dead else 0)


    print("\n--- FINAL ENVIRONMENT ---")
    view_environment(grid, pos, visited, n, reveal=True)
    print(f"  GAME OVER | Final Score: {score}\n")

# -----------------------------
# MAIN
# -----------------------------

if __name__ == "__main__":
    print("=== WUMPUS WORLD ===")
    n    = int(input("Grid size (n): "))
    mode = input("Manual or Random? (M/R): ").strip().upper()
    play_game(n, manual=(mode == "M"))
