document.addEventListener('DOMContentLoaded', function() {
    const dispatchSelect = document.getElementById('id_dispatch');
    const detailsDiv = document.getElementById('dispatch-details');
    const gradeBody = document.getElementById('grade-body');
    const addGradeBtn = document.getElementById('add-grade-row');
    const totalForms = document.getElementById('id_grades-TOTAL_FORMS');

    // Fetch dispatch details
    function loadDispatchDetails(dispatchId) {
        if (!dispatchId) {
            detailsDiv.style.display = 'none';
            return;
        }
        fetch(`/inventory/ajax/dispatch-colors/?dispatch_id=${dispatchId}`)
            .then(response => response.json())
            .then(data => {
                if (data.dispatch_number) {
                    document.getElementById('dd-number').textContent = data.dispatch_number;
                    document.getElementById('dd-date').textContent = data.dispatch_date;
                    document.getElementById('dd-manufacturer').textContent = data.manufacturer;
                    document.getElementById('dd-fabric').textContent = data.fabric;
                    document.getElementById('dd-qty').textContent = data.dispatch_quantity;
                    detailsDiv.style.display = 'block';
                    // Optionally pre‑fill a grade row with the main color
                    // We'll let user add rows manually
                } else {
                    detailsDiv.style.display = 'none';
                }
            })
            .catch(() => detailsDiv.style.display = 'none');
    }

    // Initial load if editing
    if (dispatchSelect && dispatchSelect.value) {
        loadDispatchDetails(dispatchSelect.value);
    }

    // On change
    if (dispatchSelect) {
        dispatchSelect.addEventListener('change', function() {
            loadDispatchDetails(this.value);
        });
    }

    // Add grade row
    if (addGradeBtn) {
        addGradeBtn.addEventListener('click', function() {
            const formIdx = parseInt(totalForms.value);
            const newRow = document.createElement('tr');
            newRow.classList.add('grade-row');
            newRow.innerHTML = `
                <td><input type="text" name="grades-${formIdx}-color" class="form-control" placeholder="Color"></td>
                <td><input type="number" name="grades-${formIdx}-dispatch_quantity" class="form-control" step="0.01" placeholder="Dispatch Qty" readonly></td>
                <td><input type="number" name="grades-${formIdx}-grade_a" class="form-control grade-input" step="0.01" placeholder="0"></td>
                <td><input type="number" name="grades-${formIdx}-grade_b" class="form-control grade-input" step="0.01" placeholder="0"></td>
                <td><input type="number" name="grades-${formIdx}-cp" class="form-control grade-input" step="0.01" placeholder="0"></td>
            `;
            gradeBody.appendChild(newRow);
            totalForms.value = formIdx + 1;
        });
    }

    // Auto-calculate received, loss, gain per row? The backend does this on save.
});