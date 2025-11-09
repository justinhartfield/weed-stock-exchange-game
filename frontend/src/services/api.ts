import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth endpoints
export const authApi = {
  register: (email: string, username: string, password: string) =>
    api.post('/auth/register', { email, username, password }),
  
  login: (email: string, password: string) =>
    api.post('/auth/login', { email, password }),
  
  getMe: () => api.get('/auth/me'),
};

// Trading endpoints
export const tradingApi = {
  getStrains: (skip = 0, limit = 100) =>
    api.get('/trading/strains', { params: { skip, limit } }),
  
  getStrainDetail: (strainId: number) =>
    api.get(`/trading/strains/${strainId}`),
  
  buyShares: (strain_id: number, shares: number) =>
    api.post('/trading/trades/buy', { strain_id, shares }),
  
  sellShares: (strain_id: number, shares: number) =>
    api.post('/trading/trades/sell', { strain_id, shares }),
  
  getTradeHistory: (skip = 0, limit = 50) =>
    api.get('/trading/trades/history', { params: { skip, limit } }),
};

// Portfolio endpoints
export const portfolioApi = {
  getPortfolio: () => api.get('/portfolio/portfolio'),
  
  getPerformance: () => api.get('/portfolio/portfolio/performance'),
};

// Betting endpoints
export const bettingApi = {
  placeFuturesBet: (data: any) =>
    api.post('/betting/bets/futures', data),
  
  placeHeadToHeadBet: (data: any) =>
    api.post('/betting/bets/head-to-head', data),
  
  placePropBet: (data: any) =>
    api.post('/betting/bets/prop', data),
  
  getMyBets: (skip = 0, limit = 50) =>
    api.get('/betting/bets/my-bets', { params: { skip, limit } }),
};

// Leaderboard endpoints
export const leaderboardApi = {
  getWeeklyLeaderboard: (limit = 100) =>
    api.get('/leaderboard/leaderboard/weekly', { params: { limit } }),
  
  getAllTimeLeaderboard: (limit = 100) =>
    api.get('/leaderboard/leaderboard/all-time', { params: { limit } }),
  
  getAccuracyLeaderboard: (limit = 100) =>
    api.get('/leaderboard/leaderboard/accuracy', { params: { limit } }),
  
  getAchievements: () =>
    api.get('/leaderboard/achievements'),
  
  getUserAchievements: (userId: number) =>
    api.get(`/leaderboard/achievements/user/${userId}`),
};
