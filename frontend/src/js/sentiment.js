// Sentiment analysis page scripts
import * as d3 from 'd3';
import { debounce, formatPercentage, truncateText } from './utils';

// Import specific styles
import '../css/sentiment.css';

// Keep a reference to the D3 update function
let updateBarplot = null;

document.addEventListener('DOMContentLoaded', function() {
  console.log('Sentiment analysis page loaded');

  // Setup the visualization and event listeners
  setupVisualization();
  setupEventListeners();

  // Populate baseline data so the chart has bars on load
  submitTextForAnalysis('');
});

function setupVisualization() {
  const svg = d3.select('#visualization svg');

  if (svg.empty()) {
    return;
  }

  const margin = { top: 20, right: 20, bottom: 50, left: 40 };
  const width = +svg.attr('width') - margin.left - margin.right;
  const height = +svg.attr('height') - margin.top - margin.bottom;

  const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
  const y = d3.scaleLinear().rangeRound([height, 0]);

  const g = svg
    .append('g')
    .attr('transform', `translate(${margin.left},${margin.top})`);

  const yAxis = g
    .append('g')
    .attr('class', 'y axis')
    .call(d3.axisLeft(y).ticks(10, '%'))
    .append('text')
    .attr('transform', 'rotate(-90)')
    .attr('y', 6)
    .attr('dy', '0.71em')
    .attr('text-anchor', 'end');

  const xAxis = g
    .append('g')
    .attr('class', 'x axis')
    .attr('transform', `translate(0,${height})`)
    .style('font-size', '30px')
    .call(d3.axisBottom(x));

  updateBarplot = function (data) {
    const bars = g.selectAll('rect').data(data, (d) => d.emoji);

    const t = d3.transition().duration(750);

    x.domain(data.map((d) => d.emoji));
    y.domain([0, d3.max(data, (d) => d.num)]);

    xAxis
      .style('fill-opacity', 1e-6)
      .transition(t)
      .call(d3.axisBottom(x))
      .style('fill-opacity', 1);

    bars
      .exit()
      .style('fill', 'red')
      .transition(t)
      .style('fill-opacity', 1e-6)
      .remove();

    bars
      .transition(t)
      .attr('x', (d) => x(d.emoji))
      .attr('y', (d) => y(d.num))
      .attr('height', (d) => height - y(d.num));

    bars
      .enter()
      .append('rect')
      .style('fill-opacity', 1e-6)
      .style('fill', 'green')
      .attr('x', (d) => x(d.emoji))
      .attr('y', (d) => y(d.num))
      .attr('width', x.bandwidth())
      .attr('height', (d) => height - y(d.num))
      .transition(t)
      .style('fill', 'grey')
      .style('fill-opacity', 1);
  };

  updateBarplot([]);
  updateBarplot = debounce(updateBarplot, 750);
}

function setupEventListeners() {
  const textarea = document.getElementById('target');
  
  if (textarea) {
    textarea.addEventListener(
      'input',
      debounce(function () {
        submitTextForAnalysis(textarea.value);
      }, 500)
    );
    
    // Add demo button event listeners
    document.querySelectorAll('button').forEach((button) => {
      button.addEventListener('click', function () {
        textarea.value = this.textContent;
        submitTextForAnalysis(textarea.value);
      });
    });
  }
}

// Export for testing
export function submitTextForAnalysis(text) {
  // Allow empty text so we can load baseline scores
  const processedText = truncateText(text, 280);

  const formData = new FormData();
  formData.append('text', processedText);

  fetch('/sentiment/api/score', {
    method: 'POST',
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      updateVisualization(data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function updateVisualization(data) {
  if (!updateBarplot) {
    return;
  }

  console.log('Sentiment data received:', data);
  const sentimentPercentage = formatPercentage(data.sentiment);
  console.log('Sentiment score:', sentimentPercentage);

  const barData = Object.entries(data.emoji || {})
    .map(([emoji, num]) => ({ emoji, num }))
    .sort((a, b) => b.num - a.num)
    .slice(0, 30);

  updateBarplot(barData);
}