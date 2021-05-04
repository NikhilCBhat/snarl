# Sequence Diagram
Note: Steps proceed sequentially except for processing transitions which are based on cases A, B, and C.
```
                    User                 Client         Server           Level              Player      Adversary

                      +                   +                +              +                   +          +
         +--------------------------------+-----------------------------------------------------------------------+
         |  Setup     |            Start Server            |  Setup Level |                   |          |        |
         |            +-------------------+--------------> +------------->+                   |          |        |
         |            |                   |                |              +                   |          |        |
         |            |   Start Client    |   Add User     |          Create Player           |          |        |
         |            +------------------>---------------->---------------+------------------>+          |        |
         |            |                   |                |              |                   |          |        |
         |            |   Start Game      |   Start Game   |              |                   |          |        |
         |            +------------------>+--------------->+              |                   |          |        |
         |            |                                    |              |                   |          |        |
         +--------------------------------+-----------------------------------------------------------------------+
         |  Start     |                   |                |              |                   |          |        |
 A       |  Level     |                   |                | Start Level  |   Add Players     |          |        |
+------> |            |                   |                +------------> +------------------>+          |        |
| Players|            |    Render Game    |   Game State   |              |                   |          |        |
| exit   |            | <-----------------+ <------------+ |              |                   |          |        |
| the    |            |                   |                |              |                   |          |        |
| level  +--------------------------------------------------------------------------------------------------------+
+------+ | Processing |  Show Availible   |                |              |                   |          |        |
         |            |  Actions          |  Game State    |              |                   |          |        |
B        |            | <---------------+ | <--------------+              |                   |          |        |
+------+ |            |                   |                |              +                   |          |        |
| When   |            |  Perform Action   |    Action      |     Update Player                |          |        |
| neither|            +-----------------> +--------------> +--------------+------------------>+          |        |
| A nor C|            |                   |                |              |                   |          |        |
+----->  |            |                   |                |  Update State|    Update Level   |          |        |
         |            |                   |                +<-------------+ <-----------------+          |        |
         |            |                   |                |              | Game State        |          |        |
         |            |                   |                +-------------------------------------------->+        |
         |            |                   |                |              |                   |          |        |
C+-----+ |            |    Render Game    |  Game State    |  Update State|         Do Adversary Action  |        |
+ When   |            | <---------------+ +<----------------<--------------<------------------+----------+        |
| players|            |                   |                |              |                   |          |        |
| die or +--------------------------------------------------------------------------------------------------------+
| win.   | End Game   |                   |                |              |                   |          |        |
+------> |            |  Game Over Screen |   Game State   |              |                   |          |        |
         |            +<------------------+ <--------------+              |                   |          |        |
         |            |                   |                |              |                   |          |        |
         +------------+-------------------+----------------+--------------+-------------------+----------+--------+

```