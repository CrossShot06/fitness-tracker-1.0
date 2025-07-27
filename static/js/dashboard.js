document.addEventListener('DOMContentLoaded', () => {
  let chartData = [];
  let events = [];


  try {
    const chartDataElement = document.getElementById('chart-data');
    if (chartDataElement) {
      const rawChart = chartDataElement.textContent.trim();
      if (rawChart && rawChart !== 'null') {
        const parsed = JSON.parse(rawChart);
        if (Array.isArray(parsed)) {
          chartData = parsed;
        } else {
          console.warn("chartData JSON is not an array. Got:", parsed);
        }
      } else {
        console.warn("chartData script tag is empty or null");
      }
    } else {
      console.warn("No chart-data element found!");
    }
  } catch (err) {
    console.error("Failed to parse chart-data:", err);
  }


  try {
    const eventsDataElement = document.getElementById('events-data');
    if (eventsDataElement) {
      const rawEvents = eventsDataElement.textContent.trim();
      if (rawEvents && rawEvents !== 'null') {
        const parsedEvents = JSON.parse(rawEvents);
        if (Array.isArray(parsedEvents)) {
          events = parsedEvents;
        } else {
          console.warn("eventsData JSON is not an array. Got:", parsedEvents);
        }
      } else {
        console.warn("eventsData script tag is empty or null");
      }
    } else {
      console.warn("No events-data element found!");
    }
  } catch (err) {
    console.error("Failed to parse events-data:", err);
  }


  if (chartData.length > 0) {
    const labels = chartData.map(entry => entry.date);

    function getMetricData(metric) {
      return chartData.map(entry => entry[metric] || 0);
    }

    const ctx = document.getElementById('activityChart').getContext('2d');
    let chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Steps',
          data: getMetricData('steps'),
          fill: true,
          backgroundColor: 'rgba(226, 174, 30, 0.2)',
          borderColor: '#e2ae1e',
          tension: 0.3,
          pointBackgroundColor: '#e2ae1e',
          pointRadius: 3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: { bottom: 30 }
        },
        plugins: {
          legend: {
            labels: {
              color: '#e2ae1e',
              font: { size: 14 }
            }
          },
          tooltip: {
            backgroundColor: '#1e1e1e',
            titleColor: '#e2ae1e',
            bodyColor: '#e2ae1e'
          },
          zoom: {
            pan: {
              enabled: true,
              mode: 'x',
              modifierKey: 'ctrl'
            },
            zoom: {
              wheel: { enabled: true },
              pinch: { enabled: true },
              mode: 'x'
            }
          }
        },
        scales: {
          x: {
            ticks: { color: '#e2ae1e', font: { size: 12 } },
            grid: { color: 'rgba(226, 174, 30, 0.1)' }
          },
          y: {
            beginAtZero: true,
            ticks: { color: '#e2ae1e' },
            grid: { color: 'rgba(226, 174, 30, 0.1)' }
          }
        }
      }
    });

    const selector = document.getElementById('activitySelector');
    selector.addEventListener('change', () => {
      const metric = selector.value;
      const labelText = selector.options[selector.selectedIndex].text;

      if (metric === 'workout_progress') {
        chart.config.type = 'bar';
        chart.options.scales.y.max = 100;
      } else {
        chart.config.type = 'line';
        chart.options.scales.y.max = undefined;
      }

      chart.data.datasets[0].label = labelText;
      chart.data.datasets[0].data = getMetricData(metric);
      chart.update();
    });
  } else {
    console.warn("No chart data to render. Skipping Chart.js setup.");
  }

  const calendarEl = document.getElementById('calendar');
  const calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    themeSystem: 'standard',
    height: 'parent',
    events: events,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    eventColor: '#e2ae1e',
    eventTextColor: '#000'
  });
  calendar.render();

  const form = document.querySelector('.dashboard-container form');
  form.querySelectorAll('input').forEach(input => {
    input.addEventListener('change', () => {
      if (input.value.trim() !== '') {
        form.submit();
      } else {
        input.value = '';
      }
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (input.value.trim() !== '') {
          form.submit();
        }
      }
    });
  });

  const daySelector = document.getElementById('day');
  daySelector.addEventListener('change', () => {
    const selected = daySelector.value;
    const url = new URL(window.location.href);
    url.searchParams.set('day', selected);
    window.location.href = url.toString();
  });
});
