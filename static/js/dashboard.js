document.addEventListener("DOMContentLoaded", () => {
  // Parse Django-provided stepData
  const labels = stepData.map(entry => entry.date);
  const steps = stepData.map(entry => entry.steps);

  // Get canvas
  const ctx = document.getElementById('stepsChart').getContext('2d');

  // Make Chart.js STOP resizing it down
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Steps',
        data: steps,
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
      maintainAspectRatio: false,    // so CSS height works
      layout: {
        padding: {
          bottom: 30                 // space for x-axis labels
        }
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
            wheel: {
              enabled: true
            },
            pinch: {
              enabled: true
            },
            mode: 'x'
          }
        }
      },
      scales: {
        x: {
          ticks: {
            color: '#e2ae1e',
            font: { size: 12 }
          },
          grid: {
            color: 'rgba(226, 174, 30, 0.1)'
          },
        },
        y: {
          beginAtZero: true,
          ticks: {
            color: '#e2ae1e'
          },
          grid: {
            color: 'rgba(226, 174, 30, 0.1)'
          }
        }
      }
    }
  });

  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
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
          // Only submit if the field is non-empty
          if (input.value.trim() !== '') {
              form.submit();
          } else {
              // Optionally show a warning or do nothing
              input.value = ''; // keep it blank if they want to clear
          }
      });

      // Optionally handle pressing "Enter"
      input.addEventListener('keydown', (e) => {
          if (e.key === 'Enter') {
              e.preventDefault();
              if (input.value.trim() !== '') {
                  form.submit();
              }
          }
      });
  });


});
