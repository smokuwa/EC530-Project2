import os
import sys
from multiprocessing import Process

from services import cli_service
from services import document_db_service
from services import embedding_service
from services import inference_service
from services import vector_index_service


SERVICES = [
    document_db_service.main,
    embedding_service.main,
    inference_service.main,
    vector_index_service.main,
]


def run_silently(target):
    with open(os.devnull, "w") as devnull:
        sys.stdout = devnull
        sys.stderr = devnull
        target()


def main():
    processes = []

    for target in SERVICES:
        process = Process(target=run_silently, args=(target,))
        process.daemon = True
        process.start()
        processes.append(process)

    try:
        cli_service.main()
    finally:
        for process in processes:
            if process.is_alive():
                process.terminate()
        for process in processes:
            process.join()


if __name__ == "__main__":
    main()
