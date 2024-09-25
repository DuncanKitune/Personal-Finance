function addIncomeRow() {
    const incomeSection = document.getElementById('income-section');
    const newRow = `
        <div class="input-group">
            <input type="text" name="income[]" placeholder="Income description">
            <input type="number" name="income_amount[]" placeholder="Amount">
        </div>`;
    incomeSection.insertAdjacentHTML('beforeend', newRow);
}

function addExpenseRow() {
    const expenseSection = document.getElementById('expense-section');
    const newRow = `
        <div class="input-group">
            <input type="text" name="expense[]" placeholder="Expense description">
            <input type="number" name="expense_amount[]" placeholder="Amount">
        </div>`;
    expenseSection.insertAdjacentHTML('beforeend', newRow);
}
document.getElementById('formula').addEventListener('change', function() {
    // Hide all additional input sections initially
    document.querySelectorAll('.hidden').forEach(function(el) {
        el.classList.add('hidden');
    });
    // Show the relevant inputs based on the selected formula
    var selectedFormula = this.value;
    document.getElementById('additionalInputs').classList.remove('hidden');
    if (selectedFormula === 'Value at Risk (VaR)') {
        document.getElementById('VaRInputs').classList.remove('hidden');
    } else if (selectedFormula === 'Sharpe Ratio') {
        document.getElementById('SharpeRatioInputs').classList.remove('hidden');
    } else if (selectedFormula === 'Discounted Cash Flow (DCF)') {
        document.getElementById('DCFInputs').classList.remove('hidden');
    }
    // Add more conditions for other formulas as necessary
});