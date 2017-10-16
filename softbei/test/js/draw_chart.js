/**
 * Created by hzl on 2017/5/25.
 */
function drawMarkersMap() {
    var data = google.visualization.arrayToDataTable([
        ['City', '活动', '天气'],
        ['Shenzhen', 2761477, 1285.31],
        ['Guangzhou', 1324110, 181.76],
        ['Shanghai', 959574, 117.27],
        ['Turin', 907563, 130.17]

    ]);

    var options = {
        region: 'CN',
        displayMode: 'markers',
        colorAxis: {colors: ['green', 'blue']}
    };

    var chart = new google.visualization.GeoChart(document.getElementById('chart_div'));
    chart.draw(data, options);
};