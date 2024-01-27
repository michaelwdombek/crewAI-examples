from .container_protocol import Container


def _init_container(image: str = None, container_type: str = "docker") -> Container:
    """
    Initializes a container object, optionally passes an image to use and a timeout how long the container will run
    Args:
        image: image from dockerhub to use, should be a python image
        container_type: which container engine to use, defaults to docker also supports podman

    Returns:
        container: a container object
    """
    try:
        if container_type == "docker":
            import utils.docker_client as container
            return container.Container(
                image=image)
        if container_type == "podman":
            import utils.podman_client as container
    except ImportError as e:
        print(f'could not load python library:\n {e}')
        exit(1)


def spawn_container(
        name: str = None,
        image: str = None,
        container_type: str = "docker",
        timeout: str = None) -> Container:
    """
    Initializes and starts a container, optionally passes an image to use and a timeout how long the container will run

    Args:
        name: name of the container, defaults to uuid4 str
        image: an image from dockerhub to use, should be a python image
        timeout: how long the container will run in seconds, defaults to infinity (set by the class implementation)
        container_type: which container engine to use, defaults to docker also supports podman
    Returns:
        container: a container object that is running and can be used to execute commands
    """
    container = _init_container(
        image=image,
        container_type=container_type)
    container.create(name=name, timeout=timeout)
    container.start()
    return container


def stop_container(container: Container):
    """
        Stops and removes a container
    Args:
        container:

    Returns:

    """
    container.stop()
    container.remove()
