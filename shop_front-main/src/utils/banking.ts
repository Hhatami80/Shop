export const formatCardNumber = (number: string | undefined): string => {
    if (!number) return ''
    return number.toString().replace(/(.{4})/g, '$1 ').trim()
}

export const rialToToman = (number: number): number | null => {
    if(!number) return null
    // return number / 10
    return number
}

export const tomanToRial = (number: number | null): number | null => {
    if(!number) return null
    // return number * 10
    return number
}


export const addUnit = (text: string | null, unit: string | null): string => {
    if(!text || !unit) return '';

    return `${text} ${unit}`
}