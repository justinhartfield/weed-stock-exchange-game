export interface User {
  id: number;
  email: string;
  username: string;
  weedcoins_balance: number;
}

export interface Strain {
  id: number;
  name: string;
  slug: string;
  current_price: number;
  favorite_count: number;
  pharmacy_count: number;
  change_24h?: number;
}

export interface StrainDetail extends Strain {
  base_price: number;
  popularity_score: number;
  volatility_score: number;
  price_history: PriceHistoryPoint[];
}

export interface PriceHistoryPoint {
  price: number;
  volume: number;
  timestamp: string;
}

export interface Trade {
  id: number;
  strain_id: number;
  type: 'buy' | 'sell';
  shares: number;
  price: number;
  total_cost: number;
  timestamp: string;
}

export interface Portfolio {
  weedcoins_balance: number;
  holdings_value: number;
  total_value: number;
  holdings: Holding[];
}

export interface Holding {
  strain_id: number;
  strain_name: string;
  shares: number;
  avg_buy_price: number;
  current_price: number;
  current_value: number;
  profit_loss: number;
  profit_loss_pct: number;
}

export interface FuturesBet {
  id: number;
  bet_type: 'popularity' | 'price' | 'availability';
  target_strain_id: number;
  prediction: string;
  stake: number;
  odds: number;
  potential_payout: number;
  expires_at: string;
  settled: boolean;
  outcome: 'pending' | 'won' | 'lost';
  created_at: string;
}

export interface HeadToHeadBet {
  id: number;
  strain_a_id: number;
  strain_b_id: number;
  metric: string;
  prediction: string;
  stake: number;
  odds: number;
  potential_payout: number;
  expires_at: string;
  settled: boolean;
  outcome: 'pending' | 'won' | 'lost';
  created_at: string;
}

export interface PropBet {
  id: number;
  bet_description: string;
  bet_type: string;
  stake: number;
  odds: number;
  potential_payout: number;
  expires_at: string;
  settled: boolean;
  outcome: 'pending' | 'won' | 'lost';
  created_at: string;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: number;
  username: string;
  weekly_profit?: number;
  all_time_profit?: number;
  prediction_accuracy?: number;
}

export interface Achievement {
  id: number;
  name: string;
  description: string;
  badge_icon?: string;
  criteria_type: string;
  criteria_value: number;
}

export interface UserAchievement extends Achievement {
  unlocked_at: string;
}
