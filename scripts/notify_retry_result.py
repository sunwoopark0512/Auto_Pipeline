import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')


def notify_retry_result():
    logging.info("Retry process finished. Notify as needed.")


if __name__ == "__main__":
    notify_retry_result()
