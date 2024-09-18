from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient
import os

# Azure configuration
SUBSCRIPTION_ID = os.environ.get('AZURE_SUBSCRIPTION_ID')
RESOURCE_GROUP = os.environ.get('AZURE_RESOURCE_GROUP')
LOCATION = 'eastus'

def get_azure_clients():
    credential = ClientSecretCredential(
        tenant_id=os.environ['AZURE_TENANT_ID'],
        client_id=os.environ['AZURE_CLIENT_ID'],
        client_secret=os.environ['AZURE_CLIENT_SECRET']
    )
    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)
    network_client = NetworkManagementClient(credential, SUBSCRIPTION_ID)
    resource_client = ResourceManagementClient(credential, SUBSCRIPTION_ID)
    return compute_client, network_client, resource_client

def create_vm(name, cpu_cores, ram, disk_size):
    compute_client, network_client, resource_client = get_azure_clients()

    # Create a resource group
    resource_client.resource_groups.create_or_update(RESOURCE_GROUP, {'location': LOCATION})

    # Create a virtual network
    vnet_name = f'{name}-vnet'
    subnet_name = f'{name}-subnet'
    network_client.virtual_networks.begin_create_or_update(
        RESOURCE_GROUP,
        vnet_name,
        {
            'location': LOCATION,
            'address_space': {'address_prefixes': ['10.0.0.0/16']},
            'subnets': [{'name': subnet_name, 'address_prefix': '10.0.0.0/24'}]
        }
    ).result()

    subnet = network_client.subnets.get(RESOURCE_GROUP, vnet_name, subnet_name)

    # Create a public IP address
    public_ip = network_client.public_ip_addresses.begin_create_or_update(
        RESOURCE_GROUP,
        f'{name}-ip',
        {'location': LOCATION, 'sku': {'name': 'Basic'}, 'public_ip_allocation_method': 'Dynamic'}
    ).result()

    # Create a network interface
    nic = network_client.network_interfaces.begin_create_or_update(
        RESOURCE_GROUP,
        f'{name}-nic',
        {
            'location': LOCATION,
            'ip_configurations': [{
                'name': f'{name}-ipconfig',
                'subnet': {'id': subnet.id},
                'public_ip_address': {'id': public_ip.id}
            }]
        }
    ).result()

    # Create the virtual machine
    vm_parameters = {
        'location': LOCATION,
        'os_profile': {
            'computer_name': name,
            'admin_username': 'azureuser',
            'admin_password': 'Password123!'  # In production, use a more secure method
        },
        'hardware_profile': {
            'vm_size': 'Standard_D2s_v3'  # Updated to Standard_D2s_v3 as requested
        },
        'storage_profile': {
            'image_reference': {
                'publisher': 'Canonical',
                'offer': 'UbuntuServer',
                'sku': '18.04-LTS',
                'version': 'latest'
            },
            'os_disk': {
                'create_option': 'FromImage',
                'managed_disk': {'storage_account_type': 'Standard_LRS'},
                'disk_size_gb': disk_size
            }
        },
        'network_profile': {
            'network_interfaces': [{'id': nic.id}]
        }
    }

    vm = compute_client.virtual_machines.begin_create_or_update(
        RESOURCE_GROUP, name, vm_parameters
    ).result()

    return {
        'id': vm.id,
        'name': vm.name,
        'location': vm.location,
        'vm_size': vm.hardware_profile.vm_size,
        'provisioning_state': vm.provisioning_state
    }
