import logging
import os

import dotenv
import requests

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

PORT_API_URL = "https://api.getport.io/v1"
PORT_CLIENT_ID = os.getenv("PORT_CLIENT_ID")
PORT_CLIENT_SECRET = os.getenv("PORT_CLIENT_SECRET")
JFROG_ACCESS_TOKEN = os.getenv("JFROG_ACCESS_TOKEN")
JFROG_HOST_URL = os.getenv("JFROG_HOST_URL")


REPOSITORY_BLUEPRINT = "jfrogRepository"
BUILD_BLUEPRINT = "jfrogBuild"


## Get Port Access Token
credentials = {"clientId": PORT_CLIENT_ID, "clientSecret": PORT_CLIENT_SECRET}
token_response = requests.post(f"{PORT_API_URL}/auth/access_token", json=credentials)
access_token = token_response.json()["accessToken"]

# You can now use the value in access_token when making further requests
headers = {"Authorization": f"Bearer {access_token}"}


def add_entity_to_port(blueprint_id, entity_object, transform_function):
    """A function to create the passed entity in Port

    Params
    --------------
    blueprint_id: str
        The blueprint id to create the entity in Port

    entity_object: dict
        The entity to add in your Port catalog

    transform_function: function
        A function to transform the entity object to the Port entity object

    Returns
    --------------
    response: dict
        The response object after calling the webhook
    """
    logger.info(f"Adding entity to Port: {entity_object}")
    entity_payload = transform_function(entity_object)
    response = requests.post(
        (
            f"{PORT_API_URL}/blueprints/"
            f"{blueprint_id}/entities?upsert=true&merge=true"
        ),
        json=entity_payload,
        headers=headers,
    )
    logger.info(response.json())


def get_all_builds():
    logger.info("Getting all builds")
    url = f"{JFROG_HOST_URL}/artifactory/api/build"
    response = requests.get(
        url, headers={"Authorization": "Bearer " + JFROG_ACCESS_TOKEN}
    )
    response.raise_for_status()
    builds = response.json()["builds"]
    return builds


def get_all_repositories():
    logger.info("Getting all repositories")
    url = f"{JFROG_HOST_URL}/artifactory/api/repositories"
    response = requests.get(
        url, headers={"Authorization": "Bearer " + JFROG_ACCESS_TOKEN}
    )
    response.raise_for_status()
    repositories = response.json()
    return repositories


if __name__ == "__main__":
    logger.info("Starting Port integration")
    for repository in get_all_repositories():
        repository_object = {
            "key": repository["key"],
            "description": repository.get("description", ""),
            "type": repository["type"].upper(),
            "url": repository["url"],
            "packageType": repository["packageType"].upper(),
        }
        transform_build_function = lambda x: {
            "identifier": repository_object["key"],
            "title": repository_object["key"],
            "properties": {
                **repository_object,
            },
        }
        logger.info(f"Added repository: {repository_object['key']}")
        add_entity_to_port(
            REPOSITORY_BLUEPRINT, repository_object, transform_build_function
        )

    logger.info("Completed repositories, starting builds")
    for build in get_all_builds():
        build_object = {
            "name": build["uri"].split("/")[-1],
            "uri": build["uri"],
            "lastStarted": build["lastStarted"],
        }
        transform_build_function = lambda x: {
            "identifier": build_object["name"],
            "title": build_object["name"],
            "properties": {
                **build_object,
            },
        }
        logger.info(f"Added build: {build_object['name']}")
        add_entity_to_port(BUILD_BLUEPRINT, build_object, transform_build_function)
