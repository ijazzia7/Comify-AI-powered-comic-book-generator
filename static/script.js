document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const cryptoList = document.getElementById('cryptoList');
    const cryptoDetail = document.getElementById('cryptoDetail');
    const detailCoinName = document.getElementById('detailCoinName');
    const detailCoinImage = document.getElementById('detailCoinImage');
    const detailCoinPrice = document.getElementById('detailCoinPrice');
    const detailCoinChange = document.getElementById('detailCoinChange');
    const detailCoinMarketCap = document.getElementById('detailCoinMarketCap');
    const closeDetail = document.getElementById('closeDetail');
    const searchInput = document.getElementById('searchInput');
    const filterSelect = document.getElementById('filterSelect');
    const themeToggle = document.getElementById('themeToggle');
    
    // Chart initialization
    const ctx = document.getElementById('priceChart').getContext('2d');
    let priceChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Price (USD)',
                data: [],
                borderColor: '#2a71d0',
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 5,
                fill: true,
                backgroundColor: 'rgba(42, 113, 208, 0.1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return `$${context.raw.toFixed(2)}`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        display: false
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return '$' + value.toFixed(2);
                        }
                    }
                }
            }
        }
    });
    
    // State
    let cryptocurrencies = [];
    let filteredCryptos = [];
    
    // Initialize the app
    init();
    
    function init() {
        loadCryptocurrencies();
        setupEventListeners();
        checkDarkModePreference();
    }
    
    function loadCryptocurrencies() {
        fetch('/api/cryptos')
            .then(response => response.json())
            .then(data => {
                cryptocurrencies = data;
                filteredCryptos = [...cryptocurrencies];
                renderCryptoList();
            })
            .catch(error => {
                console.error('Error fetching cryptocurrencies:', error);
                cryptoList.innerHTML = '<div class="loading">Failed to load data. Please try again later.</div>';
            });
    }
    
    function renderCryptoList() {
        cryptoList.innerHTML = '';
        
        if (filteredCryptos.length === 0) {
            cryptoList.innerHTML = '<div class="loading">No cryptocurrencies found.</div>';
            return;
        }
        
        filteredCryptos.forEach(crypto => {
            const cryptoItem = document.createElement('div');
            cryptoItem.className = 'crypto-item';
            cryptoItem.dataset.id = crypto.id;
            
            const changeClass = crypto.price_change_percentage_24h >= 0 ? 'change-positive' : 'change-negative';
            const changeIcon = crypto.price_change_percentage_24h >= 0 ? '↗' : '↘';
            
            cryptoItem.innerHTML = `
                <img src="${crypto.image}" alt="${crypto.name}">
                <div class="crypto-info">
                    <div class="crypto-name">${crypto.name}</div>
                    <div class="crypto-symbol">${crypto.symbol}</div>
                </div>
                <div class="crypto-price-data">
                    <div class="crypto-price">$${crypto.current_price.toLocaleString()}</div>
                    <div class="crypto-change ${changeClass}">${changeIcon} ${Math.abs(crypto.price_change_percentage_24h).toFixed(2)}%</div>
                </div>
            `;
            
            cryptoItem.addEventListener('click', () => showCryptoDetail(crypto));
            cryptoList.appendChild(cryptoItem);
        });
    }
    
    function showCryptoDetail(crypto) {
        // Update detail view with basic info
        detailCoinName.textContent = `${crypto.name} (${crypto.symbol.toUpperCase()})`;
        detailCoinImage.src = crypto.image;
        detailCoinPrice.textContent = `$${crypto.current_price.toLocaleString()}`;
        
        const changeClass = crypto.price_change_percentage_24h >= 0 ? 'change-positive' : 'change-negative';
        detailCoinChange.textContent = `${crypto.price_change_percentage_24h >= 0 ? '+' : ''}${crypto.price_change_percentage_24h.toFixed(2)}%`;
        detailCoinChange.className = changeClass;
        
        detailCoinMarketCap.textContent = `$${crypto.market_cap.toLocaleString()}`;
        
        // Show loading state for chart
        priceChart.data.labels = [];
        priceChart.data.datasets[0].data = [];
        priceChart.update();
        
        // Fetch historical data
        fetch(`/api/history/${crypto.id}`)
            .then(response => response.json())
            .then(historicalData => {
                updateChart(historicalData);
            })
            .catch(error => {
                console.error('Error fetching historical data:', error);
                updateChart([]);
            });
        
        // Show detail view
        cryptoDetail.style.display = 'block';
    }
    
    function updateChart(historicalData) {
        const labels = [];
        const data = [];
        
        historicalData.forEach(([timestamp, price]) => {
            const date = new Date(timestamp);
            labels.push(date.toLocaleDateString());
            data.push(price);
        });
        
        priceChart.data.labels = labels;
        priceChart.data.datasets[0].data = data;
        
        // Update line color based on price trend
        const firstPrice = data[0];
        const lastPrice = data[data.length - 1];
        const lineColor = lastPrice >= firstPrice ? '#16c784' : '#ea3943';
        const fillColor = lastPrice >= firstPrice ? 'rgba(22, 199, 132, 0.1)' : 'rgba(234, 57, 67, 0.1)';
        
        priceChart.data.datasets[0].borderColor = lineColor;
        priceChart.data.datasets[0].backgroundColor = fillColor;
        
        priceChart.update();
    }
    
    function filterCryptos() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterValue = filterSelect.value;
        
        filteredCryptos = cryptocurrencies.filter(crypto => {
            const matchesSearch = crypto.name.toLowerCase().includes(searchTerm) || 
                                 crypto.symbol.toLowerCase().includes(searchTerm);
            
            let matchesFilter = true;
            if (filterValue === 'gainers') {
                matchesFilter = crypto.price_change_percentage_24h > 0;
            } else if (filterValue === 'losers') {
                matchesFilter = crypto.price_change_percentage_24h < 0;
            }
            
            return matchesSearch && matchesFilter;
        });
        
        renderCryptoList();
    }
    
    function setupEventListeners() {
        // Close detail view
        closeDetail.addEventListener('click', () => {
            cryptoDetail.style.display = 'none';
        });
        
        // Search functionality
        searchInput.addEventListener('input', filterCryptos);
        
        // Filter functionality
        filterSelect.addEventListener('change', filterCryptos);
        
        // Theme toggle
        themeToggle.addEventListener('click', toggleDarkMode);
    }
    
    function toggleDarkMode() {
        const body = document.body;
        const isDarkMode = body.classList.contains('dark-mode');
        
        if (isDarkMode) {
            body.classList.remove('dark-mode');
            body.classList.add('light-mode');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
            localStorage.setItem('theme', 'light');
        } else {
            body.classList.remove('light-mode');
            body.classList.add('dark-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
            localStorage.setItem('theme', 'dark');
        }
        
        // Update chart colors based on theme
        updateChartTheme();
    }
    
    function checkDarkModePreference() {
        const savedTheme = localStorage.getItem('theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        
        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            document.body.classList.add('dark-mode');
            document.body.classList.remove('light-mode');
            themeToggle.innerHTML = '<i class="fas fa-sun"></i>';
        } else {
            document.body.classList.remove('dark-mode');
            document.body.classList.add('light-mode');
            themeToggle.innerHTML = '<i class="fas fa-moon"></i>';
        }
        
        updateChartTheme();
    }
    
    function updateChartTheme() {
        const isDarkMode = document.body.classList.contains('dark-mode');
        
        const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.05)' : 'rgba(0, 0, 0, 0.05)';
        const ticksColor = isDarkMode ? '#e0e0e0' : '#666';
        
        priceChart.options.scales.y.grid.color = gridColor;
        priceChart.options.scales.x.ticks.color = ticksColor;
        priceChart.options.scales.y.ticks.color = ticksColor;
        priceChart.update();
    }
});