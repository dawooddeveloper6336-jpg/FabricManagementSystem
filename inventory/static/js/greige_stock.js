document.addEventListener('DOMContentLoaded', function() {
    const exportBtn = document.getElementById('exportExcel');
    if (exportBtn) {
        exportBtn.addEventListener('click', function() {
            const table = document.getElementById('stockTable');
            if (!table) return;
            let csv = [];
            const rows = table.querySelectorAll('tr');
            for (let row of rows) {
                const cols = row.querySelectorAll('th, td');
                let rowData = [];
                for (let col of cols) {
                    let text = col.innerText.trim();
                    rowData.push(text);
                }
                csv.push(rowData.join(','));
            }
            const csvContent = csv.join('\n');
            const blob = new Blob([csvContent], { type: 'text/csv' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'greige_stock.csv';
            a.click();
            URL.revokeObjectURL(url);
        });
    }
});