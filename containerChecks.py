import docker
import sys
import configInit
import time


def checkPiholeValidity(container):
    if "pihole" in container.attrs["Config"]["Image"]:
        return True
    else:
        return False


def checkPiholeAvailability(dockerClient, config):
    try:
        container = dockerClient.containers.get(config.piholeContainerName)
        return True, container
    except Exception as e:
        return False, None


def mainChecks():
    try:
        client = docker.DockerClient(base_url='unix://var/run/docker.sock')
    except Exception as e:
        print("ERROR: Cannot find docker server! Now exiting!")
        sys.exit(0)

    print("Reading the config from the YAML file...")
    config = configInit.initConfig()

    print("Checking the availability and validity of Pihole container...")
    available, container = checkPiholeAvailability(client, config)

    if not available:
        print(
            f"WARN: The container name {config.piholeContainerName} is not valid or the container is stopped - trying again in 5 minutes")
        time.sleep(300)
        return mainChecks()

    if not checkPiholeValidity(container):
        print(f"ERROR: The container with name {config.piholeContainerName} is not created from the pihole image! Please use a container that it is the Pihole! Now exiting!")
        sys.exit(0)

    print("SUCCESS: The specified container is currently running and is in fact Pihole container!")
    return container, config
