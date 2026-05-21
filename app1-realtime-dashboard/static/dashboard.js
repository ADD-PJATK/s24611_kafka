let charts = {};
let dataUpdater;

async function subscribeTicker() {
    const select = document.getElementById('ticker-select');
    const ticker = select.value.trim().toUpperCase();

    if (!ticker) {
        alert('Please select a ticker');
        return;
    }

    try {
        const response = await fetch(`/api/subscribe/${ticker}`, {
            method: 'POST',
        });

        if (!response.ok) {
            alert('Failed to subscribe');
            return;
        }

        select.value = '';

        // Create chart for this ticker
        createChart(ticker);

        // Update subscriptions list
        updateSubscriptions();

    } catch (error) {
        console.error('Error subscribing:', error);
        alert('Error subscribing to ticker');
    }
}

async function unsubscribeTicker(ticker) {
    try {
        await fetch(`/api/unsubscribe/${ticker}`, {
            method: 'POST',
        });

        // Remove chart
        if (charts[ticker]) {
            charts[ticker].destroy();
            delete charts[ticker];
        }

        const card = document.getElementById(`chart-${ticker}`);
        if (card) {
            card.remove();
        }

        updateSubscriptions();
    } catch (error) {
        console.error('Error unsubscribing:', error);
    }
}

function createChart(ticker) {
    const container = document.getElementById('charts-container');

    // Create card
    const card = document.createElement('div');
    card.id = `chart-${ticker}`;
    card.className = 'chart-card';
    card.innerHTML = `
        <h3>
            <span class="ticker-name">${ticker}</span>
            <span class="current-price" id="price-${ticker}">-</span>
        </h3>
        <div class="price-info">
            <div class="price-info-item">
                <span class="price-info-label">Time</span>
                <span class="price-info-value" id="time-${ticker}">-</span>
            </div>
            <div class="price-info-item">
                <span class="price-info-label">Volume</span>
                <span class="price-info-value" id="volume-${ticker}">-</span>
            </div>
            <div class="price-info-item">
                <span class="price-info-label">Currency</span>
                <span class="price-info-value" id="currency-${ticker}">-</span>
            </div>
        </div>
        <div class="chart-wrapper">
            <canvas id="canvas-${ticker}"></canvas>
        </div>
    `;
    container.appendChild(card);

    // Create chart
    const ctx = document.getElementById(`canvas-${ticker}`).getContext('2d');
    charts[ticker] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: `${ticker} Price (PLN)`,
                data: [],
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: '#667eea',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    labels: {
                        color: '#333',
                        font: { size: 12 }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        color: '#999'
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        color: '#999',
                        maxRotation: 45,
                        minRotation: 0
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

async function updateData() {
    const subs = await fetch('/api/current-subscriptions').then(r => r.json());

    for (const ticker of subs.subscriptions) {
        try {
            const response = await fetch(`/api/data/${ticker}`);
            const json = await response.json();
            const { data, latest } = json;

            if (data.length === 0) continue;

            // Update chart
            if (charts[ticker]) {
                const labels = data.map(d => {
                    const date = new Date(d.ts);
                    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
                });
                const prices = data.map(d => d.price);

                charts[ticker].data.labels = labels;
                charts[ticker].data.datasets[0].data = prices;
                charts[ticker].update('none');
            }

            // Update info
            if (latest) {
                document.getElementById(`price-${ticker}`).textContent = `$${latest.price.toFixed(2)}`;
                document.getElementById(`time-${ticker}`).textContent = new Date(latest.timestamp).toLocaleTimeString();
                document.getElementById(`volume-${ticker}`).textContent = latest.volume.toLocaleString();
                document.getElementById(`currency-${ticker}`).textContent = latest.currency;
            }
        } catch (error) {
            console.error(`Error updating ${ticker}:`, error);
        }
    }
}

async function updateSubscriptions() {
    const subs = await fetch('/api/current-subscriptions').then(r => r.json());
    const list = document.getElementById('subscriptions-list');

    list.innerHTML = '';

    if (subs.subscriptions.length === 0) {
        list.innerHTML = '<p style="color: #999;">No active subscriptions. Select a ticker to begin.</p>';
        return;
    }

    for (const ticker of subs.subscriptions) {
        const badge = document.createElement('div');
        badge.className = 'ticker-badge';
        badge.innerHTML = `
            ${ticker}
            <button class="remove" onclick="unsubscribeTicker('${ticker}')" title="Unsubscribe">×</button>
        `;
        list.appendChild(badge);
    }
}

// Start auto-update interval
window.addEventListener('load', () => {
    updateSubscriptions();
    dataUpdater = setInterval(updateData, 500); // Update every 500ms
});

window.addEventListener('beforeunload', () => {
    if (dataUpdater) clearInterval(dataUpdater);
});
