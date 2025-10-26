/**
 * Formatage automatique des montants avec espacement
 * Facilite la lecture des montants lors de la saisie
 */

document.addEventListener('DOMContentLoaded', function() {
    // Sélectionner tous les champs de montants
    const moneyInputs = document.querySelectorAll('.money-input, input[name*="montant"], input[name*="prix"], input[name*="salaire"]');
    
    moneyInputs.forEach(input => {
        // Ignorer les champs readonly
        if (input.hasAttribute('readonly') || input.hasAttribute('disabled')) {
            return;
        }
        
        // Formater à l'initialisation si une valeur existe
        if (input.value) {
            formatMoneyInput(input);
        }
        
        // Filtrer les caractères non valides
        input.addEventListener('keypress', function(e) {
            // Autoriser uniquement les chiffres, point, virgule, et touches de contrôle
            const char = String.fromCharCode(e.which);
            if (!/[\d.,]/.test(char) && e.which !== 0 && e.which !== 8) {
                e.preventDefault();
            }
        });
        
        // Formater pendant la saisie
        input.addEventListener('input', function(e) {
            formatMoneyInput(e.target);
        });
        
        // Nettoyer avant la soumission du formulaire
        input.closest('form')?.addEventListener('submit', function() {
            cleanMoneyInput(input);
        });
    });
});

/**
 * Formate un champ de montant avec espacement
 */
function formatMoneyInput(input) {
    // Sauvegarder la position du curseur
    let cursorPosition = input.selectionStart;
    let oldValue = input.value;
    
    // Retirer tous les espaces existants
    let value = input.value.replace(/\s/g, '');
    
    // Séparer la partie entière et décimale
    let parts = value.split(/[.,]/);
    let integerPart = parts[0];
    let decimalPart = parts.length > 1 ? parts[1] : '';
    
    // Formater la partie entière avec des espaces tous les 3 chiffres (de droite à gauche)
    let formattedInteger = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
    
    // Reconstruire la valeur
    let formattedValue = formattedInteger;
    if (decimalPart || value.includes('.') || value.includes(',')) {
        formattedValue += '.' + decimalPart;
    }
    
    // Mettre à jour la valeur
    input.value = formattedValue;
    
    // Ajuster la position du curseur
    let spacesAdded = (formattedValue.match(/\s/g) || []).length - (oldValue.match(/\s/g) || []).length;
    let newCursorPosition = cursorPosition + spacesAdded;
    
    // Restaurer la position du curseur
    if (input === document.activeElement) {
        input.setSelectionRange(newCursorPosition, newCursorPosition);
    }
}

/**
 * Nettoie un champ de montant (retire les espaces) avant soumission
 */
function cleanMoneyInput(input) {
    input.value = input.value.replace(/\s/g, '');
}

/**
 * Formate un nombre pour l'affichage
 */
function formatMoney(amount, decimals = 0) {
    if (amount === null || amount === undefined || amount === '') {
        return '0';
    }
    
    let num = parseFloat(amount);
    if (isNaN(num)) {
        return '0';
    }
    
    // Formater avec séparateur de milliers
    return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ' ');
}

/**
 * Parse un montant formaté en nombre
 */
function parseMoney(formattedAmount) {
    if (!formattedAmount) {
        return 0;
    }
    
    // Retirer les espaces et remplacer la virgule par un point
    let cleaned = formattedAmount.toString().replace(/\s/g, '').replace(',', '.');
    let num = parseFloat(cleaned);
    
    return isNaN(num) ? 0 : num;
}

// Exporter les fonctions pour utilisation globale
window.formatMoney = formatMoney;
window.parseMoney = parseMoney;
