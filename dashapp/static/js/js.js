"use strict";

$(function () {

    // Manager dashboard highchart
    if ($("#highcharts-container").length > 0) {
        let myChart = Highcharts.chart('highcharts-container', {
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Fruit Consumption'
            },
            xAxis: {
                categories: ['Apples', 'Bananas', 'Oranges']
            },
            yAxis: {
                title: {
                    text: 'Fruit eaten'
                }
            },
            series: [{
                name: 'Jane',
                data: [1, 0, 4]
            }, {
                name: 'John',
                data: [5, 7, 3]
            }]
        });
    }

    // Income statement highchart
    if ($("#income-statement-highchart-container").length > 0) {

        let monthNames = [];
        $(".month-names").each(function() {
           monthNames.push($(this).text());
        });

        let netRevenues = [];
        $(".net-revenue-element").each(function() {
            netRevenues.push(parseFloat($(this).text()));
        });

        let netExpenses = [];
        $(".net-expense-element").each(function() {
            netExpenses.push(parseFloat($(this).text()));
        });


        Highcharts.chart('income-statement-highchart-container', {
            series: [{
                name: 'Revenues',
                data: netRevenues
            }, {
                name: 'Expenses',
                data: netExpenses
            }],
            chart: {
                type: 'area'
            },
            yAxis: {
                allowDecimals: false,
                title: {
                text: 'Units'
                }
            },
            xAxis: {
                categories: monthNames
            },
            title: {
                text: 'Revenues & Expenses'
            },
            colors: ["rgb(144, 237, 125)", "rgb(244, 91, 91)"]
        });
    }


    // Events for demo login buttons
    if ($(".manager-demo-login").length > 0) {
        $(".manager-demo-login").on("click", function(event){
            $("#id_login").val("bartoszw");
            $("#id_password").val("testujetestuje");
        });
    }

    if ($(".employee-demo-login").length > 0) {
        $(".employee-demo-login").on("click", function(event){
            $("#id_login").val("mah");
            $("#id_password").val("temporary");
        });
    }

});