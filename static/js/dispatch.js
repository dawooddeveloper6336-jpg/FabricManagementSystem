document.addEventListener('DOMContentLoaded', function() {
    // Add specification row
    const addButton = document.getElementById('add-spec-row');
    const tableBody = document.getElementById('spec-table-body');
    const totalForms = document.getElementById('id_specifications-TOTAL_FORMS');

    if (addButton) {
        addButton.addEventListener('click', function() {
            const formIdx = parseInt(totalForms.value);
            const newRow = document.createElement('tr');
            newRow.classList.add('spec-form-row');
            newRow.innerHTML = `
                <td>
                    <input type="text" name="specifications-${formIdx}-spec_name" class="form-control" placeholder="Specification Name">
                </td>
                <td>
                    <input type="text" name="specifications-${formIdx}-spec_value" class="form-control" placeholder="Specification Value">
                </td>
                <td>
                    <button type="button" class="btn btn-danger btn-sm remove-spec-row">Remove</button>
                </td>
            `;
            tableBody.appendChild(newRow);
            totalForms.value = formIdx + 1;
        });
    }

    // Remove specification row
    tableBody.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('remove-spec-row')) {
            const row = e.target.closest('tr');
            const deleteCheckbox = row.querySelector('input[name$="-DELETE"]');
            if (deleteCheckbox) {
                // For existing rows, mark delete and hide row
                deleteCheckbox.checked = true;
                row.style.display = 'none';
            } else {
                row.remove();
                // Re-index formset numbers
                // Not needed if we just remove the row and update TOTAL_FORMS
                const total = parseInt(totalForms.value);
                totalForms.value = total - 1;
            }
        }
    });
});