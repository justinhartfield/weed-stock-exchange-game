# The Strain Exchange

A dynamic virtual stock market prediction game for cannabis strains, built with Python FastAPI backend and React TypeScript frontend.

## Features

### Core Trading System
- **Real-time strain stock trading** with buy/sell functionality
- **Dynamic price calculation** based on:
  - Base price (average market price × 10)
  - Popularity component (favorite counts)
  - Volatility component (price spread analysis)
- **Portfolio management** with profit/loss tracking
- **Trade history** and performance analytics

### Betting System
- **Futures bets** - Predict strain popularity, price, or availability
- **Head-to-head matchups** - Bet on relative performance between strains
- **Prop bets** - Wager on market-wide events

### Gamification
- **Leaderboards** - Weekly profit, all-time profit, prediction accuracy
- **Achievements system** - Unlock badges for milestones
- **Starting balance** - 10,000 WeedCoins for new users

### Real-time Features
- **WebSocket integration** for live price updates
- **Background jobs** with Celery for data synchronization
- **Market events** broadcasting

## Tech Stack

### Backend
- **Python 3.11+** with FastAPI
- **PostgreSQL 15+** for primary database
- **Redis 7+** for caching and Celery broker
- **SQLAlchemy** for ORM
- **Alembic** for migrations
- **Celery** for background tasks
- **WebSockets** for real-time updates

### Frontend
- **React 18** with TypeScript
- **Vite** for build tooling
- **TailwindCSS** for styling
- **TanStack Query** for data fetching
- **Zustand** for state management
- **Axios** for API calls
- **React Router** for navigation

## Project Structure

```
weedstockexchange/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/    # API endpoints
│   │   ├── core/                # Config, security, Celery
│   │   ├── models/              # SQLAlchemy models
│   │   ├── services/            # Business logic
│   │   ├── tasks/               # Celery tasks
│   │   ├── db/                  # Database setup
│   │   ├── websocket/           # WebSocket manager
│   │   └── main.py              # FastAPI app
│   ├── alembic/                 # Database migrations
│   ├── requirements.txt
│   ├── Dockerfile
│   └── seed_data.py             # Sample data script
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API & WebSocket
│   │   ├── stores/              # Zustand stores
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
└── docker-compose.yml
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 20+ (for local development)

### Quick Start with Docker

1. **Clone the repository**
   ```bash
   cd weedstockexchange
   ```

2. **Create environment file**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Run database migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Seed initial data**
   ```bash
   docker-compose exec backend python seed_data.py
   ```

6. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development Setup

#### Backend

1. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up database**
   ```bash
   # Make sure PostgreSQL is running
   alembic upgrade head
   python seed_data.py
   ```

3. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Run Celery worker** (in separate terminal)
   ```bash
   celery -A app.core.celery_app worker --loglevel=info
   ```

5. **Run Celery beat** (in separate terminal)
   ```bash
   celery -A app.core.celery_app beat --loglevel=info
   ```

#### Frontend

1. **Install dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run development server**
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Trading
- `GET /api/v1/trading/strains` - List all strains
- `GET /api/v1/trading/strains/{id}` - Get strain details
- `POST /api/v1/trading/trades/buy` - Buy shares
- `POST /api/v1/trading/trades/sell` - Sell shares
- `GET /api/v1/trading/trades/history` - Get trade history

### Portfolio
- `GET /api/v1/portfolio/portfolio` - Get user portfolio
- `GET /api/v1/portfolio/portfolio/performance` - Get performance metrics

### Betting
- `POST /api/v1/betting/bets/futures` - Place futures bet
- `POST /api/v1/betting/bets/head-to-head` - Place H2H bet
- `POST /api/v1/betting/bets/prop` - Place prop bet
- `GET /api/v1/betting/bets/my-bets` - Get user's bets

### Leaderboard
- `GET /api/v1/leaderboard/leaderboard/weekly` - Weekly leaderboard
- `GET /api/v1/leaderboard/leaderboard/all-time` - All-time leaderboard
- `GET /api/v1/leaderboard/leaderboard/accuracy` - Accuracy leaderboard
- `GET /api/v1/leaderboard/achievements` - List achievements
- `GET /api/v1/leaderboard/achievements/user/{id}` - User achievements

### WebSocket
- `WS /ws` - Real-time updates for prices and events

## Database Schema

### Core Tables
- **users** - User accounts and WeedCoin balances
- **strains** - Cannabis strain data and prices
- **price_history** - Historical price data
- **portfolios** - User holdings
- **trades** - Trade history
- **futures_bets, head_to_head_bets, prop_bets** - Betting data
- **achievements, user_achievements** - Gamification
- **leaderboards** - Rankings

## Background Jobs

### Celery Tasks
- **sync_strain_data_task** - Runs every 5 minutes to update prices
- **settle_expired_bets_task** - Runs hourly to settle bets

## Environment Variables

See `backend/.env.example` for all available configuration options.

Key variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET` - Secret key for JWT tokens
- `INITIAL_WEEDCOINS` - Starting balance for new users
- `CORS_ORIGINS` - Allowed CORS origins

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Production Deployment

1. Update environment variables for production
2. Set strong `JWT_SECRET`
3. Configure proper database credentials
4. Enable HTTPS
5. Set up proper CORS origins
6. Configure Redis for production
7. Set up monitoring and logging

## Future Enhancements

- [ ] Metabase integration for real weed.de data
- [ ] Social features (copy trading, discussions)
- [ ] Tournaments and competitions
- [ ] Mobile app
- [ ] Advanced charting with TradingView
- [ ] Limit and stop-loss orders
- [ ] Email notifications
- [ ] Admin dashboard

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Support

For issues and questions, please open a GitHub issue.
