document.addEventListener('DOMContentLoaded', function() {
    const addBtn = document.getElementById('add-item-row');
    const itemBody = document.getElementById('item-body');
    const totalForms = document.getElementById('id_items-TOTAL_FORMS');
    const invoiceTotalSpan = document.getElementById('invoice-total');

    function computeRowAmount(row) {
        const qty = parseFloat(row.querySelector('.quantity-input').value) || 0;
        const rate = parseFloat(row.querySelector('.rate-input').value) || 0;
        const amount = qty * rate;
        const amountCell = row.querySelector('.item-amount');
        if (amountCell) amountCell.textContent = amount.toFixed(2);
        return amount;
    }

    function computeTotal() {
        let total = 0;
        document.querySelectorAll('.item-row').forEach(row => {
            total += parseFloat(row.querySelector('.item-amount')?.textContent) || 0;
        });
        invoiceTotalSpan.textContent = total.toFixed(2);
    }

    // Add row
    if (addBtn) {
        addBtn.addEventListener('click', function() {
            const idx = parseInt(totalForms.value);
            const newRow = document.createElement('tr');
            newRow.className = 'item-row';
            newRow.innerHTML = `
                <td><select name="items-${idx}-fabric" class="form-select fabric-select"><option value="">---------</option></select></td>
                <td><input type="text" name="items-${idx}-color" class="form-control color-input"></td>
                <td><select name="items-${idx}-grade" class="form-select grade-select"><option value="A">Grade A</option><option value="B">Grade B</option><option value="C">CP</option></select></td>
                <td><input type="number" name="items-${idx}-quantity" class="form-control quantity-input" step="0.01" min="0"></td>
                <td><input type="number" name="items-${idx}-rate" class="form-control rate-input" step="0.01" min="0"></td>
                <td class="item-amount">0.00</td>
                <td><button type="button" class="btn btn-danger btn-sm remove-item-row">Remove</button></td>
            `;
            itemBody.appendChild(newRow);
            totalForms.value = idx + 1;

            // Re-attach events
            attachRowEvents(newRow);
        });
    }

    function attachRowEvents(row) {
        const qtyInput = row.querySelector('.quantity-input');
        const rateInput = row.querySelector('.rate-input');
        const removeBtn = row.querySelector('.remove-item-row');

        if (qtyInput && rateInput) {
            qtyInput.addEventListener('input', function() {
                computeRowAmount(row);
                computeTotal();
            });
            rateInput.addEventListener('input', function() {
                computeRowAmount(row);
                computeTotal();
            });
        }

        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                row.remove();
                computeTotal();
            });
        }
    }

    // Attach events to existing rows
    document.querySelectorAll('.item-row').forEach(row => attachRowEvents(row));

    // Initial total
    computeTotal();
});