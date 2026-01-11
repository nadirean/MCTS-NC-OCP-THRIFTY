## Overview

**MCTS-NC-OCP-THRIFTY** contains experiments and analysis for the OCP_THRIFTY variant of the MCTS-NC (Monte Carlo Tree Search — Numba CUDA) implementation.

This project explores GPU-parallel MCTS variant (OCP-THRIFTY) and measures how configuration choices (number of trees and number of playouts) affect throughput and decision quality.

## What this repository contains

- `mcts-nc-ocp-thrifty.ipynb` — Notebook with analysis & plots for the OCP_THRIFTY experiments.
- `plots/` — Generated plots used in the report.
- `report/` — Full project report (LaTeX) summarizing methodology, experiments, monitoring, and conclusions.
- `presentation/` - presentation on the topic and results.

## Requirements & environment

**Hardware / OS**

- NVIDIA GPU required for GPU experiments (tested with RTX 1650).

**Software**

- Python >= 3.13
- CUDA toolkit and NVIDIA drivers (tested with **CUDA 12.8** in the report)
- Libraries: Numba (numba.cuda), numpy, pandas, matplotlib, seaborn, psutil, pynvml, py-cpuinfo, jupyter, ipykernel, tqdm

## Quick setup

1. Clone this repository:

```bash
git clone <this-repo-url> mcts-nc-ocp-thrifty
cd mcts-nc-ocp-thrifty
```

2. Clone the original MCTS-NC repository (required):

```bash
# upstream repo used by this project
git clone https://github.com/pklesk/mcts_numba_cuda.git mcts_numba_cuda-main
```

3. Create and activate a virtual environment:

```bash
uv sync
source .venv/bin/activate
```

## Key findings

- Throughput (playouts/sec) scales up strongly with `n_trees` and `n_playouts`; the maximum observed speed in the measured grid was for `n_trees=16, n_playouts=512`.
- Decision quality (`best_q`) is fairly stable across configurations; it was slightly higher in some low-playout configurations (report notes highest average `best_q` around `n_trees=1, n_playouts=32`).
- GPU utilization was moderate for the tested settings — potential for better occupancy by reducing host-device transfers and tuning kernel/block parameters.

Proposed improvements in the report include: reducing host<->device transfers, tuning block/thread parameters, better RNG initialization, kernel fusion, and a dynamic playout budget depending on tree depth.
