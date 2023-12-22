# example-jfrog-container-images
Python Script for Ingesting JFrog Artifacts and Builds in Port

## Getting started
In this example, you will create blueprints for `jfrog_build` and `jfrog_repository` that ingests builds and repositories from your Jfrog installation into Port. You will then use a Python script to make API calls to Jfrog's REST API to fetch the data from your account.

### Blueprints
Create the following blueprints in Port using the schemas:

#### Build
```json
{
  "identifier": "jfrogBuild",
  "description": "This blueprint represents a build from JFrog",
  "title": "JFrog Build",
  "icon": "JfrogXray",
  "schema": {
    "properties": {
      "uri": {
        "type": "string",
        "title": "Build URI",
        "description": "URI to the build"
      },
      "name": {
        "type": "string",
        "title": "Build name",
        "description": "Name of the build"
      },
      "lastStarted": {
        "type": "string",
        "title": "Last build time",
        "description": "Last time the build ran",
        "format": "date-time"
      }
    },
    "required": []
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

#### Repository
```json
{
  "identifier": "jfrogRepository",
  "description": "This blueprint represents a repository on Jfrog",
  "title": "JFrog Repository",
  "icon": "JfrogXray",
  "schema": {
    "properties": {
      "key": {
        "type": "string",
        "title": "Key",
        "description": "Name of the repository"
      },
      "description": {
        "type": "string",
        "title": "Description",
        "description": "Description of the repository"
      },
      "type": {
        "type": "string",
        "title": "Repository Type",
        "description": "Type of the repository",
        "enum": [
          "LOCAL",
          "REMOTE",
          "VIRTUAL",
          "FEDERATED",
          "DISTRIBUTION"
        ],
        "enumColors": {
          "LOCAL": "blue",
          "REMOTE": "bronze",
          "VIRTUAL": "darkGray",
          "FEDERATED": "green",
          "DISTRIBUTION": "lightGray"
        }
      },
      "url": {
        "type": "string",
        "title": "Repository URL",
        "description": "URL to the repository",
        "format": "url"
      },
      "packageType": {
        "type": "string",
        "title": "Package type",
        "description": "Type of the package"
      }
    },
    "required": []
  },
  "mirrorProperties": {},
  "calculationProperties": {},
  "aggregationProperties": {},
  "relations": {}
}
```

### Running the Python script
First clone the repository and cd into the work directory with:
```bash
$ git clone git@github.com:port-labs/example-jfrog-container-images.git
$ cd example-jfrog-container-images
```

Install the needed dependencies within the context of a virtual environment with:
```bash
$ virtualenv venv
$ source venv/bin/activate
$ pip3 install -r requirements.txt
```

To ingest your data, you need to populate some environment variables. You can do that by either duplicating the `.example.env` file and renaming the copy as `.env`, then edit the values as needed; or run the commands below in your terminal:

```bash
export JFROG_ACCESS_TOKEN=access_token_here
export PORT_CLIENT_ID=port_client_id
export PORT_CLIENT_SECRET=port_client_secret
export JFROG_HOST_URL=https://subdomain.jfrog.io
```

Each variable required are:
- JFROG_ACCESS_TOKEN: You can get that by following instructions in the [Jfrog documentation](https://jfrog.com/help/r/jfrog-platform-administration-documentation/access-tokens)
- PORT_CLIENT_ID: Port Client ID
- PORT_CLIENT_SECRET: Port Client secret
- JFROG_HOST_URL: The host URL of your Jfrog instance