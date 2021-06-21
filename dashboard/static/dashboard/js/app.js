// Random Number Generator
function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1) + min); //The maximum is inclusive and the minimum is inclusive
}

// Function for Colors
function hexToRGBA(hex, opacity) {
  return (
    "rgba(" +
    (hex = hex.replace("#", ""))
      .match(new RegExp("(.{" + hex.length / 3 + "})", "g"))
      .map(function (l) {
        return parseInt(hex.length % 2 ? l + l : l, 16);
      })
      .concat(isFinite(opacity) ? opacity : 1)
      .join(",") +
    ")"
  );
}

// Dashboard Theme colors
// custom_colors = ["#0088c7", "#00a7d8", "#31c5e4", "#63e2ec", "#94fff4"];
// custom_colors = ["#0097dc", "#a18aeb", "#ff71c0", "#ff7670", "#ffa600"];
custom_colors = ["#9092b0", "#bc8bbd", "#f27ea2", "#ff8066", "#f59f00"];

// Dashboard Theme colors in RGBA
var custom_colors_rgba = custom_colors.map(function (item) {
  return hexToRGBA(item, 0.5);
});

// Line Chart for Sales Dash Card
new Chart(document.getElementById("line-chart-dash"), {
  type: "line",
  data: {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    datasets: [
      {
        data: [247, 526, 734, 584, 433, 478, 567, 734, 784, 733, 856, 997],
        borderColor: custom_colors[0],
        fill: true,
        backgroundColor: custom_colors_rgba[0],
        lineTension: 0.5,
        pointRadius: 2,
        pointHoverRadius: 6,
      },
    ],
  },
  options: {
    repsonsive: true,
    title: {
      display: false,
    },
    plugins: {
      legend: false,
    },
    scales: {
      x: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
    },
  },
});

// Bar chart for Expenses Dash Card
new Chart(document.getElementById("bar-chart-dash"), {
  type: "bar",
  data: {
    labels: [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ],
    datasets: [
      {
        backgroundColor: [...custom_colors],
        data: [1478, 2267, 734, 784, 433, 500, 340, 567, 789, 876, 777, 343],
      },
    ],
  },
  options: {
    legend: { display: false },
    title: {
      display: false,
    },
    plugins: { legend: false },
    scales: {
      x: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
    },
    borderRadius: 4,
    barThickness: 3,
  },
});

// Donutchart for Receivables and Payables Dash Card

new Chart(document.getElementById("donut-chart-dash"), {
  type: "doughnut",
  data: {
    labels: ["Receivable", "Payable"],
    datasets: [
      {
        data: [47, 19],
        backgroundColor: [...custom_colors],
        borderWidth: 3,
        radius: 50,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: false,
      },
    },
    borderAlign: "inner",
    cutout: 40,
  },
});

// Pie Chart for Cash and Bank Dash Card
new Chart(document.getElementById("pie-chart-dash"), {
  type: "pie",
  data: {
    labels: ["Bank-In", "Bank-Out", "Cash-In", "Cash-Out"],
    datasets: [
      {
        data: [300, 150, 120, 150],
        backgroundColor: [
          custom_colors[0],
          custom_colors[1],
          custom_colors[0],
          custom_colors[1],
        ],
        borderAlign: "inner",
        borderColor: [
          custom_colors[0],
          custom_colors[0],
          custom_colors[4],
          custom_colors[4],
        ],
        radius: 50,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: false,
      },
    },
  },
});

// WaterFall Chart for P&L Movement

new Chart(document.getElementById("waterfall"), {
  type: "bar",
  data: {
    labels: [
      "Revenue",
      "Direct Expenses",
      "Gross Profit",
      "Indirect Expenses",
      "Net Profit",
    ],
    datasets: [
      {
        data: [
          [0, 5400000],
          [3000000, 5400000],
          [0, 3000000],
          [2000000, 3000000],
          [0, 2000000],
        ],
        backgroundColor: [...custom_colors],
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: { display: false, drawBorder: true },
        ticks: {
          display: true,
          autoSkip: false,
          padding: 3,
          maxRotation: 0,
          font: { size: 10 },
        },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: {
          display: false,
        },
      },
    },
  },
});

