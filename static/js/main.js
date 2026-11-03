// Computer Repair Management System (CRMS) - Vanilla JS ES6+

document.addEventListener('DOMContentLoaded', () => {
    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            });
        }, 5000);
    }

    // Print Receipt helper
    const printButtons = document.querySelectorAll('.btn-print-receipt');
    printButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            window.print();
        });
    });

    // Delete confirmation helper
    const deleteButtons = document.querySelectorAll('.btn-confirm-delete');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const itemName = btn.getAttribute('data-name') || 'this item';
            if (!confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`)) {
                e.preventDefault();
            }
        });
    });
});
