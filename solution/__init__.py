import docker
from config import Config
from docker.errors import NotFound

# Get config variables
config = Config()


def start_postgres_container() -> None:
    """
    Starts a PostgreSQL container if it doesn't exist or if it's not running.

    Return: None
    """
    client = docker.from_env()

    try:
        container = client.containers.get(config.CONT_NAME)
        if container.status != "running":
            container.start()
    except NotFound:
        client.images.pull(config.IMAGE)
        client.containers.run(
            image=config.IMAGE,
            name=config.CONT_NAME,
            environment={
                "POSTGRES_USER": config.DB_USER,
                "POSTGRES_PASSWORD": config.DB_PASS,
                "POSTGRES_DB": config.DB_NAME,
            },
            ports={"5432/tcp": 5432},
            detach=True,
            restart_policy={"Name": "always"},
            volumes={
                config.VOLUME_NAME: {"bind": "/var/lib/postgresql/data", "mode": "rw"}
            },
        )


if __name__ == "__main__":
    start_postgres_container()
