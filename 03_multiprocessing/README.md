# Lesson 3: Multiprocessing

This lesson covers process-based parallelism, `fork` and `spawn`, copy-on-write,
process synchronization, pipes, queues, managers, process pools, and scheduling
work across GPUs.

## Materials

- [Presentation](03_multiprocessing.pdf)
- [Multiprocessing notebook](code/multiprocessing.ipynb)
- `code/fork_spawn.py` and `code/fork_vs_spawn_run.py`
- `code/pipe.py`, `code/queue_example.py`, and
  `code/mps_queue_vs_manager_queue.py`
- `code/cv_mps_example.py` — process-based cross-validation with a GPU queue
- `exercises/threads_fork_spawn.py` — interaction between threads and process
  start methods

Run multiprocessing scripts as files rather than by importing them. Examples
that use `spawn` rely on the `if __name__ == "__main__"` entry-point guard.
