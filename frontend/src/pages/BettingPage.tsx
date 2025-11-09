import { useQuery } from '@tanstack/react-query';
import { bettingApi } from '@/services/api';
import { Dice5 } from 'lucide-react';

export default function BettingPage() {
  const { data: myBets } = useQuery({
    queryKey: ['my-bets'],
    queryFn: async () => {
      const response = await bettingApi.getMyBets();
      return response.data;
    },
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Betting</h1>
        <p className="text-gray-400">Place bets on future market events</p>
      </div>

      {/* Coming Soon Notice */}
      <div className="card text-center py-12">
        <Dice5 className="w-16 h-16 text-primary-500 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-white mb-2">Betting System Coming Soon</h2>
        <p className="text-gray-400 mb-6">
          Place futures bets, head-to-head matchups, and prop bets on strain performance
        </p>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-3xl mx-auto text-left">
          <div className="bg-dark-700 p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">Futures Bets</h3>
            <p className="text-sm text-gray-400">
              Predict if a strain will reach a certain price or popularity level
            </p>
          </div>
          <div className="bg-dark-700 p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">Head-to-Head</h3>
            <p className="text-sm text-gray-400">
              Bet on which strain will perform better over a time period
            </p>
          </div>
          <div className="bg-dark-700 p-4 rounded-lg">
            <h3 className="font-bold text-white mb-2">Prop Bets</h3>
            <p className="text-sm text-gray-400">
              Wager on market-wide events and milestones
            </p>
          </div>
        </div>
      </div>

      {/* My Bets */}
      {myBets && (myBets.futures_bets?.length > 0 || myBets.head_to_head_bets?.length > 0 || myBets.prop_bets?.length > 0) && (
        <div className="card">
          <h2 className="text-xl font-bold text-white mb-4">My Active Bets</h2>
          
          {/* Futures Bets */}
          {myBets.futures_bets?.length > 0 && (
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-white mb-3">Futures Bets</h3>
              <div className="space-y-2">
                {myBets.futures_bets.map((bet: any) => (
                  <div key={bet.id} className="bg-dark-700 p-4 rounded-lg">
                    <div className="flex justify-between items-start">
                      <div>
                        <p className="text-white font-medium">{bet.prediction}</p>
                        <p className="text-sm text-gray-400">
                          Stake: {bet.stake} WC | Odds: {bet.odds}x
                        </p>
                      </div>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-bold ${
                          bet.outcome === 'pending'
                            ? 'bg-yellow-500/20 text-yellow-500'
                            : bet.outcome === 'won'
                            ? 'bg-green-500/20 text-green-500'
                            : 'bg-red-500/20 text-red-500'
                        }`}
                      >
                        {bet.outcome.toUpperCase()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-400 mt-2">
                      Expires: {new Date(bet.expires_at).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
