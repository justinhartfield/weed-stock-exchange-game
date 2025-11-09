import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useParams, Link } from 'react-router-dom';
import { tradingApi } from '@/services/api';
import { TrendingUp, TrendingDown, ShoppingCart, DollarSign } from 'lucide-react';

export default function StrainTradingPage() {
  const { strainId } = useParams();
  const queryClient = useQueryClient();
  const [selectedStrainId, setSelectedStrainId] = useState<number | null>(
    strainId ? parseInt(strainId) : null
  );
  const [shares, setShares] = useState('');
  const [tradeType, setTradeType] = useState<'buy' | 'sell'>('buy');

  const { data: strains } = useQuery({
    queryKey: ['strains'],
    queryFn: async () => {
      const response = await tradingApi.getStrains();
      return response.data;
    },
  });

  const { data: strainDetail } = useQuery({
    queryKey: ['strain', selectedStrainId],
    queryFn: async () => {
      if (!selectedStrainId) return null;
      const response = await tradingApi.getStrainDetail(selectedStrainId);
      return response.data;
    },
    enabled: !!selectedStrainId,
  });

  const buyMutation = useMutation({
    mutationFn: (data: { strain_id: number; shares: number }) =>
      tradingApi.buyShares(data.strain_id, data.shares),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio'] });
      queryClient.invalidateQueries({ queryKey: ['strains'] });
      setShares('');
      alert('Purchase successful!');
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'Trade failed');
    },
  });

  const sellMutation = useMutation({
    mutationFn: (data: { strain_id: number; shares: number }) =>
      tradingApi.sellShares(data.strain_id, data.shares),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['portfolio'] });
      queryClient.invalidateQueries({ queryKey: ['strains'] });
      setShares('');
      alert('Sale successful!');
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'Trade failed');
    },
  });

  const handleTrade = () => {
    if (!selectedStrainId || !shares || parseFloat(shares) <= 0) {
      alert('Please select a strain and enter valid shares');
      return;
    }

    const data = { strain_id: selectedStrainId, shares: parseFloat(shares) };
    
    if (tradeType === 'buy') {
      buyMutation.mutate(data);
    } else {
      sellMutation.mutate(data);
    }
  };

  const totalCost = strainDetail && shares
    ? (strainDetail.current_price * parseFloat(shares)).toFixed(2)
    : '0.00';

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Strain Trading</h1>
        <p className="text-gray-400">Buy and sell strain stocks</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Strain List */}
        <div className="lg:col-span-1">
          <div className="card">
            <h2 className="text-xl font-bold text-white mb-4">Available Strains</h2>
            <div className="space-y-2 max-h-[600px] overflow-y-auto">
              {strains?.map((strain: any) => (
                <button
                  key={strain.id}
                  onClick={() => setSelectedStrainId(strain.id)}
                  className={`w-full text-left p-3 rounded-lg transition-colors ${
                    selectedStrainId === strain.id
                      ? 'bg-primary-600 text-white'
                      : 'bg-dark-700 hover:bg-dark-600 text-gray-300'
                  }`}
                >
                  <p className="font-medium">{strain.name}</p>
                  <div className="flex items-center justify-between mt-1">
                    <span className="text-sm">{strain.current_price.toFixed(2)} WC</span>
                    {strain.change_24h !== null && (
                      <span
                        className={`text-sm font-bold ${
                          strain.change_24h >= 0 ? 'text-green-400' : 'text-red-400'
                        }`}
                      >
                        {strain.change_24h >= 0 ? '+' : ''}
                        {strain.change_24h.toFixed(2)}%
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Trading Panel */}
        <div className="lg:col-span-2 space-y-6">
          {strainDetail ? (
            <>
              {/* Strain Details */}
              <div className="card">
                <h2 className="text-2xl font-bold text-white mb-4">{strainDetail.name}</h2>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div>
                    <p className="text-sm text-gray-400">Current Price</p>
                    <p className="text-xl font-bold text-white">
                      {strainDetail.current_price.toFixed(2)} WC
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Favorites</p>
                    <p className="text-xl font-bold text-primary-500">
                      {strainDetail.favorite_count}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Pharmacies</p>
                    <p className="text-xl font-bold text-blue-500">
                      {strainDetail.pharmacy_count}
                    </p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-400">Volatility</p>
                    <p className="text-xl font-bold text-yellow-500">
                      {strainDetail.volatility_score.toFixed(2)}
                    </p>
                  </div>
                </div>
              </div>

              {/* Trade Execution */}
              <div className="card">
                <h3 className="text-xl font-bold text-white mb-4">Execute Trade</h3>
                
                {/* Trade Type Selector */}
                <div className="flex space-x-4 mb-6">
                  <button
                    onClick={() => setTradeType('buy')}
                    className={`flex-1 py-3 rounded-lg font-semibold transition-colors ${
                      tradeType === 'buy'
                        ? 'bg-green-600 text-white'
                        : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
                    }`}
                  >
                    <ShoppingCart className="w-5 h-5 inline mr-2" />
                    Buy
                  </button>
                  <button
                    onClick={() => setTradeType('sell')}
                    className={`flex-1 py-3 rounded-lg font-semibold transition-colors ${
                      tradeType === 'sell'
                        ? 'bg-red-600 text-white'
                        : 'bg-dark-700 text-gray-400 hover:bg-dark-600'
                    }`}
                  >
                    <DollarSign className="w-5 h-5 inline mr-2" />
                    Sell
                  </button>
                </div>

                {/* Shares Input */}
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Number of Shares
                  </label>
                  <input
                    type="number"
                    value={shares}
                    onChange={(e) => setShares(e.target.value)}
                    className="input w-full"
                    placeholder="0.00"
                    min="0"
                    step="0.01"
                  />
                </div>

                {/* Total Cost */}
                <div className="bg-dark-700 rounded-lg p-4 mb-6">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-400">Total {tradeType === 'buy' ? 'Cost' : 'Proceeds'}:</span>
                    <span className="text-2xl font-bold text-white">{totalCost} WC</span>
                  </div>
                </div>

                {/* Execute Button */}
                <button
                  onClick={handleTrade}
                  disabled={buyMutation.isPending || sellMutation.isPending}
                  className={`w-full py-3 rounded-lg font-bold text-white transition-colors ${
                    tradeType === 'buy'
                      ? 'bg-green-600 hover:bg-green-700'
                      : 'bg-red-600 hover:bg-red-700'
                  } disabled:opacity-50 disabled:cursor-not-allowed`}
                >
                  {buyMutation.isPending || sellMutation.isPending
                    ? 'Processing...'
                    : tradeType === 'buy'
                    ? 'Buy Shares'
                    : 'Sell Shares'}
                </button>
              </div>
            </>
          ) : (
            <div className="card">
              <p className="text-center text-gray-400">Select a strain to start trading</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
