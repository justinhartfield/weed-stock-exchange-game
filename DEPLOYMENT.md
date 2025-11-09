# Deployment Guide

## Quick Start with Docker Compose

The easiest way to run the entire application is using Docker Compose.

### Prerequisites
- Docker 20.10+
- Docker Compose 2.0+

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/justinhartfield/weed-stock-exchange-game.git
   cd weed-stock-exchange-game
   ```

2. **Configure environment**
   ```bash
   cp backend/.env.example backend/.env
   ```
   
   Edit `backend/.env` and update:
   - `JWT_SECRET` - Use a strong random secret
   - `DATABASE_URL` - Keep default for Docker setup
   - `REDIS_URL` - Keep default for Docker setup

3. **Start all services**
   ```bash
   docker-compose up -d
   ```
   
   This starts:
   - PostgreSQL database (port 5432)
   - Redis cache (port 6379)
   - FastAPI backend (port 8000)
   - React frontend (port 5173)
   - Celery worker
   - Celery beat scheduler

4. **Initialize database**
   ```bash
   # Run migrations
   docker-compose exec backend alembic upgrade head
   
   # Seed sample data
   docker-compose exec backend python seed_data.py
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

6. **Create your first account**
   - Go to http://localhost:5173/register
   - Create an account (you'll get 10,000 WeedCoins)
   - Start trading!

### Stopping the Application

```bash
docker-compose down
```

To remove all data:
```bash
docker-compose down -v
```

## Production Deployment

### Option 1: Docker Compose (Recommended for VPS)

1. **Set up a VPS** (DigitalOcean, AWS, etc.)

2. **Install Docker and Docker Compose**

3. **Clone and configure**
   ```bash
   git clone https://github.com/justinhartfield/weed-stock-exchange-game.git
   cd weed-stock-exchange-game
   cp backend/.env.example backend/.env
   ```

4. **Update production settings**
   Edit `backend/.env`:
   ```env
   JWT_SECRET=<generate-strong-random-secret>
   DATABASE_URL=postgresql://user:password@postgres:5432/strainexchange
   REDIS_URL=redis://redis:6379/0
   CORS_ORIGINS=https://yourdomain.com
   ```

5. **Set up reverse proxy** (Nginx example)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:5173;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }

       location /ws {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection "Upgrade";
           proxy_set_header Host $host;
       }
   }
   ```

6. **Enable HTTPS with Let's Encrypt**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

7. **Start services**
   ```bash
   docker-compose up -d
   docker-compose exec backend alembic upgrade head
   docker-compose exec backend python seed_data.py
   ```

### Option 2: Separate Hosting

#### Backend (Railway, Render, Fly.io)

1. **Set up PostgreSQL database** (use managed service)

2. **Set up Redis** (use managed service)

3. **Deploy FastAPI app**
   - Set environment variables
   - Run migrations: `alembic upgrade head`
   - Seed data: `python seed_data.py`
   - Start with: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Deploy Celery worker**
   - Same environment as backend
   - Start with: `celery -A app.core.celery_app worker --loglevel=info`

5. **Deploy Celery beat**
   - Same environment as backend
   - Start with: `celery -A app.core.celery_app beat --loglevel=info`

#### Frontend (Vercel, Netlify, Cloudflare Pages)

1. **Build the frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

2. **Deploy `dist/` folder**

3. **Set environment variables**
   - `VITE_API_URL` - Your backend URL
   - `VITE_WS_URL` - Your WebSocket URL

### Option 3: Kubernetes

See `k8s/` directory for Kubernetes manifests (coming soon).

## Database Backups

### Manual Backup
```bash
docker-compose exec postgres pg_dump -U user strainexchange > backup.sql
```

### Restore Backup
```bash
cat backup.sql | docker-compose exec -T postgres psql -U user strainexchange
```

### Automated Backups
Set up a cron job:
```bash
0 2 * * * cd /path/to/app && docker-compose exec postgres pg_dump -U user strainexchange > backups/backup-$(date +\%Y\%m\%d).sql
```

## Monitoring

### Health Checks
- Backend: http://localhost:8000/health
- Database: `docker-compose exec postgres pg_isready`
- Redis: `docker-compose exec redis redis-cli ping`

### Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
```

### Celery Monitoring
Install Flower:
```bash
pip install flower
celery -A app.core.celery_app flower
```
Access at http://localhost:5555

## Scaling

### Horizontal Scaling
- Add more Celery workers
- Use load balancer for backend
- Use CDN for frontend

### Database Optimization
- Add indexes for frequently queried fields
- Set up read replicas
- Enable connection pooling

### Redis Optimization
- Use Redis Cluster for high availability
- Configure eviction policies
- Monitor memory usage

## Troubleshooting

### Database Connection Issues
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Check logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

### Celery Tasks Not Running
```bash
# Check worker status
docker-compose logs celery_worker

# Check beat scheduler
docker-compose logs celery_beat

# Restart workers
docker-compose restart celery_worker celery_beat
```

### WebSocket Connection Fails
- Check CORS settings in `backend/.env`
- Verify WebSocket proxy configuration in Nginx
- Check firewall rules

## Security Checklist

- [ ] Change default `JWT_SECRET`
- [ ] Use strong database passwords
- [ ] Enable HTTPS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable database SSL
- [ ] Use environment variables for secrets
- [ ] Regular security updates
- [ ] Set up monitoring and alerts
- [ ] Configure backup strategy

## Performance Tips

1. **Database**
   - Add indexes on frequently queried columns
   - Use connection pooling
   - Regular VACUUM and ANALYZE

2. **Redis**
   - Configure maxmemory policies
   - Use appropriate data structures
   - Monitor memory usage

3. **Backend**
   - Enable response compression
   - Use async endpoints where possible
   - Implement caching strategies

4. **Frontend**
   - Enable code splitting
   - Optimize images
   - Use CDN for static assets
   - Implement lazy loading

## Support

For issues and questions:
- GitHub Issues: https://github.com/justinhartfield/weed-stock-exchange-game/issues
- Documentation: See README.md
