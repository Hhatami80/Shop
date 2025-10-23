import { bankCards, type BankCard } from "../bank-cards/bankCards";
import { ibanBanksHash, type IBANBank } from "../bank-cards/ibanBanks";

export function validateIranianNationalId(id: string): boolean {
    // Only digits allowed, length 8-10
    if (!/^\d{8,10}$/.test(id)) return false;

    // Pad to 10 digits with leading zeros
    id = id.padStart(10, '0');

    const controlDigit = Number(id[9]);
    let sum = 0;

    for (let i = 0; i < 9; i++) {
        sum += Number(id[i]) * (10 - i);
    }

    const remainder = sum % 11;

    if ((remainder < 2 && controlDigit === remainder) ||
        (remainder >= 2 && controlDigit === 11 - remainder)) {
        return true;
    }

    return false;
}

export function validateBankCardNumber(cardNumber: string): boolean {
    // Remove all non-digit characters (like spaces or dashes)
    const sanitized = cardNumber.replace(/\D/g, '');

    // Card numbers are usually 13-19 digits
    if (!/^\d{13,19}$/.test(sanitized)) return false;

    let sum = 0;
    const len = sanitized.length;
    
    // Luhn algorithm
    for (let i = 0; i < len; i++) {
        let digit = Number(sanitized[len - 1 - i]); // start from right
        if (i % 2 === 1) {
            digit *= 2;
            if (digit > 9) digit -= 9;
        }
        sum += digit;
    }

    return sum % 10 === 0;
}

export function validateIranianIBAN(iban: string): boolean {
    const sanitized = iban.replace(/\s+/g, '').toUpperCase()
    if (!/^IR\d{24}$/.test(sanitized)) return false

    const rearranged = sanitized.slice(4) + sanitized.slice(0, 4)
    let numeric = ''
    for (const c of rearranged) numeric += /[A-Z]/.test(c) ? (c.charCodeAt(0) - 55).toString() : c

    return BigInt(numeric) % 97n === 1n
}

// Recognize bank by IBAN code
export function getBankFromIBAN(iban: string): IBANBank | undefined {
    const code = iban.replace(/\s+/g, '').substring(4, 7)
    return ibanBanksHash[code]
}

// Recognize bank by card prefix
export function getBankFromCard(cardNumber: string): BankCard | undefined {
    const sanitized = cardNumber.replace(/\D/g, '')
    return bankCards.find(b => sanitized.startsWith(b.card_no.toString()))
}

// Account number simple check
export function validateAccountNumber(accountNumber: string): boolean {
    return /^\d{8,18}$/.test(accountNumber)
}

export function validateIranianSheba(
    sheba: string,
    cardNumber?: string,
    accountNumber?: string
): boolean {
    console.log('--- IBAN Validation Debug ---')
    console.log('Sheba input:', sheba)
    console.log('Card number input:', cardNumber)
    console.log('Account number input:', accountNumber)

    if (!sheba) return false

    const sanitizedSheba = sheba.replace(/\s+/g, '').toUpperCase()
    
    // Validate IBAN structure
    if (!validateIranianIBAN(sanitizedSheba)) {
        console.log('IBAN structure invalid')
        return false
    }
    console.log('IBAN structure valid')

    // Validate card number if provided
    const isCardValid = cardNumber ? validateBankCardNumber(cardNumber) : true
    if (!isCardValid) console.log('Card number invalid')

    // Validate account number format if provided
    const sanitizedAccount = accountNumber ? accountNumber.replace(/\D/g, '') : undefined
    const isAccountStructurallyValid = sanitizedAccount ? validateAccountNumber(sanitizedAccount) : true
    if (!isAccountStructurallyValid) console.log('Account number structurally invalid')

    // Extract the account section from IBAN (after IR + check digits)
    let shebaAccountMatch = true
    if (sanitizedAccount) {
        const shebaBody = sanitizedSheba.slice(4) // remove IR + check digits
        const shebaAccount = shebaBody.slice(-sanitizedAccount.length)
        shebaAccountMatch = sanitizedAccount === shebaAccount
        if (!shebaAccountMatch) console.log('Account number does not match IBAN')
    }

    // Match banks if card is provided
    const cardBank = cardNumber ? getBankFromCard(cardNumber) : undefined
    const shebaBank = getBankFromIBAN(sanitizedSheba)
    console.log('Card bank detected:', cardBank)
    console.log('IBAN bank detected:', shebaBank)
    if (cardBank && shebaBank && cardBank.bank_name !== shebaBank.nickname) {
        console.log('Card and IBAN belong to different banks')
        return false
    }

    // Final result: all three must pass
    const result = isCardValid && isAccountStructurallyValid && shebaAccountMatch
    console.log('Sheba validation result:', result)
    return result
}