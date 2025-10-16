let table;
let surveyData = [];
let filterValues = {};
let charts = [];
let chartsVisible = true;
let comparisonMode = false;
let groupAFilters = {};
let groupBFilters = {};
let comparisonCharts = [];

// Load survey data
async function loadSurveyData() {
    try {
        const response = await fetch(`/api/survey/${surveyId}/data`);
        const data = await response.json();

        if (data.error) {
            alert('Error loading data: ' + data.error);
            return;
        }

        surveyData = data.data;
        initializeTable(data.columns, data.data);
        generateCharts(data.columns, data.data);
        generateFilters(data.columns, data.data);
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// Initialize DataTable
function initializeTable(columns, data) {
    const columnDefs = columns.map(col => ({
        title: col,
        data: col
    }));

    table = $('#surveyTable').DataTable({
        data: data,
        columns: columnDefs,
        pageLength: 25,
        lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
        responsive: true,
        dom: 'lrtip',
        language: {
            search: "Search:",
            lengthMenu: "Show _MENU_ entries",
            info: "Showing _START_ to _END_ of _TOTAL_ entries",
            infoEmpty: "Showing 0 to 0 of 0 entries",
            infoFiltered: "(filtered from _MAX_ total entries)",
            paginate: {
                first: "First",
                last: "Last",
                next: "Next",
                previous: "Previous"
            }
        }
    });

    // Add pagination controls
    $('#surveyTable_wrapper').append($('#surveyTable_length'));
    $('#surveyTable_wrapper').append($('#surveyTable_info'));
    $('#surveyTable_wrapper').append($('#surveyTable_paginate'));
}

// Generate dynamic filters
function generateFilters(columns, data) {
    const filtersContainer = document.getElementById('filtersContainer');

    columns.forEach(column => {
        // Get unique values for this column
        const uniqueValues = [...new Set(data.map(row => row[column]))].filter(val => val !== '');
        uniqueValues.sort();

        // Only create filter if there are reasonable number of unique values
        if (uniqueValues.length > 0 && uniqueValues.length <= 100) {
            const filterGroup = document.createElement('div');
            filterGroup.className = 'filter-group';

            const label = document.createElement('label');
            label.textContent = column;

            const select = document.createElement('select');
            select.id = `filter_${column}`;
            select.className = 'column-filter';

            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'All';
            select.appendChild(defaultOption);

            // Add options for unique values
            uniqueValues.forEach(value => {
                const option = document.createElement('option');
                option.value = value;
                option.textContent = value || '(empty)';
                select.appendChild(option);
            });

            // Add change event listener
            select.addEventListener('change', function() {
                filterValues[column] = this.value;
                applyFilters();
            });

            filterGroup.appendChild(label);
            filterGroup.appendChild(select);
            filtersContainer.appendChild(filterGroup);
        }
    });
}

// Apply filters
function applyFilters() {
    // Custom filter function
    $.fn.dataTable.ext.search.pop(); // Remove previous filter
    $.fn.dataTable.ext.search.push(function(settings, data, dataIndex) {
        const rowData = surveyData[dataIndex];

        for (let column in filterValues) {
            if (filterValues[column]) {
                // Convert both values to strings for comparison to handle numbers
                const filterVal = String(filterValues[column]);
                const rowVal = String(rowData[column]);
                if (rowVal !== filterVal) {
                    return false;
                }
            }
        }
        return true;
    });

    table.draw();
}

// Clear filters
document.getElementById('clearFilters').addEventListener('click', function() {
    filterValues = {};
    document.querySelectorAll('.column-filter').forEach(select => {
        select.value = '';
    });
    document.getElementById('globalSearch').value = '';
    $.fn.dataTable.ext.search.pop();
    table.search('').draw();
});

// Global search
document.getElementById('globalSearch').addEventListener('keyup', function() {
    table.search(this.value).draw();
});

// Export to CSV
document.getElementById('exportCSV').addEventListener('click', function() {
    const filteredData = table.rows({ search: 'applied' }).data().toArray();

    if (filteredData.length === 0) {
        alert('No data to export');
        return;
    }

    // Create CSV content
    const headers = columns.join(',');
    const rows = filteredData.map(row => {
        return columns.map(col => {
            const value = row[col] || '';
            // Escape quotes and wrap in quotes if contains comma
            return value.includes(',') || value.includes('"') || value.includes('\n')
                ? `"${value.replace(/"/g, '""')}"`
                : value;
        }).join(',');
    });

    const csv = [headers, ...rows].join('\n');

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `survey_${surveyId}_export.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
});

// Export to JSON
document.getElementById('exportJSON').addEventListener('click', function() {
    const filteredData = table.rows({ search: 'applied' }).data().toArray();

    if (filteredData.length === 0) {
        alert('No data to export');
        return;
    }

    const json = JSON.stringify(filteredData, null, 2);

    // Download
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `survey_${surveyId}_export.json`;
    a.click();
    window.URL.revokeObjectURL(url);
});

// Generate charts
function generateCharts(columns, data) {
    const chartsContainer = document.getElementById('chartsContainer');

    columns.forEach(column => {
        // Get unique values and their counts
        const valueCounts = {};
        data.forEach(row => {
            const value = row[column] || '(empty)';
            valueCounts[value] = (valueCounts[value] || 0) + 1;
        });

        const uniqueValues = Object.keys(valueCounts);

        // Only create charts for categorical data (<=20 unique values) or numeric data
        if (uniqueValues.length > 0 && uniqueValues.length <= 20) {
            createChart(column, valueCounts, chartsContainer);
        }
    });
}

function createChart(columnName, valueCounts, container) {
    // Create chart container
    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';

    const title = document.createElement('h3');
    title.textContent = columnName;
    chartDiv.appendChild(title);

    const canvasWrapper = document.createElement('div');
    canvasWrapper.className = 'chart-canvas';

    const canvas = document.createElement('canvas');
    canvasWrapper.appendChild(canvas);
    chartDiv.appendChild(canvasWrapper);
    container.appendChild(chartDiv);

    // Prepare data
    const labels = Object.keys(valueCounts);
    const data = Object.values(valueCounts);

    // Generate colors
    const colors = generateColors(labels.length);

    // Create chart
    const chart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Count',
                data: data,
                backgroundColor: colors,
                borderColor: colors.map(c => c.replace('0.7', '1')),
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });

    charts.push(chart);
}

function generateColors(count) {
    const baseColors = [
        'rgba(102, 126, 234, 0.7)',
        'rgba(118, 75, 162, 0.7)',
        'rgba(255, 99, 132, 0.7)',
        'rgba(54, 162, 235, 0.7)',
        'rgba(255, 206, 86, 0.7)',
        'rgba(75, 192, 192, 0.7)',
        'rgba(153, 102, 255, 0.7)',
        'rgba(255, 159, 64, 0.7)',
        'rgba(199, 199, 199, 0.7)',
        'rgba(83, 102, 255, 0.7)'
    ];

    const colors = [];
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    return colors;
}

// Toggle charts visibility
document.getElementById('toggleCharts').addEventListener('click', function() {
    const chartsContainer = document.getElementById('chartsContainer');
    chartsVisible = !chartsVisible;
    chartsContainer.style.display = chartsVisible ? 'grid' : 'none';
    this.textContent = chartsVisible ? 'Hide Charts' : 'Show Charts';
});

// ===== COMPARISON MODE =====

// Enable comparison mode
document.getElementById('enableComparison').addEventListener('click', function() {
    comparisonMode = true;
    document.getElementById('comparisonSection').style.display = 'block';
    generateComparisonFilters(columns, surveyData);
});

// Close comparison mode
document.getElementById('closeComparison').addEventListener('click', function() {
    comparisonMode = false;
    document.getElementById('comparisonSection').style.display = 'none';
    groupAFilters = {};
    groupBFilters = {};

    // Clear comparison charts
    comparisonCharts.forEach(chart => chart.destroy());
    comparisonCharts = [];
    document.getElementById('comparisonCharts').innerHTML = '';
});

// Clear Group A filters
document.getElementById('clearGroupA').addEventListener('click', function() {
    groupAFilters = {};
    // Reset all Group A filter dropdowns
    document.querySelectorAll('#groupAFilters select').forEach(select => {
        select.value = '';
    });
    updateComparison();
});

// Clear Group B filters
document.getElementById('clearGroupB').addEventListener('click', function() {
    groupBFilters = {};
    // Reset all Group B filter dropdowns
    document.querySelectorAll('#groupBFilters select').forEach(select => {
        select.value = '';
    });
    updateComparison();
});

// Generate comparison filters
function generateComparisonFilters(columns, data) {
    const groupAContainer = document.getElementById('groupAFilters');
    const groupBContainer = document.getElementById('groupBFilters');

    // Clear existing filters
    groupAContainer.innerHTML = '';
    groupBContainer.innerHTML = '';

    columns.forEach(column => {
        // Get unique values for this column
        const uniqueValues = [...new Set(data.map(row => row[column]))].filter(val => val !== '');
        uniqueValues.sort();

        // Only create filter if there are reasonable number of unique values
        if (uniqueValues.length > 0 && uniqueValues.length <= 100) {
            // Create Group A filter
            const filterGroupA = createComparisonFilter(column, uniqueValues, 'A');
            groupAContainer.appendChild(filterGroupA);

            // Create Group B filter
            const filterGroupB = createComparisonFilter(column, uniqueValues, 'B');
            groupBContainer.appendChild(filterGroupB);
        }
    });

    // Initial update
    updateComparison();
}

function createComparisonFilter(column, uniqueValues, group) {
    const filterGroup = document.createElement('div');
    filterGroup.className = 'filter-group';

    const label = document.createElement('label');
    label.textContent = column;

    const select = document.createElement('select');
    select.id = `filter_${group}_${column}`;
    select.className = 'comparison-filter';

    // Add default option
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'All';
    select.appendChild(defaultOption);

    // Add options for unique values
    uniqueValues.forEach(value => {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = value || '(empty)';
        select.appendChild(option);
    });

    // Add change event listener
    select.addEventListener('change', function() {
        if (group === 'A') {
            if (this.value) {
                groupAFilters[column] = this.value;
            } else {
                delete groupAFilters[column];
            }
        } else {
            if (this.value) {
                groupBFilters[column] = this.value;
            } else {
                delete groupBFilters[column];
            }
        }
        updateComparison();
    });

    filterGroup.appendChild(label);
    filterGroup.appendChild(select);
    return filterGroup;
}

// Update comparison results
function updateComparison() {
    // Filter data for each group
    const groupAData = filterData(surveyData, groupAFilters);
    const groupBData = filterData(surveyData, groupBFilters);

    // Update counts
    document.getElementById('groupACount').textContent = groupAData.length;
    document.getElementById('groupBCount').textContent = groupBData.length;

    // Generate comparison charts
    generateComparisonCharts(groupAData, groupBData);
}

function filterData(data, filters) {
    return data.filter(row => {
        for (let column in filters) {
            // Convert both values to strings for comparison to handle numbers
            const filterVal = String(filters[column]);
            const rowVal = String(row[column]);
            if (rowVal !== filterVal) {
                return false;
            }
        }
        return true;
    });
}

function generateComparisonCharts(groupAData, groupBData) {
    const chartsContainer = document.getElementById('comparisonCharts');

    // Clear existing charts
    comparisonCharts.forEach(chart => chart.destroy());
    comparisonCharts = [];
    chartsContainer.innerHTML = '';

    if (groupAData.length === 0 && groupBData.length === 0) {
        chartsContainer.innerHTML = '<p style="text-align: center; color: #999;">Select filters to compare data</p>';
        return;
    }

    // Generate comparison charts for each categorical column
    columns.forEach(column => {
        // Get unique values for this column from both groups
        const allValues = new Set([
            ...groupAData.map(row => row[column]),
            ...groupBData.map(row => row[column])
        ]);

        // Only create charts for columns with reasonable unique values
        if (allValues.size > 0 && allValues.size <= 20) {
            createComparisonChart(column, groupAData, groupBData, Array.from(allValues), chartsContainer);
        }
    });

    if (chartsContainer.innerHTML === '') {
        chartsContainer.innerHTML = '<p style="text-align: center; color: #999;">No chartable columns found</p>';
    }
}

function createComparisonChart(columnName, groupAData, groupBData, values, container) {
    // Create chart container
    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';

    const title = document.createElement('h3');
    title.textContent = columnName;
    chartDiv.appendChild(title);

    const canvasWrapper = document.createElement('div');
    canvasWrapper.className = 'chart-canvas';

    const canvas = document.createElement('canvas');
    canvasWrapper.appendChild(canvas);
    chartDiv.appendChild(canvasWrapper);
    container.appendChild(chartDiv);

    // Count values for each group
    const groupACounts = {};
    const groupBCounts = {};

    values.forEach(val => {
        groupACounts[val] = groupAData.filter(row => row[columnName] === val).length;
        groupBCounts[val] = groupBData.filter(row => row[columnName] === val).length;
    });

    values.sort();

    // Create chart
    const chart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: values,
            datasets: [
                {
                    label: 'Group A',
                    data: values.map(val => groupACounts[val] || 0),
                    backgroundColor: 'rgba(102, 126, 234, 0.7)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Group B',
                    data: values.map(val => groupBCounts[val] || 0),
                    backgroundColor: 'rgba(255, 99, 132, 0.7)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });

    comparisonCharts.push(chart);
}

// Initialize on page load
loadSurveyData();
