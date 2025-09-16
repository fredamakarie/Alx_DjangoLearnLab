# Permissions Setup

- Book model has 4 custom permissions:
  - can_view → Viewers, Editors, Admins
  - can_create → Editors, Admins
  - can_edit → Editors, Admins
  - can_delete → Admins only

- Groups:
  - Viewers: can_view
  - Editors: can_view, can_create, can_edit
  - Admins: all permissions

- Decorators:
  Use @permission_required('<app_name>.<permission>') on views.


# Security Configurations

- DEBUG = False in production
- HTTPS enforced with CSRF_COOKIE_SECURE, SESSION_COOKIE_SECURE
- X_FRAME_OPTIONS = DENY (clickjacking protection)
- Content Security Policy applied via django-csp
- All forms protected with {% csrf_token %}
- ORM used to prevent SQL injection

# Security Configuration

- Enforced HTTPS with SECURE_SSL_REDIRECT
- HSTS enabled for 1 year with preload + subdomains
- Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
- Extra headers: X_FRAME_OPTIONS, SECURE_CONTENT_TYPE_NOSNIFF, SECURE_BROWSER_XSS_FILTER
- Nginx configured with SSL/TLS certificates (Let's Encrypt)
