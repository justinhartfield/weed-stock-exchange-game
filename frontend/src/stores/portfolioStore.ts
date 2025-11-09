import { create } from 'zustand';
import { Portfolio } from '@/types';

interface PortfolioState {
  portfolio: Portfolio | null;
  setPortfolio: (portfolio: Portfolio) => void;
  updateBalance: (newBalance: number) => void;
}

export const usePortfolioStore = create<PortfolioState>((set) => ({
  portfolio: null,

  setPortfolio: (portfolio: Portfolio) => set({ portfolio }),

  updateBalance: (newBalance: number) =>
    set((state) =>
      state.portfolio
        ? {
            portfolio: {
              ...state.portfolio,
              weedcoins_balance: newBalance,
              total_value: newBalance + state.portfolio.holdings_value,
            },
          }
        : state
    ),
}));
