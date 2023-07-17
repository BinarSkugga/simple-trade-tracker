import {formnum} from "@/utils";

const defaultPieChartOpts = {
    chart: {
        width: '100%',
        type: 'pie',
    },
    plotOptions: {
        pie: {
            dataLabels: {
                offset: -30
            }
        }
    },
    tooltip: {
        y: {
            formatter(val: number) {
                return '$' + formnum(val)
            }
        }
    },
    dataLabels: {
        formatter(val: number, opts: any) {
            const name = opts.w.globals.labels[opts.seriesIndex]
            return [name, formnum(val) + '%']
        }
    },
    legend: {
        show: false
    }
}

export const gainBreakdownChart = {
    ...defaultPieChartOpts,
    labels: ['Dividend', 'Capital']
}

export const stockBreakdownChart = {
    ...defaultPieChartOpts,
    labels: [],
    plotOptions: {
        pie: {
            dataLabels: {
                offset: -15
            }
        }
    },
}

export const sectorBreakdownChart = {
    ...defaultPieChartOpts,
    labels: [],
    plotOptions: {
        pie: {
            dataLabels: {
                offset: -15
            }
        }
    },
}