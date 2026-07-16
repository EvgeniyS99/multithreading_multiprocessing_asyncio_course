from concurrent.futures import ProcessPoolExecutor, as_completed
from sklearn.model_selection import KFold
import multiprocessing as mp
import os

mp.set_start_method('spawn', force=True)


def run_fold_with_gpu_queue(dataset, info, train_idx, val_idx, fold, savepath, config, gpu_q):
    # 1) занять GPU (если свободных нет — блокируемся)
    gpu_id = gpu_q.get()
    try:
        os.environ["CUDA_VISIBLE_DEVICES"] = str(gpu_id)

        train(dataset, info, train_idx, val_idx,
              gpu_idx=0, device_id=gpu_id,
              fold=fold, savepath=savepath, config=config)

        return fold, gpu_id

    except Exception as e:
        print('Exception in process', e)
    finally:
        gpu_q.put(gpu_id)


def parallel_training(dataset, info, savepath, cv=5,
                      gpu_ids=[0, 1, 2], random_state=0,
                      config=None):
    kf = KFold(n_splits=cv, shuffle=True, random_state=random_state)

    # Manager нужен, чтобы очередь GPU была proxy и её можно было передать в submit()
    with mp.Manager() as manager:
        gpu_queue = manager.Queue()
        for gpu_id in gpu_ids:
            gpu_queue.put(gpu_id)

        futures = []
        with ProcessPoolExecutor(max_workers=cv) as executor:
            for fold, (train_idx, val_idx) in enumerate(kf.split(dataset)):
                futures.append(executor.submit(
                    run_fold_with_gpu_queue,
                    dataset, info, train_idx, val_idx, fold, savepath, config, gpu_queue
                ))

            # as_completed — получать результаты по мере завершения фолдов
            results = [f.result() for f in as_completed(futures)]

    return results
