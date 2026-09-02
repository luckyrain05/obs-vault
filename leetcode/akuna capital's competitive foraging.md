You and a rival forager take turns moving around a 15×15 [[graphs|grid]] eating food. The rival follows a fixed, deterministic strategy. The game ends when all food is eaten; your goal is to eat more of it than the rival.

Each round, you move first, then the rival moves. Repeat until all food is gone.

Your move: stay put, or step left, right, up, or down. The destination must be:

1. On the grid
2. Not a wall
3. Not the rival's current cell

Landing on food eats it, netting you 1 point.

## Input

You are given 15 [[arrays]] of 15 characters each.

| Char | Meaning     |
| ---- | ----------- |
| `.`  | empty space |
| `#`  | wall        |
| `P`  | you         |
| `O`  | the rival   |
| `F`  | food        |

There is exactly one `P` and one `O`.

## The Rival

After your move, the rival steps one cell along a shortest path toward the nearest reachable food, calculated with [[bfs]] and follows the same rules of movement as you. If no food is reachable, the rival stays put.

## Output

Return a string of characters, each one of `U`, `D`, `L`, `R`, or `S` (Up, Down, Left, Right, Stay), representing your moves in the game.

Your string must be a valid set of moves, and must end exactly when the game would end. It is guaranteed that a valid set of moves that ends the game always exists.

## Scoring

Your score per testcase is:

```
10 × (Food you collect / Total Food)
```

1. There are many hidden boards in the judge that your code will run against.
2. Your code must terminate within 10 s.
3. Your final score is the sum of your scores per testcase.
4. You will be judged on both the efficacy and creativity of your solution. You are not expected (nor is it possible) to get 100% on every testcase.

# Solution

