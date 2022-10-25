import { defineStore } from 'pinia'
// @ts-ignore
import {StockModel} from "@/models/StockModel";

const dfn = {"short_name":"DIVIDEND 15 SPLIT CORP","long_name":"Dividend 15 Split Corp.","symbol":"DFN.TO","sector":"Financial Services","exchange":"TOR","timezone":"America/Toronto","currency":"CAD","price":7.18,"beta":1.591541,"dividend_yield":0.1693,"ex_dividend_date":1666915200,"payout_ratio":1.0619,"debt_equity_ratio":1.747,"monthly_return":0.10129783333333332}
const div = {"short_name":"DIVERSIFIED ROYALTY CORP","long_name":"Diversified Royalty Corp.","symbol":"DIV.TO","sector":"Industrials","exchange":"TOR","timezone":"America/Toronto","currency":"CAD","price":2.92,"beta":1.595824,"dividend_yield":0.081599995,"ex_dividend_date":1665619200,"payout_ratio":1.0356,"debt_equity_ratio":1.692,"monthly_return":0.019855998783333332}

export const useStocksStore = defineStore({
    id: 'stocks',
    state: () => ({
        stocks: [dfn, div]
    })
})
