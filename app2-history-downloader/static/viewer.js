let currentData = [];

function showStatus(message, type = 'info') {
    const status = document.getElementById('status');
    status.textContent = message;
    status.className = `status-message ${type}`;
}

function clearResults() {
    document.getElementById('results').innerHTML = '';
    currentData = [];
}

async function fetchData() {
    const select = document.getElementById('ticker-select');
    const duration = document.getElementById('duration').value;

    const selected = Array.from(select.selectedOptions).map(opt => opt.value);

    if (selected.length === 0) {
        showStatus('Please select at least one ticker', 'error');
        return;
    }

    showStatus(`⏳ Fetching data for ${selected.length} ticker(s) (${duration} minutes)...`, 'loading');

    const btn = document.getElementById('fetch-btn');
    btn.disabled = true;
    btn.innerHTML = '<span class="spinner"></span> Fetching...';

    try {
        const response = await fetch('/api/fetch-history', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tickers: selected, duration: duration })
        });

        if (!response.ok) {
            const error = await response.json();
            showStatus(`Error: ${error.error}`, 'error');
            return;
        }

        const result = await response.json();
        currentData = result.data;

        showStatus(`✅ Fetched ${result.count} records`, 'success');

        if (currentData.length > 0) {
            displayResults(currentData, selected);
        } else {
            showStatus('No data found for selected tickers', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showStatus(`Error: ${error.message}`, 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = '📥 Fetch Data';
    }
}

function displayResults(data, tickers) {
    clearResults();
    const resultsDiv = document.getElementById('results');

    // Results header
    const header = document.createElement('div');
    header.className = 'results-header';
    header.innerHTML = `
        <h2>📈 Results (${data.length} records)</h2>
        <div class="export-buttons">
            <button class="secondary-btn" onclick="exportData('csv')">📥 Download CSV</button>
            <button class="secondary-btn" onclick="exportData('json')">📥 Download JSON</button>
        </div>
    `;
    resultsDiv.appendChild(header);

    // Chart
    displayChart(data, tickers);

    // Table
    displayTable(data);
}

function displayChart(data, tickers) {
    if (data.length === 0) return;

    const resultsDiv = document.getElementById('results');
    const container = document.createElement('div');
    container.className = 'chart-container';

    const canvas = document.createElement('canvas');
    container.innerHTML = `<h3>Price Trend</h3>`;
    container.appendChild(canvas);
    resultsDiv.appendChild(container);

    // Prepare data by ticker
    const tickerData = {};
    data.forEach(record => {
        if (!tickerData[record.ticker]) {
            tickerData[record.ticker] = [];
        }
        tickerData[record.ticker].push(record);
    });

    // Sort each ticker's data by timestamp
    Object.keys(tickerData).forEach(ticker => {
        tickerData[ticker].sort((a, b) => new Date(a.ts) - new Date(b.ts));
    });

    // Build datasets
    const colors = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b'];
    const datasets = [];
    let colorIdx = 0;

    Object.keys(tickerData).forEach(ticker => {
        const color = colors[colorIdx++ % colors.length];
        datasets.push({
            label: ticker,
            data: tickerData[ticker].map(d => d.price),
            borderColor: color,
            backgroundColor: color + '20',
            borderWidth: 2,
            fill: false,
            tension: 0.3,
            pointRadius: 3,
            pointBackgroundColor: color
        });
    });

    const labels = data.length > 0 ? data.map(d => {
        const date = new Date(d.ts);
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    }).slice(0, 50) : []; // Show max 50 labels to avoid crowding

    new Chart(canvas, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: { color: '#333' }
                }
            },
            scales: {
                y: {
                    ticks: { color: '#999' },
                    grid: { color: 'rgba(0, 0, 0, 0.05)' }
                },
                x: {
                    ticks: { color: '#999', maxRotation: 45 },
                    grid: { display: false }
                }
            }
        }
    });
}

function displayTable(data) {
    if (data.length === 0) return;

    const resultsDiv = document.getElementById('results');
    const wrapper = document.createElement('div');
    wrapper.className = 'table-wrapper';

    const table = document.createElement('table');
    table.innerHTML = `
        <thead>
            <tr>
                <th>Ticker</th>
                <th>Timestamp</th>
                <th>Price</th>
                <th>Currency</th>
                <th>Volume</th>
                <th>Seq</th>
            </tr>
        </thead>
        <tbody></tbody>
    `;

    const tbody = table.querySelector('tbody');
    data.forEach(record => {
        const row = document.createElement('tr');
        const date = new Date(record.ts);
        row.innerHTML = `
            <td class="ticker-cell">${record.ticker}</td>
            <td>${date.toLocaleString()}</td>
            <td>${record.price.toFixed(2)}</td>
            <td>${record.currency}</td>
            <td>${record.volume.toLocaleString()}</td>
            <td>${record.seq}</td>
        `;
        tbody.appendChild(row);
    });

    wrapper.appendChild(table);
    resultsDiv.appendChild(wrapper);
}

async function exportData(format) {
    if (currentData.length === 0) {
        showStatus('No data to export', 'error');
        return;
    }

    const endpoint = format === 'csv' ? '/api/export-csv' : '/api/export-json';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ data: currentData })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        // Download file
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = response.headers.get('content-disposition')?.split('filename=')[1] || `data.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        showStatus(`✅ Downloaded as ${format.toUpperCase()}`, 'success');
    } catch (error) {
        console.error('Export error:', error);
        showStatus(`Error exporting data: ${error.message}`, 'error');
    }
}
