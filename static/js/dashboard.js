document.addEventListener('DOMContentLoaded', function() {
    const vmForm = document.getElementById('vm-form');
    const vmList = document.getElementById('vm-list');

    // Load existing VMs
    loadVMs();

    // Handle form submission
    vmForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData(vmForm);
        const vmData = Object.fromEntries(formData.entries());

        fetch('/api/vms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(vmData),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            loadVMs();
            vmForm.reset();
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    });

    function loadVMs() {
        fetch('/api/vms')
        .then(response => response.json())
        .then(vms => {
            vmList.innerHTML = '';
            vms.forEach(vm => {
                const vmElement = document.createElement('div');
                vmElement.classList.add('vm-item');
                vmElement.innerHTML = `
                    <h3>${vm.name}</h3>
                    <p>CPU Cores: ${vm.cpu_cores}</p>
                    <p>RAM: ${vm.ram} GB</p>
                    <p>Disk Size: ${vm.disk_size} GB</p>
                `;
                vmList.appendChild(vmElement);
            });
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }
});
