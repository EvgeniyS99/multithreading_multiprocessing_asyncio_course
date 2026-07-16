import os
import sys
import time
import multiprocessing as mp


# --- "состояние интерпретатора" на уровне модуля ---
GLOBAL_LIST = ["module_init"]     # создаётся при импорте модуля
GLOBAL_VALUE = 1                  # тоже

def child(label: str, parent_modules: list, name: str):
    global GLOBAL_VALUE
    # Этот код выполнится в дочернем процессе
    print(f'RUN CHILD NUMBER {name}')
    print(f"\n[{label} CHILD] pid={os.getpid()}, ppid={os.getppid()}")
    print(f"[{label} CHILD] GLOBAL_VALUE={GLOBAL_VALUE}")
    print(f"[{label} CHILD] GLOBAL_LIST={GLOBAL_LIST}")
    child_modules = sorted(sys.modules)
    print(f"[{label} CHILD] imported modules count={child_modules}")
    print(f'[CHILD] diff modules {set(child_modules)-set(parent_modules)}')

    # покажем, что память не общая: меняем globals в ребёнке
    GLOBAL_LIST.append("child_was_here")
    # и “пишем” в глобал (вызовет COW при fork)
    # (в spawn это просто своя память)
    GLOBAL_VALUE = 999

    print(f"[{label} CHILD] after mutation: GLOBAL_VALUE={GLOBAL_VALUE}")
    print(f"[{label} CHILD] after mutation: GLOBAL_LIST={GLOBAL_LIST}")

def run_main(method: str):
    global GLOBAL_VALUE
    print("\n" + "=" * 70)
    print(f"[PARENT] method={method}, pid={os.getpid()}")
    print(f"[PARENT] before starting child: GLOBAL_VALUE={GLOBAL_VALUE}, GLOBAL_LIST={GLOBAL_LIST}")
    parent_modules = sorted(sys.modules)
    print(f"[PARENT] imported modules count={parent_modules}")

    # ВАЖНО: меняем состояние ПЕРЕД стартом процесса
    GLOBAL_LIST.append("parent_added_before_start")
    GLOBAL_VALUE = 42

    print(f"[PARENT] after mutation (before start): GLOBAL_VALUE={GLOBAL_VALUE}, GLOBAL_LIST={GLOBAL_LIST}")

    ctx = mp.get_context(method)
    p1 = ctx.Process(target=child, args=(method, parent_modules, 'child process 1'))
    p2 = ctx.Process(target=child, args=(method, parent_modules, 'child process 2'))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # Проверим, что изменения ребёнка не вернулись в родителя
    print(f"\n[PARENT] after child exit: GLOBAL_VALUE={GLOBAL_VALUE}, GLOBAL_LIST={GLOBAL_LIST}")

if __name__ == "__main__":
    # spawn есть везде
    # fork'а нет на Windows
    run_main("fork")
