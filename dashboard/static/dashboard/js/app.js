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
// custom_colors = ["#9092b0", "#bc8bbd", "#f27ea2", "#ff8066", "#f59f00"];
custom_colors = ["#005f73", "#0a9396", "#94d2bd", "#e9d8a6", "#ee9b00"];

// proper case function (JScript 5.5+)
function toProperCase(s) {
  return s.toLowerCase().replace(/^(.)|\s(.)/g, function ($1) {
    return $1.toUpperCase();
  });
}

// find digits in a number
function find_digits(n) {
  if (n > 0) {
    return parseInt(Math.log10(n)) + 1;
  } else if (n == 0) {
    return 1;
  } else {
    return parseInt(Math.log10(-n)) + 1;
  }
}

// Dashboard Theme colors in RGBA
var custom_colors_rgba = custom_colors.map(function (item) {
  return hexToRGBA(item, 0.5);
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

// Update Income Dash Card:
function income_dash_card(data) {
  $("#income-chart-dash").remove();
  $("#income-chart-dash-div").append(
    '<canvas id="income-chart-dash"></canvas>'
  );
  var $income_chart = $("#income-chart-dash");
  var income_dash = $income_chart[0].getContext("2d");

  if (find_digits(data.present_income) > 6) {
    $("#income-amount-present").html(
      "&#8377;&nbsp;" +
        Math.round(data.present_income / 100000, 2).toLocaleString("hi") +
        " L"
    );
  } else {
    $("#income-amount-present").html(
      "&#8377;&nbsp;" + Math.round(data.present_income, 0).toLocaleString("hi")
    );
  }
  $("#income-amount-present").attr({
    title: "₹ " + Math.round(data.present_income, 0).toLocaleString("hi"),
  });
  // $("#income-amount-present").html(
  //   "&#8377;&nbsp;" +
  //     data.present_income.toLocaleString("hi") +
  //     data.present_income_denomination
  // );
  // custom_colors$("#income-amount-present").attr({ title: data.present_income });
  $("#income-amount-previous").html(
    "&nbsp;&nbsp;from &#8377;&nbsp;" +
      data.previous_income.toLocaleString("hi") +
      data.previous_income_denomination
  );
  $("#perc-change-income").removeClass("perc_increase");
  $("#perc-change-income").removeClass("perc_decrease");
  if (data.perc_change_income > 0) {
    $("#perc-change-income").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_income +
        " %"
    );
    $("#perc-change-income").addClass("perc_increase");
  } else {
    $("#perc-change-income").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_income) +
        " %"
    );
    $("#perc-change-income").addClass("perc_decrease");
  }
  new Chart(income_dash, {
    type: "line",
    data: {
      labels: data.income_chart_labels,
      datasets: [
        {
          data: data.income_chart_data,
          borderColor: custom_colors[0],
          fill: true,
          backgroundColor: custom_colors_rgba[0],
          lineTension: 0.5,
          pointRadius: 1,
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
        tooltip: {
          callbacks: {
            label: (tooltipItems) => {
              const v = tooltipItems.dataset.data[tooltipItems.dataIndex];
              return v.toLocaleString("hi");
            },
          },
        },
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
}

// Update Expense Dash Card:
function expense_dash_card(data) {
  $("#expense-chart-dash").remove();
  $("#expense-chart-dash-div").append(
    '<canvas id="expense-chart-dash"></canvas>'
  );
  var $expense_chart = $("#expense-chart-dash");
  var expense_dash = $expense_chart[0].getContext("2d");

  $("#expense-amount-present").html(
    "&#8377;&nbsp;" +
      data.present_expense.toLocaleString("hi") +
      data.present_expense_denomination
  );
  $("#expense-amount-previous").html(
    "&nbsp;&nbsp;from &#8377;&nbsp;" +
      data.previous_expense.toLocaleString("hi") +
      data.previous_expense_denomination
  );
  $("#perc-change-expense").removeClass("perc_increase");
  $("#perc-change-expense").removeClass("perc_decrease");
  if (data.perc_change_expense > 0) {
    $("#perc-change-expense").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_expense +
        " %"
    );
    $("#perc-change-expense").addClass("perc_increase");
  } else {
    $("#perc-change-expense").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_expense) +
        " %"
    );
    $("#perc-change-expense").addClass("perc_decrease");
  }
  new Chart(expense_dash, {
    type: "bar",
    data: {
      labels: data.expense_chart_labels,
      datasets: [
        {
          backgroundColor: [...custom_colors],
          data: data.expense_chart_data,
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
}

// Update Receivable and Payable Dash Card:
function recpay_dash_card(data) {
  $("#recpay-chart-dash").remove();
  $("#recpay-chart-dash-div").append(
    '<canvas id="recpay-chart-dash" style="height: 80px" class="m-0 d-flex justify-content-end"></canvas>'
  );
  var $recpay_chart = $("#recpay-chart-dash");
  var recpay_dash = $recpay_chart[0].getContext("2d");

  $("#receivable-amount-present").removeAttr("style");

  $("#receivable-amount-present").html(
    "&#8377;&nbsp;" +
      data.present_debtor.toLocaleString("hi") +
      data.present_debtor_denomination
  );
  if (data.perc_change_debtor > 0) {
    $("#receivable-amount-present").css({ color: "#00c9a7" });
  } else {
    $("#receivable-amount-present").css({ color: "#ed4c78" });
  }

  $("#payable-amount-present").removeAttr("style");

  $("#payable-amount-present").html(
    "&#8377;&nbsp;" +
      data.present_creditor.toLocaleString("hi") +
      data.present_creditor_denomination
  );
  if (data.perc_change_creditor > 0) {
    $("#payable-amount-present").css({ color: "#00c9a7" });
  } else {
    $("#payable-amount-present").css({ color: "#ed4c78" });
  }
  new Chart(recpay_dash, {
    type: "doughnut",
    data: {
      labels: ["Receivable", "Payable"],
      datasets: [
        {
          data: data.recpay_chart_data,
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
}

// Update Cash and Bank Dash Card:
function cashbank_dash_card(data) {
  $("#cashbank-chart-dash").remove();
  $("#cashbank-chart-dash-div").append(
    '<canvas id="cashbank-chart-dash" style="height: 80px" class="m-0 d-flex justify-content-end"></canvas>'
  );
  var $cashbank_chart = $("#cashbank-chart-dash");
  var cashbank_dash = $cashbank_chart[0].getContext("2d");

  $("#cash-amount-present").removeAttr("style");

  $("#cash-amount-present").html(
    "&#8377;&nbsp;" +
      data.present_cash.toLocaleString("hi") +
      data.present_cash_denomination
  );
  if (data.perc_change_cash > 0) {
    $("#cash-amount-present").css({ color: "#00c9a7" });
  } else {
    $("#cash-amount-present").css({ color: "#ed4c78" });
  }

  $("#bank-amount-present").removeAttr("style");

  $("#bank-amount-present").html(
    "&#8377;&nbsp;" +
      data.present_bank.toLocaleString("hi") +
      data.present_bank_denomination
  );
  if (data.perc_change_bank > 0) {
    $("#bank-amount-present").css({ color: "#00c9a7" });
  } else {
    $("#bank-amount-present").css({ color: "#ed4c78" });
  }
  new Chart(cashbank_dash, {
    type: "pie",
    data: {
      labels: ["Cash", "Bank"],
      datasets: [
        {
          data: data.cashbank_chart_data,
          backgroundColor: [custom_colors[4], custom_colors[0]],
          borderAlign: "inner",
          borderColor: [custom_colors[4], custom_colors[0]],
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
}

// Update P&L Movement Dash Card:
function pl_dash_card(data) {
  $("#pl-chart-dash").remove();
  $("#pl-chart-dash-div").append(
    '<canvas id="pl-chart-dash" class="chart p-0 w-100 h-100" style="display: block"></canvas>'
  );
  var $pl_chart = $("#pl-chart-dash");
  var pl_dash = $pl_chart[0].getContext("2d");

  $("#income-pl").html(
    "&#8377;&nbsp;" +
      data.present_income.toLocaleString("hi") +
      data.present_income_denomination
  );
  $("#perc-change-income-pl").removeClass("perc_increase");
  $("#perc-change-income-pl").removeClass("perc_decrease");
  if (data.perc_change_income > 0) {
    $("#perc-change-income-pl").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_income +
        " %"
    );
    $("#perc-change-income-pl").addClass("perc_increase");
  } else {
    $("#perc-change-income-pl").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_income) +
        " %"
    );
    $("#perc-change-income-pl").addClass("perc_decrease");
  }

  $("#direct-expense-pl").html(
    "&#8377;&nbsp;" +
      data.present_direct_expense.toLocaleString("hi") +
      data.present_direct_expense_denomination
  );
  $("#perc-change-direct-expense-pl").removeClass("perc_increase");
  $("#perc-change-direct-expense-pl").removeClass("perc_decrease");
  if (data.perc_change_direct_expense > 0) {
    $("#perc-change-direct-expense-pl").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_direct_expense +
        " %"
    );
    $("#perc-change-direct-expense-pl").addClass("perc_increase");
  } else {
    $("#perc-change-direct-expense-pl").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_direct_expense) +
        " %"
    );
    $("#perc-change-direct-expense-pl").addClass("perc_decrease");
  }
  $("#gp-pl").html(
    "&#8377;&nbsp;" +
      data.present_gross_profit.toLocaleString("hi") +
      data.present_gross_profit_denomination
  );
  $("#perc-change-gp-pl").removeClass("perc_increase");
  $("#perc-change-gp-pl").removeClass("perc_decrease");
  if (data.perc_change_gross_profit > 0) {
    $("#perc-change-gp-pl").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_gross_profit +
        " %"
    );
    $("#perc-change-gp-pl").addClass("perc_increase");
  } else {
    $("#perc-change-gp-pl").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_gross_profit) +
        " %"
    );
    $("#perc-change-gp-pl").addClass("perc_decrease");
  }
  $("#indirect-expense-pl").html(
    "&#8377;&nbsp;" +
      data.present_indirect_expense.toLocaleString("hi") +
      data.present_indirect_expense_denomination
  );
  $("#perc-change-indirect-expense-pl").removeClass("perc_increase");
  $("#perc-change-indirect-expense-pl").removeClass("perc_decrease");
  if (data.perc_change_indirect_expense > 0) {
    $("#perc-change-indirect-expense-pl").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_indirect_expense +
        " %"
    );
    $("#perc-change-indirect-expense-pl").addClass("perc_increase");
  } else {
    $("#perc-change-indirect-expense-pl").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_indirect_expense) +
        " %"
    );
    $("#perc-change-indirect-expense-pl").addClass("perc_decrease");
  }
  $("#np-pl").html(
    "&#8377;&nbsp;" +
      data.present_net_profit.toLocaleString("hi") +
      data.present_net_profit_denomination
  );
  $("#perc-change-np-pl").removeClass("perc_increase");
  $("#perc-change-np-pl").removeClass("perc_decrease");
  if (data.perc_change_net_profit > 0) {
    $("#perc-change-np-pl").html(
      '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
        data.perc_change_net_profit +
        " %"
    );
    $("#perc-change-np-pl").addClass("perc_increase");
  } else {
    $("#perc-change-np-pl").html(
      '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
        Math.abs(data.perc_change_net_profit) +
        " %"
    );
    $("#perc-change-np-pl").addClass("perc_decrease");
  }
  new Chart(pl_dash, {
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
            [0, data.pl_chart_data[0]],
            [data.pl_chart_data[2], data.pl_chart_data[0]],
            [0, data.pl_chart_data[2]],
            [data.pl_chart_data[4], data.pl_chart_data[2]],
            [0, data.pl_chart_data[4]],
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
        tooltip: {
          callbacks: {
            label: (tooltipItems) => {
              const v = tooltipItems.dataset.data[tooltipItems.dataIndex];
              const net = v[1] - v[0];
              return net.toLocaleString("hi");
            },
          },
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
}

// Update Top Customers Dash Card:
function top_customer_dash_card(data) {
  $("#top-5-customers").remove();
  $("#top-5-customers-div").append(
    '<canvas class="chart" id="top-5-customers" style="display: block"></canvas>'
  );
  var $top_customer_chart = $("#top-5-customers");
  var top_customer_dash = $top_customer_chart[0].getContext("2d");

  var customer_total = data.top_customer_chart_total.reduce((a, b) => a + b, 0);

  // Update First Table Row
  var party = data.top_customer_chart_labels[0];
  if (typeof party !== "undefined") {
    $("#top-customer-heading").removeAttr("style");
    $("#top-customer-row-1").removeAttr("style");
    try {
      $("#top-customer-1").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-customer-1").html("");
    }
    try {
      $("#top-customer-1-name").html(toProperCase(party.split(" ")[0]));
      $("#top-customer-1-name").attr({ title: toProperCase(party) });
      $("#top-customer-total").css("display", "");
      $("#top-customer-total").html(
        "&#8377;&nbsp;" +
          Math.round(customer_total / 100000, 0).toLocaleString("hi") +
          " L"
      );
    } catch (error) {
      $("#top-customer-1-name").html("");
    }

    if (find_digits(data.top_customer_chart_total[0]) > 6) {
      $("#top-customer-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.top_customer_chart_total[0] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_customer_chart_total[0], 0).toLocaleString("hi")
      );
    }
    $("#top-customer-1-count").html(
      Math.round(data.top_customer_chart_count[0], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_receivables[party]) > 6) {
      $("#top-customer-1-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_receivables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-1-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_receivables[party], 0).toLocaleString(
            "hi"
          )
      );
    }
    $("#top-customer-1-receivable-perc").removeClass("perc_increase");
    $("#top-customer-1-receivable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_receivables[party] > 0) {
      $("#top-customer-1-receivable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_receivables[party] +
          " %"
      );
      $("#top-customer-1-receivable-perc").addClass("perc_increase");
    } else {
      $("#top-customer-1-receivable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_receivables[party]) +
          " %"
      );
      $("#top-customer-1-receivable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-customer-row-1").css("display", "None");
    $("#top-customer-heading").css("display", "None");
  }
  var party = data.top_customer_chart_labels[1];
  if (typeof party !== "undefined") {
    $("#top-customer-row-2").removeAttr("style");
    try {
      $("#top-customer-2").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-customer-2").html("");
    }
    try {
      $("#top-customer-2-name").html(toProperCase(party.split(" ")[0]));
      $("#top-customer-2-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-customer-2-name").html("");
    }

    if (find_digits(data.top_customer_chart_total[1]) > 6) {
      $("#top-customer-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.top_customer_chart_total[1] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_customer_chart_total[1], 0).toLocaleString("hi")
      );
    }
    $("#top-customer-2-count").html(
      Math.round(data.top_customer_chart_count[1], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_receivables[party]) > 6) {
      $("#top-customer-2-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_receivables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-2-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_receivables[party], 0).toLocaleString(
            "hi"
          )
      );
    }
    $("#top-customer-2-receivable-perc").removeClass("perc_increase");
    $("#top-customer-2-receivable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_receivables[party] > 0) {
      $("#top-customer-2-receivable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_receivables[party] +
          " %"
      );
      $("#top-customer-2-receivable-perc").addClass("perc_increase");
    } else {
      $("#top-customer-2-receivable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_receivables[party]) +
          " %"
      );
      $("#top-customer-2-receivable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-customer-row-2").css("display", "None");
  }
  var party = data.top_customer_chart_labels[2];
  if (typeof party !== "undefined") {
    $("#top-customer-row-3").removeAttr("style");
    try {
      $("#top-customer-3").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-customer-3").html("");
    }
    try {
      $("#top-customer-3-name").html(toProperCase(party.split(" ")[0]));
      $("#top-customer-3-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-customer-3-name").html("");
    }

    if (find_digits(data.top_customer_chart_total[2]) > 6) {
      $("#top-customer-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.top_customer_chart_total[2] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_customer_chart_total[2], 0).toLocaleString("hi")
      );
    }
    $("#top-customer-3-count").html(
      Math.round(data.top_customer_chart_count[2], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_receivables[party]) > 6) {
      $("#top-customer-3-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_receivables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-3-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_receivables[party], 0).toLocaleString(
            "hi"
          )
      );
    }
    $("#top-customer-3-receivable-perc").removeClass("perc_increase");
    $("#top-customer-3-receivable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_receivables[party] > 0) {
      $("#top-customer-3-receivable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_receivables[party] +
          " %"
      );
      $("#top-customer-3-receivable-perc").addClass("perc_increase");
    } else {
      $("#top-customer-3-receivable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_receivables[party]) +
          " %"
      );
      $("#top-customer-3-receivable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-customer-row-3").css("display", "None");
  }
  var party = data.top_customer_chart_labels[3];
  if (typeof party !== "undefined") {
    $("#top-customer-row-4").removeAttr("style");
    try {
      $("#top-customer-4").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-customer-4").html("");
    }
    try {
      $("#top-customer-4-name").html(toProperCase(party.split(" ")[0]));
      $("#top-customer-4-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-customer-4-name").html("");
    }

    if (find_digits(data.top_customer_chart_total[3]) > 6) {
      $("#top-customer-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.top_customer_chart_total[3] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_customer_chart_total[3], 0).toLocaleString("hi")
      );
    }
    $("#top-customer-4-count").html(
      Math.round(data.top_customer_chart_count[3], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_receivables[party]) > 6) {
      $("#top-customer-4-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_receivables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-4-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_receivables[party], 0).toLocaleString(
            "hi"
          )
      );
    }
    $("#top-customer-4-receivable-perc").removeClass("perc_increase");
    $("#top-customer-4-receivable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_receivables[party] > 0) {
      $("#top-customer-4-receivable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_receivables[party] +
          " %"
      );
      $("#top-customer-4-receivable-perc").addClass("perc_increase");
    } else {
      $("#top-customer-4-receivable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_receivables[party]) +
          " %"
      );
      $("#top-customer-4-receivable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-customer-row-4").css("display", "None");
  }
  var party = data.top_customer_chart_labels[4];
  if (typeof party !== "undefined") {
    $("#top-customer-row-5").removeAttr("style");
    try {
      $("#top-customer-5").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-customer-5").html("");
    }
    try {
      $("#top-customer-5-name").html(toProperCase(party.split(" ")[0]));
      $("#top-customer-5-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-customer-5-name").html("");
    }

    if (find_digits(data.top_customer_chart_total[4]) > 6) {
      $("#top-customer-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.top_customer_chart_total[4] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_customer_chart_total[4], 0).toLocaleString("hi")
      );
    }
    $("#top-customer-5-count").html(
      Math.round(data.top_customer_chart_count[4], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_receivables[party]) > 6) {
      $("#top-customer-5-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_receivables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-customer-5-receivable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_receivables[party], 0).toLocaleString(
            "hi"
          )
      );
    }
    $("#top-customer-5-receivable-perc").removeClass("perc_increase");
    $("#top-customer-5-receivable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_receivables[party] > 0) {
      $("#top-customer-5-receivable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_receivables[party] +
          " %"
      );
      $("#top-customer-5-receivable-perc").addClass("perc_increase");
    } else {
      $("#top-customer-5-receivable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_receivables[party]) +
          " %"
      );
      $("#top-customer-5-receivable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-customer-row-5").css("display", "None");
  }
  new Chart(top_customer_dash, {
    type: "doughnut",
    data: {
      labels: data.top_customer_chart_labels,
      datasets: [
        {
          data: data.top_customer_chart_total,
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
        tooltip: {
          titleFont: { size: 5 },
        },
      },
      // borderAlign: "inner",
      cutout: 70,
    },
  });
}

// Update Top Vendors Dash Card:
function top_vendor_dash_card(data) {
  $("#top-5-vendors").remove();
  $("#top-5-vendors-div").append(
    '<canvas class="chart px-3" id="top-5-vendors" style="display: block"></canvas>'
  );
  var $top_vendor_chart = $("#top-5-vendors");
  var top_vendor_dash = $top_vendor_chart[0].getContext("2d");

  // Update First Table Row
  var party = data.top_vendor_chart_labels[0];
  if (typeof party !== "undefined") {
    $("#top-vendor-heading").removeAttr("style");
    $("#top-vendor-row-1").removeAttr("style");
    try {
      $("#top-vendor-1").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-vendor-1").html("");
    }
    try {
      $("#top-vendor-1-name").html(toProperCase(party.split(" ")[0]));
      $("#top-vendor-1-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-vendor-1-name").html("");
    }

    if (find_digits(data.top_vendor_chart_total[0]) > 6) {
      $("#top-vendor-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[0] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-vendor-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[0], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-1-count").html(
      Math.round(data.top_vendor_chart_count[0], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_payables[party]) > 6) {
      $("#top-vendor-1-payable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_payables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-vendor-1-payable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_payables[party], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-1-payable-perc").removeClass("perc_increase");
    $("#top-vendor-1-payable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_payables[party] > 0) {
      $("#top-vendor-1-payable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_payables[party] +
          " %"
      );
      $("#top-vendor-1-payable-perc").addClass("perc_increase");
    } else {
      $("#top-vendor-1-payable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_payables[party]) +
          " %"
      );
      $("#top-vendor-1-payable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-vendor-row-1").css("display", "None");
    $("#top-vendor-heading").css("display", "None");
  }
  var party = data.top_vendor_chart_labels[1];
  if (typeof party !== "undefined") {
    $("#top-vendor-row-2").removeAttr("style");
    try {
      $("#top-vendor-2").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-vendor-2").html("");
    }
    try {
      $("#top-vendor-2-name").html(toProperCase(party.split(" ")[0]));
      $("#top-vendor-2-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-vendor-2-name").html("");
    }

    if (find_digits(data.top_vendor_chart_total[1]) > 6) {
      $("#top-vendor-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[1] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-vendor-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[1], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-2-count").html(
      Math.round(data.top_vendor_chart_count[1], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_payables[party]) > 6) {
      $("#top-vendor-2-payable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_payables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-vendor-2-payable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_payables[party], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-2-payable-perc").removeClass("perc_increase");
    $("#top-vendor-2-payable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_payables[party] > 0) {
      $("#top-vendor-2-payable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_payables[party] +
          " %"
      );
      $("#top-vendor-2-payable-perc").addClass("perc_increase");
    } else {
      $("#top-vendor-2-payable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_payables[party]) +
          " %"
      );
      $("#top-vendor-2-payable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-vendor-row-2").css("display", "None");
  }
  var party = data.top_vendor_chart_labels[2];
  if (typeof party !== "undefined") {
    $("#top-vendor-row-3").removeAttr("style");
    try {
      $("#top-vendor-3").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-vendor-3").html("");
    }
    try {
      $("#top-vendor-3-name").html(toProperCase(party.split(" ")[0]));
      $("#top-vendor-3-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-vendor-3-name").html("");
    }

    if (find_digits(data.top_vendor_chart_total[2]) > 6) {
      $("#top-vendor-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[2] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-vendor-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[2], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-3-count").html(
      Math.round(data.top_vendor_chart_count[2], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_payables[party]) > 6) {
      $("#top-vendor-3-payable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_payables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-vendor-3-payable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_payables[party], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-3-payable-perc").removeClass("perc_increase");
    $("#top-vendor-3-payable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_payables[party] > 0) {
      $("#top-vendor-3-payable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_payables[party] +
          " %"
      );
      $("#top-vendor-3-payable-perc").addClass("perc_increase");
    } else {
      $("#top-vendor-3-payable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_payables[party]) +
          " %"
      );
      $("#top-vendor-3-payable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-vendor-row-3").css("display", "None");
  }
  var party = data.top_vendor_chart_labels[3];
  if (typeof party !== "undefined") {
    $("#top-vendor-row-4").removeAttr("style");
    try {
      $("#top-vendor-4").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-vendor-4").html("");
    }
    try {
      $("#top-vendor-4-name").html(toProperCase(party.split(" ")[0]));
      $("#top-vendor-4-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-vendor-4-name").html("");
    }

    if (find_digits(data.top_vendor_chart_total[3]) > 6) {
      $("#top-vendor-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[3] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-vendor-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[3], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-4-count").html(
      Math.round(data.top_vendor_chart_count[3], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_payables[party]) > 6) {
      $("#top-vendor-4-payable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_payables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-vendor-4-payable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_payables[party], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-4-payable-perc").removeClass("perc_increase");
    $("#top-vendor-4-payable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_payables[party] > 0) {
      $("#top-vendor-4-payable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_payables[party] +
          " %"
      );
      $("#top-vendor-4-payable-perc").addClass("perc_increase");
    } else {
      $("#top-vendor-4-payable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_payables[party]) +
          " %"
      );
      $("#top-vendor-4-payable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-vendor-row-4").css("display", "None");
  }
  var party = data.top_vendor_chart_labels[4];
  if (typeof party !== "undefined") {
    $("#top-vendor-row-5").removeAttr("style");
    try {
      $("#top-vendor-5").html(toProperCase(party.charAt(0)));
    } catch (error) {
      $("#top-vendor-5").html("");
    }
    try {
      $("#top-vendor-5-name").html(toProperCase(party.split(" ")[0]));
      $("#top-vendor-5-name").attr({ title: toProperCase(party) });
    } catch (error) {
      $("#top-vendor-5-name").html("");
    }

    if (find_digits(data.top_vendor_chart_total[4]) > 6) {
      $("#top-vendor-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[4] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-vendor-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.top_vendor_chart_total[4], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-5-count").html(
      Math.round(data.top_vendor_chart_count[4], 0).toLocaleString("hi")
    );

    if (find_digits(data.present_party_payables[party]) > 6) {
      $("#top-vendor-5-payable").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.present_party_payables[party] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-vendor-5-payable").html(
        "&#8377;&nbsp;" +
          Math.round(data.present_party_payables[party], 0).toLocaleString("hi")
      );
    }
    $("#top-vendor-5-payable-perc").removeClass("perc_increase");
    $("#top-vendor-5-payable-perc").removeClass("perc_decrease");
    if (data.perc_change_party_payables[party] > 0) {
      $("#top-vendor-5-payable-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_party_payables[party] +
          " %"
      );
      $("#top-vendor-5-payable-perc").addClass("perc_increase");
    } else {
      $("#top-vendor-5-payable-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_party_payables[party]) +
          " %"
      );
      $("#top-vendor-5-payable-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-vendor-row-5").css("display", "None");
  }
  new Chart(top_vendor_dash, {
    type: "bar",
    data: {
      labels: data.top_vendor_chart_labels,
      datasets: [
        {
          data: data.top_vendor_chart_total,
          backgroundColor: [...custom_colors],
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
        tooltip: {
          callbacks: {
            label: (tooltipItems) => {
              const v = tooltipItems.dataset.data[tooltipItems.dataIndex];
              return v.toLocaleString("hi");
            },
          },
        },
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
}

// Update Top Income Ledgers Dash Card:
function top_income_ledgers_dash_card(data) {
  $("#top-5-income-ledgers").remove();
  $("#top-5-income-ledgers-div").append(
    '<canvas class="chart p-0" id="top-5-income-ledgers" style="display: block" width="200" height="200"></canvas>'
  );
  var $top_income_ledgers_chart = $("#top-5-income-ledgers");
  var top_income_ledgers_dash = $top_income_ledgers_chart[0].getContext("2d");

  // Update First Table Row
  var ledger = data.income_ledgers_chart_labels[0];
  if (typeof ledger !== "undefined") {
    $("#top-income-ledgers-heading").removeAttr("style");
    $("#top-income-ledgers-row-1").removeAttr("style");
    try {
      $("#top-income-ledger-1").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-income-ledger-1").html("");
    }
    try {
      $("#top-income-ledger-1-name").html(
        toProperCase(ledger.slice(0, 30))
        // toProperCase(ledger.split(" ")[0] + " " + ledger.split(" ")[1])
      );
      $("#top-income-ledger-1-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-income-ledger-1-name").html("");
    }

    if (find_digits(data.income_ledgers_chart_data[0]) > 6) {
      $("#top-income-ledger-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.income_ledgers_chart_data[0] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-income-ledger-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.income_ledgers_chart_data[0], 0).toLocaleString("hi")
      );
    }
    $("#top-income-ledger-1-perc").removeClass("perc_increase");
    $("#top-income-ledger-1-perc").removeClass("perc_decrease");
    if (data.perc_change_top_income_ledgers[ledger] > 0) {
      $("#top-income-ledger-1-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_income_ledgers[ledger] +
          " %"
      );
      $("#top-income-ledger-1-perc").addClass("perc_increase");
    } else {
      $("#top-income-ledger-1-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_income_ledgers[ledger]) +
          " %"
      );
      $("#top-income-ledger-1-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-income-ledgers-row-1").css("display", "None");
    $("#top-income-ledgers-heading").css("display", "None");
  }
  var ledger = data.income_ledgers_chart_labels[1];
  if (typeof ledger !== "undefined") {
    $("#top-income-ledger-row-2").removeAttr("style");
    try {
      $("#top-income-ledger-2").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-income-ledger-2").html("");
    }
    try {
      $("#top-income-ledger-2-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-income-ledger-2-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-income-ledger-2-name").html("");
    }

    if (find_digits(data.income_ledgers_chart_data[1]) > 6) {
      $("#top-income-ledger-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.income_ledgers_chart_data[1] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-income-ledger-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.income_ledgers_chart_data[1], 0).toLocaleString("hi")
      );
    }
    $("#top-income-ledger-2-perc").removeClass("perc_increase");
    $("#top-income-ledger-2-perc").removeClass("perc_decrease");
    if (data.perc_change_top_income_ledgers[ledger] > 0) {
      $("#top-income-ledger-2-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_income_ledgers[ledger] +
          " %"
      );
      $("#top-income-ledger-2-perc").addClass("perc_increase");
    } else {
      $("#top-income-ledger-2-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_income_ledgers[ledger]) +
          " %"
      );
      $("#top-income-ledger-2-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-income-ledger-row-2").css("display", "None");
  }
  var ledger = data.income_ledgers_chart_labels[2];
  if (typeof ledger !== "undefined") {
    $("#top-income-ledger-row-3").removeAttr("style");
    try {
      $("#top-income-ledger-3").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-income-ledger-3").html("");
    }
    try {
      $("#top-income-ledger-3-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-income-ledger-3-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-income-ledger-3-name").html("");
    }

    if (find_digits(data.income_ledgers_chart_data[2]) > 6) {
      $("#top-income-ledger-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.income_ledgers_chart_data[2] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-income-ledger-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.income_ledgers_chart_data[2], 0).toLocaleString("hi")
      );
    }
    $("#top-income-ledger-3-perc").removeClass("perc_increase");
    $("#top-income-ledger-3-perc").removeClass("perc_decrease");
    if (data.perc_change_top_income_ledgers[ledger] > 0) {
      $("#top-income-ledger-3-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_income_ledgers[ledger] +
          " %"
      );
      $("#top-income-ledger-3-perc").addClass("perc_increase");
    } else {
      $("#top-income-ledger-3-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_income_ledgers[ledger]) +
          " %"
      );
      $("#top-income-ledger-3-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-income-ledger-row-3").css("display", "None");
  }
  var ledger = data.income_ledgers_chart_labels[3];
  if (typeof ledger !== "undefined") {
    $("#top-income-ledger-row-4").removeAttr("style");
    try {
      $("#top-income-ledger-4").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-income-ledger-4").html("");
    }
    try {
      $("#top-income-ledger-4-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-income-ledger-4-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-income-ledger-4-name").html("");
    }

    if (find_digits(data.income_ledgers_chart_data[3]) > 6) {
      $("#top-income-ledger-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.income_ledgers_chart_data[3] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-income-ledger-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.income_ledgers_chart_data[3], 0).toLocaleString("hi")
      );
    }
    $("#top-income-ledger-4-perc").removeClass("perc_increase");
    $("#top-income-ledger-4-perc").removeClass("perc_decrease");
    if (data.perc_change_top_income_ledgers[ledger] > 0) {
      $("#top-income-ledger-4-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_income_ledgers[ledger] +
          " %"
      );
      $("#top-income-ledger-4-perc").addClass("perc_increase");
    } else {
      $("#top-income-ledger-4-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_income_ledgers[ledger]) +
          " %"
      );
      $("#top-income-ledger-4-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-income-ledger-row-4").css("display", "None");
  }
  var ledger = data.income_ledgers_chart_labels[4];
  if (typeof ledger !== "undefined") {
    $("#top-income-ledger-row-5").removeAttr("style");
    try {
      $("#top-income-ledger-5").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-income-ledger-5").html("");
    }
    try {
      $("#top-income-ledger-5-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-income-ledger-5-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-income-ledger-5-name").html("");
    }

    if (find_digits(data.income_ledgers_chart_data[4]) > 6) {
      $("#top-income-ledger-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.income_ledgers_chart_data[4] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-income-ledger-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.income_ledgers_chart_data[4], 0).toLocaleString("hi")
      );
    }
    $("#top-income-ledger-5-perc").removeClass("perc_increase");
    $("#top-income-ledger-5-perc").removeClass("perc_decrease");
    if (data.perc_change_top_income_ledgers[ledger] > 0) {
      $("#top-income-ledger-5-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_income_ledgers[ledger] +
          " %"
      );
      $("#top-income-ledger-5-perc").addClass("perc_increase");
    } else {
      $("#top-income-ledger-5-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_income_ledgers[ledger]) +
          " %"
      );
      $("#top-income-ledger-5-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-income-ledger-row-5").css("display", "None");
  }
  new Chart(top_income_ledgers_dash, {
    type: "pie",
    data: {
      labels: data.income_ledgers_chart_labels,
      datasets: [
        {
          data: data.income_ledgers_chart_data,
          backgroundColor: [...custom_colors],
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      title: {
        display: false,
      },
      plugins: {
        legend: false,
      },
    },
  });
}

// Update Top Expense Ledgers Dash Card:
function top_expense_ledgers_dash_card(data) {
  $("#top-5-expense-ledgers").remove();
  $("#top-5-expense-ledgers-div").append(
    '<canvas class="chart p-0" id="top-5-expense-ledgers" style="display: block" width="200" height="200"></canvas>'
  );
  var $top_expense_ledgers_chart = $("#top-5-expense-ledgers");
  var top_expense_ledgers_dash = $top_expense_ledgers_chart[0].getContext("2d");

  // Update First Table Row
  var ledger = data.expense_ledgers_chart_labels[0];
  if (typeof ledger !== "undefined") {
    $("#top-expense-ledgers-heading").removeAttr("style");
    $("#top-expense-ledgers-row-1").removeAttr("style");
    try {
      $("#top-expense-ledger-1").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-expense-ledger-1").html("");
    }
    try {
      $("#top-expense-ledger-1-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-expense-ledger-1-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-expense-ledger-1-name").html("");
    }

    if (find_digits(data.expense_ledgers_chart_data[0]) > 6) {
      $("#top-expense-ledger-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.expense_ledgers_chart_data[0] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-expense-ledger-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.expense_ledgers_chart_data[0], 0).toLocaleString("hi")
      );
    }
    $("#top-expense-ledger-1-perc").removeClass("perc_increase");
    $("#top-expense-ledger-1-perc").removeClass("perc_decrease");
    if (data.perc_change_top_expense_ledgers[ledger] > 0) {
      $("#top-expense-ledger-1-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_expense_ledgers[ledger] +
          " %"
      );
      $("#top-expense-ledger-1-perc").addClass("perc_increase");
    } else {
      $("#top-expense-ledger-1-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_expense_ledgers[ledger]) +
          " %"
      );
      $("#top-expense-ledger-1-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-expense-ledgers-row-1").css("display", "None");
    $("#top-expense-ledgers-heading").css("display", "None");
  }
  var ledger = data.expense_ledgers_chart_labels[1];
  if (typeof ledger !== "undefined") {
    $("#top-expense-ledgers-row-2").removeAttr("style");
    try {
      $("#top-expense-ledger-2").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-expense-ledger-2").html("");
    }
    try {
      $("#top-expense-ledger-2-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-expense-ledger-2-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-expense-ledger-2-name").html("");
    }

    if (find_digits(data.expense_ledgers_chart_data[1]) > 6) {
      $("#top-expense-ledger-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.expense_ledgers_chart_data[1] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-expense-ledger-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.expense_ledgers_chart_data[1], 0).toLocaleString("hi")
      );
    }
    $("#top-expense-ledger-2-perc").removeClass("perc_increase");
    $("#top-expense-ledger-2-perc").removeClass("perc_decrease");
    if (data.perc_change_top_expense_ledgers[ledger] > 0) {
      $("#top-expense-ledger-2-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_expense_ledgers[ledger] +
          " %"
      );
      $("#top-expense-ledger-2-perc").addClass("perc_increase");
    } else {
      $("#top-expense-ledger-2-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_expense_ledgers[ledger]) +
          " %"
      );
      $("#top-expense-ledger-2-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-expense-ledgers-row-2").css("display", "None");
  }
  var ledger = data.expense_ledgers_chart_labels[2];
  if (typeof ledger !== "undefined") {
    $("#top-expense-ledgers-row-3").removeAttr("style");
    try {
      $("#top-expense-ledger-3").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-expense-ledger-3").html("");
    }
    try {
      $("#top-expense-ledger-3-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-expense-ledger-3-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-expense-ledger-3-name").html("");
    }

    if (find_digits(data.expense_ledgers_chart_data[2]) > 6) {
      $("#top-expense-ledger-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.expense_ledgers_chart_data[2] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-expense-ledger-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.expense_ledgers_chart_data[2], 0).toLocaleString("hi")
      );
    }
    $("#top-expense-ledger-3-perc").removeClass("perc_increase");
    $("#top-expense-ledger-3-perc").removeClass("perc_decrease");
    if (data.perc_change_top_expense_ledgers[ledger] > 0) {
      $("#top-expense-ledger-3-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_expense_ledgers[ledger] +
          " %"
      );
      $("#top-expense-ledger-3-perc").addClass("perc_increase");
    } else {
      $("#top-expense-ledger-3-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_expense_ledgers[ledger]) +
          " %"
      );
      $("#top-expense-ledger-3-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-expense-ledgers-row-3").css("display", "None");
  }
  var ledger = data.expense_ledgers_chart_labels[3];
  if (typeof ledger !== "undefined") {
    $("#top-expense-ledgers-row-4").removeAttr("style");
    try {
      $("#top-expense-ledger-4").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-expense-ledger-4").html("");
    }
    try {
      $("#top-expense-ledger-4-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-expense-ledger-4-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-expense-ledger-4-name").html("");
    }

    if (find_digits(data.expense_ledgers_chart_data[3]) > 6) {
      $("#top-expense-ledger-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.expense_ledgers_chart_data[3] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-expense-ledger-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.expense_ledgers_chart_data[3], 0).toLocaleString("hi")
      );
    }
    $("#top-expense-ledger-4-perc").removeClass("perc_increase");
    $("#top-expense-ledger-4-perc").removeClass("perc_decrease");
    if (data.perc_change_top_expense_ledgers[ledger] > 0) {
      $("#top-expense-ledger-4-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_expense_ledgers[ledger] +
          " %"
      );
      $("#top-expense-ledger-4-perc").addClass("perc_increase");
    } else {
      $("#top-expense-ledger-4-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_expense_ledgers[ledger]) +
          " %"
      );
      $("#top-expense-ledger-4-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-expense-ledgers-row-4").css("display", "None");
  }
  var ledger = data.expense_ledgers_chart_labels[4];
  if (typeof ledger !== "undefined") {
    $("#top-expense-ledgers-row-5").removeAttr("style");
    try {
      $("#top-expense-ledger-5").html(toProperCase(ledger.charAt(0)));
    } catch (error) {
      $("#top-expense-ledger-5").html("");
    }
    try {
      $("#top-expense-ledger-5-name").html(toProperCase(ledger.slice(0, 30)));
      $("#top-expense-ledger-5-name").attr({ title: toProperCase(ledger) });
    } catch (error) {
      $("#top-expense-ledger-5-name").html("");
    }

    if (find_digits(data.expense_ledgers_chart_data[4]) > 6) {
      $("#top-expense-ledger-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(
            data.expense_ledgers_chart_data[4] / 100000,
            0
          ).toLocaleString("hi") +
          " L"
      );
    } else {
      $("#top-expense-ledger-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.expense_ledgers_chart_data[4], 0).toLocaleString("hi")
      );
    }
    $("#top-expense-ledger-5-perc").removeClass("perc_increase");
    $("#top-expense-ledger-5-perc").removeClass("perc_decrease");
    if (data.perc_change_top_expense_ledgers[ledger] > 0) {
      $("#top-expense-ledger-5-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_expense_ledgers[ledger] +
          " %"
      );
      $("#top-expense-ledger-5-perc").addClass("perc_increase");
    } else {
      $("#top-expense-ledger-5-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_expense_ledgers[ledger]) +
          " %"
      );
      $("#top-expense-ledger-5-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-expense-ledgers-row-5").css("display", "None");
  }
  new Chart(top_expense_ledgers_dash, {
    type: "polarArea",
    data: {
      labels: data.expense_ledgers_chart_labels,
      datasets: [
        {
          data: data.expense_ledgers_chart_data,
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
}

// Update Ageing Dash Card:
function ageing_dash_card(data) {
  $("#ageing").remove();
  $("#ageing-div").append(
    '<canvas class="chart px-3" id="ageing" style="display: block"></canvas>'
  );
  var $ageing_chart = $("#ageing");
  var ageing_dash = $ageing_chart[0].getContext("2d");

  if (find_digits(data.receivable_ageing_value[0]) > 6) {
    $("#ageing-1-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[0] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-1-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[0], 0).toLocaleString("hi")
    );
  }
  $("#ageing-1-count-drs").html(
    Math.round(data.receivable_ageing_count[0], 0).toLocaleString("hi")
  );

  if (find_digits(data.payable_ageing_value[0]) > 6) {
    $("#ageing-1-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[0] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-1-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[0], 0).toLocaleString("hi")
    );
  }
  $("#ageing-1-count-crs").html(
    Math.round(data.payable_ageing_count[0], 0).toLocaleString("hi")
  );

  if (find_digits(data.receivable_ageing_value[1]) > 6) {
    $("#ageing-2-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[1] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-2-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[1], 0).toLocaleString("hi")
    );
  }
  $("#ageing-2-count-drs").html(
    Math.round(data.receivable_ageing_count[1], 0).toLocaleString("hi")
  );

  if (find_digits(data.payable_ageing_value[1]) > 6) {
    $("#ageing-2-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[1] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-2-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[1], 0).toLocaleString("hi")
    );
  }
  $("#ageing-2-count-crs").html(
    Math.round(data.payable_ageing_count[1], 0).toLocaleString("hi")
  );

  if (find_digits(data.receivable_ageing_value[2]) > 6) {
    $("#ageing-3-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[2] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-3-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[2], 0).toLocaleString("hi")
    );
  }
  $("#ageing-3-count-drs").html(
    Math.round(data.receivable_ageing_count[2], 0).toLocaleString("hi")
  );

  if (find_digits(data.payable_ageing_value[2]) > 6) {
    $("#ageing-3-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[2] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-3-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[2], 0).toLocaleString("hi")
    );
  }
  $("#ageing-3-count-crs").html(
    Math.round(data.payable_ageing_count[2], 0).toLocaleString("hi")
  );

  if (find_digits(data.receivable_ageing_value[3]) > 6) {
    $("#ageing-4-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[3] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-4-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[3], 0).toLocaleString("hi")
    );
  }
  $("#ageing-4-count-drs").html(
    Math.round(data.receivable_ageing_count[3], 0).toLocaleString("hi")
  );

  if (find_digits(data.payable_ageing_value[3]) > 6) {
    $("#ageing-4-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[3] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-4-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[3], 0).toLocaleString("hi")
    );
  }
  $("#ageing-4-count-crs").html(
    Math.round(data.payable_ageing_count[3], 0).toLocaleString("hi")
  );

  if (find_digits(data.receivable_ageing_value[4]) > 6) {
    $("#ageing-5-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[4] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-5-amount-drs").html(
      "&#8377;&nbsp;" +
        Math.round(data.receivable_ageing_value[4], 0).toLocaleString("hi")
    );
  }
  $("#ageing-5-count-drs").html(
    Math.round(data.receivable_ageing_count[4], 0).toLocaleString("hi")
  );

  if (find_digits(data.payable_ageing_value[4]) > 6) {
    $("#ageing-5-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[4] / 100000, 0).toLocaleString(
          "hi"
        ) +
        " L"
    );
  } else {
    $("#ageing-5-amount-crs").html(
      "&#8377;&nbsp;" +
        Math.round(data.payable_ageing_value[4], 0).toLocaleString("hi")
    );
  }
  $("#ageing-5-count-crs").html(
    Math.round(data.payable_ageing_count[4], 0).toLocaleString("hi")
  );

  new Chart(ageing_dash, {
    type: "bar",
    data: {
      labels: data.ageing_labels,
      datasets: [
        {
          label: "Receivable",
          data: data.receivable_ageing_value,
          backgroundColor: custom_colors[0],
          borderRadius: 5,
        },
        {
          label: "Payable",
          data: data.payable_ageing_value,
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
}

// Update Receipts Vs Payments Dash Card:
function rec_pay_dash_card(data) {
  $("#rec-pay").remove();
  $("#rec-pay-div").append(
    '<canvas class="chart p-0" id="rec-pay" style="display: block"></canvas>'
  );
  var $rec_pay_chart = $("#rec-pay");
  var rec_pay_dash = $rec_pay_chart[0].getContext("2d");

  new Chart(rec_pay_dash, {
    type: "bar",
    data: {
      labels: data.receipts_payments_labels,
      datasets: [
        {
          label: "Bank Receipt",
          data: data.bank_receipts_value,
          borderColor: custom_colors_rgba[0],
          backgroundColor: custom_colors_rgba[0],
          borderRadius: 5,
          order: 1,
          yAxisID: "yAxis",
        },
        {
          label: "Bank Payment",
          data: data.bank_payments_value,
          borderColor: custom_colors_rgba[4],
          backgroundColor: custom_colors_rgba[4],
          borderRadius: 5,
          order: 1,
          yAxisID: "yAxis",
        },
        {
          label: "Cash Receipt",
          data: data.cash_receipts_value,
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
          data: data.cash_payments_value,
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
}

// Update Top 5 Cost Centers Dash Card:
function cc_dash_card(data) {
  $("#top-5-cc").remove();
  $("#top-5-cc-div").append(
    '<canvas id="top-5-cc" class="chart p-1 h-100" id="tree-top-5-cc"></canvas>'
  );
  var $top_cc_chart = $("#top-5-cc");
  var top_cc_dash = $top_cc_chart[0].getContext("2d");

  // Update First Table Row
  var cc = data.cc_category_chart_labels[0];
  if (typeof cc !== "undefined") {
    $("#top-cc-heading").removeAttr("style");
    $("#top-cc-row-1").removeAttr("style");
    try {
      $("#top-cc-1").html(toProperCase(cc.charAt(0)));
    } catch (error) {
      $("#top-cc-1").html("");
    }
    try {
      $("#top-cc-1-name").html(
        toProperCase(cc.split(" ")[0] + " " + cc.split(" ")[1])
      );
      $("#top-cc-1-name").attr({ title: toProperCase(cc) });
    } catch (error) {
      $("#top-cc-1-name").html("");
    }

    if (find_digits(data.cc_category_chart_data[0]) > 6) {
      $("#top-cc-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[0] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-cc-1-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[0], 0).toLocaleString("hi")
      );
    }
    $("#top-cc-1-perc").removeClass("perc_increase");
    $("#top-cc-1-perc").removeClass("perc_decrease");
    if (data.perc_change_top_cc_category[cc] > 0) {
      $("#top-cc-1-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_cc_category[cc] +
          " %"
      );
      $("#top-cc-1-perc").addClass("perc_increase");
    } else {
      $("#top-cc-1-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_cc_category[cc]) +
          " %"
      );
      $("#top-cc-1-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-cc-row-1").css("display", "None");
    $("#top-cc-heading").css("display", "None");
  }
  var cc = data.cc_category_chart_labels[1];
  if (typeof cc !== "undefined") {
    $("#top-cc-row-2").removeAttr("style");
    try {
      $("#top-cc-2").html(toProperCase(cc.charAt(0)));
    } catch (error) {
      $("#top-cc-2").html("");
    }
    try {
      $("#top-cc-2-name").html(
        toProperCase(cc.split(" ")[0] + " " + cc.split(" ")[1])
      );
      $("#top-cc-2-name").attr({ title: toProperCase(cc) });
    } catch (error) {
      $("#top-cc-2-name").html("");
    }

    if (find_digits(data.cc_category_chart_data[1]) > 6) {
      $("#top-cc-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[1] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-cc-2-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[1], 0).toLocaleString("hi")
      );
    }
    $("#top-cc-2-perc").removeClass("perc_increase");
    $("#top-cc-2-perc").removeClass("perc_decrease");
    if (data.perc_change_top_cc_category[cc] > 0) {
      $("#top-cc-2-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_cc_category[cc] +
          " %"
      );
      $("#top-cc-2-perc").addClass("perc_increase");
    } else {
      $("#top-cc-2-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_cc_category[cc]) +
          " %"
      );
      $("#top-cc-2-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-cc-row-2").css("display", "None");
  }
  var cc = data.cc_category_chart_labels[2];
  if (typeof cc !== "undefined") {
    $("#top-cc-row-3").removeAttr("style");
    try {
      $("#top-cc-3").html(toProperCase(cc.charAt(0)));
    } catch (error) {
      $("#top-cc-3").html("");
    }
    try {
      $("#top-cc-3-name").html(
        toProperCase(cc.split(" ")[0] + " " + cc.split(" ")[1])
      );
      $("#top-cc-3-name").attr({ title: toProperCase(cc) });
    } catch (error) {
      $("#top-cc-3-name").html("");
    }

    if (find_digits(data.cc_category_chart_data[2]) > 6) {
      $("#top-cc-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[2] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-cc-3-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[2], 0).toLocaleString("hi")
      );
    }
    $("#top-cc-3-perc").removeClass("perc_increase");
    $("#top-cc-3-perc").removeClass("perc_decrease");
    if (data.perc_change_top_cc_category[cc] > 0) {
      $("#top-cc-3-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_cc_category[cc] +
          " %"
      );
      $("#top-cc-3-perc").addClass("perc_increase");
    } else {
      $("#top-cc-3-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_cc_category[cc]) +
          " %"
      );
      $("#top-cc-3-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-cc-row-3").css("display", "None");
  }
  var cc = data.cc_category_chart_labels[3];
  if (typeof cc !== "undefined") {
    $("#top-cc-row-4").removeAttr("style");
    try {
      $("#top-cc-4").html(toProperCase(cc.charAt(0)));
    } catch (error) {
      $("#top-cc-4").html("");
    }
    try {
      $("#top-cc-4-name").html(
        toProperCase(cc.split(" ")[0] + " " + cc.split(" ")[1])
      );
      $("#top-cc-4-name").attr({ title: toProperCase(cc) });
    } catch (error) {
      $("#top-cc-4-name").html("");
    }

    if (find_digits(data.cc_category_chart_data[3]) > 6) {
      $("#top-cc-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[3] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-cc-4-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[3], 0).toLocaleString("hi")
      );
    }
    $("#top-cc-4-perc").removeClass("perc_increase");
    $("#top-cc-4-perc").removeClass("perc_decrease");
    if (data.perc_change_top_cc_category[cc] > 0) {
      $("#top-cc-4-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_cc_category[cc] +
          " %"
      );
      $("#top-cc-4-perc").addClass("perc_increase");
    } else {
      $("#top-cc-4-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_cc_category[cc]) +
          " %"
      );
      $("#top-cc-4-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-cc-row-4").css("display", "None");
  }
  var cc = data.cc_category_chart_labels[4];
  if (typeof cc !== "undefined") {
    $("#top-cc-row-5").removeAttr("style");
    try {
      $("#top-cc-5").html(toProperCase(cc.charAt(0)));
    } catch (error) {
      $("#top-cc-5").html("");
    }
    try {
      $("#top-cc-5-name").html(
        toProperCase(cc.split(" ")[0] + " " + cc.split(" ")[1])
      );
      $("#top-cc-5-name").attr({ title: toProperCase(cc) });
    } catch (error) {
      $("#top-cc-5-name").html("");
    }

    if (find_digits(data.cc_category_chart_data[4]) > 6) {
      $("#top-cc-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[4] / 100000, 0).toLocaleString(
            "hi"
          ) +
          " L"
      );
    } else {
      $("#top-cc-5-amount").html(
        "&#8377;&nbsp;" +
          Math.round(data.cc_category_chart_data[4], 0).toLocaleString("hi")
      );
    }
    $("#top-cc-5-perc").removeClass("perc_increase");
    $("#top-cc-5-perc").removeClass("perc_decrease");
    if (data.perc_change_top_cc_category[cc] > 0) {
      $("#top-cc-5-perc").html(
        '<span><i class="fas fa-arrow-up"></i></span>&nbsp;' +
          data.perc_change_top_cc_category[cc] +
          " %"
      );
      $("#top-cc-5-perc").addClass("perc_increase");
    } else {
      $("#top-cc-5-perc").html(
        '<span><i class="fas fa-arrow-down"></i></span>&nbsp;' +
          Math.abs(data.perc_change_top_cc_category[cc]) +
          " %"
      );
      $("#top-cc-5-perc").addClass("perc_decrease");
    }
  } else {
    $("#top-cc-row-5").css("display", "None");
  }
  new Chart(top_cc_dash, {
    type: "treemap",
    data: {
      datasets: [
        {
          tree: data.cc_category_chart_data,
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
}
