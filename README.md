# LocalSignets

Local API for Signets

## Getting Started

### Prerequisites

*This project was built and tested on Python v3.12*

- Python 3
    ```
    python --version
    ```

### Installation

1. Clone the repo
2. Navigate to the cloned directory
3. Install dependencies
    ```bash
    # Create a virtual environment (recommended)
    python -m venv .venv
    source ./.venv/bin/activate  # On Windows use `.venv\Scripts\activate

    # Install requirements
    pip install -r requirements.txt
    ```
4. Configure your `./responses` directory.
   - To start, you can create a directory called `responses` in the root of this project and copy all the contents from `./responses-template` into it. The data in the `./responses` directory is what the API will return. If you want to fill it with you own data, you can retrieve your data with [the bruno collection](#bruno)
5. Run the API
   ```bash
   python signets.py
   ```
6. Get the IP address of the machine running the server
7. Point your ETSMobile application to use your local API
    - Go to `urls.dart` in Notre-Dame
        ```bash
        # Replace
        static const String signetsAPI = "https://signets-ens.etsmtl.ca/Secure/WebServices/SignetsMobile.asmx";

        # With
        static const String signetsAPI = http://<IP_FROM_STEP_6>:8000
        ```

ETSMobile should now use your local API instead of the remote one. You can add/modify files in the responses directory to fit your needs.

Additionnally, you can retrieve the XML from Signets or your local API using the Bruno collection in `./docs/signets.json`. More info [here](#bruno-collection).

The responses can be found in `./responses`. You can edit them as you wish

## Bruno

### Step 1. Import the collection

Import the `signets.json` into your Bruno client.

![collection](./docs/bruno_import.png)

### Step 2. Set Collection Variables

Set your username and password that you use for ETSMobile.
Additionally, you could set the `localAPI` address if you have the API running on another machine.

![vars](./docs/bruno_vars.png)

### Step 3. Testing Endpoints

You can now call the endpoints from the imported collection.
- To call the Signets production endpoint use `{{signets}}` as the endpoint.
- To call your local API use `{{localAPI}}` as the endpoint.

*Note that some endpoints require you to specify some data in the request body. (e.g: listeElementsEvaluation, listeHoraireEtProf, listeHoraireDesSeances, listeEvaluationCours)*