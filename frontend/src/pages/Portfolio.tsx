import { useQuery } from '@tanstack/react-query';
import { portfolioApi, tradingApi } from '@/services/api';
import { Link } from 'react-router-dom';
import { TrendingUp, TrendingDown, Briefcase } from 'lucide-react';

export default function Portfolio() {
  const { data: portfolio, isLoading: portfolioLoading } = useQuery({
    queryKey: ['portfolio'],
    queryFn: async () => {
      const response = await portfolioApi.getPortfolio();
      return response.data;
    },
  });

  const { data: performance } = useQuery({
    queryKey: ['portfolio-performance'],
    queryFn: async () => {
      const response = await portfolioApi.getPerformance();
      return response.data;
    },
  });

  const { data: tradeHistory } = useQuery({
    queryKey: ['trade-history'],
    queryFn: async () => {
      const response = await tradingApi.getTradeHistory();
      return response.data;
    },
  });

  if (portfolioLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-xl text-gray-400">Loading portfolio...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-white mb-2">My Portfolio</h1>
        <p className="text-gray-400">Track your holdings and performance</p>
      </div>

      {/* Portfolio Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Total Value</p>
          <p className="text-3xl font-bold text-white">
            {portfolio?.total_value.toFixed(2)} WC
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Holdings Value</p>
          <p className="text-3xl font-bold text-primary-500">
            {portfolio?.holdings_value.toFixed(2)} WC
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-400 mb-1">Liquid Balance</p>
          <p className="text-3xl font-bold text-blue-500">
            {portfolio?.weedcoins_balance.toFixed(2)} WC
          </p>
        </div>
      </div>

      {/* Performance Metrics */}
      {performance && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="card">
            <div className="flex items-center mb-3">
              <TrendingUp className="w-6 h-6 text-green-500 mr-2" />
              <h3 className="text-lg font-bold text-white">Best Performer</h3>
            </div>
            {performance.best_performer ? (
              <div>
                <p className="text-white font-medium">{performance.best_performer.strain_name}</p>
                <p className="text-green-500 text-2xl font-bold">
                  +{performance.best_performer.profit_loss_pct.toFixed(2)}%
                </p>
                <p className="text-sm text-gray-400">
                  Profit: {performance.best_performer.profit_loss.toFixed(2)} WC
                </p>
              </div>
            ) : (
              <p className="text-gray-400">No holdings yet</p>
            )}
          </div>

          <div className="card">
            <div className="flex items-center mb-3">
              <TrendingDown className="w-6 h-6 text-red-500 mr-2" />
              <h3 className="text-lg font-bold text-white">Worst Performer</h3>
            </div>
            {performance.worst_performer ? (
              <div>
                <p className="text-white font-medium">{performance.worst_performer.strain_name}</p>
                <p className="text-red-500 text-2xl font-bold">
                  {performance.worst_performer.profit_loss_pct.toFixed(2)}%
                </p>
                <p className="text-sm text-gray-400">
                  Loss: {performance.worst_performer.profit_loss.toFixed(2)} WC
                </p>
              </div>
            ) : (
              <p className="text-gray-400">No holdings yet</p>
            )}
          </div>
        </div>
      )}

      {/* Holdings */}
      <div className="card">
        <h2 className="text-xl font-bold text-white mb-4 flex items-center">
          <Briefcase className="w-6 h-6 mr-2" />
          Current Holdings
        </h2>
        {portfolio?.holdings && portfolio.holdings.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dark-700">
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">Strain</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Shares</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Avg Buy Price</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Current Price</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Current Value</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">P/L</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">P/L %</th>
                </tr>
              </thead>
              <tbody>
                {portfolio.holdings.map((holding: any) => (
                  <tr key={holding.strain_id} className="border-b border-dark-700 hover:bg-dark-700">
                    <td className="py-3 px-4">
                      <Link
                        to={`/trading/${holding.strain_id}`}
                        className="text-white hover:text-primary-500 font-medium"
                      >
                        {holding.strain_name}
                      </Link>
                    </td>
                    <td className="text-right py-3 px-4 text-white">{holding.shares.toFixed(2)}</td>
                    <td className="text-right py-3 px-4 text-gray-400">
                      {holding.avg_buy_price.toFixed(2)} WC
                    </td>
                    <td className="text-right py-3 px-4 text-white">
                      {holding.current_price.toFixed(2)} WC
                    </td>
                    <td className="text-right py-3 px-4 text-white">
                      {holding.current_value.toFixed(2)} WC
                    </td>
                    <td
                      className={`text-right py-3 px-4 font-medium ${
                        holding.profit_loss >= 0 ? 'text-green-500' : 'text-red-500'
                      }`}
                    >
                      {holding.profit_loss >= 0 ? '+' : ''}
                      {holding.profit_loss.toFixed(2)} WC
                    </td>
                    <td
                      className={`text-right py-3 px-4 font-bold ${
                        holding.profit_loss_pct >= 0 ? 'text-green-500' : 'text-red-500'
                      }`}
                    >
                      {holding.profit_loss_pct >= 0 ? '+' : ''}
                      {holding.profit_loss_pct.toFixed(2)}%
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-400 mb-4">You don't have any holdings yet</p>
            <Link to="/trading" className="btn-primary">
              Start Trading
            </Link>
          </div>
        )}
      </div>

      {/* Trade History */}
      <div className="card">
        <h2 className="text-xl font-bold text-white mb-4">Recent Trades</h2>
        {tradeHistory && tradeHistory.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-dark-700">
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">Date</th>
                  <th className="text-left py-3 px-4 text-gray-400 font-medium">Type</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Shares</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Price</th>
                  <th className="text-right py-3 px-4 text-gray-400 font-medium">Total</th>
                </tr>
              </thead>
              <tbody>
                {tradeHistory.slice(0, 10).map((trade: any) => (
                  <tr key={trade.id} className="border-b border-dark-700">
                    <td className="py-3 px-4 text-gray-400">
                      {new Date(trade.timestamp).toLocaleString()}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`px-2 py-1 rounded text-xs font-bold ${
                          trade.type === 'buy'
                            ? 'bg-green-500/20 text-green-500'
                            : 'bg-red-500/20 text-red-500'
                        }`}
                      >
                        {trade.type.toUpperCase()}
                      </span>
                    </td>
                    <td className="text-right py-3 px-4 text-white">{trade.shares.toFixed(2)}</td>
                    <td className="text-right py-3 px-4 text-gray-400">
                      {trade.price.toFixed(2)} WC
                    </td>
                    <td className="text-right py-3 px-4 text-white">
                      {trade.total_cost.toFixed(2)} WC
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p className="text-center text-gray-400 py-8">No trades yet</p>
        )}
      </div>
    </div>
  );
}
