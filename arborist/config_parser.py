import json


def get_config_data():
    providers = []
    datasets = []
    providersRequiredFields = set()
    datasetsRequiredFields = set()

    with open('arborist/data/config.json') as json_file:
        data = json.load(json_file)
        for provider in data['providers']:
            providers.append(provider)
        for dataset in data['datasets']:
            datasets.append(dataset)
        for requiredField in data['providers_required_fields']:
            providersRequiredFields.add(requiredField)
        for requiredField in data['datasets_required_fields']:
            datasetsRequiredFields.add(requiredField)

    # Each provider must have all required fields
    for provider in providers:
        providerKeys = set([key for key in provider])
        if not providersRequiredFields.issubset(providerKeys):
            exit("{} is a required field for providers, but have not been supplied for all providers\n"
                 "Check config.json and try again\n"
                 "Exiting".format(', '.join(list(providersRequiredFields - providerKeys))))

    # Each dataset must have all required fields
    for dataset in datasets:
        datasetKeys = set([key for key in dataset])
        if not datasetsRequiredFields.issubset(datasetKeys):
            exit("{} is a required field for datasets, but have not been supplied for all datasets\n"
                 "Check config.json and try again\n"
                 "Exiting".format(', '.join(list(datasetsRequiredFields - datasetKeys))))

    # Each dataset must have a provider
    providersSetA = set([dataset['provider'] for dataset in datasets])
    providersSetB = set([provider['provider'] for provider in providers])

    if not providersSetA.issubset(providersSetB):
        exit("{} has not been listed as a dataset provider\n"
             "Add The provider to the config.json or remove datasets using the provider\n"
             "Exiting".format(', '.join(list(providersSetA - providersSetB))))

    # Format dataset fields
    providers = format_providers(providers)
    datasets = format_datasets(datasets)

    return providers, datasets


def format_datasets(datasets):
    formattedDatasets = []
    for dataset in datasets:
        newDataset = dataset.copy()
        newDataset['provider'] = dataset['provider'].lower().replace(' ', '_')
        newDataset['version'] = dataset['version'].replace('.', '_')
        newDataset['update_date'] = dataset['update_date'].replace('.', '-').replace('/', '-')
        newDataset['name'] = dataset['name'].lower().replace('.', '_').replace('/', '_')
        formattedDatasets.append(newDataset)

    return formattedDatasets


def format_providers(providers):
    formattedProviders = []
    for provider in providers:
        newProvider = provider.copy()
        newProvider['provider'] = provider['provider'].lower().replace(' ', '_')
        formattedProviders.append(newProvider)

    return formattedProviders