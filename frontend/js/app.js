/**
 * 股票行情系统前端应用
 * 使用原生JavaScript实现
 */

class StockApp {
    constructor() {
        this.baseURL = '/api';
        this.currentStock = null;
        this.currentPage = 1;
        this.pageSize = 20;
        this.chart = null;
        
        this.init();
    }
    
    /**
     * 初始化应用
     */
    init() {
        this.bindEvents();
        this.loadMarketOverview();
        this.loadHotStocks();
    }
    
    /**
     * 绑定事件监听器
     */
    bindEvents() {
        // 搜索功能
        const searchBtn = document.getElementById('searchBtn');
        const searchInput = document.getElementById('searchInput');
        
        searchBtn.addEventListener('click', () => this.searchStocks());
        searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.searchStocks();
            }
        });
        
        // 返回按钮
        const backBtn = document.getElementById('backBtn');
        backBtn.addEventListener('click', () => this.showHotStocks());
        
        // 分页按钮
        const prevPage = document.getElementById('prevPage');
        const nextPage = document.getElementById('nextPage');
        
        prevPage.addEventListener('click', () => this.changePage(-1));
        nextPage.addEventListener('click', () => this.changePage(1));
        
        // 图表周期按钮
        const periodBtns = document.querySelectorAll('.period-btn');
        periodBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                periodBtns.forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                
                if (this.currentStock) {
                    const period = parseInt(e.target.dataset.period);
                    this.loadStockHistory(this.currentStock, period);
                }
            });
        });
        
        // 模态框关闭
        const closeModal = document.getElementById('closeModal');
        const errorModal = document.getElementById('errorModal');
        
        closeModal.addEventListener('click', () => {
            errorModal.style.display = 'none';
        });
        
        window.addEventListener('click', (e) => {
            if (e.target === errorModal) {
                errorModal.style.display = 'none';
            }
        });
    }
    
    /**
     * 显示错误信息
     */
    showError(message) {
        const errorMessage = document.getElementById('errorMessage');
        const errorModal = document.getElementById('errorModal');
        
        errorMessage.textContent = message;
        errorModal.style.display = 'flex';
    }
    
    /**
     * 发起API请求
     */
    async apiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${this.baseURL}${endpoint}`, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API请求失败:', error);
            this.showError(`请求失败: ${error.message}`);
            throw error;
        }
    }
    
    /**
     * 加载市场概览
     */
    async loadMarketOverview() {
        try {
            const data = await this.apiRequest('/market/');
            this.updateMarketOverview(data);
        } catch (error) {
            console.error('加载市场概览失败:', error);
        }
    }
    
    /**
     * 更新市场概览显示
     */
    updateMarketOverview(data) {
        // 更新上证指数
        if (data.sh_index) {
            const shValue = document.getElementById('shIndexValue');
            const shChange = document.getElementById('shIndexChange');
            
            shValue.textContent = data.sh_index.current.toFixed(2);
            
            const changeText = `${data.sh_index.change_amount >= 0 ? '+' : ''}${data.sh_index.change_amount.toFixed(2)} (${data.sh_index.change_rate >= 0 ? '+' : ''}${data.sh_index.change_rate.toFixed(2)}%)`;
            shChange.textContent = changeText;
            shChange.className = `index-change ${data.sh_index.change_rate >= 0 ? 'up' : 'down'}`;
        }
        
        // 更新深证成指
        if (data.sz_index) {
            const szValue = document.getElementById('szIndexValue');
            const szChange = document.getElementById('szIndexChange');
            
            szValue.textContent = data.sz_index.current.toFixed(2);
            
            const changeText = `${data.sz_index.change_amount >= 0 ? '+' : ''}${data.sz_index.change_amount.toFixed(2)} (${data.sz_index.change_rate >= 0 ? '+' : ''}${data.sz_index.change_rate.toFixed(2)}%)`;
            szChange.textContent = changeText;
            szChange.className = `index-change ${data.sz_index.change_rate >= 0 ? 'up' : 'down'}`;
        }
        
        // 更新市场统计
        document.getElementById('totalStocks').textContent = data.total_stocks || '--';
        document.getElementById('upCount').textContent = data.up_count || '--';
        document.getElementById('downCount').textContent = data.down_count || '--';
    }
    
    /**
     * 搜索股票
     */
    async searchStocks() {
        const keyword = document.getElementById('searchInput').value.trim();
        
        if (!keyword) {
            this.showError('请输入搜索关键词');
            return;
        }
        
        try {
            const data = await this.apiRequest(`/search/?q=${encodeURIComponent(keyword)}`);
            this.showSearchResults(data);
        } catch (error) {
            console.error('搜索失败:', error);
        }
    }
    
    /**
     * 显示搜索结果
     */
    showSearchResults(results) {
        const searchResults = document.getElementById('searchResults');
        const resultsContainer = document.getElementById('resultsContainer');
        const hotStocks = document.getElementById('hotStocks');
        const stockDetail = document.getElementById('stockDetail');
        
        // 隐藏其他区域
        hotStocks.style.display = 'none';
        stockDetail.style.display = 'none';
        
        // 清空并显示搜索结果
        resultsContainer.innerHTML = '';
        
        if (results.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align: center; color: #666; padding: 2rem;">未找到相关股票</p>';
        } else {
            results.forEach(stock => {
                const card = this.createStockCard(stock);
                resultsContainer.appendChild(card);
            });
        }
        
        searchResults.style.display = 'block';
        searchResults.classList.add('fade-in');
    }
    
    /**
     * 创建股票卡片
     */
    createStockCard(stock) {
        const card = document.createElement('div');
        card.className = 'result-card';
        card.addEventListener('click', () => this.showStockDetail(stock.code));
        
        const changeClass = stock.change_rate >= 0 ? 'up' : 'down';
        const changeSymbol = stock.change_rate >= 0 ? '+' : '';
        
        card.innerHTML = `
            <div class="result-header">
                <div>
                    <div class="stock-code">${stock.code}</div>
                    <div class="stock-name">${stock.name}</div>
                </div>
                <div style="text-align: right;">
                    <div class="stock-price">¥${stock.current_price.toFixed(2)}</div>
                    <div class="stock-change ${changeClass}">${changeSymbol}${stock.change_rate.toFixed(2)}%</div>
                </div>
            </div>
        `;
        
        return card;
    }
    
    /**
     * 加载热门股票
     */
    async loadHotStocks() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        const stocksGrid = document.getElementById('stocksGrid');
        
        loadingIndicator.style.display = 'block';
        stocksGrid.innerHTML = '';
        
        try {
            const data = await this.apiRequest(`/list/?page=${this.currentPage}&page_size=${this.pageSize}`);
            this.updateHotStocks(data);
            this.updatePagination(data);
        } catch (error) {
            console.error('加载热门股票失败:', error);
        } finally {
            loadingIndicator.style.display = 'none';
        }
    }
    
    /**
     * 更新热门股票显示
     */
    updateHotStocks(data) {
        const stocksGrid = document.getElementById('stocksGrid');
        stocksGrid.innerHTML = '';
        
        data.results.forEach(stock => {
            const card = document.createElement('div');
            card.className = 'stock-card';
            card.addEventListener('click', () => this.showStockDetail(stock.code));
            
            card.innerHTML = `
                <div class="stock-header">
                    <div class="stock-info">
                        <h4>${stock.name}</h4>
                        <div class="code">${stock.code}</div>
                    </div>
                    <div class="stock-price-info">
                        <div class="price">--</div>
                        <div class="change">--</div>
                    </div>
                </div>
            `;
            
            stocksGrid.appendChild(card);
            
            // 异步加载实时价格
            this.loadStockRealtime(stock.code, card);
        });
    }
    
    /**
     * 加载股票实时数据
     */
    async loadStockRealtime(code, cardElement) {
        try {
            const data = await this.apiRequest(`/stocks/${code}/realtime/`);
            
            const priceElement = cardElement.querySelector('.price');
            const changeElement = cardElement.querySelector('.change');
            
            priceElement.textContent = `¥${data.current_price}`;
            
            const changeClass = data.change_rate >= 0 ? 'up' : 'down';
            const changeSymbol = data.change_rate >= 0 ? '+' : '';
            
            changeElement.textContent = `${changeSymbol}${data.change_rate}%`;
            changeElement.className = `change ${changeClass}`;
            
        } catch (error) {
            console.error(`加载股票 ${code} 实时数据失败:`, error);
        }
    }
    
    /**
     * 更新分页信息
     */
    updatePagination(data) {
        const prevPage = document.getElementById('prevPage');
        const nextPage = document.getElementById('nextPage');
        const pageInfo = document.getElementById('pageInfo');
        
        const totalPages = Math.ceil(data.count / this.pageSize);
        
        prevPage.disabled = this.currentPage <= 1;
        nextPage.disabled = this.currentPage >= totalPages;
        
        pageInfo.textContent = `第 ${this.currentPage} 页 / 共 ${totalPages} 页`;
    }
    
    /**
     * 切换页面
     */
    changePage(direction) {
        this.currentPage += direction;
        this.loadHotStocks();
    }
    
    /**
     * 显示股票详情
     */
    async showStockDetail(code) {
        this.currentStock = code;
        
        const searchResults = document.getElementById('searchResults');
        const hotStocks = document.getElementById('hotStocks');
        const stockDetail = document.getElementById('stockDetail');
        
        // 隐藏其他区域
        searchResults.style.display = 'none';
        hotStocks.style.display = 'none';
        
        // 显示股票详情
        stockDetail.style.display = 'block';
        stockDetail.classList.add('fade-in');
        
        try {
            // 加载股票基本信息和实时数据
            await this.loadStockInfo(code);
            
            // 加载历史数据和图表
            await this.loadStockHistory(code, 30);
            
        } catch (error) {
            console.error('加载股票详情失败:', error);
        }
    }
    
    /**
     * 加载股票基本信息
     */
    async loadStockInfo(code) {
        try {
            const [stockInfo, realtimeData] = await Promise.all([
                this.apiRequest(`/stocks/${code}/`),
                this.apiRequest(`/stocks/${code}/realtime/`)
            ]);
            
            // 更新标题
            document.getElementById('stockTitle').textContent = `${stockInfo.name} (${stockInfo.code})`;
            
            // 更新实时数据
            this.updateRealtimeInfo(realtimeData);
            
        } catch (error) {
            console.error('加载股票信息失败:', error);
        }
    }
    
    /**
     * 更新实时行情信息
     */
    updateRealtimeInfo(data) {
        document.getElementById('currentPrice').textContent = `¥${data.current_price}`;
        
        const changeClass = data.change_rate >= 0 ? 'up' : 'down';
        const changeSymbol = data.change_rate >= 0 ? '+' : '';
        
        const priceChangeElement = document.getElementById('priceChange');
        priceChangeElement.textContent = `${changeSymbol}${data.change_amount} (${changeSymbol}${data.change_rate}%)`;
        priceChangeElement.className = `price-change ${changeClass}`;
        
        document.getElementById('openPrice').textContent = `¥${data.open_price}`;
        document.getElementById('highPrice').textContent = `¥${data.high_price}`;
        document.getElementById('lowPrice').textContent = `¥${data.low_price}`;
        document.getElementById('preClose').textContent = `¥${data.pre_close}`;
        document.getElementById('volume').textContent = this.formatNumber(data.volume);
        document.getElementById('amount').textContent = this.formatNumber(data.amount);
    }
    
    /**
     * 加载股票历史数据
     */
    async loadStockHistory(code, days = 30) {
        try {
            const endDate = new Date();
            const startDate = new Date();
            startDate.setDate(endDate.getDate() - days);
            
            const startDateStr = startDate.toISOString().split('T')[0];
            const endDateStr = endDate.toISOString().split('T')[0];
            
            const data = await this.apiRequest(`/stocks/${code}/history/?start_date=${startDateStr}&end_date=${endDateStr}`);
            
            this.updateHistoryTable(data);
            this.updateChart(data);
            
        } catch (error) {
            console.error('加载历史数据失败:', error);
        }
    }
    
    /**
     * 更新历史数据表格
     */
    updateHistoryTable(data) {
        const tableBody = document.getElementById('historyTableBody');
        tableBody.innerHTML = '';
        
        data.slice(0, 10).forEach(item => {  // 只显示最近10条
            const row = document.createElement('tr');
            
            const changeClass = item.change_rate >= 0 ? 'change-up' : 'change-down';
            const changeSymbol = item.change_rate >= 0 ? '+' : '';
            
            row.innerHTML = `
                <td>${item.date}</td>
                <td>¥${item.open_price}</td>
                <td>¥${item.high_price}</td>
                <td>¥${item.low_price}</td>
                <td>¥${item.close_price}</td>
                <td class="${changeClass}">${changeSymbol}${item.change_rate}%</td>
                <td>${this.formatNumber(item.volume)}</td>
            `;
            
            tableBody.appendChild(row);
        });
    }
    
    /**
     * 更新价格图表
     */
    updateChart(data) {
        const ctx = document.getElementById('priceChart').getContext('2d');
        
        // 销毁现有图表
        if (this.chart) {
            this.chart.destroy();
        }
        
        // 准备数据
        const labels = data.map(item => item.date).reverse();
        const prices = data.map(item => parseFloat(item.close_price)).reverse();
        
        // 创建新图表
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: '收盘价',
                    data: prices,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: '日期'
                        }
                    },
                    y: {
                        display: true,
                        title: {
                            display: true,
                            text: '价格 (¥)'
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }
    
    /**
     * 显示热门股票列表
     */
    showHotStocks() {
        const searchResults = document.getElementById('searchResults');
        const stockDetail = document.getElementById('stockDetail');
        const hotStocks = document.getElementById('hotStocks');
        
        searchResults.style.display = 'none';
        stockDetail.style.display = 'none';
        hotStocks.style.display = 'block';
        
        this.currentStock = null;
    }
    
    /**
     * 格式化数字显示
     */
    formatNumber(num) {
        if (num >= 100000000) {
            return (num / 100000000).toFixed(2) + '亿';
        } else if (num >= 10000) {
            return (num / 10000).toFixed(2) + '万';
        } else {
            return num.toLocaleString();
        }
    }
}

// 当页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    new StockApp();
});
