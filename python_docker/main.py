from utils.container_controller import spawn_container, stop_container
import logging

USE_DOCKER = True   # set to False if you want to use podman


def main():
    logging.basicConfig(level=logging.WARNING)
    container = spawn_container(
        container_type="docker" if USE_DOCKER else "podman",
        # image="python:3.8",
        # timeout=10,
        # name="testcontainer",
    )

    print(container.command('python --version'))
    stop_container(container)


if __name__ == "__main__":
    main()