```python
from __future__ import annotations

import random
import sys
import time
from collections import deque
from dataclasses import dataclass, field
from enum import IntEnum
from typing import (
    AbstractSet,
    Dict,
    List,
    Optional,
    Tuple,
)

'''
================
Global Constants
================
'''
Cell = Tuple[int, int]

N = 15

DELTA: Dict[str, Cell] = {
    'U': (-1, 0),
    'D': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
    'S': (0, 0),
}

ORDER: List[str] = ['U', 'D', 'L', 'R']

'''
============================
Global Classes and Functions
============================
'''
class Player(IntEnum):
    YOU = 0
    RIVAL = 1
    

def other_player(p: Player) -> Player:
    if p == Player.YOU:
        return Player.RIVAL
    else:
        return Player.YOU


def in_grid(p: Cell) -> bool:
    return 0 <= p[0] < N and 0 <= p[1] < N

@dataclass
class GameState:
    player_positions: List[Cell]
    foods: set[Cell]
    foods_eaten: List[set[Cell]] = field(
        default_factory = lambda: [set(), set()]
    )
    current_player: Player = Player.YOU

    def change_player(self) -> None:
        self.current_player = other_player(
            self.current_player
        )

    def copy(self) -> GameState:
        return GameState(
            player_positions = list(
                self.player_positions
            ),
            foods = set(self.foods),
            foods_eaten = [
                set(eaten)
                for eaten in self.foods_eaten
            ],
            current_player=self.current_player,
        )
        

class Board:
    def __init__(self, grid: List[str]) -> None:
        self.walls: set[Cell] = set()
        self.state: GameState = self._parse(grid)

    def _parse(self, grid: List[str]) -> GameState:
        foods: set[Cell] = set()
        you: Cell = (-1, -1)
        rival: Cell = (-1, -1)
        for r in range(N):
            for c in range(N):
                ch = grid[r][c]
                if ch == '#':
                    self.walls.add((r, c))
                elif ch == 'F':
                    foods.add((r, c))
                elif ch == 'P':
                    you = (r, c)
                elif ch == 'O':
                    rival = (r, c)
        return GameState(
            player_positions=[you, rival],
            foods=foods,
        )

    def bfs(
        self,
        start: Cell,
        blocked: AbstractSet[Cell] = frozenset(),
    ) -> Tuple[Dict[Cell, int], Dict[Cell, str]]:
    
        dist: Dict[Cell, int] = {start: 0}
        first_move: Dict[Cell, str] = {start: 'S'}
        queue = deque([start])
        
        while queue:
            curr_pos = queue.popleft()
            for direction in ORDER:
                dr, dc = DELTA[direction]
                next_pos = (
                    curr_pos[0] + dr,
                    curr_pos[1] + dc,
                )
                
                if (
                    in_grid(next_pos)
                    and next_pos not in self.walls
                    and next_pos not in blocked
                    and next_pos not in dist
                ):
                    fm = first_move[curr_pos]
                    first_move[next_pos] = (
                        direction if fm == 'S' else fm
                    )
                    dist[next_pos] = (
                        dist[curr_pos] + 1
                    )
                    queue.append(next_pos)
                    
        return dist, first_move

    def rival_move(
        self,
        state: GameState,
    ) -> str:
    
        rival = state.player_positions[
            Player.RIVAL
        ]
        you = state.player_positions[Player.YOU]
        dist, first_move = self.bfs(
            rival,
            blocked={you},
        )
        reachable = [
            f for f in state.foods
            if f in dist
        ]
        
        if not reachable:
            return 'S'
            
        closest_food = min(
            reachable,
            key=lambda f: (
                dist[f],
                ORDER.index(first_move[f]),
            ),
        )
        
        return first_move[closest_food]

    def make_player_move(
        self,
        state: GameState,
        move: str,
        player: Player,
    ) -> None:
    
        dr, dc = DELTA[move]
        r, c = state.player_positions[player]
        new_pos = (r + dr, c + dc)
        state.player_positions[player] = new_pos
        
        if new_pos in state.foods:
            state.foods.discard(new_pos)
            state.foods_eaten[player].add(
                new_pos
            )
        state.change_player()

'''
=================
Start of Solution
=================
'''

TIME_BUDGET = 9.0
ROUND_CAP = 4000
_INF = 10 ** 9


def exact_rival_move(
    walls: AbstractSet[Cell],
    you: Cell,
    rival: Cell,
    foods: AbstractSet[Cell],
) -> Tuple[str, int]:

    if not foods:
        return 'S', -1
        
    dist: Dict[Cell, int] = {rival: 0}
    first: Dict[Cell, str] = {rival: 'S'}
    queue = deque([rival])
    hits: List[Cell] = []
    hit_d = -1
    
    while queue:
        cur = queue.popleft()
        d = dist[cur]
        if hit_d >= 0 and d >= hit_d:
            break
        cr, cc = cur
        fc = first[cur]
        
        for direction in ORDER:
            dr, dc = DELTA[direction]
            nxt = (cr + dr, cc + dc)
            
            if (
                nxt not in dist
                and 0 <= nxt[0] < N
                and 0 <= nxt[1] < N
                and nxt not in walls
                and nxt != you
            ):
                first[nxt] = (
                    direction if fc == 'S' else fc
                )
                dist[nxt] = d + 1
                queue.append(nxt)
                
                if nxt in foods:
                    hit_d = d + 1
                    hits.append(nxt)
                    
    if not hits:
        return 'S', -1
        
    return (
        first[min(
            hits,
            key=lambda f: ORDER.index(
                first[f]
            ),
        )],
        hit_d,
    )


def play(grid: List[str]) -> str:
    t0 = time.time()
    board = Board(grid)
    walls = board.walls
    you0, rival0 = board.state.player_positions
    foods0 = frozenset(board.state.foods)
    
    if not foods0:
        return ""

    _dcache: Dict[Cell, Dict[Cell, int]] = {}

    def sdist(cell: Cell) -> Dict[Cell, int]:
        d = _dcache.get(cell)
        if d is None:
            d = board.bfs(cell)[0]
            _dcache[cell] = d
        return d

    zrng = random.Random(0xF00D)
    Z = {
        (r, c): zrng.getrandbits(61)
        for r in range(N)
        for c in range(N)
    }
    
    fh0 = 0
    for f in foods0:
        fh0 ^= Z[f]

    def evaluate(
        you: Cell,
        rival: Cell,
        foods,
        mc: int,
        rc: int,
        rv_fd: int = 0,
        own_w: float = 8.0,
        deny_w: float = 0.0,
    ) -> float:
    
        s = 100.0 * (mc - rc)
        if foods:
            gy = sdist(you).get
            gv = sdist(rival).get
            mine = 0
            near_own = _INF
            near_any = _INF
            
            for f in foods:
                dm = gy(f, _INF)
                if dm < near_any:
                    near_any = dm
                if dm <= gv(f, _INF):
                    mine += 1
                    if dm < near_own:
                        near_own = dm
                        
            s += own_w * (2 * mine - len(foods))
            s += deny_w * (
                30 if rv_fd < 0
                else min(rv_fd, 30)
            )
            if near_own < _INF:
                s -= 0.2 * near_own
            elif near_any < _INF:
                s -= 0.05 * near_any
        return s

    def greedy_finish(
        you: Cell,
        rival: Cell,
        foods,
        mc: int,
        rc: int,
        race_aware: bool = True,
    ) -> Tuple[int, str, bool]:
    
        foods = set(foods)
        out: List[str] = []
        seen: Dict[tuple, int] = {}
        guard = 0
        
        while foods and guard < 2 * ROUND_CAP:
            guard += 1
            dist, first = board.bfs(
                you,
                blocked={rival},
            )
            gv = sdist(rival).get
            mv = 'S'
            bk = None
            for f in foods:
                dm = dist.get(f)
                if dm is None:
                    continue
                win = (
                    0 if (
                        not race_aware
                        or dm <= gv(f, _INF)
                    )
                    else 1
                )
                k = (
                    win,
                    dm,
                    ORDER.index(first[f]),
                )
                if bk is None or k < bk:
                    bk = k
                    mv = first[f]
            if (
                mv == 'S'
                and exact_rival_move(
                    walls,
                    you,
                    rival,
                    foods,
                )[0] == 'S'
            ):
                key = (
                    you,
                    rival,
                    len(foods),
                )
                n = seen.get(key, 0)
                seen[key] = n + 1
                cands = []
                for m2 in ORDER:
                    d2 = DELTA[m2]
                    p2 = (
                        you[0] + d2[0],
                        you[1] + d2[1],
                    )
                    if (
                        in_grid(p2)
                        and p2 not in walls
                        and p2 != rival
                    ):
                        dd = min((
                            sdist(p2).get(
                                f,
                                _INF,
                            )
                            for f in foods
                        ))
                        cands.append((dd, m2))
                if cands:
                    cands.sort()
                    mv = cands[n % len(cands)][1]
            out.append(mv)
            d = DELTA[mv]
            you = (
                you[0] + d[0],
                you[1] + d[1],
            )
            if you in foods:
                foods.discard(you)
                mc += 1
                if not foods:
                    break
            rm = exact_rival_move(
                walls,
                you,
                rival,
                foods,
            )[0]
            d = DELTA[rm]
            rival = (
                rival[0] + d[0],
                rival[1] + d[1],
            )
            if rival in foods:
                foods.discard(rival)
                rc += 1
        return mc - rc, "".join(out), not foods

    best_fin: Optional[Tuple[int, int, str]] = (
        None
    )
    candidates: List[Tuple[int, int, str]] = []

    def note_finish(
        mc: int,
        rc: int,
        moves: str,
    ) -> None:
        nonlocal best_fin
        cand = (mc - rc, -len(moves), moves)
        if (
            best_fin is None
            or cand > best_fin
        ):
            best_fin = cand

    def run_beam(
        width_base: int,
        own_w: float = 8.0,
        deny_w: float = 0.0,
    ) -> int:
        root_foods = set(foods0)
        beam = [(
            evaluate(
                you0,
                rival0,
                root_foods,
                0,
                0,
                0,
                own_w,
                deny_w,
            ),
            you0,
            rival0,
            root_foods,
            0,
            0,
            fh0,
            "",
        )]
        rounds = 0
        while beam:
            rounds += 1
            el = time.time() - t0
            if (
                rounds > ROUND_CAP
                or el > TIME_BUDGET * 0.9
            ):
                break
            frac = el / TIME_BUDGET
            if frac > 0.8:
                width = max(4, width_base // 8)
            elif frac > 0.65:
                width = max(6, width_base // 4)
            elif frac > 0.5:
                width = max(8, width_base // 2)
            else:
                width = width_base
            nxt: Dict[tuple, tuple] = {}
            for (
                _,
                you,
                rival,
                foods,
                mc,
                rc,
                fh,
                moves,
            ) in beam:
                yr, yc = you
                for m in 'UDLRS':
                    dr, dc = DELTA[m]
                    ny = (yr + dr, yc + dc)
                    if (
                        m != 'S'
                        and (
                            not (
                                0 <= ny[0] < N
                                and 0 <= ny[1] < N
                            )
                            or ny in walls
                            or ny == rival
                        )
                    ):
                        continue
                    nfoods = foods
                    nmc = mc
                    nfh = fh
                    if ny in nfoods:
                        nfoods = set(nfoods)
                        nfoods.discard(ny)
                        nmc += 1
                        nfh ^= Z[ny]
                    nmoves = moves + m
                    if not nfoods:
                        note_finish(nmc, rc, nmoves)
                        continue
                    rm, rfd = exact_rival_move(
                        walls,
                        ny,
                        rival,
                        nfoods,
                    )
                    rdr, rdc = DELTA[rm]
                    nrv = (
                        rival[0] + rdr,
                        rival[1] + rdc,
                    )
                    nrc = rc
                    if nrv in nfoods:
                        if nfoods is foods:
                            nfoods = set(nfoods)
                        nfoods.discard(nrv)
                        nrc += 1
                        nfh ^= Z[nrv]
                        if not nfoods:
                            note_finish(
                                nmc,
                                nrc,
                                nmoves,
                            )
                            continue
                    key = (ny, nrv, nfh)
                    sc = evaluate(
                        ny,
                        nrv,
                        nfoods,
                        nmc,
                        nrc,
                        rfd,
                        own_w,
                        deny_w,
                    )
                    cur = nxt.get(key)
                    if (
                        cur is None
                        or sc > cur[0]
                    ):
                        nxt[key] = (
                            sc,
                            ny,
                            nrv,
                            nfoods,
                            nmc,
                            nrc,
                            nfh,
                            nmoves,
                        )
            if not nxt:
                break
            beam = sorted(
                nxt.values(),
                key=lambda t: t[0],
                reverse=True,
            )[:width]
        if beam:
            top = max(
                beam,
                key=lambda t: t[0],
            )
            d, tail, done = greedy_finish(
                top[1],
                top[2],
                top[3],
                top[4],
                top[5],
            )
            if done:
                candidates.append((
                    d,
                    -(len(top[7]) + len(tail)),
                    top[7] + tail,
                ))
        return rounds

    for ra in (True, False):
        d, ms, done = greedy_finish(
            you0,
            rival0,
            foods0,
            0,
            0,
            race_aware=ra,
        )
        if done:
            candidates.append((d, -len(ms), ms))

    p1_start = time.time()
    rounds1 = run_beam(12)
    e1 = time.time() - p1_start

    per_node_round = (
        e1 / (rounds1 * 12)
        if rounds1 and e1 > 1e-4
        else None
    )
    if per_node_round:
        remaining = (
            TIME_BUDGET - (time.time() - t0)
        )
        if remaining > 1.3 * e1:
            width2 = int(
                (remaining * 0.8)
                / (rounds1 * per_node_round)
            )
            width2 = max(12, min(128, width2))
            run_beam(width2, own_w=8.0, deny_w=0.0)
        remaining = (
            TIME_BUDGET - (time.time() - t0)
        )
        if remaining > 1.3 * e1:
            width3 = int(
                (remaining * 0.8)
                / (rounds1 * per_node_round)
            )
            width3 = max(12, min(96, width3))
            run_beam(
                width3,
                own_w=16.0,
                deny_w=1.2,
            )

    if best_fin is not None:
        candidates.append(best_fin)
    if not candidates:
        d, ms, _done = greedy_finish(
            you0,
            rival0,
            set(foods0),
            0,
            0,
        )
        candidates.append((d, -len(ms), ms))
    return max(candidates)[2]


if __name__ == "__main__":
    _lines = sys.stdin.read().splitlines()
    _grid = [
        (
            _lines[i]
            if i < len(_lines)
            else ''
        ).ljust(N)[:N]
        for i in range(N)
    ]
    print(play(_grid))
```

## TS Complexity

## Explanation

## Notes

- [[beam search]]
