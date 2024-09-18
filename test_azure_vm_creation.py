from azure_utils import create_vm
import logging

logging.basicConfig(level=logging.INFO)

def test_vm_creation():
    try:
        vm_details = create_vm("test-vm", 1, 1, 30)  # The values remain the same, but the actual VM size will be Standard_D1_v1
        logging.info(f"VM created successfully: {vm_details}")
        return True
    except Exception as e:
        logging.error(f"Error creating VM: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_vm_creation()
    print(f"VM creation {'succeeded' if success else 'failed'}")
