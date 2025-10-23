# 🔒 Guide de Sécurité - ETRAGC SARLU

## 📋 Mesures de Sécurité Implémentées

### 1. **Protection contre les Attaques par Force Brute (Django-Axes)**
- ✅ Blocage après 5 tentatives de connexion échouées
- ✅ Verrouillage de 1 heure
- ✅ Combinaison IP + Utilisateur
- ✅ Logs des tentatives suspectes

### 2. **Protection CSRF (Cross-Site Request Forgery)**
- ✅ Tokens CSRF sur tous les formulaires
- ✅ Cookies CSRF sécurisés
- ✅ SameSite=Strict

### 3. **Sécurité des Sessions**
- ✅ Cookies HttpOnly (protection XSS)
- ✅ Cookies Secure (HTTPS uniquement en production)
- ✅ Expiration après 24h d'inactivité
- ✅ SameSite=Strict

### 4. **Content Security Policy (CSP)**
- ✅ Restriction des sources de scripts
- ✅ Protection contre XSS
- ✅ Blocage du framing (clickjacking)

### 5. **Headers de Sécurité**
- ✅ X-Frame-Options: DENY
- ✅ X-Content-Type-Options: nosniff
- ✅ X-XSS-Protection: 1; mode=block
- ✅ Referrer-Policy: same-origin
- ✅ HSTS (HTTP Strict Transport Security) en production

### 6. **Validation des Mots de Passe**
- ✅ Minimum 8 caractères
- ✅ Pas de mots de passe communs
- ✅ Pas uniquement numérique
- ✅ Différent des informations utilisateur

### 7. **Protection des Données**
- ✅ Chiffrement des mots de passe (PBKDF2)
- ✅ Variables sensibles dans .env (non versionnées)
- ✅ Logs de sécurité
- ✅ Limitation de taille des uploads (10 MB)

### 8. **Rate Limiting**
- ✅ Limitation du nombre de requêtes
- ✅ Protection contre le spam
- ✅ Protection des endpoints sensibles

## 🚀 Installation des Packages de Sécurité

```powershell
pip install -r requirements.txt
```

## ⚙️ Configuration

### 1. Variables d'Environnement (.env)

```env
# Sécurité
SECRET_KEY=votre-cle-secrete-tres-longue-et-aleatoire
DEBUG=False  # TOUJOURS False en production
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
```

### 2. Créer le dossier de logs

```powershell
mkdir logs
```

### 3. Appliquer les migrations

```powershell
python manage.py migrate
```

## 🛡️ Bonnes Pratiques de Sécurité

### Pour les Administrateurs

1. **Mots de passe forts**
   - Minimum 12 caractères
   - Mélange de majuscules, minuscules, chiffres et symboles
   - Unique pour chaque service

2. **Mise à jour régulière**
   ```powershell
   pip list --outdated
   pip install --upgrade django
   ```

3. **Sauvegardes régulières**
   ```powershell
   # Base de données
   python manage.py dumpdata > backup_$(date +%Y%m%d).json
   
   # MySQL
   mysqldump -u user -p etragc_db > backup.sql
   ```

4. **Surveillance des logs**
   ```powershell
   # Vérifier les tentatives de connexion suspectes
   type logs\axes.log
   type logs\security.log
   ```

5. **HTTPS obligatoire en production**
   - Utiliser Let's Encrypt pour un certificat gratuit
   - Configurer le serveur web (Nginx/Apache)

### Pour les Développeurs

1. **Ne jamais commiter**
   - Fichier `.env`
   - Mots de passe
   - Clés API
   - Données sensibles

2. **Valider les entrées utilisateur**
   ```python
   from django.core.validators import validate_email
   from django.core.exceptions import ValidationError
   ```

3. **Utiliser les QuerySets Django**
   - Éviter le SQL brut
   - Protection automatique contre SQL Injection

4. **Échapper les sorties**
   - Django le fait automatiquement dans les templates
   - Utiliser `|safe` avec précaution

## 🔍 Vérification de Sécurité

### 1. Check Django

```powershell
python manage.py check --deploy
```

### 2. Test de Sécurité

```powershell
# Installer safety
pip install safety

# Scanner les vulnérabilités
safety check
```

### 3. Audit des Dépendances

```powershell
pip-audit
```

## 🚨 En Cas d'Incident de Sécurité

### 1. Réaction Immédiate

```powershell
# 1. Mettre l'application en maintenance
# Créer un fichier maintenance.html

# 2. Changer toutes les clés
# Générer une nouvelle SECRET_KEY
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# 3. Révoquer les sessions actives
python manage.py clearsessions

# 4. Analyser les logs
type logs\security.log
type logs\axes.log
```

### 2. Investigation

1. Identifier la source de l'attaque
2. Vérifier les logs d'accès
3. Analyser les modifications de la base de données
4. Vérifier l'intégrité des fichiers

### 3. Récupération

1. Restaurer depuis une sauvegarde saine
2. Patcher la vulnérabilité
3. Renforcer la sécurité
4. Notifier les utilisateurs si nécessaire

## 📊 Monitoring

### 1. Logs à Surveiller

- `logs/security.log` - Événements de sécurité
- `logs/axes.log` - Tentatives de connexion échouées
- Logs du serveur web
- Logs de la base de données

### 2. Alertes à Configurer

- Tentatives de connexion multiples échouées
- Accès à des URLs sensibles
- Erreurs 500 répétées
- Uploads de fichiers suspects

## 🔐 Checklist de Sécurité Production

- [ ] DEBUG=False
- [ ] SECRET_KEY unique et sécurisée
- [ ] ALLOWED_HOSTS configuré
- [ ] HTTPS activé (certificat SSL)
- [ ] Base de données avec mot de passe fort
- [ ] Firewall configuré
- [ ] Sauvegardes automatiques
- [ ] Logs activés et surveillés
- [ ] Mises à jour de sécurité appliquées
- [ ] Accès SSH sécurisé (clés, pas de mot de passe)
- [ ] Utilisateur non-root pour l'application
- [ ] Permissions fichiers correctes (644 pour fichiers, 755 pour dossiers)
- [ ] .env non accessible publiquement
- [ ] Rate limiting activé
- [ ] CORS configuré si API
- [ ] CSP configuré
- [ ] Headers de sécurité activés

## 📚 Ressources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Django Security](https://docs.djangoproject.com/en/4.2/topics/security/)
- [Mozilla Observatory](https://observatory.mozilla.org/)
- [Security Headers](https://securityheaders.com/)

## 🆘 Support

En cas de problème de sécurité critique:
1. Contacter immédiatement l'administrateur système
2. Documenter l'incident
3. Ne pas paniquer, suivre la procédure

---

**Dernière mise à jour:** Octobre 2025
**Version:** 1.0
