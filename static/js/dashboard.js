document.addEventListener('DOMContentLoaded', function() {
    const vmForm = document.getElementById('vm-form');
    if (vmForm) {
        vmForm.addEventListener('submit', handleVMFormSubmit);
    }

    loadVMs();
});

function loadVMs() {
    fetch('/api/vms')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateVMList(data);
        })
        .catch(error => {
            console.error('Error loading VMs:', error);
            const vmList = document.getElementById('vm-list');
            if (vmList) {
                vmList.innerHTML = '<p>Error loading VMs. Please try again later.</p>';
            }
        });
}

function updateVMList(vms) {
    const vmList = document.getElementById('vm-list');
    if (!vmList) return;

    if (vms.length === 0) {
        vmList.innerHTML = '<p>No VMs provisioned yet.</p>';
        return;
    }

    let html = '<ul>';
    vms.forEach(vm => {
        html += `<li>${vm.name} - CPU: ${vm.cpu_cores}, RAM: ${vm.ram}GB, Disk: ${vm.disk_size}GB</li>`;
    });
    html += '</ul>';
    vmList.innerHTML = html;
}

function handleVMFormSubmit(event) {
    event.preventDefault();
    // Add form submission logic here
    console.log('VM form submitted');
}
