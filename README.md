django-e2ee-chat
---

# Requirements
- docker
- docker-compose

# Production
## docker-compose.yml
```yaml
version: '3'

services:
  django-e2ee-chat:
    build: https://github.com/wvffle/django-e2ee-chat.git
    environment:
      - DJANGO_APP_SECRET="some-strong-secret"
      - DJANGO_ALLOWED_HOST="https://chat.example.com"
    ports:
      - 80:8080
```

# Development
```shell
git clone https://github.com/wvffle/django-e2ee-chat.git
cd django-e2ee-chat
docker-compose up -d
```

## Suggested PyCharm configuration
1. Install following plugins:
```md
# Development
- Conventional Commit
- Commitlint Conventional Commit


# Backend related:
- Poetry

# Frontend related:
- Node.js
- Vue.js
- Tailwind CSS
```
2. Create a new python environment (Poetry environment)
3. Set project environment to Poetry environment
