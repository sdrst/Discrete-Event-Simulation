# Discrete Event Simulation

A discrete-event simulation of a two-stage (tandem) queueing system, driven by a
custom binary min-heap event scheduler with O(n log n) complexity.

Customers arrive, wait for one of several **primary** servers, then move on to
wait for one of several **secondary** servers before leaving the system. Each
event (arrival, primary service completion, secondary service completion) is
scheduled on a min-heap keyed by event time, so the simulation always processes
events in chronological order.

## Project structure

```
.
├── src/des/
│   ├── cli.py          # entry point: reads input, drives the event loop, prints stats
│   ├── simulation.py    # Simulation class: core event-handling logic
│   ├── event.py         # Event: a single scheduled arrival/service event
│   ├── server.py        # Server: per-server busy/idle state
│   ├── queue.py          # Queue: FIFO wait queue used by each stage
│   └── heap.py          # siftup/siftdown: min-heap operations over events
├── data/
│   └── sample_input.txt # example input file
├── docs/
│   └── DES.pdf          # write-up of the simulation's design and results
├── pyproject.toml
└── LICENSE
```

## Installation

Requires Python 3.8+. No external dependencies.

```bash
pip install -e .
```

## Usage

Run as an installed command:

```bash
des
```

or as a module, without installing:

```bash
python -m des
```

You'll be prompted for an input file:

```
Please enter a filename: data/sample_input.txt
```

The simulation runs to completion and prints per-event queue state as it goes,
followed by summary statistics: total served, average time and length in each
queue, and per-server idle time.

## Input file format

Whitespace-separated:

```
<primary server count>
<secondary server count>
<arrival time> <primary service time> <secondary service time>
<arrival time> <primary service time> <secondary service time>
...
```

Each subsequent line describes one customer: the time they arrive, how long
they need at the primary stage, and how long they need at the secondary stage.
See `data/sample_input.txt` for an example.

## License

MIT — see [LICENSE](LICENSE).
