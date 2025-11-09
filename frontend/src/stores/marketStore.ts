import { create } from 'zustand';
import { Strain } from '@/types';

interface MarketState {
  strains: Strain[];
  selectedStrain: Strain | null;
  updateStrain: (strainId: number, price: number, changePct: number) => void;
  setStrains: (strains: Strain[]) => void;
  setSelectedStrain: (strain: Strain | null) => void;
}

export const useMarketStore = create<MarketState>((set) => ({
  strains: [],
  selectedStrain: null,

  updateStrain: (strainId: number, price: number, changePct: number) =>
    set((state) => ({
      strains: state.strains.map((strain) =>
        strain.id === strainId
          ? { ...strain, current_price: price, change_24h: changePct }
          : strain
      ),
      selectedStrain:
        state.selectedStrain?.id === strainId
          ? { ...state.selectedStrain, current_price: price, change_24h: changePct }
          : state.selectedStrain,
    })),

  setStrains: (strains: Strain[]) => set({ strains }),

  setSelectedStrain: (strain: Strain | null) => set({ selectedStrain: strain }),
}));
