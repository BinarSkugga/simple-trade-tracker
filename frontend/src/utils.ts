const numberFormatter = Intl.NumberFormat('en-CA', {style: 'decimal', minimumFractionDigits: 2, maximumFractionDigits: 2})

export function formatMoney(number: any) {
    return numberFormatter.format(number)
}

export function formnum(number: any) {
    return numberFormatter.format(number)
}