// Top 5 Customers

new Chart(document.getElementById("donut-top-5-Customers"), {
  type: "doughnut",
  data: {
    labels: [
      "Customer-1",
      "Customer-2",
      "Customer-3",
      "Customer-4",
      "Customer-5",
    ],
    datasets: [
      {
        data: [47, 19, 71, 51, 22],
        backgroundColor: [...custom_colors],
        borderWidth: 4,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: {
        display: false,
      },
    },
    // borderAlign: "inner",
    cutout: 70,
  },
});

// Top 5 Vendors
new Chart(document.getElementById("h-bar-top-5-expenses"), {
  type: "bar",
  data: {
    labels: ["Party-1", "Party-2", "Party-3", "Party-4", "Party-5"],
    datasets: [
      {
        backgroundColor: [...custom_colors],

        data: [8000, 5000, 3000, 2000, 1000],
        borderColor: [...custom_colors],
      },
    ],
  },
  options: {
    indexAxis: "y",
    elements: {
      bar: {
        borderWidth: 2,
      },
    },
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
    },
  },
});

// Top 5 Sales Accounts
new Chart(document.getElementById("pie-top-5-incomes"), {
  type: "pie",
  data: {
    labels: ["Income-1", "Income-2", "Income-3", "Income-4", "Income-5"],
    datasets: [
      {
        backgroundColor: [...custom_colors],
        data: [12, 19, 10, 17, 28],
        borderWidth: 2,
      },
    ],
  },
  options: {
    repsonsive: true,
    title: {
      display: false,
    },
    plugins: {
      legend: false,
    },
  },
});

