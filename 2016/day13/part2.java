import java.util.ArrayDeque;
import java.util.HashSet;
import java.util.Queue;
import java.util.Set;

record Pos(int x, int y) {};
record State(int steps, Pos position) {};

class part {
    public static int salt = 1364;

    public static int[] d_ = { -1, 0, 1 };

    public static boolean checkIfOpenSpace(int x, int y, int salt) {
        int common = x*x + 3*x + 2*x*y + y + y*y;
        int desc = common + salt;

        int bitCount = 0;
        while (desc != 0) {
            desc = desc & (desc - 1);
            bitCount++;
        }

        return (bitCount % 2) == 0;
    }

    public static int bfs(Pos startPos, int stepLimit, int salt) {
        Queue<State> queue = new ArrayDeque<>();
        queue.add(new State(0, startPos));

        Set<Pos> visited = new HashSet<>();
        while (!queue.isEmpty()) {
            State cur = queue.poll();

            if (cur.steps() > stepLimit) {
                return visited.size();
            }

            if (visited.contains(cur.position())) {
                continue;
            }
            visited.add(cur.position());

            for (int dx : d_) {
                for (int dy : d_) {
                    if (dx == 0 || dy == 0) {
                        if (dx == 0 && dy == 0) {
                            continue;
                        }
                    } else {
                        continue;
                    }

                    int nx = cur.position().x() + dx;
                    int ny = cur.position().y() + dy;

                    if (nx < 0 || ny < 0) {
                        continue;
                    }

                    if (!checkIfOpenSpace(nx, ny, salt)) {
                        continue;
                    }

                    Pos newPosition = new Pos(nx, ny);
                    if (visited.contains(newPosition)) {
                        continue;
                    }

                    queue.add(new State( cur.steps()+1, newPosition));
                }
            }
        }

        return visited.size();
    }

    public static void main(String args[]) {
        Pos startPos = new Pos(1,1);

        int part2Locs = bfs(startPos, 50, salt);
        System.out.printf(">> part2 locations: %d\n", part2Locs);
    }
}
