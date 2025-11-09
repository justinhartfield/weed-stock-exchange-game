import { useQuery } from '@tanstack/react-query';
import { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { tradingApi, portfolioApi } from '@/services/api';
import { useMarketStore } from '@/stores/marketStore';
import { usePortfolioStore } from '@/stores/portfolioStore';
import { wsService } from '@/services/websocket';
import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react';

export default function Dashboard() {
  const { strains, setStrains, updateStrain } = useMarketStore();
  const { portfolio, setPortfolio } = usePortfolioStore();

  const { data: strainsData } = useQuery({
    queryKey: ['strains'],
    queryFn: async () => {
      const response = await tradingApi.getStrains(0, 20);
      return response.data;
    },
  });

  const { data: portfolioData } = useQuery({
    queryKey: ['portfolio'],
    queryFn: async () => {
      const response = await portfolioApi.getPortfolio();
      return response.data;
    },
  });

  useEffect(() => {
    if (strainsData) {
      setStrains(strainsData);
    }
  }, [strainsData, setStrains]);

  useEffect(() => {
    if (portfolioData) {
      setPortfolio(portfolioData);
    }
  }, [portfolioData, setPortfolio]);

  // Listen for WebSocket price updates
  useEffect(() => {
    const handlePriceUpdate = (data: any) => {
      updateStrain(data.strain_id, data.price, data.change_pct);
    };

    wsService.on('price_update', handlePriceUpdate);

    return () => {
      wsService.off('price_update', handlePriceUpdate);
    };
  }, [updateStrain]);

  const topGainers = [...strains]
    .filter((s) => s.change_24h !== undefined && s.change_24h !== null)
    .sort((a, b) => (b.change_24h || 0) - (a.change_24h || 0))
    .slice(0, 5);

  const topLosers = [...strains]
    .filter((s) => s.change_24h !== undefined && s.change_24h !== null)
    .sort((a, b) => (a.change_24h || 0) - (b.change_24h || 0))
    .slice(0, 5);

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard</h1>
        <p className="text-gray-400">Welcome to The Strain Exchange</p>
      </div>

      {/* Portfolio Overview */}
      {portfolio && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <p className="text-sm text-gray-400 mb-1">Total Portfolio Value</p>
            <p className="text-3xl font-bold text-white">{portfolio.total_value.toFixed(2)} WC</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-400 mb-1">Holdings Value</p>
            <p className="text-3xl font-bold text-primary-500">{portfolio.holdings_value.toFixed(2)} WC</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-400 mb-1">Liquid Balance</p>
            <p className="text-3xl font-bold text-blue-500">{portfolio.weedcoins_balance.toFixed(2)} WC</p>
          </div>
        </div>
      )}

      {/* Market Movers */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Gainers */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white flex items-center">
              <TrendingUp className="w-5 h-5 mr-2 text-green-500" />
              Top Gainers
            </h2>
            <Link to="/trading" className="text-primary-500 hover:text-primary-400 text-sm flex items-center">
              View All <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          <div className="space-y-3">
            {topGainers.map((strain) => (
              <Link
                key={strain.id}
                to={`/trading/${strain.id}`}
                className="flex items-center justify-between p-3 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors"
              >
                <div>
                  <p className="font-medium text-white">{strain.name}</p>
                  <p className="text-sm text-gray-400">{strain.current_price.toFixed(2)} WC</p>
                </div>
                <div className="text-right">
                  <p className="text-green-500 font-bold">+{strain.change_24h?.toFixed(2)}%</p>
                  <p className="text-xs text-gray-400">24h</p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Top Losers */}
        <div className="card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-white flex items-center">
              <TrendingDown className="w-5 h-5 mr-2 text-red-500" />
              Top Losers
            </h2>
            <Link to="/trading" className="text-primary-500 hover:text-primary-400 text-sm flex items-center">
              View All <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          <div className="space-y-3">
            {topLosers.map((strain) => (
              <Link
                key={strain.id}
                to={`/trading/${strain.id}`}
                className="flex items-center justify-between p-3 bg-dark-700 rounded-lg hover:bg-dark-600 transition-colors"
              >
                <div>
                  <p className="font-medium text-white">{strain.name}</p>
                  <p className="text-sm text-gray-400">{strain.current_price.toFixed(2)} WC</p>
                </div>
                <div className="text-right">
                  <p className="text-red-500 font-bold">{strain.change_24h?.toFixed(2)}%</p>
                  <p className="text-xs text-gray-400">24h</p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/trading" className="card hover:bg-dark-700 transition-colors cursor-pointer">
          <TrendingUp className="w-8 h-8 text-primary-500 mb-3" />
          <h3 className="text-lg font-bold text-white mb-2">Start Trading</h3>
          <p className="text-gray-400 text-sm">Buy and sell strain stocks to grow your portfolio</p>
        </Link>

        <Link to="/betting" className="card hover:bg-dark-700 transition-colors cursor-pointer">
          <TrendingUp className="w-8 h-8 text-blue-500 mb-3" />
          <h3 className="text-lg font-bold text-white mb-2">Place Bets</h3>
          <p className="text-gray-400 text-sm">Predict market movements and win big</p>
        </Link>

        <Link to="/leaderboard" className="card hover:bg-dark-700 transition-colors cursor-pointer">
          <TrendingUp className="w-8 h-8 text-yellow-500 mb-3" />
          <h3 className="text-lg font-bold text-white mb-2">Leaderboard</h3>
          <p className="text-gray-400 text-sm">See how you rank against other traders</p>
        </Link>
      </div>
    </div>
  );
}