// Top 5 Expense Accounts
new Chart(document.getElementById("polar-top-5-expenses"), {
  type: "polarArea",
  data: {
    labels: ["Expense-1", "Expense-2", "Expense-3", "Expense-4", "Expense-5"],
    datasets: [
      {
        data: [50, 40, 30, 20, 10],
        backgroundColor: [...custom_colors],
        borderWidth: 5,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      r: {
        angleLines: { display: false },
        ticks: { display: false },
        grid: { display: true },
      },
      x: {
        grid: { display: false, drawBorder: false },
        ticks: {
          display: false,
          autoSkip: false,
          padding: 0,
          maxRotation: 0,
          font: { size: 10 },
        },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: {
          display: false,
        },
      },
    },
  },
});

// Receivable vs Payable Ageing
new Chart(document.getElementById("bar-ageing"), {
  type: "bar",
  data: {
    labels: ["0-30", "31-60", "61-90", "91-120", "> 120"],
    datasets: [
      {
        label: "Receivable",
        data: [50, 90, 30, 70, 10],
        backgroundColor: custom_colors[0],
        borderRadius: 5,
      },
      {
        label: "Payable",
        data: [120, 50, 25, 90, 35],
        backgroundColor: custom_colors[4],
        borderRadius: 5,
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      x: {
        grid: { display: true, drawBorder: true },
        ticks: {
          display: true,
          autoSkip: false,
          padding: 0,
          maxRotation: 0,
          font: { size: 10 },
        },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: {
          display: false,
        },
      },
    },
  },
});

// Tree Map Top 5 Cost Centres
new Chart(document.getElementById("tree-top-5-cc"), {
  type: "treemap",
  data: {
    datasets: [
      {
        tree: [8, 4, 3, 3, 1],
        backgroundColor: [...custom_colors],
      },
    ],
  },
  options: {
    repsonsive: true,
    title: {
      display: false,
    },
    plugins: {
      dataLabels: false,
      legend: false,
    },
  },
});

// Radar Chart for Top 3 Inventory Items
new Chart(document.getElementById("radar-top-3-inventory"), {
  type: "radar",
  data: {
    labels: ["Apr", "May", "Jun", "Jul", "Aug", "Sept"],
    datasets: [
      {
        label: "Product-1",
        backgroundColor: custom_colors_rgba[0],
        borderColor: custom_colors[0],
        fill: -1,
        data: [
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
        ],
      },
      {
        label: "Produt-2",
        backgroundColor: custom_colors_rgba[1],
        borderColor: custom_colors[1],
        fill: -1,
        data: [
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
        ],
      },
      {
        label: "Product-3",
        backgroundColor: custom_colors_rgba[2],
        borderColor: custom_colors[2],
        fill: -1,
        data: [
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(50000, 450000),
          getRandomIntInclusive(10000, 700000),
          getRandomIntInclusive(10000, 700000),
        ],
      },
    ],
  },
  options: {
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
      title: {
        display: false,
      },
    },
    scales: {
      r: {
        angleLines: { display: true },
        ticks: { display: false },
      },
      x: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
      y: {
        grid: { display: false, drawBorder: false },
        ticks: { display: false },
      },
    },
  },
});

// Area chart for Receipts v/s Payments
new Chart(document.getElementById("area-chart-accounts"), {
  type: "bar",
  data: {
    labels: ["April", "May", "June", "July", "August", "September"],
    datasets: [
      {
        label: "Bank Receipt",
        data: [247, 526, 734, 584, 433, 478],
        borderColor: custom_colors_rgba[0],
        backgroundColor: custom_colors_rgba[0],
        borderRadius: 5,
        order: 1,
        yAxisID: "yAxis",
      },
      {
        label: "Bank Payment",
        data: [200, 100, 800, 300, 200, 150],
        borderColor: custom_colors_rgba[4],
        backgroundColor: custom_colors_rgba[4],
        borderRadius: 5,
        order: 1,
        yAxisID: "yAxis",
      },
      {
        label: "Cash Receipt",
        data: [100, 300, 200, 700, 50, 10],
        borderColor: custom_colors_rgba[0],
        fill: true,
        backgroundColor: custom_colors_rgba[0],
        order: 0,
        type: "line",
        lineTension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 6,
        yAxisID: "yAxis_1",
      },
      {
        label: "Cash Payment",
        data: [50, 400, 10, 2500, 300, 432],
        borderColor: custom_colors_rgba[4],
        fill: true,
        backgroundColor: custom_colors_rgba[4],
        order: 0,
        type: "line",
        lineTension: 0.3,
        pointRadius: 2,
        pointHoverRadius: 6,
        yAxisID: "yAxis_1",
      },
    ],
  },
  options: {
    repsonsive: true,
    title: {
      display: false,
    },
    plugins: {
      legend: false,
    },
    scales: {
      x: {
        grid: { display: true, drawBorder: true },
        ticks: {
          display: true,
          autoSkip: false,
          padding: 0,
          maxRotation: 0,
          font: { size: 10 },
        },
      },
      yAxis: {
        type: "linear",
        display: false,
        position: "left",
        grid: { drawOnChart: false },
        ticks: {
          display: false,
        },
      },
      yAxis_1: {
        type: "linear",
        display: false,
        position: "left",
        grid: { drawOnChart: false },
        ticks: {
          display: false,
        },
      },
    },
  },
});

// Data Table Initialization
$(document).ready(function () {
  $("#example").DataTable({
    scrollY: "200px",
    scrollCollapse: true,
    paging: true,
  });
});

// Change color of spans based on theme chosen:

$(document).ready(function () {
  $(".first_value").css("background", custom_colors[0]);
  $(".second_value").css("background", custom_colors[1]);
  $(".third_value").css("background", custom_colors[2]);
  $(".fourth_value").css("background", custom_colors[3]);
  $(".fifth_value").css("background", custom_colors[4]);
  $(".first_color").css("color", custom_colors[0]);
  $(".second_color").css("color", custom_colors[1]);
  $(".third_color").css("color", custom_colors[2]);
  $(".fourth_color").css("color", custom_colors[3]);
  $(".fifth_color").css("color", custom_colors[4]);
});

$("#reportrange").on("apply.daterangepicker", function (ev, picker) {
  console.log(picker.startDate.format("YYYY-MM-DD"));
  console.log(picker.endDate.format("YYYY-MM-DD"));
});
